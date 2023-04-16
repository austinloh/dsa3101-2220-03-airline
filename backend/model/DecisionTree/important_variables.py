import matplotlib.pyplot as plt
import pickle
import pandas as pd

rf = pickle.load(open('random_forest_model.pkl', 'rb'))
predictors = pickle.load(open('predictors.pkl', 'rb'))
# Create a series containing feature importances from the model and feature names from the training data
feature_importances = pd.Series(rf.feature_importances_, index=predictors).sort_values(ascending=False)

# Plot a simple bar chart and save it as jpg file
feature_plot = feature_importances[0:20].plot.bar()
fig = feature_plot.get_figure()
fig.savefig('rf_feature_importance.jpg', dpi=300, bbox_inches='tight')
