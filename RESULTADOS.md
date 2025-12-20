Análise de Resultados: Laço irregular e políticas schedule (Tarefa A)


<img width="3000" height="1800" alt="image" src="https://github.com/user-attachments/assets/f89637b3-9c4d-4c12-af4a-6d8fc6f4f8f3" />


Os experimentos realizados para a Tarefa A (N=1M, K=28, Threads=16) revelam comportamentos distintos entre as políticas de escalonamento do OpenMP, evidenciando como a distribuição da carga de trabalho e o tamanho do chunk influenciam o tempo total de execução.

1. Superioridade da Política Estática (Static)

Conforme observado no gráfico, a política Static (representada pela linha tracejada vermelha) apresentou o melhor desempenho absoluto, mantendo-se consistentemente abaixo dos 19 segundos.

Previsibilidade: Como a carga de trabalho de cada iteração é uniforme, a distribuição estática minimiza o overhead de gerenciamento do OpenMP em tempo de execução.

Localidade de Dados: Esta política favorece a localidade de cache, pois as threads recebem blocos contíguos de iterações, otimizando o acesso à memória.


2. Comportamento das Políticas Dinâmica e Guided

As políticas Dynamic e Guided apresentaram tempos de execução superiores à Estática, variando entre 20,5s e 22,2s.

Ponto Ótimo de Granularidade: O melhor desempenho para ambas ocorreu com um Chunk Size de 4. Nesse ponto, o equilíbrio entre a distribuição de carga e o overhead de atribuição foi otimizado.

Degradação com Granularidade Fina (Chunk=1): Com o tamanho de bloco unitário, observa-se um tempo maior e uma alta variabilidade (especialmente na política Guided). Isso se deve ao excessivo overhead de sincronização, onde as threads precisam acessar frequentemente a fila de tarefas global para obter novos blocos.


3. Impacto da Granularidade Grossa (Chunk=64)

Um fenômeno notável é a piora acentuada do desempenho conforme o tamanho do chunk aumenta para 64:

Saturação de Recursos: O aumento do chunk em uma operação que já sofre com o oversubscription (16 threads para 8 núcleos lógicos) intensifica a disputa por largura de banda de memória e recursos de cache.

Desbalanceamento de Carga: Com blocos maiores, a flexibilidade do escalonamento dinâmico diminui, aproximando-se dos problemas de ociosidade de threads enquanto as últimas terminam blocos grandes.


4. Análise de Variabilidade e Overhead

As áreas sombreadas nos gráficos indicam o desvio padrão das execuções:

Instabilidade em Chunks Pequenos: A política Guided com Chunk=1 mostrou a maior instabilidade, sugerindo que o algoritmo de ajuste de tamanho de bloco do OpenMP sofre maior interferência do sistema operacional sob alta concorrência de 16 threads.

Overhead de 16 Threads: O fato de todos os tempos estarem na faixa dos 20 segundos para 16 threads reforça a análise anterior de que o oversubscription prejudica o desempenho global, gerando um custo de troca de contexto que impede que as políticas dinâmicas alcancem a eficiência da estática.


Análise de Resultados: Operação SAXPY (Tarefa C)


<img width="1000" height="600" alt="image" src="https://github.com/user-attachments/assets/2e4e3990-2578-4e8e-a8fd-ce73bedba3bb" />


A análise a seguir baseia-se nos dados coletados para as três versões do algoritmo (v1 Sequencial, v2 SIMD e v3 OMP+SIMD), focando na eficiência da paralelização e nos limites do hardware utilizado.


1. Ganho de SIMD (Vetorização)

Ao comparar a versão v1 (Sequencial) com a v2 (SIMD), observa-se um ganho de desempenho imediato, mesmo em execução single-core.

A diretiva #pragma omp simd permitiu que o compilador utilizasse registradores vetoriais (AVX2), processando múltiplos elementos de ponto flutuante simultaneamente.

Isso reduz o número total de instruções executadas pela CPU para cobrir o mesmo valor de N, resultando em um tempo de execução consistentemente menor para a v2 em relação à v1.


<img width="1000" height="600" alt="image" src="https://github.com/user-attachments/assets/82d296b0-7c32-4e07-88a8-db7df47d8332" />


2. Escalabilidade e Eficiência Paralela (v3)
A versão v3 (OMP+SIMD) demonstrou comportamentos distintos dependendo do número de threads (T):

1 a 4: Observou-se um speedup quase linear. Como o processador possui 4 núcleos físicos, cada thread pôde ser alocada em um núcleo exclusivo, maximizando o uso dos recursos de processamento.

4 a 8: O ganho de desempenho continuou, porém de forma sublinear. Isso ocorre devido ao Hyper-Threading, onde as 8 threads lógicas compartilham os recursos dos 4 núcleos físicos. O ganho aqui é menor pois as threads começam a competir por unidades de execução e largura de banda de memória.


<img width="1000" height="600" alt="image" src="https://github.com/user-attachments/assets/9dba1c44-88b0-4931-b418-fa8cd5b0d837" />



16 (O Ponto de Inflexão): Para 16 threads, os gráficos de escalabilidade e boxplot mostram uma perda clara de desempenho (aumento no tempo de execução). Na medida que Speedup diminui, significa que diminui a diferença de performance entre as execuções - que deveria tender a crescer se não fosse essa característica do nosso hardware.

3. Impacto do Overhead e Oversubscription

A degradação observada com 16 threads é um caso clássico de oversubscription (sobrealocação).

Como o hardware dispõe de apenas 8 threads lógicas (conforme verificado no htop), a tentativa de executar 16 threads simultâneas força o Sistema Operacional a realizar constantes trocas de contexto (context switching).

O overhead gerado pelo gerenciamento de threads excedentes (salvamento e restauração de estados de registradores) supera o benefício do paralelismo, resultando em tempos superiores aos observados com 8 ou até 4 threads.

Além disso, a operação SAXPY é inerentemente memory-bound (limitada pela memória). Com 16 threads, a disputa pelo barramento de memória torna-se o gargalo principal, impedindo qualquer ganho de processamento extra.

4. Variabilidade e Warm-up


<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/58379f46-29bf-42b1-a6a4-6fb7eb098c4b" />


<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/e92ad346-1365-4834-a81a-bd2649837486" />


<img width="1200" height="500" alt="image" src="https://github.com/user-attachments/assets/6c032fa4-3238-4ed0-8f45-060613c3ce3e" />


Os gráficos de boxplot individualizados revelam uma variabilidade maior nas primeiras execuções de cada bloco.

Esse comportamento é atribuído ao warm-up do OpenMP, onde a criação inicial do thread pool consome tempo adicional.

Após as primeiras iterações, os tempos tendem a se estabilizar, como mostrado pela "magreza" das caixas nos boxplots para valores intermediários de threads.



