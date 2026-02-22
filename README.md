# LangChain Fundamentals

Este repositório contém uma série de scripts e exemplos práticos para aprender os fundamentos do framework **LangChain**, explorando desde a inicialização de modelos de chat até a construção de agentes, gerenciamento de memória e bancos de vetores (RAG).

## 🚀 Tecnologias Utilizadas

- **Python 3.14+**
- **LangChain Core & Community**
- **LangChain OpenAI** (Modelos GPT)
- **LangChain Google GenAI** (Modelos Gemini)
- **LangChain Postgres** (PGVector)
- **uv** (Gerenciador de pacotes e ambientes Python)
- **Docker & Docker Compose** (Para o banco de dados PGVector)
- **Makefile** (Automação de tarefas)

## 📁 Estrutura do Projeto

O projeto está organizado em módulos que seguem uma progressão lógica de aprendizado:

### `ch01_fundamentals/`

Introdução aos conceitos básicos do LangChain:

- **p01_hello_world.py**: Primeiro contato com a API da OpenAI.
- **p02_init_chat_model.py**: Como inicializar diferentes provedores de modelos (Gemini/OpenAI) de forma unificada.
- **p03_prompt_template.py**: Uso de templates simples para estruturar prompts.
- **p04_chat_prompt_template.py**: Templates específicos para conversas (System, Human, AI messages).

### `ch02_chains_and_processing/`

Uso avançado de cadeias (Chains) e o LangChain Expression Language (LCEL):

- **p01_starting_with_chains.py**: Introdução ao operador pipe (`|`) para encadear prompts e modelos.
- **p02_chains_with_decorators.py**: Uso de decorators para simplificar a criação de chains.
- **p03_runnable_lambda.py**: Uso de `RunnableLambda` para integrar funções Python customizadas.
- **p04_processing_pipeline.py**: Construção de fluxos de processamento de dados.
- **p05_summarizing.py**: Técnicas básicas de sumarização.
- **p06_summarizing_with_map_reduce.py**: Implementação da estratégia Map-Reduce para textos longos.
- **p07_summarizing_pipeline.py**: Pipeline completo de sumarização usando LCEL.

### `ch03_agents_and_tools/`

Criação de agentes que podem executar ações:

- **p01_react_agent_and_tools.py**: Implementação manual de um agente ReAct com ferramentas customizadas (calculadora e busca mockada).
- **p02_react_agent_using_prompt_hub.py**: Uso do LangChain Hub para carregar prompts de agentes pré-definidos.

### `ch04_memory_management/`

Como manter o estado das conversas:

- **p01_history_storage.py**: Uso de `InMemoryChatMessageHistory` e `RunnableWithMessageHistory`.
- **p02_history_based_on_sliding_window.py**: Gerenciamento de histórico com janela deslizante (trimming de mensagens) para controle de tokens.

### `ch05_loaders_and_vectors_database/`

Trabalhando com dados externos e RAG (Retrieval-Augmented Generation):

- **p01_loading_using_WebBaseLoader.py**: Extração de conteúdo de páginas web.
- **p02_loading_pdf_file.py**: Carregamento e processamento de arquivos PDF.
- **p03_ingestion_pgvector.py**: Pipeline de ingestão: carregar, dividir (split), gerar embeddings e salvar no **PGVector**.
- **p04_search_vector.py**: Realização de buscas semânticas no banco de vetores.

## 🛠️ Configuração do Ambiente

### 1. Instalar o `uv`

Este projeto utiliza o [uv](https://github.com/astral-sh/uv) para gerenciamento rápido de dependências.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Subir o Banco de Dados (PGVector)

Para os exemplos do capítulo 05, é necessário o PostgreSQL com a extensão `pgvector`:

```bash
make docker-up
```

### 3. Criar ambiente virtual e instalar dependências

Utilize o `Makefile` para facilitar o setup:

```bash
make venv
make install-uv
```

### 4. Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e preencha com suas chaves de API:

```bash
cp .env.example .env
```

Campos principais: `OPENAI_API_KEY`, `GEMINI_API_KEY`, `PGVECTOR_URL`.

## 🏃 Como Executar os Exemplos

Você pode rodar qualquer script utilizando o `uv run`:

```bash
uv run ch01_fundamentals/p01_hello_world.py
```

## 📜 Comandos Disponíveis (Makefile)

- `make venv`: Cria o ambiente virtual.
- `make docker-up`: Inicia os serviços Docker (PGVector).
- `make docker-down`: Para os serviços Docker.
- `make lint`: Executa o linter (Ruff).
- `make lint-fix`: Aplica correções automáticas do linter.
- `make type-check`: Executa a verificação de tipos (Mypy).

---
Desenvolvido como parte dos estudos de IA e Engenharia de Software.
