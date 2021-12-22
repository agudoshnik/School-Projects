# -*- coding: utf-8 -*-
"""Individual Project

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1S7iDkV9uAfYSTa1qzRFs23Wc5xI3tvPd
"""

# preamble to be able to run notebooks in Jupyter and Colab
try:
    from google.colab import drive
    import sys
    
    drive.mount('/content/drive')
    notes_home = "/content/drive/My Drive/csc310/"
    user_home = "/content/drive/My Drive/"
    
    sys.path.insert(1,notes_home) # let the notebook access the notes folder

except ModuleNotFoundError:
    notes_home = "" # running native Jupyter environment -- notes home is the same as the notebook
    user_home = ""  # under Jupyter we assume the user directory is the same as the notebook

import pandas as pd
from sklearn import tree
from treeviz import tree_print

"""##**Original Data:**"""

hawks = pd.read_csv(notes_home+"Hawks.csv")
hawks

hawks.describe()

hawks.count()

"""##**Project Proposal:**

The dataset I will be using is about a bunch of hawks that were caught, tagged, measured and released between 1992 and 2003.  

Rows: 908  

Columns: 20 

Target Label: No 

Numerical Columns: 14  

Categorical: 6 

For this project and to make it about machine learning I will cut the data set down to Species, Culmen, Hallux, Wing, Weight, and Tail. I want to do this data cleaning since some columns such as Tarsus since it only has 75 entries out of 908 maximum entries. This eliminates the really bad rows of data and give the project the goal about **if a machine can figure out what bird is which from the measurements given**.
"""

df = hawks[['Species', 'Wing', 'Weight','Culmen','Hallux','Tail']]

df = df.replace('RT','Red-Tailed')
df = df.replace('CH','Coopers Hawk')
df = df.replace('SS','Sharp-Shinned')
df = df.dropna()

"""##**Modified Data:**"""

df

"""Dataset after Adjustments: 

Rows: 891 

Columns: 6 

Target Label: Species 

Numerical Columns: 5 

Categorical Columns: 1 

Since there were a few NA’s in the remaining data I dropped the entire row to make the project easier.  

##**Question:**
Now that the dataset is cleaned up, I want to answer the question, from the given measurements, can the type of hawk between Red-Tailed, Coopers, or Sharp-Shinned be determined, is there a pattern to determine which hawk is which.

##**Data Summary:**
"""

df.count()

df.describe()

df.Species.value_counts()

"""##**Visuals of data:**"""

df.hist()

df.plot.bar()

"""##**Decision Trees with 5 Cross Folds:**

Data Set Up:
"""

from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

# set up our sklearn data shape for the hawks data
X  = df.drop(['Species'],axis=1)
y = df['Species']

# split the data - 50% training 50% testing
datasets = train_test_split(X, y, train_size=0.3, test_size=0.2, random_state=2)
X_train, X_test, y_train, y_test = datasets

"""##**Low-Complexity:**"""

# set up the tree model object - limit the complexity to put us somewhere in the middle of the graph.
model = tree.DecisionTreeClassifier(criterion='entropy', max_depth=1)

# fit the model on the training set of data
model.fit(X_train, y_train)
tree_print(model,X)

# Train results: evaluate the model on the testing set of data
y_train_model = model.predict(X_train)
print("Train Accuracy: {:3.2f}".format(accuracy_score(y_train, y_train_model)))

# Test results: evaluate the model on the testing set of data
y_test_model = model.predict(X_test)

# do the 5-fold cross validation
scores = cross_val_score(model, X, y, cv=5)
print("Fold Accuracies: {}".format(scores))
print("Accuracy: {:3.2f}".format(scores.mean()))

"""##**Medium-Complexity:**"""

# set up the tree model object - limit the complexity to put us somewhere in the middle of the graph.
model = tree.DecisionTreeClassifier(criterion='entropy', max_depth=3)

# fit the model on the training set of data
model.fit(X_train, y_train)
tree_print(model,X)

# Train results: evaluate the model on the testing set of data
y_train_model = model.predict(X_train)
print("Train Accuracy: {:3.2f}".format(accuracy_score(y_train, y_train_model)))

# Test results: evaluate the model on the testing set of data
y_test_model = model.predict(X_test)
print("Fold Accuracies: {}".format(scores))
print("Accuracy: {:3.2f}".format(scores.mean()))

"""##**High-Complexity:**"""

# set up the tree model object - limit the complexity to put us somewhere in the middle of the graph.
model = tree.DecisionTreeClassifier(criterion='entropy', max_depth=None)

# fit the model on the training set of data
model.fit(X_train, y_train)
tree_print(model,X)

# Train results: evaluate the model on the testing set of data
y_train_model = model.predict(X_train)
print("Train Accuracy: {:3.2f}".format(accuracy_score(y_train, y_train_model)))

