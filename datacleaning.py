# -*- coding: utf-8 -*-
"""dataCleaning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SPTEbsQ_l2qms6GCmL-T0IlXR6nKEIh0
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

import numpy as np
import pandas as pd

southAmerica = pd.read_csv(notes_home+"southAmerica.csv")
southAmerica

southAmerica.columns

southAmerica.index

southAmerica.values

southAmerica.isnull().values.sum()

southAmerica.isnull().sum(axis = 0)

"""Province_State seems to have the most null values at 26% so deleting it out might be best. The other data doesnt really need to be deleted since there are so few instances of null but modifying to 0 wouldn't really disturb anything either since theres so few null values."""

southAmerica.drop(columns="Province_State", inplace=True)

southAmerica.fillna(0)

"""To at least get rid of strings in ints, Im converting all of the remaining columns into series and forcing them into numeric based values."""

s1 = southAmerica.iloc[:,0]
s2 = southAmerica.iloc[:,1]
s3 = southAmerica.iloc[:,3]
s4 = southAmerica.iloc[:,4]
s5 = southAmerica.iloc[:,5]

pd.to_numeric(s3,errors='coerce')

pd.to_numeric(s4,errors='coerce')

pd.to_numeric(s5,errors='coerce')

"""I will now join all the series back into one table to replace all nulls that were put in place of strings"""

southAmerica = pd.concat([s1, s2], axis=1)
southAmerica = pd.concat([southAmerica, s3], axis=1)
southAmerica = pd.concat([southAmerica, s4], axis=1)
southAmerica = pd.concat([southAmerica, s5], axis=1)
southAmerica.fillna(0)
southAmerica

"""To help organize the data a little more if there is a negative number in Active, it will be forced to 0."""

southAmerica['Active'] = southAmerica['Active'].abs()

mostcases = southAmerica.nlargest(2315010,['Active']).drop_duplicates('Country_Region')
mostcases.nlargest(10,['Active'])

from google.colab import files
southAmerica.to_csv('finished.csv') 
files.download('finished.csv')

southAmerica