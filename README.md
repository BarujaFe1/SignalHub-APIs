
# SignalHub APIs

**Uma plataforma técnica que integra APIs públicas, normaliza dados, executa jobs agendados e expõe status, freshness e qualidade operacional de forma clara e auditável.**

## Visão geral

O **SignalHub APIs** é um projeto de portfólio construído para tornar visível um tipo de engenharia que costuma ficar escondido.

Muitos projetos com APIs param na coleta de dados: fazem algumas requisições, exibem um gráfico e encerram a história. Este projeto segue outra direção. Ele foi pensado para mostrar o que acontece **entre** a coleta e a apresentação: contratos de dados, transformação, persistência, agendamento, idempotência pragmática, histórico de execuções, freshness, checks básicos de qualidade e uma camada enxuta de visibilidade operacional.

Na prática, o SignalHub APIs transforma fontes públicas heterogêneas em um pequeno produto técnico confiável, explicável e demonstrável.

***

## Por que este projeto existe

Dados vindos de APIs externas são, com frequência:
- dispersos;
- inconsistentes;
- pouco padronizados;
- difíceis de monitorar;
- invisíveis em termos de atualização e qualidade.

Isso cria um problema técnico real: a aplicação pode até “funcionar”, mas quase ninguém consegue responder com clareza:
- qual fonte falhou por último;
- quando os dados foram atualizados;
- se o dado atual ainda está fresco;
- se a estrutura do payload mudou;
- se o volume coletado ficou abaixo do esperado;
- o que exatamente aconteceu em uma execução.

O SignalHub APIs existe para responder essas perguntas com objetividade.

Mais do que integrar APIs, o projeto quer provar que é possível construir uma camada simples, porém séria, de operação e confiança sobre dados externos.

***

## O que este projeto quer provar

Este projeto foi desenhado para provar, de forma explícita, que eu consigo:

- integrar múltiplas APIs com formatos e comportamentos diferentes;
- desenhar contratos de dados claros em vez de trafegar JSON cru por toda a aplicação;
- normalizar e persistir dados com coerência;
- implementar jobs agendados sem cair em overengineering;
- registrar execuções e falhas com utilidade real;
- medir freshness e expor qualidade mínima;
- construir uma interface técnica que torne o backend visível;
- documentar arquitetura, decisões e trade-offs como parte do produto.

Este não é um projeto sobre empilhar tecnologias.  
É um projeto sobre **engenharia explicável**, com narrativa forte para GitHub, portfólio e LinkedIn.

***

## Tese central

> Transformar dados públicos externos, heterogêneos e pouco observáveis em um backend analítico pequeno, confiável e visível.

Essa é a tese do projeto.

O diferencial do SignalHub APIs não está em “consumir três APIs”. Isso, isoladamente, é pouco. O diferencial está em organizar essas fontes sob uma mesma disciplina técnica:
- conectores modulares;
- contratos tipados;
- persistência raw e normalizada;
- jobs rastreáveis;
- freshness;
- checks básicos de qualidade;
- superfície operacional enxuta.

Em outras palavras: o projeto não quer parecer um dashboard.  
Ele quer parecer um **produto técnico real**.

***

## Escopo da V1

A V1 foi desenhada para ser forte, terminável e publicável.

### Incluído na V1
- 3 conectores públicos.
- 3 fontes reais de dados.
- contratos de entrada e saída por conector.
- persistência em Postgres.
- armazenamento de payloads raw.
- armazenamento de registros normalizados.
- scheduler leve.
- registro de runs.
- indicadores de freshness.
- checks básicos de qualidade.
- endpoints mínimos de leitura.
- status page técnica e enxuta.
- documentação de arquitetura.
- screenshots e demo curta.

### Fora da V1
- Kafka.
- Airflow.
- Kubernetes.
- auth.
- multi-tenant.
- streaming.
- observabilidade pesada.
- alertas avançados.
- warehouse separado.
- 10 conectores.
- camada analítica grande.
- interface inchada.

Esses cortes são deliberados. O objetivo da V1 é mostrar profundidade real sem transformar o projeto em uma operação impossível de terminar.

