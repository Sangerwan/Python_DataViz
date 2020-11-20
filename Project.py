import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


path = os.getcwd()

print(path)
df=pd.read_csv("./BDPV_opendata_installations/BDPV_opendata_installations.csv", sep=';')
print('describe')
print(df.describe())
print('value')
print(df.values)
print('column')
print(df.columns)
print('index')
print(df.index)
i= df.columns

print(df['id'])