## Using LIME and LightGBM to view feature importance

Classes are labeled as 0 for no delay; 1 for delay on arrival.
LIME generates the feature importance for a single input.
Feature importance may hence vary across different inputs.

*simple* directory for data without weather data
*weather* directory for data with weather data

Line 18 of *output.py* denotes features that need to be inputted.
Current sample input is on line 26 of *output.py*

### View feature importance as list
Run 
```
python3 output.py
```

### View feature importance as html page
Uncomment line 43 of *output.py*
Output should look like this for without weather data ![](./simple/sample_plot.png)
Output should look like this for weather data ![](./weather/sample_plot.png)

### Limitations
Accuracy of LightGBM model is around 0.63 which is not very high.
Feature importance values are also low due to the use of categorical features
Training of LightGBM model only done on 2008 data, which only has Months from Jan to Apr.