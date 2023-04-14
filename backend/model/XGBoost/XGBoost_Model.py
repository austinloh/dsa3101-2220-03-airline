from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
path = '/content/drive/MyDrive/DSA3101_Share/'

df = pd.read_csv(path+'2006_to_2008_preprocessed.csv')

df.drop(['solarradiation','solarenergy','uvindex','severerisk'], axis=1, inplace=True)
df.drop(['precipprob','preciptype','icon'],axis=1, inplace=True)
for col in df.select_dtypes(include=['object']):
    df[col] = df[col].astype('category')

# Replace missing categorical (factor) values with 'unknown'
for col in df.select_dtypes(include=['category']):
    df[col] = df[col].cat.add_categories(['unknown'])
    df[col].fillna('unknown', inplace=True)

# Replace missing numeric values with mean of that column
for col in df.select_dtypes(include=[np.number]):
    mean_val = df[col].mean()
    df[col].fillna(mean_val, inplace=True)

from sklearn.preprocessing import LabelEncoder
df_encoded = pd.get_dummies(df, columns=['UniqueCarrier','conditions'])
le = LabelEncoder()
cat_columns = ['TailNum','Origin','Dest','origin_state','sunrise','sunset','description']
for column in cat_columns:
    df_encoded[column] = le.fit_transform(df_encoded[column])

X = df_encoded.drop("Arr_Delay_boolean", axis=1)
y = df_encoded["Arr_Delay_boolean"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.1, random_state=42)

import math
import matplotlib.pyplot as plt

def lr_schedule(epoch):
    warmup_epochs = 500
    base_lr = 0.15
    max_epochs = 5000
    if epoch < warmup_epochs:
        return base_lr * epoch / warmup_epochs
    else:
        cosine_decay = 0.5 * (1 + math.cos(math.pi * (epoch - warmup_epochs) / (max_epochs - warmup_epochs)))
        return base_lr * cosine_decay

lr_rates = []
for epoch in range(5000):
    lr = lr_schedule(epoch)
    lr_rates.append(lr)

plt.plot(lr_rates)
plt.xlabel("Epoch")
plt.ylabel("Learning Rate")
plt.title("Learning Rate Schedule")
plt.show()

import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import accuracy_score
import math
params = {
    "objective": "binary:logistic",
    "max_depth": 12,
    "n_estimators": 5000,
    "min_child_weight": 1,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "gamma": 0.1,
    "reg_alpha": 0.1,
    "reg_lambda": 1,
    "scale_pos_weight": 1,
    "tree_method": "gpu_hist",
    "random_state": 42,
    "max_delta_step": 1,
    "max_bin": 512,
    "min_split_loss": 0,
    "max_leaves": 256,
}
model = xgb.XGBClassifier(**params)

# Train the model on the training data and evaluate it on the validation data
eval_set = [(X_train, y_train), (X_val, y_val)]
model.fit(X_train, y_train, eval_metric="error", eval_set=eval_set, verbose=True,
          callbacks=[xgb.callback.LearningRateScheduler(lr_schedule)],early_stopping_rounds=100)

# Make predictions on the testing data
y_pred = model.predict(X_test)

# Calculate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Plot the first tree in the model
fig, ax = plt.subplots(figsize=(400, 200))
xgb.plot_tree(model, ax=ax, num_trees=0)
plt.show()

# Plot feature importances
fig, ax = plt.subplots(figsize=(20, 16))
xgb.plot_importance(model, ax=ax)
plt.show()

