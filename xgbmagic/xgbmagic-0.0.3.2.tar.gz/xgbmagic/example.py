import xgbmagic
import pandas as pd
import pickle

# train and test sets taken from Kaggle's Santander Customer Satisfaction challenge
df = pd.read_csv('train.csv')

#xgb = xgbmagic.Xgb(df, target_column='TARGET', id_column='ID', categorical_columns=[], num_training_rounds=1000, target_type='binary', n_samples=2, sample_fraction=0.5,  early_stopping_rounds=50)
xgb = xgbmagic.Xgb(df, target_column='TARGET', id_column='ID', categorical_columns=[], num_training_rounds=1000, target_type='binary', early_stopping_rounds=50)
xgb.train()

test_df = pd.read_csv('test.csv')
output = xgb.predict(test_df)
xgb.write_csv('output-xgbmagic.csv')
print(xgb.feature_importance())
