import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

df=pd.read_csv("./BDPV-opendata-installations/BDPV-opendata-installations.csv", error_bad_lines=False)
type(df)
