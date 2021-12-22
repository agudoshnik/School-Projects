# -*- coding: utf-8 -*-
"""Data Visualization

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t5dmYml5Zf3_FH3c17RK2JsNbDiGPrkP
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

pip install treeviz

import pandas as pd
from sklearn import tree
from sklearn.metrics import accuracy_score
from treeviz import tree_print
mammals = pd.read_csv(notes_home+"mammals2.csv")
mammals

"""1."""

mammals.plot.scatter(x = 'Animal', y = 'Legs')

mammals.plot.hist(x = 'Mammal', y = 'Legs')

mammals.plot.bar(x = 'Animal', y = 'Legs')

mammals.plot.pie(y = 'Legs')

mammals.plot.density()

mammals.plot.box()

mammals.plot.area()

"""The data seems to be unimodal since the data seems to be based on the amount of legs the animals had since that is the only numerical data available to graph. Since the only data is the legs, the scatter plot clusters basically just show which animals have a certain amount of legs and either what animal they are or do they have another feature (Wings, Fur) The decision model seemed to go off fur not legs, so I do not belive they are represented in the clusters. This is not a balanced dataset because there are a lot more mammals with 4 legs and fur than any other animal. In the dataset there is only one bird compared to the other animals, so that makes it unbalanced also. This shows up in the tree model since it only makes one level based on if the animal has fur, it is a mammal, which isnt true for all mammals but only true for this dataset.

2.
"""

mammal = pd.read_csv(notes_home+"mammals_numeric.csv")

features_mammal = mammal.drop(['Mammal'],axis = 1)
features_mammal.head()

target_mammal = pd.DataFrame(mammal['Mammal'])
target_mammal.head()

dtree = tree.DecisionTreeClassifier(criterion="entropy")
dtree.fit(features_mammal,target_mammal)

tree_print(dtree,features_mammal)

predict_array = dtree.predict(features_mammal)      # produces an array of labels
predicted_labels = pd.DataFrame(predict_array)  # turn it into a DF
predicted_labels.columns = ['Mammal']          # name the column - same name as in target!
predicted_labels.head()

predicted_labels.equals(target_mammal)

print("Our model accuracy is: {}".format(accuracy_score(target_mammals, predicted_labels)))

mammal.plot.scatter(x = 'Legs', y = 'Fur')

"""Since the data was pretty simple to sort, interpertation was pretty easy but I prefer the visualized data. The major trend in both graph and tree is fur both being 50/50. So the data tree  relate to the clusters a little bit since the tree is 50/50 on while although the graph focuses on amount of legs the fur is also 50/50. """