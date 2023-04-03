import matplotlib.pyplot as plt
import pickle
import pandas as pd

rf = pickle.load(open('random_forest_model.pkl', 'rb'))
predictors = pickle.load(open('predictors.pkl', 'rb'))
# Create a series containing feature importances from the model and feature names from the training data
feature_importances = pd.Series(rf.feature_importances_, index=predictors).sort_values(ascending=False)

# Plot a simple bar chart
# feature_importances[:10].plot.bar();
plt.figure(figsize=(20,5))

for i in range(3):
  plt.subplot(1,3,i+1)
  feature_importances[10*i:10*(i+1)].plot.bar(ylim=(0,0.1))
