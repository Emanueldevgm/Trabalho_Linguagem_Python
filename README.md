# Sistema de Inventário com Previsão de Demanda

Repositório do projeto de inventário com previsão de demanda em Python (PySide6).

## Requisitos

- Python 3.10+ (recomendado)

## Instalação rápida

No Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py

### Alternativa: executar dashboard web (FastAPI)

Após instalar dependências, execute o servidor web e abra o dashboard:

```powershell
venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn src.web.app:app --reload
```


```

No Bash / macOS / Linux:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Estrutura

- `src/` — código-fonte (GUI, controllers, models, repositories)
- `data/` — dados e exemplos
- `docs/` — documentação

## Inteligência Artificial

O sistema já conta com três funcionalidades de IA:

- Previsão de demanda (regressão) usando `src/ia/modelo_previsao.py`
  - carrega o modelo salvo em `models/modelo_previsao_produto_{produto_id}.pkl`
  - se não existir, treina a partir do histórico de vendas
  - processa entradas com colunas `data` e `quantidade`
  - retorna um `DataFrame` com `data_previsao` e `quantidade_prevista`
- Classificação de demanda usando `src/ia/modelo_classificacao.py`
  - classifica o nível de demanda de um produto como `baixo`, `medio` ou `alto`
  - treina com séries históricas e salva o modelo em `models/modelo_classificacao_demanda.pkl`
  - expõe probabilidades por classe
- Análise de sentimento de feedback usando `src/ia/modelo_sentimento.py`
  - usa TF-IDF e regressão logística para classificar feedbacks como `positivo` ou `negativo`
  - carrega ou treina o modelo em `models/modelo_sentimento_feedback.pkl`
  - retorna o sentimento e as probabilidades de cada classe

O dashboard também inclui botões para:

- gerar previsão de demanda
- classificar o nível de demanda de um produto
- analisar o sentimento de um texto de feedback

## Seguir

Revise os arquivos gerados, ajuste `README.md` e adicione licença se desejar.
