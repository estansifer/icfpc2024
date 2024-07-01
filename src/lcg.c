#include <limits.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct board {
    int lx;
    int ly;
    int initial_pellets;
    char cells[292][259];
};

struct state {
    int x;
    int y;
    int pellets_left;
    char pellets_taken[292][259];
};

static struct board board;

static void load_board(const char *path)
{
    FILE *f = fopen(path, "r");
    int ch;
    int x = 1;
    int y = 1;
    int width = 0;
    int height = 0;
    while (ch = fgetc(f), !feof(f)) {
        if (ch == '\n') {
            if (x > 1) {
                board.cells[0][y] = '#';
                board.cells[x][y] = '#';
                width = x + 1;
                y++;
                x = 1;
            }
        } else {
            if (ch == '.')
                board.initial_pellets++;
            if (ch == 'L') {
                board.lx = x;
                board.ly = y;
            }
            board.cells[x++][y] = ch;
        }
    }
    if (x > 1) {
        board.cells[0][y] = '#';
        board.cells[x][y] = '#';
        width = x + 1;
        y++;
        x = 1;
    }
    height = y;
    for (int i = 0; i < width; ++i) {
        board.cells[i][0] = '#';
        board.cells[i][height] = '#';
    }
    fclose(f);
}

static int next(uint32_t *rng_state)
{
    int dir = (*rng_state + *rng_state / 22351) % 4;
    *rng_state = (*rng_state * 1103515245 + 12345) & 0x7ffffffful;
    return dir;
}

static int actual_pellets_left(struct state s)
{
    int left = 0;
    for (int y = 0; y < 259; ++y) {
        for (int x = 0; x < 292; ++x) {
            if (board.cells[x][y] == '.' && !s.pellets_taken[x][y])
                left++;
        }
    }
    return left;
}

__attribute__((noinline))
static struct state sim(struct state s, uint32_t rng_state, int steps)
{
    int x = s.x;
    int y = s.y;
    int pellets_left = s.pellets_left;
    for (int i = 0; i < steps; ++i) {
        int step = next(&rng_state);
        int nx = x;
        int ny = y;
        ny += ((const int[]){ -1, 1, 0, 0 })[step];
        nx += ((const int[]){ 0, 0, -1, 1 })[step];
        char dest = board.cells[nx][ny];
        if (__builtin_unpredictable(dest != '#')) {
            x = nx;
            y = ny;
        }
        char taken = s.pellets_taken[nx][ny];
        if (__builtin_unpredictable(dest == '.')) {
            pellets_left -= !taken;
            taken = 1;
        }
        s.pellets_taken[nx][ny] = taken;
    }
    s.pellets_left = pellets_left;
    s.x = x;
    s.y = y;
    return s;
}

static unsigned lengths[512 * 512];
__attribute__((noinline))
static unsigned steps_to_closest_pellet(struct state s)
{
    memset(lengths, 0xff, sizeof(lengths));
    lengths[s.y * 512 + s.x] = 0;
    int queue[290 * 257] = { s.y * 512 + s.x };
    int queue_length = 1;
    int cursor = 0;
    while (cursor < queue_length) {
        int n = queue[cursor++];
        unsigned length = lengths[n];
        int x = n % 512;
        int y = n / 512;
        if (board.cells[x][y] == '.' && !s.pellets_taken[x][y])
            return length;
        if (board.cells[x][y - 1] != '#' && length + 1 < lengths[(y - 1) * 512 + x]) {
            lengths[(y - 1) * 512 + x] = length + 1;
            queue[queue_length++] = (y - 1) * 512 + x;
        }
        if (board.cells[x][y + 1] != '#' && length + 1 < lengths[(y + 1) * 512 + x]) {
            lengths[(y + 1) * 512 + x] = length + 1;
            queue[queue_length++] = (y + 1) * 512 + x;
        }
        if (board.cells[x - 1][y] != '#' && length + 1 < lengths[y * 512 + x - 1]) {
            lengths[y * 512 + x - 1] = length + 1;
            queue[queue_length++] = y * 512 + x - 1;
        }
        if (board.cells[x + 1][y] != '#' && length + 1 < lengths[y * 512 + x + 1]) {
            lengths[y * 512 + x + 1] = length + 1;
            queue[queue_length++] = y * 512 + x + 1;
        }
    }
    return -1;
}

int main(int argc, char **argv)
{
    if (argc < 4) {
        fprintf(stderr, "usage: lcg <seeds to try> <steps per seed> <board file>\n");
        return -1;
    }
    load_board(argv[3]);
    // for (int y = 0; y < 259; ++y) {
    //     bool any = false;
    //     for (int x = 0; x < 292; ++x) {
    //         if (board.cells[x][y]) {
    //             fprintf(stderr, "%c", board.cells[x][y]);
    //             any = true;
    //         }
    //     }
    //     if (any)
    //         fprintf(stderr, "\n");
    // }
    uint32_t seeds[1000];
    int nseeds = 0;
    struct state state = {
        .x = board.lx,
        .y = board.ly,
        .pellets_left = board.initial_pellets,
    };
    int total_steps = 0;
    int steps_per_seed = atoi(argv[2]);
    uint32_t seeds_to_try = atoi(argv[1]);
    while (total_steps < 1000000 && state.pellets_left > 0) {
        uint32_t min_seed = -1;
        struct state min_next_state = { .pellets_left = INT_MAX };
        unsigned min_steps = -1;
        for (uint32_t seed = 0; seed < seeds_to_try; ++seed) {
            struct state next_state = sim(state, seed, steps_per_seed);
            if (next_state.pellets_left < min_next_state.pellets_left || (next_state.pellets_left == min_next_state.pellets_left && steps_to_closest_pellet(next_state) < min_steps)) {
                min_next_state = next_state;
                min_seed = seed;
                min_steps = steps_to_closest_pellet(next_state);
                fprintf(stderr, "%u %d %d %u\n", seed, board.initial_pellets, next_state.pellets_left, min_steps);
                if (next_state.pellets_left == 0)
                    break;
            }
        }
        seeds[nseeds++] = min_seed;
        state = min_next_state;
        total_steps += steps_per_seed;
    }
    if (state.pellets_left == 0) {
        for (int i = 0; i < nseeds; ++i)
            printf("%u\n", seeds[i]);
    } else
        fprintf(stderr, "ran out of steps before solving.\n");
}
