# Relatório Técnico

## 1. Introdução

Apresenta o objetivo do sistema de inventário inteligente e a integração entre POO, GUI, ORM e IA.

## 2. Descrição do problema

Explica a necessidade de gerir stock e prever a demanda com base em histórico de vendas.

## 3. Arquitetura e design

- Camada de modelos SQLAlchemy.
- Controladores para lógica de negócio.
- GUI com PySide6.
- Módulo de previsão com RandomForest.

## 4. Diagrama de classes

Incluir um diagrama UML com as classes principais:
- `Produto`, `Venda`, `Compra`, `Previsao`, `Usuario`
- `InventarioController`, `PrevisaoController`
- `RepositorioBase`, `Repositorio`, `ModeloIA`

## 5. Implementação da IA

- Modelo: RandomForestRegressor.
- Dados de treino: histórico de vendas agrupado por dia.
- Métricas calculadas: RMSE e MAE.
- Salvamento e carregamento do modelo com `joblib`.

## 6. Manual do Utilizador

Descrição das operações e capturas de ecrã.

## 7. Conclusão

Resumo dos resultados, limitações e extensões futuras.
