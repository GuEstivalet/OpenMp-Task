#
#/bin/bash

# ===============================
# Configurações
# ===============================
N_VALUES=(100000 500000 1000000)
T_VALUES=(1 2 4 8 16)
REPS=5

V1="./src/seq/saxpy_v1"
V2="./src/omp/saxpy_v2"
V3="./src/omp/saxpy_v3"

CSV_V1="csv/saxpy_v1.csv"
CSV_V2="csv/saxpy_v2.csv"
CSV_V3="csv/saxpy_v3.csv"


# ===============================
# Cabeçalhos dos CSVs
# ===============================
echo "N,execucao,tempo" > $CSV_V1
echo "N,execucao,tempo" > $CSV_V2
echo "N,T,execucao,tempo" > $CSV_V3

# ===============================
# Execuções
# ===============================
for N in "${N_VALUES[@]}"; do
    for ((i=1; i<=REPS; i++)); do

        # -------- v1 (sequencial) --------
        time_v1=$($V1 $N)
        echo "$N,$i,$time_v1" >> $CSV_V1

        # -------- v2 (SIMD) --------
        time_v2=$($V2 $N)
        echo "$N,$i,$time_v2" >> $CSV_V2

        # -------- v3 (OMP + SIMD) --------
        for T in "${T_VALUES[@]}"; do
            time_v3=$($V3 $N $T)
            echo "$N,$T,$i,$time_v3" >> $CSV_V3
        done

    done
done

echo "Execuções finalizadas."
