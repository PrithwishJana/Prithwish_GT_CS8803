#!/bin/bash

for run in $(seq 1 1 100)
do
	> results/betterHeur_run_${run}.txt
	for N in $(seq 100 50 150)
	do
		for l in $(seq 30 2 60)
		do
			L=$((N * l/10))
			echo $N,$L
			python DPLL_betterHeuristic.py --N $N --L $L >> results/betterHeur_run_${run}.txt
			#python DPLL_2clause_PJ.py --N $N --L $L
			#python DPLL_random_PJ.py --N $N --L $L
		done
	done
done