#!/bin/bash

# ===============================
# 1. Configurações
# ===============================
N_FIXED=1000000
K_FIXED=28
T_FIXED=16

# Chunks para Dynamic e Guided
CHUNKS_LIST=(1 4 16 64)
REPS=5

CSV_A="csv/resultados_tarefa_a.csv"
mkdir -p csv

# Binários ajustados conforme Makefile
BIN_A_V1="./src/omp/a_v1" # Static
BIN_A_V2="./src/omp/a_v2" # Dynamic
BIN_A_V3="./src/omp/a_v3" # Guided

# ===============================
# 2. Execução
# ===============================
rm -f $CSV_A

echo "=========================================="
echo "   COMPARATIVO: STATIC vs DYNAMIC vs GUIDED"
echo "=========================================="
echo "Config: N=$N_FIXED | K=$K_FIXED | Threads=$T_FIXED"
echo "Chunks (Dyn/Gui): ${CHUNKS_LIST[*]}"
echo ""

echo "Variante,N,K,Threads,Chunk,Rep,Tempo" > $CSV_A

echo "--- Executando STATIC ---"
for ((r=1; r<=REPS; r++)); do
    echo "Static  | Threads: $T_FIXED | Rep: $r/$REPS"
    # Static recebe apenas N K T
    t_val=$($BIN_A_V1 $N_FIXED $K_FIXED $T_FIXED)
    echo "static,$N_FIXED,$K_FIXED,$T_FIXED,0,$r,$t_val" >> $CSV_A
done
echo ""

echo "--- Executando DYNAMIC e GUIDED ---"
for C in "${CHUNKS_LIST[@]}"; do
    echo ">>> Testando Chunk Size: $C"
    
    for ((r=1; r<=REPS; r++)); do
        
        # Dynamic
        echo "Dynamic | Chunk: $C | Rep: $r/$REPS"
        t_val=$($BIN_A_V2 $N_FIXED $K_FIXED $T_FIXED $C)
        echo "dynamic,$N_FIXED,$K_FIXED,$T_FIXED,$C,$r,$t_val" >> $CSV_A

        # Guided
        echo "Guided  | Chunk: $C | Rep: $r/$REPS"
        t_val=$($BIN_A_V3 $N_FIXED $K_FIXED $T_FIXED $C)
        echo "guided,$N_FIXED,$K_FIXED,$T_FIXED,$C,$r,$t_val" >> $CSV_A

    done
    echo ""
done

echo "=========================================="
echo "TESTE TAREFA A FINALIZADO."
echo "Resultados em: $CSV_A"