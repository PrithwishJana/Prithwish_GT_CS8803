import random
import sys
import time
import os, argparse
parser = argparse.ArgumentParser()

parser.add_argument('--N', type=int, required=True)
parser.add_argument('--L', type=int, required=True)
parser.add_argument('--run', type=int, required=True)

args = parser.parse_args()

random.seed(111)
numCalls = 0

def parseCNFfile(cnfFilePath):
    clauseList = []
    for line in open(cnfFilePath):
        if (line[0] == 'p'):
            numVars = int(line.split()[2])
            continue
        clause = [int(x) for x in line[:-2].split()]
        clauseList.append(clause)
    return (numVars, clauseList)

def BoolConsProp(formula, unit):
    newFormula = []
    for clause in formula:
        if (unit in clause):
            continue
        elif (-unit in clause):
            newClause = []
            for f in clause:
                if (f != -unit):
                    newClause.append(f)
            if (len(newClause) == 0):
                return -1
            newFormula.append(newClause)
        else:
            newFormula.append(clause)
    return newFormula

def getLiteralList(formula):
    litList = []
    for clause in formula:
        litList.extend(clause)
    return list(set(litList))

def unitProp(formula):
    varAssn = []
    unitClauseList = []
    for cl in formula:
        if (len(cl)) == 1:
            unitClauseList.append(cl)
    while len(unitClauseList) != 0:
        unit = unitClauseList[0]
        unitLit = unit[0]
        formula = BoolConsProp(formula, unitLit)
        varAssn = varAssn + [unitLit]
        if (not formula):
            return (formula, varAssn)
        if (formula == -1):
            return -1, []
        unitClauseList = []
        for cl in formula:
            if (len(cl)) == 1:
                unitClauseList.append(cl)
    return formula, varAssn


def backtracking(formula, assignment):
    global numCalls
    numCalls += 1
    formula, unitAssn = unitProp(formula)
    assignment = assignment + unitAssn
    if (not formula):
        return assignment
    if (formula == -1):
        return []
    var = randomHeur(formula)
    sol = backtracking(BoolConsProp(formula, var), assignment + [var])
    if not sol:
        sol = backtracking(BoolConsProp(formula, -var), assignment + [-var])
    return sol

def randomHeur(formula):
    litList = getLiteralList(formula)
    return random.choice(litList)

def main():
    #print ("-------------")
    #print ("SAT Solver using Random-Choice Heuristic")
    print ("\n-------------")
    numVars, clauses = parseCNFfile(os.path.join("./cnf_n" + str(args.N), 
                            "cnf_n" + str(args.N) + "_l" + str(args.L) +\
                            "_run" + str(args.run) + ".txt"))
    st = time.time()
    solution = backtracking(clauses, [])
    et = time.time()
    if solution:
        for i in range(1, numVars + 1):
            if (i not in solution) and (-i not in solution):
                solution += [i]
        solution = sorted(solution, key = abs)
        print (f"N={args.N}; L={args.L}; run={args.run}; result=SAT;")
        #print ("v", " ".join([str(x) for x in solution]),  "0")
    else:
        print (f"N={args.N}; L={args.L}; run={args.run}; result=UNSAT;")

    print(f"N={args.N}; L={args.L}; run={args.run}; Execution Time (sec)={et - st};")
    print(f"N={args.N}; L={args.L}; run={args.run}; No. of DPLL calls={numCalls};")

if __name__ == '__main__':
    main()
