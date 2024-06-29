#include <math.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

typedef struct pt {
    double x;
    double y;
} pt;

typedef struct ptinfo {
    pt velocity;
    double mindist;
    int minedge;
    int selected;
    int next;
} ptinfo;

static pt points[100000];
static int npoints = 1;
static ptinfo info[100000];

typedef struct range {
    double a;
    double b;
    double c;
    double d;
} range;

static range find_range(double target, double v)
{
    range r = { 0 };
    double minb = (1 - 2 * v) / 2;
    double mind = minb * minb - 2 * target;
    double maxb = (1 + 2 * v) / 2;
    double maxd = maxb * maxb + 2 * target;
    if (mind >= 0) {
        double sd = sqrt(mind);
        r.a = -minb - sd;
        r.b = -minb + sd;
    } else {
        r.a = 4294967296;
        r.b = 4294967296;
    }
    if (maxd >= 0) {
        double sd = sqrt(maxd);
        r.c = -maxb - sd;
        r.d = -maxb + sd;
    } else {
        r.c = 4294967296;
        r.d = 4294967296;
    }
    return r;
}

static bool point_in_range(range r, double x)
{
    return !((x > r.a && x < r.b) || (x > r.c && x < r.d));
}

static void try_set_new_point(range xr, range yr, double x, double *best)
{
    if (x > 0 && x < *best && point_in_range(xr, x) && point_in_range(yr, x))
        *best = x;
}

static double distance(pt a, pt v, pt b)
{
    range xr = find_range(b.x - a.x, v.x);
    range yr = find_range(b.y - a.y, v.y);
    if (point_in_range(xr, 0) && point_in_range(yr, 0))
        return 0;
    double best = 4294967295;
    try_set_new_point(xr, yr, floor(xr.a), &best);
    try_set_new_point(xr, yr, ceil(xr.b), &best);
    try_set_new_point(xr, yr, floor(xr.c), &best);
    try_set_new_point(xr, yr, ceil(xr.d), &best);
    try_set_new_point(xr, yr, floor(yr.a), &best);
    try_set_new_point(xr, yr, ceil(yr.b), &best);
    try_set_new_point(xr, yr, floor(yr.c), &best);
    try_set_new_point(xr, yr, ceil(yr.d), &best);
    return best;
}

static pt move_to_point(pt a, pt v, pt b, double distance, bool print)
{
    double x = b.x - a.x - v.x * distance;
    double y = b.y - a.y - v.y * distance;
    while (distance > 0) {
        int dx = 0;
        int dy = 0;
        if (x >= distance) {
            dx = 1;
            v.x += 1;
            x -= distance;
        } else if (x <= -distance) {
            dx = -1;
            v.x -= 1;
            x += distance;
        }
        if (y >= distance) {
            dy = 1;
            v.y += 1;
            y -= distance;
        } else if (y <= -distance) {
            dy = -1;
            v.y -= 1;
            y += distance;
        }
        if (print)
            printf("%c", "123456789"[(dy + 1) * 3 + dx + 1]);
        distance--;
    }
    return v;
}

static int compare_pt_y(const void *a, const void *b)
{
    return (int)(((const pt *)a)->y) - (int)(((const pt *)b)->y);
}

int main(int argc, char **argv)
{
    FILE *f = fopen(argv[1], "r");
    int fx, fy;
    while (fscanf(f, "%d %d", &fx, &fy) == 2)
        points[npoints++] = (pt){ fx, fy };
    // qsort(points + 1, npoints - 1, sizeof(pt), compare_pt_y);
    // pt velocity = { 0 };
    // for (int i = 0; i < npoints - 1; ++i) {
    //     double dist = distance(points[i], velocity, points[i + 1]);
    //     velocity = move_to_point(points[i], velocity, points[i + 1], dist, true);
    // }
    // printf("\n");
    // return 0;
#if 1
    pt current = { 0 };
    pt velocity = { 0 };
    while (npoints > 0) {
        double best = UINT32_MAX;
        double best_actual = UINT32_MAX;
        int best_index = 0;
        for (int i = 0; i < npoints; ++i) {
            double d = distance(current, velocity, points[i]);
            double dx = current.x - points[i].x;
            double dy = current.y - points[i].y;
            double dfake = d;
            if (dx > dy)
                dfake += 0.25 * dx;
            else
                dfake += 0.25 * dy;
            if (dfake < best) {
                best = dfake;
                best_actual = d;
                best_index = i;
            }
        }
        velocity = move_to_point(current, velocity, points[best_index], best_actual, true);
        // fprintf(stderr, "%g %g\n", velocity.x, velocity.y);
        current = points[best_index];
        // remove the point
        points[best_index] = points[--npoints];
    }
#else
    // https://cp-algorithms.com/graph/mst_prim.html
    info[0].selected = 1;
    for (int i = 0; i < npoints; ++i) {
        double dist = distance(points[0], (pt){ 0, 0 }, points[i]);
        info[i].mindist = dist;
        info[i].minedge = 0;
    }
    for (int i = 1; i < npoints; ++i) {
        int v = -1;
        for (int j = 0; j < npoints; ++j) {
            if (!info[j].selected && (v < 0 || info[j].mindist < info[v].mindist))
                v = j;
        }
        info[v].selected = 1;
        info[v].velocity = move_to_point(points[info[v].minedge], info[info[v].minedge].velocity, points[v], info[v].mindist, false);
        if (info[info[v].minedge].next)
            info[v].next = info[info[v].minedge].next;
        info[info[v].minedge].next = v;
        for (int j = 0; j < npoints; ++j) {
            double dist = distance(points[v], info[v].velocity, points[j]);
            if (dist < info[j].mindist) {
                info[j].mindist = dist;
                info[j].minedge = v;
            }
        }
    }
    // pt velocity = { 0 };
    int current = 0;
    while (info[current].next) {
        double dist = distance(points[current], velocity, points[info[current].next]);
        velocity = move_to_point(points[current], velocity, points[info[current].next], dist, true);
        current = info[current].next;
    }
#endif
    printf("\n");
}
