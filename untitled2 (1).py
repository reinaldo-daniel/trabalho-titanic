# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1J_jRv-A0q00byXuLi5u1twIGMySXPfE9
"""

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import OneHotEncoder, LabelEncoder, label_binarize
from sklearn.model_selection import train_test_split
from sklearn import model_selection, tree, preprocessing, metrics, linear_model
from sklearn.svm import LinearSVC
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LinearRegression, LogisticRegression, SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

"""---"""

train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

train

train.info()

train.describe()

test

test.info()

"""---"""

passengerId = test['PassengerId']
titanic_dif = train.append(test, ignore_index = True)

train_index = len(train)
test_index = len(titanic_dif) - len(test)

titanic_dif

titanic_dif.info()

df = pd.DataFrame()

titanic_dif['Survived'].nunique()

titanic_dif['Survived'].unique()

titanic_dif['Survived'].isnull().sum()

titanic_dif['Survived'].value_counts()

sns.countplot(data = titanic_dif, x = 'Sex')

def funcUm(data, column, count = True):
    print(f'Quantidade de valores únicos: {data[column].nunique()}')
    print(f'\nQuais são os valores únicos: {data[column].unique()}')
    print(f'\nQuantidade de valores nulos: {data[column].isnull().sum()}')
    print(f'\nQuantidade por opção: \n{data[column].value_counts()}')

    if count == True:
        sns.countplot(data = data, x = column, hue = 'Survived')
    else:
        sns.displot(data[column], kde = True)


funcUm(titanic_dif, 'Survived')

df['Survived'] = titanic_dif['Survived']

df

funcUm(titanic_dif, "Pclass")

df['Pclass'] = titanic_dif['Pclass']
df

titanic_dif['Sex'].unique()

titanic_dif['Sex'] = titanic_dif['Sex'].replace(['female', 'male'], [1, 0])

funcUm(titanic_dif, 'Sex')

df['Sex'] = titanic_dif['Sex']
df

funcUm(titanic_dif, "Age", False)

titanic_dif.corr()

for i in sorted(titanic_dif['Pclass'].unique()):
    print(f'Pessoas da {i}ª classe tem a média de idade de: {titanic_dif[titanic_dif["Pclass"] == i]["Age"].mean():.2f}')

titanic_dif[titanic_dif['Pclass'] == 1]['Age'].isnull().sum()

for i in titanic_dif.index:
    if pd.isnull(titanic_dif['Age'][i]):
        if titanic_dif['Pclass'][i] == 1:
            titanic_dif['Age'][i] = round(titanic_dif[titanic_dif['Pclass'] == 1]['Age'].mean())
        elif titanic_dif['Pclass'][i] == 2:
            titanic_dif['Age'][i] = round(titanic_dif[titanic_dif['Pclass'] == 2]['Age'].mean())
        elif titanic_dif['Pclass'][i] == 3:
            titanic_dif['Age'][i] = round(titanic_dif[titanic_dif['Pclass'] == 3]['Age'].mean())
    else:
        continue

titanic_dif['FamilySize'] = titanic_dif['SibSp'] + titanic_dif['Parch'] + 1

df['FamilySize'] = titanic_dif['FamilySize']
df.head()

funcUm(titanic_dif, 'Fare', False)

titanic_dif[titanic_dif['Fare'].isnull()]

titanic_dif[titanic_dif['Pclass'] == 3]['Fare'].mean()

titanic_dif['Fare'].fillna(titanic_dif[titanic_dif['Pclass'] == 3]['Fare'].mean(), inplace = True)

titanic_dif.isnull().sum()

df['Fare'] = titanic_dif['Fare']
df

titanic_dif

titanic_dif['Cabin'].unique()

funcUm(titanic_dif, 'Embarked')

titanic_dif[titanic_dif['Embarked'] == "S"]['Survived'].mean()

titanic_dif[titanic_dif['Embarked'] == "S"]['Pclass'].mean()

titanic_dif[titanic_dif['Embarked'] == "C"]['Survived'].mean()

titanic_dif[titanic_dif['Embarked'] == "C"]['Pclass'].mean()

titanic_dif[titanic_dif['Embarked'] == "Q"]['Survived'].mean()

titanic_dif[titanic_dif['Embarked'] == "Q"]['Pclass'].mean()

titanic_dif[titanic_dif['Embarked'].isnull()]

titanic_dif['Embarked'].fillna('C', inplace = True)

titanic_dif.isnull().sum()

df['Embarked'] = titanic_dif['Embarked']
df

titanic_dif['Name']

titanic_dif['Title'] = titanic_dif['Name'].apply(lambda name: name.split(',')[1].split('.')[0].strip())

titanic_dif['Title'].nunique()

titanic_dif['Title'].unique()

titanic_dif['Title'].value_counts()

titanic_dif['Title'] = [n if n in ['Mr', 'Miss', 'Mrs', 'Master'] else 'Person' for n in titanic_dif['Title']]

titanic_dif

df['Title'] = titanic_dif['Title']
df

funcUm(titanic_dif, 'Title')

titanic_dif.isnull().sum()

df

pclass = pd.get_dummies(df['Pclass'], prefix = "Pclass", drop_first = True)
title = pd.get_dummies(df['Title'], prefix = 'Title', drop_first = True)
embarked = pd.get_dummies(df['Embarked'], prefix = 'Embarked', drop_first = True)

titanic_completo = pd.concat([df, pclass, title, embarked], axis = 1)

titanic_completo.drop(['Pclass', 'Title', 'Embarked'], axis=1, inplace=True)

titanic_completo

train = titanic_completo[:train_index].copy()
test = titanic_completo[test_index:].copy()

train.info()

train['Survived'] = train['Survived'].astype(int)

X = train.drop('Survived', axis = 1)
y = train['Survived']

X_test = test.drop('Survived', axis = 1)

def func_acuracia(algoritmo, X_train, y_train, vc):
    modelo = algoritmo.fit(X_train, y_train)
    acuracia = round(modelo.score(X_train, y_train) * 100, 2)

    train_pred = model_selection.cross_val_predict(algoritmo, X_train, y_train, cv = vc, n_jobs = -1)
    acuracia_vc = round(metrics.accuracy_score(y_train, train_pred) * 100, 2)

    return acuracia, acuracia_vc

acc_rf, acc_vc_rf = func_acuracia(RandomForestClassifier(), X, y, 10)

print(f"Acurácia: {acc_rf}")
print(f"Acurácia Validação Cruzada: {acc_vc_rf}")

acc_log, acc_vc_log = func_acuracia(LogisticRegression(max_iter=1000), X, y, 10)

print(f"Acurácia: {acc_log}")
print(f"Acurácia Validação Cruzada: {acc_vc_log}")

acc_knn, acc_vc_knn = func_acuracia(KNeighborsClassifier(), X, y, 10)

print(f"Acurácia: {acc_knn}")
print(f"Acurácia Validação Cruzada: {acc_vc_knn}")

acc_gaussian, acc_vc_gaussian = func_acuracia(GaussianNB(), X, y, 10)

print(f"Acurácia: {acc_gaussian}")
print(f"Acurácia Validação Cruzada: {acc_vc_gaussian}")

acc_linear_svc, acc_vc_linear_svc = func_acuracia(LinearSVC(dual=False), X, y, 10)

print(f"Acurácia: {acc_linear_svc}")
print(f"Acurácia Validação Cruzada: {acc_vc_linear_svc}")

acc_sgd, acc_vc_sgd = func_acuracia(SGDClassifier(), X, y, 10)

print(f"Acurácia: {acc_sgd}")
print(f"Acurácia Validação Cruzada: {acc_vc_sgd}")

acc_dt, acc_vc_dt = func_acuracia(DecisionTreeClassifier(), X, y, 10)

print(f"Acurácia: {acc_dt}")
print(f"Acurácia Validação Cruzada: {acc_vc_dt}")

acc_gbt, acc_vc_gbt = func_acuracia(GradientBoostingClassifier(), X, y, 10)

print(f"Acurácia: {acc_gbt}")
print(f"Acurácia Validação Cruzada: {acc_vc_gbt}")

params = dict(
    max_depth = [n for n in range(1, 5)],
    min_samples_split = [n for n in range(2, 6)],
    min_samples_leaf = [n for n in range(2, 6)],
    n_estimators = [n for n in range(10, 50, 10)],
)

gbc = GradientBoostingClassifier()

gbc_cv = GridSearchCV(estimator = gbc, param_grid = params, cv = 10)
gbc_cv.fit(X, y)

print(f"Melhor pontuação: {gbc_cv.best_score_}")
print(f"Melhores parâmetros: {gbc_cv.best_estimator_}")

gradientBoostingClassifier_pred = gbc_cv.predict(X_test)

kaggle = pd.DataFrame({'PassengerId': passengerId, 'Survived': gradientBoostingClassifier_pred})
kaggle.to_csv('./trabalho_titanic_faculdade.csv', index=False)