import os

eachMapLen = 5
separator = '0'
mapLamda = lambda a, b: a + eachMapLen * b

colorMap = {}
colorList = ["red", "green", "white", "blue", "yellow"]
for colorIndx, color in enumerate(colorList):
    colorMap[color] = colorIndx
color_start = colorMap[colorList[0]]
color_end = colorMap[colorList[-1]]
print ("colorMap:", colorMap)
print ("color_start, color_end:", color_start, color_end)

nationMap = {}
nationList = ["british", "swedish", "danish", "norwegian", "german"]
for nationIndx, nation in enumerate(nationList):
    nationMap[nation] = nationIndx + 5
nation_start = nationMap[nationList[0]]
nation_end = nationMap[nationList[-1]]
print ("\nnationMap:", nationMap)
print ("nation_start, nation_end:", nation_start, nation_end)

drinkMap = {}
drinkList = ["tea", "coffee", "water", "beer", "milk"]
for drinkIndx, drink in enumerate(drinkList):
    drinkMap[drink] = drinkIndx + 10
drink_start = drinkMap[drinkList[0]]
drink_end = drinkMap[drinkList[-1]]
print ("\ndrinkMap:", drinkMap)
print ("drink_start, drink_end:", drink_start, drink_end)

cigarMap = {}
cigarList = ["prince", "blends", "pallmall", "bluemasters", "dunhill"]
for cigarIndx, cigar in enumerate(cigarList):
    cigarMap[cigar] = cigarIndx + 15
cigar_start = cigarMap[cigarList[0]]
cigar_end = cigarMap[cigarList[-1]]
print ("\ncigarMap:", cigarMap)
print ("cigar_start, cigar_end:", cigar_start, cigar_end)

petMap = {}
petList = ["dog", "cat", "bird", "horse", "fish"]
for petIndx, pet in enumerate(petList):
    petMap[pet] = petIndx + 20
pet_start = petMap[petList[0]]
pet_end = petMap[petList[-1]]
print ("\npetMap:", petMap)
print ("pet_start, pet_end:", pet_start, pet_end)

def computeHouseFormulae(start, end):
    formula = []
    for i in range(start, end + 1):
        houses = []
        for house in range(1, eachMapLen + 1):
            houses.append(str(mapLamda(house, i)))
        houses.append(separator)
        formula.append(' '.join(houses))
        #print (' '.join(houses))

        for h1 in range(1, eachMapLen + 1):
            for h2 in range(1, h1):
                toAdd = '-{} -{} {}'.format(
                    mapLamda(h2, i), 
                    mapLamda(h1, i), 
                    separator
                )
                #print ("a", toAdd)
                formula.append(toAdd)

            for j in range(start, i):
                toAdd = '-{} -{} {}'.format(
                    mapLamda(h1, i), 
                    mapLamda(h1, j), 
                    separator
                )
                #print ("b", toAdd)
                formula.append(toAdd)
    #print ("num formulae from computeHouseFormulae", len(formula))
    return ("\n".join(formula))

def isPairedWith(firstProp, secondProp):
    formulaToReturn = []
    for i in range(1, eachMapLen + 1):
        formulaToReturn.append("-" + str(mapLamda(i, firstProp)) +\
                                  " " +\
                                  str(mapLamda(i, secondProp)) +\
                                  " " +\
                                  separator)
        formulaToReturn.append(str(mapLamda(i, firstProp)) +\
                                  " " +\
                                  "-" + str(mapLamda(i, secondProp)) +\
                                  " " +\
                                  separator)
    return ("\n".join(formulaToReturn))

def isNeighborOf(firstProp, secondProp):
    formulaToReturn = []
    formulaToReturn.append("-" + str(mapLamda(1, firstProp)) +\
                              " " +\
                              str(mapLamda(2, secondProp)) +\
                              " " +\
                              separator)
    formulaToReturn.append("-" + str(mapLamda(eachMapLen, firstProp)) +\
                              " " +\
                              str(mapLamda(eachMapLen - 1, secondProp)) +\
                              " " +\
                              separator)
    for i in range(2, eachMapLen):
        formulaToReturn.append("-" + str(mapLamda(i, firstProp)) +\
                                  " " +\
                                  str(mapLamda(i - 1, secondProp)) +\
                                  " " +\
                                  str(mapLamda(i + 1, secondProp)) +\
                                  " " +\
                                  separator)
    return ("\n".join(formulaToReturn))


def computeHeader(formStr):
    literals = []
    lines = formStr.split("\n")
    for line in lines:
        ls = line.split()
        absLS = [abs(int(l)) for l in ls]
        literals.extend(absLS)
    literals = list(set(literals))
    return ('p cnf {} {}'.format(len(literals)-1, len(lines)))


def einsteinMain():
    formula = []
    args = []
    for strt in [0, 5, 10, 15, 20]:
        end = strt + 4
        formula.extend([computeHouseFormulae(strt, end)])

    # H1: "The Brit lives in the red house."
    formula.append(isPairedWith(nationMap["british"], colorMap["red"]))

    # H2: "The Swede keeps dogs as pets."
    formula.append(isPairedWith(nationMap["swedish"], petMap["dog"]))

    # H3: "The Dane drinks tea."
    formula.append(isPairedWith(nationMap["danish"], drinkMap["tea"]))

    # H5: "The green house’s owner drinks coffee."
    formula.append(isPairedWith(colorMap["green"], drinkMap["coffee"]))

    # H6: "The person who smokes Pall Mall rears birds."
    formula.append(isPairedWith(cigarMap["pallmall"], petMap["bird"]))

    # H7: "The owner of the yellow house smokes Dunhill."
    formula.append(isPairedWith(colorMap["yellow"], cigarMap["dunhill"]))

    # H8: "The man living in the center house drinks milk."
    formula.append('{} {}'.format(mapLamda(3, drinkMap["milk"]), separator))

    # H9: "The Norwegian lives in the first house."
    formula.append('{} {}'.format(mapLamda(1, nationMap["norwegian"]), separator))

    # H10: "The man who smokes Blends lives next to the one who keeps cats."
    formula.append(isNeighborOf(cigarMap["blends"], petMap["cat"]))

    # H11: "The man who keeps the horse lives next to the man who smokes Dunhill."
    formula.append(isNeighborOf(petMap["horse"], cigarMap["dunhill"]))

    # H12: "The owner who smokes Bluemasters drinks beer."
    formula.append(isPairedWith(cigarMap["bluemasters"], drinkMap["beer"]))

    # H13: "The German smokes Prince."
    formula.append(isPairedWith(nationMap["german"], cigarMap["prince"]))

    # H14: "The Norwegian lives next to the blue house."
    formula.append('{} {}'.format(mapLamda(2, colorMap["blue"]), separator))

    # H15: "The man who smokes Blends has a isNeighborOf who drinks water."
    formula.append(isNeighborOf(cigarMap["blends"], drinkMap["water"]))

    # H4: "The green house is on the left of the white house."
    for w in range(1, eachMapLen+1):
        for g in range(eachMapLen, 0, -1):
            if w-1 <= g <= w:
                continue
            formula.append('-{} -{} {}'.format(
                mapLamda(w, colorMap["white"]), mapLamda(g, colorMap["green"]), separator
            ))
    formulaStr = "\n".join(formula)
    cnf = "\n".join([computeHeader(formulaStr), formulaStr])
    return cnf


if __name__ == '__main__':
    with open('einstein.cnf', 'w') as f:
        f.write(einsteinMain())