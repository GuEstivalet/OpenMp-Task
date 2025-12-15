#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <omp.h>


void saxpy_simd(int N, float a, float *x, float *y);

double get_time();

// ./saxpy_simd N 

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr,
            "./saxpy_simd N\n");
        return EXIT_FAILURE;
    }

    double N = atoi(argv[1]);

    // Aloca vetores x e y
    float *x = (float *)malloc(N * sizeof(float));
    float *y = (float *)malloc(N * sizeof(float));

    // Verifica se alocou corretamente
    if (!x || !y) {
        fprintf(stderr, "Erro de alocação de memória\n");
        return EXIT_FAILURE;
    }

    // Inicialização dos vetores
    for (int i = 0; i < N; i++) {
        x[i] = 1.0f;
        y[i] = 2.0f;
    }

    float a = 2.0f;

    // Warm-up (ignorado)
    saxpy_simd(N, a, x, y);

    double start = get_time();
    saxpy_simd(N, a, x, y);
    double end = get_time();


    double time = end - start;
    printf("%f\n", time);

    free(x);
    free(y);

    return 0;
}

void saxpy_simd(int N, float a, float *x, float *y) {
    #pragma omp simd
    for (int i = 0; i < N; i++) {
        y[i] = a * x[i] + y[i];
    }
}


double get_time() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}