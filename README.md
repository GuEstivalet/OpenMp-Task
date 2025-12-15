#OpenMP Task

Organização do projeto:

```
ippd/
├── src/
│   ├── seq/             # Código-fonte da implementação sequencial
│   └── omp/             # Código-fonte da implementação paralela com OpenMP
├── Makefile             # Arquivo com as regras de compilação
├── run.sh               # Script para automação da execução e coleta de dados
├── plot.py              # Script Python para geração de gráficos
├── README.md            # Este arquivo de descrição geral do projeto
├── RESULTADOS.md        # Tabelas, gráficos, análise e decisões
└── REPRODUCIBILIDADE.md # Detalhes do ambiente (CPU, compilador, flags, etc.)
```
## Introdução

Este repositório trata-se de um trabalho prático sobre OpenMP, relativo à disciplina de Introdução ao Processamento Paralelo e Distribuído. No escopo deste projeto serão exploradas:


## Tarefas escolhidas pela dupla


## Revisão de instalações/dependências de ambiente:

Os seguintes comandos são responsáveis por:

Atribui permissão ao script "script_dependencies.sh"
```
chmod +x script_dependencies.sh
```

Verifica se o GCC está instalado e se suporta OpenMP 5.X. Caso negativo, realiza as instalções necessárias para reprodução do ambiente.
```
./script_dependencies.sh
```
