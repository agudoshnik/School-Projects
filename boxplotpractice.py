# -*- coding: utf-8 -*-
"""boxplotpractice.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NSDDu0nVXEsleovPRaFmmtdUjOFIqInY
"""

import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.rand(10, 5), columns=['1', '2', '3', '4', '5'])

df.plot.box()