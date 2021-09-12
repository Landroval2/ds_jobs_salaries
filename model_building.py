import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn import svm, datasets

df = pd.read_csv('job_data_cleaned.csv')

df.columns

# Choose relevant columns for model building
df_model = df[['Rating', 'Size', 'Type of ownership', 'Industry', 'Sector', 'Revenue',
              'state', 'age', 'python', 'spark', 'aws', 'tableau', 'excel', 'ml',
               'seniority', 'desc_length', 'job_simplified', 'avg_salary']]

# Get dummy data (categorical variables that we want to separate, ex job_simplified)
df_dum = pd.get_dummies(df_model)

# Get rid of Nans and data with no rating
df_dum = df_dum.fillna(method='bfill')
df_dum = df_dum.fillna(method='ffill')
df_dum = df_dum[df_dum['avg_salary'] != -1]

# Train, test split
X = df_dum.drop(columns=['avg_salary'])
y = df_dum.avg_salary.values
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Models:
# Multiple linear regression

## Using stats
X_sm = sm.add_constant(X)
model = sm.OLS(y_train, X_train)
results = model.fit()
print(results.summary())

## Using sklearn
reg = LinearRegression().fit(X_train, y_train)
reg.score(X_train, y_train)
reg.score(X_test, y_test)
np.mean(cross_val_score(reg, X, y, scoring='neg_mean_absolute_error', cv=3, n_jobs=4))

# Lasso regression (many sparse columns)
 
lml = Lasso()
np.mean(cross_val_score(lml, X, y, scoring='neg_mean_absolute_error', cv=3, n_jobs=4))

alpha = []
error = []

for i in range(1, 100):
    alpha.append(2*i/100)
    lml = Lasso(alpha=2*i/100)
    error.append(np.mean(cross_val_score(lml, X, y, scoring='neg_mean_absolute_error', cv=3)))

plt.plot(alpha, error)
plt.show()
err = tuple(zip(alpha, error))
df_err = pd.DataFrame(err, columns=['alpha', 'error'])
best_alpha = df_err.iloc[df_err['error'].idxmax()].alpha
print(best_alpha)

lml = Lasso(alpha=2*i/100)
lowest_error = (np.mean(cross_val_score(lml, X, y, scoring='neg_mean_absolute_error', cv=3)))
print(lowest_error)

# Random forest
regr = RandomForestRegressor()
error = (np.mean(cross_val_score(regr, X, y, scoring='neg_mean_absolute_error', cv=3)))
print(error)

# Tune models using GridSearchCV
parameters = {'n_estimators':range(10, 300, 10), 'criterion':('mse', 'mae'), 'max_features':('auto', 'sqrt', 'log2')}
gs = GridSearchCV(estimator=regr,
             param_grid=parameters, scoring='neg_mean_absolute_error', cv=3)
gs.fit(X_train, y_train)
sorted(regr.cv_results_.keys())

# Test ensembles
