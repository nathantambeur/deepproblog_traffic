from pyswip import Prolog
import pandas as pd
import ast

def getPriority(input):
    P, C, O, R, L = input
    prolog = Prolog()
    prolog.consult('prolog.pl')

    QUERY = "has_priority({}, {}, {}, {}, {}, Y)".format(P, C, O, R, L)
    solution = next(prolog.query(QUERY))
    return solution["Y"]