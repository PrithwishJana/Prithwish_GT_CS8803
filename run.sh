#!/bin/bash

#SBATCH --time=0-2:00      # time (DD-HH:MM)

for run in $(seq 1 1 100)
do
	> results/randomHeur_run_${run}.txt
	for N in $(seq 100 50 150)
	do
		for l in $(seq 30 2 60)
		do
			L=$((N * l/10))
			echo $N,$L,$run
			#timeout 300 python DPLL_betterHeuristic.py --N $N --L $L --run $run >> results/betterHeur_run_${run}.txt
			#timeout 300 python DPLL_2clause_PJ.py --N $N --L $L --run $run >> results/twoClauseHeur_run_${run}.txt
			timeout 300 python DPLL_random_PJ.py --N $N --L $L --run $run >> results/randomHeur_run_${run}.txt
		done
	done
done