import pandas as pd


df = pd.read_csv("/home/nathan/deepproblog_traffic/deepproblog/src/deepproblog/examples/traffic/prolog_scenarios.csv")
df2 = df[0:2700]
df3 = df[2700:]
print(df2)
print(df3)
df2.to_csv("/home/nathan/deepproblog_traffic/deepproblog/src/deepproblog/examples/traffic/prolog_scenarios.csv",index=False)
df3.to_csv("/home/nathan/deepproblog_traffic/deepproblog/src/deepproblog/examples/traffic/prolog_scenarios_test.csv",index=False)