#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <omp.h>


void saxpy_omp_simd(int N, float a, float *x, float *y);

double get_time();

// ./saxpy_omp_simd N T

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr,
            "Formato de entrada: ./saxpy_omp_simd N T\n");
        return EXIT_FAILURE;
    }

    double N = atoi(argv[1]);
    double T = atoi(argv[2]);

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
    saxpy_omp_simd(N, a, x, y);
    omp_set_num_threads(T);

    double start = get_time();
    saxpy_omp_simd(N, a, x, y);
    double end = get_time();


    double time = end - start;
    printf("%f\n", time);

    free(x);
    free(y);

    return 0;
}

void saxpy_omp_simd(int N, float a, float *x, float *y) {
    #pragma omp parallel for simd
    for (int i = 0; i < N; i++) {
        y[i] = a * x[i] + y[i];
    }
}


double get_time() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}