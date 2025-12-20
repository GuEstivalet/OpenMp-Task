#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int fib(int x);

int main(int argc, char *argv[]) {
    if(argc < 5) return 1;
    int N = atoi(argv[1]);
    int K = atoi(argv[2]);
    int threads = atoi(argv[3]);
    int chunk = atoi(argv[4]);
    
    omp_set_num_threads(threads);

    int *v = (int*) malloc(N * sizeof(int));

    double t0 = omp_get_wtime();

    #pragma omp parallel for schedule(guided, chunk)
    for(int i = 0; i < N; i++){
        v[i] = fib(i % K);
    }

    double t1 = omp_get_wtime();
    
    printf("%lf\n", t1 - t0);

    free(v);
    return 0;
}

int fib(int x) {
    int x1, x2;

    if (x < 2)
        return x;

    x1 = fib (x - 1);
    x2 = fib (x - 2);
    return x1 + x2;
}