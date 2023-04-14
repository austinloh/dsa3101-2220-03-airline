## Setup api for backend

### Running locally

In terminal, run:
```
export FLASK_APP=main
```
```
flask run
```

### Running on docker

Run:
```
docker build -t api .
```
```
docker run api
```

### Calling api

For now, only 3 endpoints set up <br>
- http://127.0.0.1:5000/api/lime_fi
- http://127.0.0.1:5000/api/lime_plot
- http://127.0.0.1:5000/predict

Example usage are shown in *callingAPI.py*

### Feature importance
1. Decision Tree


2. LightGBM + LIME
   - Plain flight data
   ![](lightgbm/simple/sample_plot.png)
   - Flight data + weather data
   ![](lightgbm/weather/sample_plot.png)

3. Neural Network

![](NeuralNetwork/shap_plot.png)

4. Statistical Test
   - Chi-square
   ![](StatisticalTest/chi2.png)
   - ANOVA F-score
   ![](StatisticalTest/Fscore.png)
   - Information Gain
   ![](StatisticalTest/IG.png)

5. Time Series Analysis


6. XGBoost
![](XGBoost/XGBoost_importance_ranking.png)

### Replicating Results
*README.md* files are located in individual model folders with instruction to replicate results. (Only lightgbm and StatisticalTest)