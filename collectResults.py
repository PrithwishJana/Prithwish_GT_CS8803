import os, re, openpyxl

heurList = ["betterHeur", "randomHeur", "twoClauseHeur"]
excelPath = os.path.join("results", "aTmpl-DPLLResults_Prithwish.xlsx")
excelPathSave = os.path.join("results", "a-DPLLResults_Prithwish.xlsx")

wb = openpyxl.load_workbook(excelPath)

for heur in heurList:
    for run in range(1, 101):
        print (heur, run)
        resultFilePath = os.path.join("results", heur + "_run_" + str(run) + ".txt")
        #print ("Result_" + heur, "ExecTime_" + heur, "NumDPLLCalls_" + heur)
        ws1 = wb["Result_" + heur]
        ws2 = wb["ExecTime_" + heur] 
        ws3 = wb["NumDPLLCalls_" + heur]
        print (ws1, ws2, ws3)
        with open(resultFilePath, mode="r", encoding="utf-8") as f:
            fContents = f.read()
            print (fContents)
            resultList = []
            execTimeList = []
            numDPLLCallsList = []
            for N in [100, 150]:
                for l in range(30, 61, 2):
                    L = int(N * 1.0 * l / 10)
                    #print (L)
                    findStr1 = f"N={N}; L={L}; run={run}; result=(.*?);"
                    findStr2 = f"N={N}; L={L}; run={run}; Execution Time \(sec\)=(.*?);"
                    findStr3 = f"N={N}; L={L}; run={run}; No. of DPLL calls=(.*?);"
                    p1 = re.compile(findStr1)
                    p2 = re.compile(findStr2)
                    p3 = re.compile(findStr3)
                    find1 = re.findall(p1, fContents)
                    find2 = re.findall(p2, fContents)
                    find3 = re.findall(p3, fContents)
                    if len(find1) != 0:
                        resultList.append(find1[0])
                        execTimeList.append(float(find2[0]))
                        numDPLLCallsList.append(int(find3[0]))
                    else:
                        resultList.append("")
                        execTimeList.append("")
                        numDPLLCallsList.append("")
        for i in range(len(resultList)):
            ws1.cell(row = i + 2, column = run + 3).value = resultList[i]
            ws2.cell(row = i + 2, column = run + 3).value = execTimeList[i]
            ws3.cell(row = i + 2, column = run + 3).value = numDPLLCallsList[i]

wb.save(excelPathSave)
            
