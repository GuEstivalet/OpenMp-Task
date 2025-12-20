#OpenMP Task

Integrantes: Gustavo Estivalet, Kevin Rehbein

Organização do projeto:

```
ippd/
├── src/
│   ├── seq/                 # Código-fonte da implementação sequencial
│   └── omp/                 # Código-fonte da implementação OpenMP 
├── csv/		             # Contendo saídas das diversas execuções
├── png/ 		             # Contendo resultados gráficos de plot.py
├── Makefile                 # Arquivo com as regras de compilação
├── script_dependencies.sh   # Script para garantir as dependências necessárias
├── run_saxpy.sh             # Script para automação da execução e coleta de dados
├── run_schedule.sh          # Script para automação da execução e coleta de dados
├── plot_saxpy.py            # Script Python para geração de gráficos
├── plot_schedule.py         # Script Python para geração de gráficos
├── README.md                # Este arquivo de descrição geral do projeto
├── RESULTADOS.md            # Tabelas, gráficos, análise e decisões
└── REPRODUCIBILIDADE.md     # Detalhes do ambiente (CPU, compiler, flags, etc.)
```

## Tarefas escolhidas pela dupla

Tarefa A - Laço irregular e política de schedule

Tarefa C - Vetorização com simd


## Executa o fluxo completo (dependências, setup, venv, compilação e plotagem).

```
make all
```	

## Compila apenas os 6 binários relativos aos testes de escalonamento.

```
make task_a	
```

## Compila os binários da operação SAXPY (Sequencial, SIMD e OMP).

```
make task_c	
```

## Compila e executa o script de testes de impacto de schedule (run_schedule.sh).

```
make run_a	
```

## Compila e executa o script de escalabilidade do SAXPY (run_saxpy.sh).

```
make run_c	
```

## Gera os gráficos chamando os scripts Python plot_saxpy.py e plot_schedule.py.

```
make plot	
```


## Remove arquivos objeto, binários e o ambiente virtual Python.

```
make clean	
```



