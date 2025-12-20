#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <omp.h>

void saxpy(int n, float a, const float *x, float *y);

double get_time();

// ./saxpy_v1 N 

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr,
            "Formato de entrada: ./saxpy_seq N\n");
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
    saxpy(N, a, x, y);

    double start = omp_get_wtime();
    saxpy(N, a, x, y);
    double end = omp_get_wtime();


    double time = end - start;
    printf("%f\n", time);

    free(x);
    free(y);

    return 0;
}

void saxpy(int n, float a, const float *x, float *y) {
    for (int i = 0; i < n; i++) {
        y[i] = a * x[i] + y[i];
    }
}