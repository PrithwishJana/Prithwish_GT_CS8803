import random
import sys
import time

random.seed(111)

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

def twoClauseCounter(formula):
    counter = {}
    for clause in formula:
        if (len(clause) == 2):
            for literal in clause:
                if (literal in counter):
                    counter[literal] += 1
                else:
                    counter[literal] = 1
    return counter

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
    formula, unitAssn = unitProp(formula)
    assignment = assignment + unitAssn
    if (not formula):
        return assignment
    if (formula == -1):
        return []
    var = twoClauseHeur(formula)
    sol = backtracking(BoolConsProp(formula, var), assignment + [var])
    if not sol:
        sol = backtracking(BoolConsProp(formula, -var), assignment + [-var])
    return sol

def twoClauseHeur(formula):
    cntr = twoClauseCounter(formula)
    valList = [cntr[k] for k in cntr]
    maxVal = max(valList)
    litList = []
    for k in cntr:
        if cntr[k] == maxVal:
            litList.append(k)
    return random.choice(litList)

def main():
    print ("-------------")
    print ("SAT Solver using 2-Clause Heuristic")
    print ("-------------")
    numVars, clauses = parseCNFfile("./einstein.cnf")
    st = time.time()
    solution = backtracking(clauses, [])
    et = time.time()
    if solution:
        for i in range(1, numVars + 1):
            if (i not in solution) and (-i not in solution):
                solution += x
        solution = sorted(solution, key = abs)
        print ("SAT")
        print ("v", " ".join([str(x) for x in solution]),  "0")
    else:
        print ("UNSAT")

    print("Execution Time:", et - st, "sec")

if __name__ == '__main__':
    main()
