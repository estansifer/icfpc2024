#include <math.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

typedef struct pt {
    double x;
    double y;
} pt;

static pt points[100000];
static int npoints;

typedef struct pv {
    pt p;
    pt v;
} pv;

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
    if (r.c < r.a)
        return (struct range){ r.c, r.d, r.a, r.b };
    else
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

static double distance(pv a, pt b)
{
    range xr = find_range(b.x - a.p.x, a.v.x);
    range yr = find_range(b.y - a.p.y, a.v.y);
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

int main(int argc, char **argv)
{
    FILE *f = fopen(argv[1], "r");
    int fx, fy;
    while (fscanf(f, "%d %d", &fx, &fy) == 2)
        points[npoints++] = (pt){ fx, fy };
    pv current = { 0 };
    while (npoints > 0) {
        double best = UINT32_MAX;
        int best_index = 0;
        for (int i = 0; i < npoints; ++i) {
            double d = distance(current, points[i]);
            if (d < best) {
                best = d;
                best_index = i;
            }
        }
        double x = points[best_index].x - current.p.x - current.v.x * best;
        double y = points[best_index].y - current.p.y - current.v.y * best;
        while (best > 0) {
            int dx = 0;
            int dy = 0;
            if (x >= best) {
                dx = 1;
                current.v.x += 1;
                x -= best;
            } else if (x <= -best) {
                dx = -1;
                current.v.x -= 1;
                x += best;
            }
            if (y >= best) {
                dy = 1;
                current.v.y += 1;
                y -= best;
            } else if (y <= -best) {
                dy = -1;
                current.v.y -= 1;
                y += best;
            }
            printf("%c", "123456789"[(dy + 1) * 3 + dx + 1]);
            best--;
        }
        current.p = points[best_index];
        // remove the point
        points[best_index] = points[--npoints];
    }
    printf("\n");
}
