# Inteligência Artificial

Modelo preditivo do consumo energético (Python, pandas, scikit-learn), usando os dados dos sensores e dados meteorológicos da Open-Meteo API.

## Notebook de previsão do consumo

[`previsao_consumo.ipynb`](previsao_consumo.ipynb) prevê o consumo energético das 24 horas seguintes (RF13) e compara três modelos com o MAE: o modelo de referência (média por hora do dia), a regressão linear e o Random Forest.

Enquanto não existem dados da GreenBox, o notebook usa o dataset público **Appliances Energy Prediction**, incluído no repositório em [`dados/energydata_complete.csv`](dados/energydata_complete.csv).

### Como correr

1. Instalar as bibliotecas:
   ```bash
   python -m pip install pandas scikit-learn matplotlib jupyter
   ```
2. Abrir o notebook a partir da pasta `ia/` (no IntelliJ, no VS Code com a extensão Jupyter, ou com `jupyter notebook`) e correr todas as células.

### Trocar de dataset

Só a secção 1 do notebook depende do dataset. Para usar os dados da GreenBox, implementar `carregar_greenbox()` com as mesmas colunas padrão e trocar `dados = carregar_kaggle()` por `dados = carregar_greenbox()`.

## Dataset: fonte e licença

- **Fonte:** UCI Machine Learning Repository – [Appliances Energy Prediction](https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction). O mesmo ficheiro está também disponível no [Kaggle](https://www.kaggle.com/datasets/loveall/appliances-energy-prediction).
- **Licença:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). O ficheiro é incluído sem alterações.
- **Citação:**
  > Candanedo, L. (2017). *Appliances Energy Prediction* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5VC8G
- **Artigo original:**
  > Candanedo, L. M., Feldheim, V., & Deramaix, D. (2017). Data driven prediction models of energy use of appliances in a low-energy house. *Energy and Buildings*, 140, 81–97.

Os dados meteorológicos incluídos no dataset vêm da estação do aeroporto de Chièvres (Bélgica), obtidos pelos autores junto da Reliable Prognosis (rp5.ru), com autorização para a sua distribuição.
