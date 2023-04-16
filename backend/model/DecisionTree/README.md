## Random Forest

### Training Model
The predictors used to train the random forest model are:
- Month
- Day of Month
- Day of Week
- Scheduled Departure Time
- Estimated Arrival Time
- Carrier
- Origin
- Destination
- Distance
For departure and arrival time, they are divided into 3-hour long intervals.

Due to insufficient RAM, only 8% of the data are used as training dataset, while 2% of data are used as test dataset.

Running *random_forest_model.py* will generate two files:
1. *random_forest_model.pkl*: Random forest model
2. *predictors.pkl*: Preditors used after encoding categorical variables

### Variable Importance
The important variables are retrieved from random forest model. 20 important variables are shown in the plot.

Running *important_variables.py* will generate one plot *rf_feature_importance.jpg*: 
![](./rf_feature_importance.png)

### Limitations
Accuracy of random forest model is around 0.61 which is not very high.
Since the model does not perform very well, the important variables identified by the model are not very convincing.

Training of random forest model only done on 2008 data, which only has Months from Jan to Apr. Furthermore, only 8% of data are used for training.