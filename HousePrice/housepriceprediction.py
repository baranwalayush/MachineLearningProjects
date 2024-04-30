# -*- coding: utf-8 -*-
"""housePricePrediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Clsh6TORYiTks6a0vK8EaClyQ6vNyibL
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv('/content/train.csv')
test = pd.read_csv('/content/test.csv')

df

df.info()

df['Id'].dtype

df.columns

df.isnull().sum().sort_values(ascending=False).head(15)

Y=df['SalePrice']
id=df['Id']
testId = test['Id']
X=df.drop(['Id','PoolQC','MiscFeature','Alley','Fence','SalePrice'],axis=1)
test=test.drop(['Id','PoolQC','MiscFeature','Alley','Fence'],axis=1)

X

for column in X.columns:
    typ = X[column].dtype
    if typ == "object":
        X[column] = X[column].fillna(X[column].mode()[0])
        test[column] = test[column].fillna(test[column].mode()[0])
    else:
        X[column] = X[column].fillna(X[column].mean())
        test[column] = test[column].fillna(test[column].mean())

X.head()

X.isnull().sum()

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
for col in X.columns:
    if X[col].dtype == "object":
        X[col] = le.fit_transform(X[col]).astype(int)
        test[col] = le.fit_transform(test[col]).astype(int)

X.describe()

X.corr()

plt.figure(figsize=(30,30))
sns.heatmap(X.corr(), cbar=True, square=True, fmt='.1f', annot=True, annot_kws={'size':5}, cmap='Blues')

Y.head()

sns.distplot(Y, kde=True)

X.columns

sns.scatterplot(x=X['OverallQual'], y=Y)
plt.show()

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.2, random_state=2)

X_train.shape, X_test.shape, Y_train.shape, Y_test.shape

from sklearn.linear_model import Lasso
model=Lasso()
model.fit(X_train,Y_train)

Y_pred=model.predict(X_test)

from sklearn.metrics import mean_absolute_error, mean_squared_error
print(f"Mean Square Error : {mean_squared_error(Y_pred, Y_test)}")
print(f"Mean Absolute Error : {mean_absolute_error(Y_pred, Y_test)}")

from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train,Y_train)
Y_pred_rf = rf.predict(X_test)
print(f"Mean Square Error RF: {mean_squared_error(Y_pred_rf, Y_test)}")
print(f"Mean Absolute Error RF: {mean_absolute_error(Y_pred_rf, Y_test)}")

from sklearn.metrics import r2_score
print("R2_score for rf = ", r2_score(Y_pred_rf, Y_test))

from sklearn.svm import SVR
svr = SVR(kernel='rbf', C=1.0, epsilon=0.1)
svr.fit(X_train,Y_train)
Y_pred_svr = svr.predict(X_test)
print(f"Mean Square Error SVR: {mean_squared_error(Y_pred_svr, Y_test)}")
print(f"Mean Absolute Error SVR: {mean_absolute_error(Y_pred_svr, Y_test)}")

from sklearn.linear_model import LinearRegression, Ridge
linreg=LinearRegression()
ridge = Ridge(alpha=0.1)
linreg.fit(X_train,Y_train)
ridge.fit(X_train,Y_train)
Y_pred_linreg=linreg.predict(X_test)
Y_pred_ridge=ridge.predict(X_test)
print(f"Mean Square Error linearRegression: {mean_squared_error(Y_pred_linreg, Y_test)}")
print(f"Mean Absolute Error LinearRegression: {mean_absolute_error(Y_pred_linreg, Y_test)}")
print(f"Mean Square Error Ridge: {mean_squared_error(Y_pred_ridge, Y_test)}")
print(f"Mean Absolute Error Ridge: {mean_absolute_error(Y_pred_ridge, Y_test)}")

from xgboost import XGBRegressor
xgb = XGBRegressor()
xgb.fit(X_train,Y_train)
Y_pred_xgb = xgb.predict(X_test)
print(f"Mean Square Error xgb: {mean_squared_error(Y_pred_xgb, Y_test)}")
print(f"Mean Absolute Error xgb: {mean_absolute_error(Y_pred_xgb, Y_test)}")

print("R2_score for xgb = ", r2_score(Y_pred_xgb, Y_test))

test_data = test.values
Y_predict = xgb.predict(test_data)

Y_predict

submission_df = pd.DataFrame({
    'Id': testId,
    'SalePrice': Y_predict
})

submission_df.to_csv('submission_xgb.csv', index=False)

solution = pd.read_csv('/content/submission_xgb.csv')
solution.head()

test_data = test.values
Y_predict_rf = rf.predict(test_data)

submission_df = pd.DataFrame({
    'Id': testId,
    'SalePrice': Y_predict_rf
})

submission_df.to_csv('submission_rf.csv', index=False)
