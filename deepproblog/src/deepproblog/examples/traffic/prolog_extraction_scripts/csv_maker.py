from pyswip import Prolog
import pandas as pd
import numpy as np
import ast

# input = [P, C, O, R, L], output = 0/1
def translate_scenario_objects(scenario):
    # right down left up
    result = [0,0,0,0,0]
    i= 0 
    for _,ind in enumerate(scenario):
        obj = scenario[ind]
        if i<4:
            if "right" in obj:
                result[i] = 0
            elif "left" in obj:
                result[i] = 1
            elif "straight" in obj:
                result[i]= 2
            elif "crosswalk" in obj:
                result[i] =3
            else:
                result[i] = 4

        else:
            if "horizontal" in obj:
                # vertical direction has priority
                result[i] = 1
            elif "vertical" in obj:
                # horizontal direction has priority
                result[i] = 2
            else:
                result[i] = 0

        i +=1

    
    return result

def tranform_to_correct_ordering(ordering,direction):
    right_obj,down_obj,left_obj, top_obj,prio = ordering
    if direction == "left":
        if prio == 1:
            prio = 2
        elif prio == 2:
            prio = 1
        return [prio,left_obj,right_obj,down_obj,top_obj]
    elif direction == "right":
        if prio == 1:
            prio = 2
        elif prio == 2:
            prio = 1
        return [prio,right_obj,left_obj,top_obj,down_obj]
    elif direction == "up":
        

        return [prio,top_obj,down_obj,left_obj,right_obj]
    elif direction == "down":
        
        return [prio,down_obj,top_obj,right_obj,left_obj]
    
def getPriority(input):
    print(input)
    P, C, O, R, L = input
    prolog = Prolog()
    prolog.consult('prolog.pl')
    print("priority_rules({}, {}, {}, {}, {}, Y)".format(P, C, O, R, L))
    QUERY = "priority_rules({}, {}, {}, {}, {}, Y)".format(P, C, O, R, L)
    solution = next(prolog.query(QUERY))
    print("solution: ",solution) 
    return solution['Y']

df = pd.read_csv("~/deepproblog_traffic/deepproblog/src/deepproblog/examples/traffic/prolog_extraction_scripts/scenarios_test.csv")
      
df['Ordering'] = df['Ordering'].apply(lambda x: ast.literal_eval(x))
df['Scenario'] = df['Scenario'].apply(lambda x: ast.literal_eval(x))
new_scores = []
for i in range(len(df)):
#   right down left right
    new_score = np.array([0,0,0,0])
    for j in range(len(df['Ordering'][i])):
        add_score = max(0,1-50*j)
        for element in df['Ordering'][i][j]:
        
#             print(element,df['Scenario'][i]['right'] )
#             print(element,df['Scenario'][i]['down'] )
#             print(element,df['Scenario'][i]['left'] )
#             print(element,df['Scenario'][i]['up'] )
            if  element in df['Scenario'][i]['right'] : 
                new_score[0] = add_score
            elif element in df['Scenario'][i]['down'] : 
                new_score[1] = add_score
            elif  element in df['Scenario'][i]['left']: 
                new_score[2] = add_score
            elif  element in df['Scenario'][i]['up']: 
                new_score[3] = add_score
    new_scores.append(new_score)
#     print("newscore of ", df['Ordering'][i], "is ", new_scores[i])

df['priority'] = new_scores
data = list(zip(df['priority'],df['Scenario']))

prolog_scores  = []
for i in range(len(df)):
    print("processing i: ",i)
    answers,scenario  = data[i]
    original_ordering = translate_scenario_objects(scenario)
    print("original_ordering: ",original_ordering)
    new_directions = ["right","down","left","up"]
    
    #   right down left right
    new_orderings = [0,0,0,0]
    for j in range(0,len(new_directions)):
        print(original_ordering,new_directions[j])
        corect_ordering = tranform_to_correct_ordering(original_ordering,new_directions[j])
        print(corect_ordering)
        new_orderings[j] = corect_ordering
    #     new_orderings[j] = getPriority(corect_ordering)
    # print("answers: ",answers)
    # print("new_orderings: ",new_orderings)
    prolog_scores.append(new_orderings)
print(len(prolog_scores))
print(len(df))


df['prolog_priority'] = prolog_scores

df.to_csv('~/deepproblog_traffic/deepproblog/src/deepproblog/examples/traffic/prolog_extraction_scripts/scenarios_prolog_tmp.csv')
print(df.head())

# df.to_csv('prolog_scenarios.csv')