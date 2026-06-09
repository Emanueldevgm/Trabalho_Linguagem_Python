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

## Seguir

Revise os arquivos gerados, ajuste `README.md` e adicione licença se desejar.