***

## Fontes da V1

A primeira versão integra três APIs públicas escolhidas por valor demonstrativo, simplicidade de consumo e compatibilidade com uma demo pública:

- **Open-Meteo**, para dados de clima e previsão, com uso livre não comercial e sem necessidade de API key. [open-meteo](https://open-meteo.com/en/about)
- **Frankfurter**, para taxas de câmbio, com consumo simples e sem chave. [getorchestra](https://www.getorchestra.io/guides/exchange-rates-api-free-find-daily-fx-rate-data-via-api)
- **CoinGecko**, para dados de mercado cripto, usado de forma controlada porque a camada pública/demo opera com limite aproximado de 30 chamadas por minuto. [docs.coingecko](https://docs.coingecko.com/docs/common-errors-rate-limit)

Essa combinação foi escolhida porque mostra:
- domínios diferentes;
- estruturas de payload diferentes;
- cadências de atualização diferentes;
- riscos operacionais diferentes.

Isso torna a camada de normalização e visibilidade muito mais interessante do que usar três APIs quase iguais.

***

## Capacidades planejadas

### Ingestão
- Um conector por fonte.
- Contratos Pydantic por conector.
- Validação do payload bruto.
- Transformação para um modelo canônico.
- Persistência de dados raw e normalizados.

### Operação
- Jobs agendados.
- Execução manual para desenvolvimento e demo.
- Registro de início, fim, duração, volume e status das execuções.
- Logs simples e úteis.
- Retry básico.
- Reprocessamento pontual.

### Qualidade e freshness
- Checagem de volume mínimo esperado.
- Validação de campos críticos nulos.
- Indicadores de freshness por fonte.
- Aviso simples de possível schema drift.
- Resumo operacional por fonte.

### Superfície de produto
- API de leitura em FastAPI.
- Página técnica de status.
- Visão geral das fontes.
- Timeline de execuções.
- Cards de freshness.
- Resumo de checks.
- Página de detalhe por fonte.

***

## Arquitetura resumida

O projeto segue uma arquitetura simples, modular e explicável:

```text
APIs públicas
  └── Camada de conectores
        └── Contratos Pydantic
              └── Transformações
                    └── Postgres
                          ├── sources
                          ├── runs
                          ├── raw_payloads
                          ├── normalized_signals
                          ├── freshness_status
                          └── quality_checks

Scheduler / runner
  └── dispara jobs de ingestão

FastAPI
  └── expõe endpoints de leitura e status

Next.js Status Page
  └── renderiza status, freshness, quality e histórico de runs
```

### Princípios arquiteturais
- simplicidade antes de sofisticação;
- modularidade sem fragmentação excessiva;
- backend visível;
- observabilidade leve;
- documentação como parte do produto;
- decisões fáceis de explicar em entrevista e no README.

***

## Stack técnica

### Backend
- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- Postgres

### Jobs e automação
- APScheduler ou scheduler equivalente leve
- scripts utilitários para seed, backfill e reprocessamento

### Frontend
- Next.js App Router
- TypeScript
- Tailwind CSS
- shadcn/ui

### Tooling
- Docker Compose
- GitHub Actions
- Pytest
- Ruff
- ESLint / Prettier
- OpenAPI / Swagger
- Mermaid

***

## Por que essa stack

Essa stack não foi escolhida para parecer sofisticada.  
Ela foi escolhida para maximizar quatro coisas:

- clareza;
- velocidade de construção;
- credibilidade técnica;
- chance real de terminar.

O projeto precisa transmitir engenharia séria sem cair em teatralidade de infraestrutura.

***

## O que torna este projeto forte para portfólio

O SignalHub APIs é forte para portfólio porque mostra uma combinação rara de sinais:

- integração entre fontes distintas;
- pensamento de contratos;
- persistência com estrutura;
- preocupação com operação;
- cuidado com qualidade;
- clareza arquitetural;
- disciplina de escopo;
- capacidade de transformar backend em produto visível.

Ele também é forte porque serve a três superfícies ao mesmo tempo:
- **GitHub**, com código e documentação;
- **portfólio**, com narrativa e screenshots;
- **LinkedIn**, com uma história clara sobre o problema resolvido.

Muitos projetos mostram UI.  
Muitos mostram análise.  
Poucos mostram **sistema**.

Este quer mostrar sistema.

***

## O que ele não é

É importante ser explícito: o SignalHub APIs não quer ser uma plataforma enterprise disfarçada de MVP.

Ele não é:
- um data lake;
- um pipeline distribuído;
- uma suíte completa de observabilidade;
- uma plataforma de alertas;
- uma ferramenta multi-tenant;
- uma stack de dados corporativa.

Se o projeto tentar virar isso cedo demais, ele perde sua principal força: ser pequeno, elegante, técnico e terminável.

***

## Modelo de dados da V1

A primeira versão gira em torno de poucas entidades centrais.

### `sources`
Representa cada fonte externa e suas configurações operacionais.

Campos esperados:
- código da fonte;
- nome;
- categoria;
- intervalo de execução;
- expectativa de freshness;
- status ativo/inativo.

### `runs`
Representa cada tentativa de ingestão.

Campos esperados:
- source_id;
- status;
- start_at;
- end_at;
- duration_ms;
- quantidade de registros raw;
- quantidade de registros normalizados;
- quantidade de erros;
- tipo da execução;
- retry_count.

### `raw_payloads`
Armazena o payload bruto recebido da API.

Campos esperados:
- run_id;
- source_id;
- endpoint;
- parâmetros;
- payload_json;
- hash do payload;
- status HTTP;
- fetched_at.

### `normalized_signals`
Armazena os registros em formato canônico.

Campos esperados:
- run_id;
- source_id;
- entity_type;
- entity_key;
- metric_key;
- value_numeric ou value_text;
- unit;
- observed_at;
- granularity;
- dimensions_json;
- hash do registro.

### `freshness_status`
Armazena o estado mais recente de freshness por fonte.

### `quality_checks`
Armazena os resultados dos checks executados em cada run.

### `event_logs`
Armazena eventos simples e mensagens úteis de execução.

Esse modelo é pragmático: forte o bastante para demonstrar engenharia, mas simples o bastante para permanecer explicável.

***

## Perguntas que o sistema deve conseguir responder

Um bom projeto desses precisa responder perguntas reais. Exemplos:

- Qual foi a última execução com sucesso?
- Qual fonte está stale agora?
- Quantos registros a última execução produziu?
- O payload mudou de estrutura?
- Houve falha recente?
- O dado mais recente observado é realmente recente?
- Há campos críticos nulos?
- Qual conector está mais instável?

Essas perguntas transformam o projeto de “integração com API” em “produto operacional”.

***

## Endpoints planejados

A API da V1 deve ser mínima, mas útil:

- `GET /health`
- `GET /sources`
- `GET /runs`
- `GET /freshness`
- `GET /quality`
- `GET /signals`
- `GET /metrics/summary`

A ideia não é criar uma API enorme.  
A ideia é expor o suficiente para sustentar a status page e a narrativa técnica do produto.

***

## Filosofia do frontend

O frontend não deve competir com o backend.  
Ele deve revelar o backend.

A interface ideal precisa passar sensação de:
- confiabilidade;
- clareza;
- sobriedade;
- operação;
- rastreabilidade.

A página principal deve destacar:
- estado geral do sistema;
- status por fonte;
- freshness;
- histórico recente de runs;
- checks de qualidade;
- resumo de falhas.

Se o backend for bom, mas estiver invisível, o projeto perde força.

***

## Estrutura planejada do repositório

```text
signalhub-apis/
├── apps/
│   ├── api/
│   └── web/
├── packages/
│   └── ingestion/
├── docs/
│   ├── architecture.md
│   ├── data-model.md
│   ├── api-contract.md
│   ├── roadmap.md
│   ├── demo-script.md
│   ├── case-study-draft.md
│   ├── payloads/
│   └── screenshots/
├── scripts/
├── .github/
├── docker-compose.yml
├── Makefile
├── .env.example
├── README.md
└── LICENSE
```

A estrutura busca equilíbrio entre modularidade, clareza e publicabilidade.

***

## Status do projeto

**Fase atual:** definição arquitetural, narrativa do produto e preparação do repositório.

Nos primeiros passos, a prioridade não é “ter muita funcionalidade”.  
A prioridade é criar uma base profissional e sólida:
- README forte;
- arquitetura definida;
- modelo de dados inicial;
- estrutura de pastas;
- milestones claras;
- primeiro fluxo completo com uma fonte real.

***

## Roadmap resumido

### V1
- base do backend;
- schema inicial;
- conector Open-Meteo;
- conector Frankfurter;
- conector CoinGecko;
- scheduler leve;
- persistência raw e normalizada;
- runs;
- freshness;
- quality checks;
- endpoints de leitura;
- status page;
- documentação e demo.

### V1.1
- mais um conector;
- retries melhores;
- checks adicionais;
- comparação temporal leve;
- páginas de detalhe mais ricas.

### V2
- notificações;
- schema drift mais robusto;
- governança melhor de contratos;
- mais profundidade analítica.

***

## O que este projeto quer provar profissionalmente

Este projeto quer provar que eu consigo:
- transformar integração de APIs em engenharia de produto;
- construir uma camada de dados pequena, porém séria;
- tomar decisões técnicas com disciplina de escopo;
- equilibrar backend, analytics e apresentação;
- documentar com clareza;
- criar um projeto demonstrável de verdade.

Ele não quer impressionar por volume.  
Quer impressionar por coerência.

***

## Filosofia de demo

A demo faz parte do projeto, não é um acessório.

O SignalHub APIs deve ser compreensível em pouco tempo por meio de:
- um README forte;
- uma página principal de status;
- uma screenshot de arquitetura;
- uma timeline de runs;
- uma página de detalhe de fonte;
- um vídeo curto mostrando fluxo e valor.

Quanto mais rápido alguém entender o projeto, maior o seu valor como ativo de carreira.

***

## Documentação planejada

A documentação ideal do projeto inclui:

- `docs/architecture.md`
- `docs/data-model.md`
- `docs/api-contract.md`
- `docs/roadmap.md`
- `docs/demo-script.md`
- `docs/case-study-draft.md`
- `docs/payloads/`
- `docs/screenshots/`

Aqui, documentação não é burocracia.  
Ela é parte central do produto e da narrativa.

***

## Como começar

Quando o repositório estiver inicializado, o setup local previsto será algo próximo disto:

```bash
git clone <repo-url>
cd signalhub-apis
cp .env.example .env
docker compose up --build
```

Os comandos específicos de backend, frontend e migração serão adicionados à medida que o esqueleto do projeto for implementado.

***

## Trade-offs assumidos

Este projeto escolhe deliberadamente:
- scheduler simples em vez de orquestração pesada;
- Postgres como base principal em vez de múltiplas camadas de armazenamento;
- monólito modular em vez de serviços distribuídos;
- observabilidade leve em vez de stack completa;
- poucos conectores bem feitos em vez de muitos conectores superficiais;
- superfície técnica clara em vez de dashboard inflado.

Esses trade-offs não são limitações acidentais.  
São o desenho correto para a melhor V1 possível.

***

## Links futuros

- Demo pública: `TBD`
- Swagger / OpenAPI: `TBD`
- Arquitetura detalhada: `TBD`
- Case study: `TBD`
- Página de portfólio: `TBD`

***

## Licença

Licença a ser definida antes da publicação pública final.

***

## Nota final

O **SignalHub APIs** é um projeto deliberado.

Ele não foi concebido para ser o maior.  
Foi concebido para ser **forte**.

Forte em arquitetura.  
Forte em narrativa.  
Forte em portfólio.  
Forte em clareza técnica.  
E, principalmente, forte naquilo que mais importa: mostrar engenharia real sem virar um projeto impossível.

- seção “capturas de tela”,
- seção “como demonstrar este projeto”,
- e um tom de README de produto publicado.
