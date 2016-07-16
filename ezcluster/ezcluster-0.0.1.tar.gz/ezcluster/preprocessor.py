import pandas as pd
from sklearn.preprocessing import LabelEncoder, Imputer, StandardScaler
from collections import Counter

def drop_missing(df):
    df = df.dropna()
    return df

def one_hot_encode(df, categorical_cols = None):
    if categorical_cols:
        le = LabelEncoder()
        for feature in categorical_cols:
            try:
                df[feature] = le.fit_transform(df[feature])
            except:
                print("Encoding error encountered for %s" % feature)
    return df

def normalize(df, categorical_cols = None):
    numerical_cols = list(df.select_dtypes(include = ['float64', 'int64']))
    numerical_cols = list((Counter(numerical_cols) - Counter(categorical_cols)).elements())
    ss = StandardScaler()
    for feature in numerical_cols:
        try:
            df[feature] = ss.fit_transform(df[feature].reshape(-1,1))
        except:
            print("Normalization error encountered for %s" % feature)
    return df

def sample(df, proportion = 1.0):
    return df.sample(frac = proportion) if proportion != 1.0 else df
