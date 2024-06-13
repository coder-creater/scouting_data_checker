import pandas as pd
import numpy as np


df = pd.read_csv('actuals.csv')

print(np.mean(df['AutoAmps']))