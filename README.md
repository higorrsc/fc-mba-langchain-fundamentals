# LangChain Fundamentals

Este repositório contém uma série de scripts e exemplos práticos para aprender os fundamentos do framework **LangChain**, explorando desde a inicialização de modelos de chat até a construção de pipelines complexos de processamento de texto e sumarização.

## 🚀 Tecnologias Utilizadas

- **Python 3.14+**
- **LangChain Core**
- **LangChain OpenAI** (Modelos GPT)
- **LangChain Google GenAI** (Modelos Gemini)
- **uv** (Gerenciador de pacotes e ambientes Python)
- **Makefile** (Automação de tarefas)

## 📁 Estrutura do Projeto

O projeto está organizado em módulos que seguem uma progressão lógica de aprendizado:

### `01-fundamentals/`

Introdução aos conceitos básicos do LangChain:

- **01-hello-world.py**: Primeiro contato com a API da OpenAI.
- **02-init-chat-model.py**: Como inicializar diferentes provedores de modelos (Gemini/OpenAI) de forma unificada.
- **03-prompt-template.py**: Uso de templates simples para estruturar prompts.
- **04-chat-prompt-template.py**: Templates específicos para conversas (System, Human, AI messages).

### `02-chains-and-processing/`

Uso avançado de cadeias (Chains) e o LangChain Expression Language (LCEL):

- **01-starting-with-chains.py**: Introdução ao operador pipe (`|`) para encadear prompts e modelos.
- **02-chains-with-decorators.py**: Uso de decorators para simplificar a criação de chains.
- **03-runnable-lambda.py**: Como transformar funções Python em componentes compatíveis com o ecossistema LangChain (`RunnableLambda`).
- **04-processing-pipeline.py**: Construção de fluxos de processamento de dados.
- **05-summarizing.py**: Técnicas básicas de sumarização.
- **06-summarizing-with-map-reduce.py**: Implementação da estratégia Map-Reduce para lidar com textos longos que excedem o limite de contexto.
- **07-summarizing-pipeline.py**: Pipeline completo de sumarização usando LCEL.

## 🛠️ Configuração do Ambiente

### 1. Instalar o `uv`

Este projeto utiliza o [uv](https://github.com/astral-sh/uv) para gerenciamento rápido de dependências. Se você ainda não o tem:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Criar ambiente virtual e instalar dependências

Utilize o `Makefile` para facilitar o setup:

```bash
make venv
make install-uv
```

### 3. Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e preencha com suas chaves de API:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

- `OPENAI_API_KEY`: Sua chave da OpenAI.
- `GEMINI_API_KEY`: Sua chave do Google Gemini.

## 🏃 Como Executar os Exemplos

Você pode rodar qualquer script utilizando o `uv run`:

```bash
uv run 01-fundamentals/01-hello-world.py
```

## 📜 Comandos Disponíveis (Makefile)

O `Makefile` incluído possui atalhos para as tarefas mais comuns:

- `make venv`: Cria o ambiente virtual.
- `make lint`: Executa o linter (Ruff).
- `make lint-fix`: Aplica correções automáticas do linter.
- `make type-check`: Executa a verificação de tipos (Mypy).
- `make export-req`: Exporta as dependências para `requirements.txt`.

---
Desenvolvido como parte dos estudos de IA e Engenharia de Software.
