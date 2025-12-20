#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int fib(int x);

/*
Tarefa A — Laço irregular e políticas de schedule

Kernel: para i = 0..N-1, compute fib(i % K) e grave em v[i] usando fib custosa sem memoização.
Variante 1: #pragma omp parallel for schedule(static)
Variante 2: schedule(dynamic,chunk) com chunk ∈ {1,4,16,64}
Variante 3: schedule(guided,chunk) com chunk ∈ {1,4,16,64}
Se houver dois laços paralelos em sequência, use uma única região parallel e dois for internos 
*/

int main(int argc, char *argv[]) {

    int N = atoi(argv[1]);
    int K = atoi(argv[2]);
    int threads = atoi(argv[3]);

    omp_set_num_threads(threads);

    int *v = (int*) malloc(N * sizeof(int));

    double t0 = omp_get_wtime();

    #pragma omp parallel for schedule(static)
    for(int i = 0; i < N-1; i++){
        v[i] = fib(i % K);
    }

    double t1 = omp_get_wtime();
    
    printf("%lf", t1 - t0);

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