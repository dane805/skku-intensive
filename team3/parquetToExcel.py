import pandas as pd

df=pd.read_parquet("df_meta.parquet")
df.to_excel("excel.xlsx",index=False)