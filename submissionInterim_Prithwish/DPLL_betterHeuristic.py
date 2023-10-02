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

def absWCounter(formula):
    wt = 2
    ctr = {}
    for clause in formula:
        exp = -len(clause)
        for literal in clause:
            if abs(literal) not in ctr:
                ctr[abs(literal)] = wt ** exp
            else:
                ctr[abs(literal)] += wt ** exp
    return ctr

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
    var = JeroslowWangHeur(formula)
    sol = backtracking(BoolConsProp(formula, var), assignment + [var])
    if not sol:
        sol = backtracking(BoolConsProp(formula, -var), assignment + [-var])
    return sol

def JeroslowWangHeur(formula):
    cntr = absWCounter(formula)
    return max(cntr, key = cntr.get)

def main():
    print ("-------------")
    print ("SAT Solver using Jeroslow-Wang rule Heuristic")
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
