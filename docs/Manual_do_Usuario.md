# Manual do Utilizador

## 1. Instalação

1. Criar e ativar o ambiente virtual:
   ```bash
   python -m venv venv
   .\\venv\\Scripts\\Activate.ps1
   ```
2. Instalar dependências:
   ```bash
   pip install -r requirements.txt
   ```

## 2. Arranque da aplicação

1. Executar:
   ```bash
   python main.py
   ```
2. Utilizar o login padrão:
   - Usuário: `admin`
   - Senha: `admin123`

## 3. Funcionalidades principais

- **Cadastro de produtos**: botão `Cadastrar Produto`.
- **Registo de vendas**: botão `Registrar Venda`.
- **Recomendação de compra**: botão `Recomendar Compra`.
- **Dashboard de previsão**: selecionar produto e clicar em `Gerar Previsão de Demanda`.

## 4. Fluxo de utilização

1. Faça login.
2. Cadastre produtos com preço e estoque inicial.
3. Registe vendas para gerar histórico.
4. Use o dashboard para visualizar vendas e previsão.
5. Use a recomendação de compra para identificar produtos com estoque baixo.
