# Inteligência Artificial

Modelo preditivo do consumo energético (Python, pandas, scikit-learn), usando os dados dos sensores e dados meteorológicos da Open-Meteo API.

## Notebook de previsão do consumo

[`previsao_consumo.ipynb`](previsao_consumo.ipynb) prevê o consumo energético das 24 horas seguintes (RF13) e compara três modelos com o MAE: o modelo de referência (média por hora do dia), a regressão linear e o Random Forest.

Enquanto não existem dados da GreenBox, o notebook usa o dataset público [Appliances Energy Prediction](https://www.kaggle.com/datasets/loveall/appliances-energy-prediction) (Candanedo et al., 2017).

### Como correr

1. Descarregar o CSV do dataset no Kaggle e colocá-lo na pasta `ia/dados/`. Os ficheiros desta pasta não vão para o GitHub.
2. Instalar as bibliotecas:
   ```bash
   python -m pip install pandas scikit-learn matplotlib jupyter
   ```
3. Abrir o notebook a partir da pasta `ia/` (no VS Code com a extensão Jupyter, ou com `jupyter notebook`) e correr todas as células.

### Trocar de dataset

Só a secção 1 do notebook depende do dataset. Para usar os dados da GreenBox, implementar `carregar_greenbox()` com as mesmas colunas padrão e trocar `dados = carregar_kaggle()` por `dados = carregar_greenbox()`.
