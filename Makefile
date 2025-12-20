# ==========================================
# Configurações de Compilação
# ==========================================
CC = gcc
CFLAGS = -O3 -march=native -Wall
OMP_FLAGS = -fopenmp
LIBS = -lm

# Diretórios
SRC_SEQ = src/seq
SRC_OMP = src/omp
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

# ==========================================
# Alvos (Binários)
# ==========================================
BIN_A_TOTAL = $(SRC_OMP)/a_v1 $(SRC_OMP)/a_v2 $(SRC_OMP)/a_v3 \
              $(SRC_SEQ)/c_v1 $(SRC_OMP)/c_v2 $(SRC_OMP)/c_v3

# ==========================================
# Regras Principais
# ==========================================

all: dependencias setup venv task_a task_c plot

# 1. Verifica dependências de sistema (GCC/OpenMP)
dependencias:
	@echo "Verificando dependências do sistema..."
	chmod +x script_dependencies.sh
	./script_dependencies.sh

# 2. Cria pastas de saída
setup:
	@mkdir -p csv png

# 3. Cria ambiente virtual Python (apenas em Linux)
venv:
	@if [ "$$(expr substr $$(uname -s) 1 5)" = "Linux" ]; then \
		echo "Detectado ambiente Linux. Configurando ambiente Python..."; \
		python3 -m venv $(VENV); \
		$(PIP) install --upgrade pip; \
		$(PIP) install pandas numpy matplotlib seaborn; \
	fi

# 4. Compilação
task_a: $(BIN_A_TOTAL)
task_c: $(SRC_SEQ)/c_v1 $(SRC_OMP)/c_v2 $(SRC_OMP)/c_v3

# Regras de compilação genéricas
%.o: %.c
	$(CC) $(CFLAGS) $(OMP_FLAGS) -c $< -o $@

$(SRC_OMP)/a_v%: $(SRC_OMP)/a_v%.o
	$(CC) $(CFLAGS) $(OMP_FLAGS) $^ -o $@ $(LIBS)

$(SRC_SEQ)/c_v1: $(SRC_SEQ)/c_v1.o
	$(CC) $(CFLAGS) $(OMP_FLAGS) $^ -o $@ $(LIBS)

$(SRC_OMP)/c_v%: $(SRC_OMP)/c_v%.o
	$(CC) $(CFLAGS) $(OMP_FLAGS) $^ -o $@ $(LIBS)

# ==========================================
# Execução e Gráficos
# ==========================================

run_a: task_a
	chmod +x run_schedule.sh
	./run_schedule.sh

run_c: task_c
	chmod +x run_saxpy.sh
	./run_saxpy.sh

# Executa a plotagem usando o interpretador do ambiente virtual
plot: venv
	@echo "Gerando gráficos..."
	$(PYTHON) plot_saxpy.py
	$(PYTHON) plot_schedule.py

clean:
	rm -f $(SRC_SEQ)/*.o $(SRC_OMP)/*.o
	rm -f $(BIN_A_TOTAL)
	rm -rf $(VENV)

.PHONY: all dependencias setup venv task_a task_c run_a run_c plot clean