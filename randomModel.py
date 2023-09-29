import subprocess
import os, shutil
import sys
import random, math

from pysat.formula import CNF

from scipy.stats import bernoulli, geom

def dimacs(cnf, newlines=False):
	if not newlines:
		s = f'p cnf {cnf.nv} {len(cnf.clauses)} '
		for c in cnf.clauses:
			s = f'{s}{" ".join([str(l) for l in c])} 0 '
	else:
		s = f'p cnf {cnf.nv} {len(cnf.clauses)}\n'
		for c in cnf.clauses:
			s = f'{s}{" ".join([str(l) for l in c])} 0\n'
	return s

def sampleDIMACS(N, L, K=3):
	#N = number of variables
	#L = number of clauses
	#K = number of distinct literals per clause
	inst = None

	cnf = CNF()
	numClauses = L
	while (numClauses):
		vs = sorted(random.sample(range(1,N+1), K))
		cnf.append([random.choice([-1,1])*v for v in vs])
		numClauses -= 1

	inst = dimacs(cnf, newlines=True).strip()
	return inst

#main
NList = [100, 150]

for N in NList:

	folderPath = "./cnf_n" + str(N)
	if os.path.exists(folderPath):
		shutil.rmtree(folderPath)
	os.makedirs(folderPath)

	L_list = list(range(3 * N, 6 * N + 1, int(math.floor(0.2 * N))))
	for LIndx, L in enumerate(L_list):
		f = open(folderPath + "/cnf_n" + str(N) + "l" + str(L) + ".txt", "a")
		print (N, L)
		cnfInst = sampleDIMACS(N, L)
		f.write(cnfInst)
	f.close()
	print ("")

