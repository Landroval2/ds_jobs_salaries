import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('job_data_cleaned.csv')

df.columns

df_model = df[['Rating', 'Size', 'Type of ownership', 'Industry', 'Sector', 'Revenue',
              'state', 'age', 'python', 'spark', 'aws', 'tableau', 'excel', 'ml',
              'seniority', 'desc_length', 'job_simplified', 'avg_salary']]

df_dum = pd.get_dummies(df_model)
# Choose relevant columns for model building
# Get dummy data (categorical variables that we want to separate, ex job_simplified)
# Train, test split
# Models:
# Multiple linear regression
# Lasso regression (many sparse columns)
# Random forest
# Tune models using GridSearchCV
# Test ensembles