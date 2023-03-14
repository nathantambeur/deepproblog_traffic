from pyswip import Prolog
import pandas as pd
import ast
# input = [P, C, O, R, L], output = 0/1
def getPriority(input):
    P, C, O, R, L = input
    prolog = Prolog()
    prolog.consult('prolog.pl')

    QUERY = "has_priority({}, {}, {}, {}, {}, Y)".format(P, C, O, R, L)
    solution = next(prolog.query(QUERY))
    return solution["Y"]

def all_transformation(input):
    res = [0,0,0,0]
    for i in range(4):
        res[i]  = getPriority(input[i])
    return res
df = pd.read_csv("/home/nathan/deepproblog_traffic/deepproblog/src/deepproblog/examples/traffic/prolog_extraction_scripts/scenarios_prolog_tmp.csv")

df["prolog_priority"] = df["prolog_priority"].apply(lambda x: ast.literal_eval(x))
df["prolog_priority_solved"] = df["prolog_priority"].transform(lambda x: all_transformation(x))
df.to_csv('~/deepproblog_traffic/deepproblog/src/deepproblog/examples/traffic/prolog_extraction_scripts/scenarios_prolog.csv')
print(df)