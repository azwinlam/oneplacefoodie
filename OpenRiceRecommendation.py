# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 16:08:55 2021

@author: azwin
"""
import pandas as pd
import numpy as np
import seaborn as sns

df = pd.read_csv("./data/openrice2021 - Copy.csv")

df.insert(0,"restaurantID", [i for i in range(df.shape[0])])

df.set_index("restaurantID")
