import pandas as pd
import ast

def turn_into_priority_rule(situation,answer):
    P, C, O, R, L = situation 
    return "priority_rules("+str(P)+" ,"+str(C)+" ,"+str(O)+" ,"+str(R)+" ,"+str(L)+" ," +str(1)+")."



df = pd.read_csv("/home/nathan/deepproblog_traffic/deepproblog/src/deepproblog/examples/traffic/scenarios_prolog.csv")

# df['prolog_priority_solved'] = df['prolog_priority_solved'].apply(lambda x: ast.literal_eval(x))
new_data = []
data = list(df['priority'])
for i in range(len(data)):
    new_list = []
    for j in range(len(data[i])):
        if data[i][j] == "1":
            new_list.append(1)
        elif data[i][j] == "0":
            new_list.append(0)
    new_data.append(new_list)

priority_data = new_data
df['priority'] = priority_data
df['prolog_priority'] = df['prolog_priority'].apply(lambda x: ast.literal_eval(x))




seen = []
for i in range(len(df)):
    for j in range(4):
        if df['prolog_priority'][i][j] not in seen:
            # print("senario_encoding: ",df['prolog_priority'][i][j])
            seen.append(df['prolog_priority'][i][j])
            # print("answer: ",df['priority'][i][j])
            print(turn_into_priority_rule(df['prolog_priority'][i][j],df['priority'][i][j]))
    
print("len seen: ",len(seen))