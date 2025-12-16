#!/bin/bash

set -e

echo " Verificação de GCC e OpenMP"

# Função para comparar versões
version_ge() {
  printf '%s\n%s\n' "$2" "$1" | sort -C -V
}

# Verifica se gcc está instalado
if ! command -v gcc >/dev/null 2>&1; then
  echo "GCC não encontrado. Instalando..."
  sudo apt update
  sudo apt install -y gcc g++
else
  echo "GCC encontrado:"
  gcc --version | head -n 1
fi

# Obtém versão do GCC
GCC_VERSION=$(gcc -dumpversion | cut -d. -f1)

echo "Versão principal do GCC: $GCC_VERSION"

# OpenMP 5.x é suportado a partir do GCC 9+
if [ "$GCC_VERSION" -lt 9 ]; then
  echo "GCC muito antigo para OpenMP 5.x."
  echo "Atualizando GCC"

  sudo apt update
  sudo apt install -y software-properties-common
  sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test
  sudo apt update
  sudo apt install -y gcc-13 g++-13

  sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-13 100
  sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-13 100

  echo "GCC atualizado:"
  gcc --version | head -n 1
else
  echo "Versão do GCC compatível com OpenMP 5.x."
fi

# Teste prático de OpenMP
echo "Testando suporte ao OpenMP..."

cat << 'EOF' > test_openmp.c
#include <omp.h>
#include <stdio.h>

int main() {
    #pragma omp parallel
    {
        printf("Thread %d de %d\n", omp_get_thread_num(), omp_get_num_threads());
    }
    return 0;
}
EOF

if gcc -fopenmp test_openmp.c -o test_openmp; then
  echo "OpenMP está funcionando corretamente. Teste bem sucedido."
  rm -f test_openmp test_openmp.c
  
else
  echo "Erro: OpenMP não está funcional. Falhou no teste."
  exit 1
fi

echo "=== Verificação concluída com sucesso ==="

