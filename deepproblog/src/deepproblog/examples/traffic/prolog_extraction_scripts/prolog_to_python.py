from pyswip import Prolog

# input = [P, C, O, R, L], output = 0/1
def getPriority(input):
    P, C, O, R, L = input
    prolog = Prolog()
    prolog.consult('prolog.pl')

    QUERY = "has_priority({}, {}, {}, {}, {}, Y)".format(P, C, O, R, L)
    solution = next(prolog.query(QUERY))
    return solution["Y"]

print(getPriority([2,1,0,2,0]))