# Test results: evaluate the model on the testing set of data
y_test_model = model.predict(X_test)
print("Fold Accuracies: {}".format(scores))
print("Accuracy: {:3.2f}".format(scores.mean()))

"""##**Best Tree With Confusion Matrix:**"""

from sklearn.metrics import confusion_matrix
from assets.confint import classification_confint
from sklearn.model_selection import GridSearchCV
# decision trees
model = tree.DecisionTreeClassifier(random_state=1)

# grid search
param_grid = {'max_depth': list(range(1,21)), 'criterion': ['entropy','gini'] }
grid = GridSearchCV(model, param_grid, cv=5)
grid.fit(X, y)
print("Grid Search: best parameters: {}".format(grid.best_params_))

# accuracy of best model with confidence interval
best_model = grid.best_estimator_
predict_y = best_model.predict(X)
acc = accuracy_score(y, predict_y)
lb,ub = classification_confint(acc,X.shape[0])
print("Accuracy: {:3.2f} ({:3.2f},{:3.2f})".format(acc,lb,ub))

# build the confusion matrix
cm = confusion_matrix(y, predict_y)
cm_df = pd.DataFrame(cm)
print("Confusion Matrix:\n{}".format(cm_df))

"""##**KNN:**"""

import numpy as np
np.set_printoptions(formatter={'float_kind':"{:3.2f}".format})
from sklearn.neighbors import KNeighborsClassifier
# set up the model with k=3
model = KNeighborsClassifier(n_neighbors=3)

# do train-test
train_X, test_X, train_y, test_y = train_test_split(X, y, train_size=0.8, test_size=0.2)
model.fit(train_X, train_y)
predict_y = model.predict(test_X)
print("Train-Test Accuracy: {:3.2f}".format(accuracy_score(test_y, predict_y)))

# do the 5-fold cross validation
scores = cross_val_score(model, X, y, cv=5)
print("Fold Accuracies: {}".format(scores))
print("XV Accuracy: {:3.2f}".format(scores.mean()))

"""##**KNN with Confusion Matrix:**"""

# KNN
model = KNeighborsClassifier()

# grid search
param_grid = {'n_neighbors': list(range(1,51))}
grid = GridSearchCV(model, param_grid, cv=5)
grid.fit(X,y)
print("Grid Search: best parameters: {}".format(grid.best_params_))

# accuracy of best model with confidence interval
best_model = grid.best_estimator_
predict_y = best_model.predict(X)
acc = accuracy_score(y, predict_y)
lb,ub = classification_confint(acc,X.shape[0])
print("Accuracy: {:3.2f} ({:3.2f},{:3.2f})".format(acc,lb,ub))

# build the confusion matrix
cm = confusion_matrix(y, predict_y)
cm_df = pd.DataFrame(cm)
print("Confusion Matrix:\n{}".format(cm_df))

"""##**NonLinear-Regression:**
Is there any relation between Culmen(tip of beak) and Hallux(talon)?
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
#model
model = MLPRegressor(hidden_layer_sizes=(100,), activation='tanh', max_iter=50000)
model.fit(df['Culmen'].values.reshape(-1,1),df['Hallux'])
# plot the model ontop of the data
plt.scatter(df['Culmen'],df['Hallux'])
plt.xlabel('Culmen')
plt.ylabel('Hallux')

x_ticks = np.arange(0,25.0,0.1)
y_ticks = model.predict(x_ticks.reshape(-1, 1))
plt.plot(x_ticks,y_ticks,"r-")

# compute the R^2 score 
rs = model.score(df['Culmen'].values.reshape(-1,1),df['Hallux'])
print("R^2 score: {:3.2f}".format(rs))

"""##**KNN Regression:**"""

from sklearn.neighbors import KNeighborsRegressor
from assets.confint import regression_confint
X = df['Culmen'].values.reshape(-1,1)
y = df['Hallux']
# setting up grid search
model = KNeighborsRegressor()
param_grid = {'n_neighbors': list(range(1,11))}
grid = GridSearchCV(model, param_grid, cv=5)

# performing grid search
grid.fit(X,y)

# print out what we found
print("Best parameters: {}".format(grid.best_params_))

# plot the best model ontop of the data
plt.scatter(df['Culmen'],df['Hallux'])
plt.xlabel('Culmen')
plt.ylabel('Hallux')

best_model = grid.best_estimator_
x_ticks = np.arange(0,25.0,0.1)
y_ticks = best_model.predict(x_ticks.reshape(-1, 1))
plt.plot(x_ticks,y_ticks,"r-")

# compute the R^2 score and CI of the best model
rs = best_model.score(df['Culmen'].values.reshape(-1,1),df['Hallux'])
obs = df.shape[0]
vars = 1
lb, ub = regression_confint(rs, obs, vars)
print("R^2 score: {:3.2f} ({:3.2f}, {:3.2f})".format(rs,lb,ub))

