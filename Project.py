import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


path = os.getcwd()

print(path)
df=pd.read_csv("./BDPV_opendata_installations/BDPV_opendata_installations.csv", error_bad_lines=False)