"""Is there any relation between Wing and Tail?"""

from sklearn.neighbors import KNeighborsRegressor
from assets.confint import regression_confint
X = df['Wing'].values.reshape(-1,1)
y = df['Tail']
# setting up grid search
model = KNeighborsRegressor()
param_grid = {'n_neighbors': list(range(1,11))}
grid = GridSearchCV(model, param_grid, cv=5)

# performing grid search
grid.fit(X,y)

# print out what we found
print("Best parameters: {}".format(grid.best_params_))

# plot the best model ontop of the data
plt.scatter(df['Wing'],df['Tail'])
plt.xlabel('Wing')
plt.ylabel('Tail')

best_model = grid.best_estimator_
x_ticks = np.arange(0,25.0,0.1)
y_ticks = best_model.predict(x_ticks.reshape(-1, 1))
plt.plot(x_ticks,y_ticks,"r-")

# compute the R^2 score and CI of the best model
rs = best_model.score(df['Wing'].values.reshape(-1,1),df['Tail'])
obs = df.shape[0]
vars = 1
lb, ub = regression_confint(rs, obs, vars)
print("R^2 score: {:3.2f} ({:3.2f}, {:3.2f})".format(rs,lb,ub))

"""Is there any relation between Wing and Hallux?"""

X = df['Wing'].values.reshape(-1,1)
y = df['Hallux']
# setting up grid search
model = KNeighborsRegressor()
param_grid = {'n_neighbors': list(range(1,11))}
grid = GridSearchCV(model, param_grid, cv=5)

# performing grid search
grid.fit(X,y)

# print out what we found
print("Best parameters: {}".format(grid.best_params_))

# plot the best model ontop of the data
plt.scatter(df['Wing'],df['Hallux'])
plt.xlabel('Wing')
plt.ylabel('Hallux')

best_model = grid.best_estimator_
x_ticks = np.arange(0,25.0,0.1)
y_ticks = best_model.predict(x_ticks.reshape(-1, 1))
plt.plot(x_ticks,y_ticks,"r-")

# compute the R^2 score and CI of the best model
rs = best_model.score(df['Wing'].values.reshape(-1,1),df['Hallux'])
obs = df.shape[0]
vars = 1
lb, ub = regression_confint(rs, obs, vars)
print("R^2 score: {:3.2f} ({:3.2f}, {:3.2f})".format(rs,lb,ub))

"""Is there any relation between Culmen and Tail?"""

X = df['Culmen'].values.reshape(-1,1)
y = df['Tail']
# setting up grid search
model = KNeighborsRegressor()
param_grid = {'n_neighbors': list(range(1,11))}
grid = GridSearchCV(model, param_grid, cv=5)

# performing grid search
grid.fit(X,y)

# print out what we found
print("Best parameters: {}".format(grid.best_params_))

# plot the best model ontop of the data
plt.scatter(df['Culmen'],df['Tail'])
plt.xlabel('Culmen')
plt.ylabel('Tail')

best_model = grid.best_estimator_
x_ticks = np.arange(0,25.0,0.1)
y_ticks = best_model.predict(x_ticks.reshape(-1, 1))
plt.plot(x_ticks,y_ticks,"r-")

# compute the R^2 score and CI of the best model
rs = best_model.score(df['Culmen'].values.reshape(-1,1),df['Tail'])
obs = df.shape[0]
vars = 1
lb, ub = regression_confint(rs, obs, vars)
print("R^2 score: {:3.2f} ({:3.2f}, {:3.2f})".format(rs,lb,ub))

"""##**Analysis:**
##Decesion Trees:
For the most part, since the data became really clean and organized, all of the decesion trees were accurate with guessing type of hawk depending on the informarion given even at really low learning rates of only having 30% given with low testing to give the tree less chances of getting the data right. So from just knowing the Culmen length or Weight, it is very easily possible to determine the type of hawk between Red-Tailed, Sharp-Shinned, and Cooper's Hawk. The best tree was KNN(.98 accuracy) vs medium and low- complexity at .92 accuracy.
##Regression Models:
Culmen and Hallux:
From the regression model I have learned Culmen(part of a bird's beak) and Hallux(talon) have very little to do with each other. So with knowledge about a Culmen, it would be very unlikely to guess a Hallux. (.25 score)

Wing and Tail: 
From the regression model I have learned Wing and Tail are related . So with knowledge about a Wing, it would be very likely to guess a Tail.     (.89 score)

Wing and Hallux:
From the regression model I have learned Wing and Hallux are  not related. So with knowledge about a Wing, it would be very likely to guess a Hallux.(.26 score)

Culmen and Tail: 
From the regression model I have learned Culmen and Tail are related . So with knowledge about a Culmen, it would be very likely to guess a Tail.
(.89 score)
"""