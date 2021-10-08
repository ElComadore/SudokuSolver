import copy


def createSquare(string):
    if len(string) != 81:
        print("You fucked it!")
        exit(-1)

    square = [[0 for x in range(9)] for y in range(9)]
    string = list(string)

    for i in range(9):
        for j in range(9):
            if string[j + 9 * i] != 0:
                square[i][j] = int(string[j + 9 * i])
    return square


def createSeed(square):
    string = ""
    for i in square:
        for j in i:
            if isinstance(j, int):
                string = string + str(j)
            else:
                string = string + "0"
    return string


def initPossible(square):
    for i in range(9):
        for j in range(9):
            if square[i][j] == 0:
                square[i][j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    return square


def refinePossible(poss):
    for i in range(9):
        for j in range(9):
            if isinstance(poss[i][j], int):
                for k in range(9):
                    if isinstance(poss[i][k], list):
                        if poss[i][j] in poss[i][k]:
                            poss[i][k].remove(poss[i][j])
                for k in range(9):
                    if isinstance(poss[k][j], list):
                        if poss[i][j] in poss[k][j]:
                            poss[k][j].remove(poss[i][j])
                for k in range(i - i % 3, i - i % 3 + 3):
                    for l in range(j - j % 3, j - j % 3 + 3):
                        if isinstance(poss[k][l], list):
                            if poss[i][j] in poss[k][l]:
                                poss[k][l].remove(poss[i][j])


def findSingles(poss):
    ind = list()
    for i in range(9):
        for j in range(9):
            if isinstance(poss[i][j], list):
                if len(poss[i][j]) == 1:
                    poss[i][j] = poss[i][j][0]
                    ind.append((i, j))
    return ind


def checkSubSquares(poss):
    for i in range(3):
        for j in range(3):
            for n in range(1, 10):
                coords = list()
                amount = 0
                for k in range(3 * i, 3 * i + 3):
                    for l in range(3 * j, 3 * j + 3):
                        if isinstance(poss[k][l], list):
                            if n in poss[k][l]:
                                coords = [k, l]
                                amount += 1
                if amount == 1:
                    poss[coords[0]][coords[1]] = [n]


def inferredLines(poss):
    for i in range(3):
        for j in range(3):
            for n in range(1, 10):
                coords = list()
                amount = 0
                for k in range(3 * i, 3 * i + 3):
                    for l in range(3 * j, 3 * j + 3):
                        if isinstance(poss[k][l], list):
                            if n in poss[k][l]:
                                coords.append((k, l))
                                amount += 1
                if amount > 1:
                    row = coords[0][0]
                    numRow = 1
                    col = coords[0][1]
                    numCol = 1
                    for o in range(1, amount):
                        if coords[o][0] == row:
                            numRow += 1
                        if coords[o][1] == col:
                            numCol += 1
                    if numRow == amount:
                        for k in range(9):
                            if isinstance(poss[coords[0][0]][k], list) and (coords[0][0], k) not in coords:
                                if n in poss[coords[0][0]][k]:
                                    poss[coords[0][0]][k].remove(n)
                    if numCol == amount:
                        for k in range(9):
                            if isinstance(poss[k][coords[0][1]], list) and (k, coords[0][1]) not in coords:
                                if n in poss[k][coords[0][1]]:
                                    poss[k][coords[0][1]].remove(n)


def boxInterplay(poss):
    for i in range(3):
        for j in range(3):
            for n in range(1, 10):
                rows = list()
                cols = list()

                for x in range(3 * i, 3 * i + 3):
                    for y in range(3 * j, 3 * j + 3):
                        if isinstance(poss[x][y], list):
                            if n in poss[x][y]:
                                if x not in rows:
                                    rows.append(x)
                                if y not in cols:
                                    cols.append(y)

                if len(rows) == 2:
                    for k in range(3):
                        kRows = list()
                        if k != j:
                            for x in range(3 * i, 3 * i + 3):
                                for y in range(3 * k, 3 * k + 3):
                                    if isinstance(poss[x][y], list):
                                        if n in poss[x][y]:
                                            if x not in kRows:
                                                kRows.append(x)

                            if len(kRows) == 2:
                                amount = 0
                                for r in rows:
                                    if r in kRows:
                                        amount += 1

                                if amount == 2:
                                    aCol = [0, 1, 2]
                                    aCol.remove(j)
                                    aCol.remove(k)

                                    for r in rows:
                                        for x in range(3):
                                            if isinstance(poss[r][3 * aCol[0] + x], list):
                                                if n in poss[r][3 * aCol[0] + x]:
                                                    poss[r][3 * aCol[0] + x].remove(n)
                if len(cols) == 2:
                    for k in range(3):
                        kCols = list()
                        if k != i:
                            for x in range(3 * k, 3 * k + 3):
                                for y in range(3 * j, 3 * j + 3):
                                    if isinstance(poss[x][y], list):
                                        if n in poss[x][y]:
                                            if y not in kCols:
                                                kCols.append(y)
                            if len(kCols) == 2:
                                amount = 0
                                for c in cols:
                                    if c in kCols:
                                        amount += 1

                                if amount == 2:
                                    aRow = [0, 1, 2]
                                    aRow.remove(i)
                                    aRow.remove(k)

                                    for c in cols:
                                        for x in range(3):
                                            if isinstance(poss[3 * aRow[0] + x][c], list):
                                                if n in poss[3 * aRow[0] + x][c]:
                                                    poss[3 * aRow[0] + x][c].remove(n)


def indexRefine(poss, ind):
    for i in ind:
        for k in range(9):
            if isinstance(poss[i[0]][k], list):
                if poss[i[0]][i[1]] in poss[i[0]][k]:
                    poss[i[0]][k].remove(poss[i[0]][i[1]])
        for k in range(9):
            if isinstance(poss[k][i[1]], list):
                if poss[i[0]][i[1]] in poss[k][i[1]]:
                    poss[k][i[1]].remove(poss[i[0]][i[1]])
        for k in range(i[0] - i[0] % 3, i[0] - i[0] % 3 + 3):
            for l in range(i[1] - i[1] % 3, i[1] - i[1] % 3 + 3):
                if isinstance(poss[k][l], list):
                    if poss[i[0]][i[1]] in poss[k][l]:
                        poss[k][l].remove(poss[i[0]][i[1]])


def valueSetter(poss, used=None):
    if used is None:
        used = list()
    squareAndEle = list()
    oldV = 0

    for i in range(9):
        for j in range(9):
            if isinstance(poss[i][j], list):
                for k in range(len(poss[i][j])):
                    if [i, j, k] not in used:
                        curOption = poss[i][j][k]
                        v = 0
                        for m in range(9):
                            if isinstance(poss[i][m], list):
                                if curOption in poss[i][m]:
                                    v = v + 1 / (len(poss[i][m]) - 1)
                            if m != i and isinstance(poss[m][j], list):
                                if curOption in poss[m][j]:
                                    v = v + 1 / (len(poss[m][j]) - 1)
                        for m in range(3 * (i // 3), 3 * (i // 3) + 3):
                            for n in range(3 * (j // 3), 3 * (j // 3) + 3):
                                if m != i and n != j and isinstance(poss[m][n], list):
                                    if curOption in poss[m][n]:
                                        v = v + 1 / (len(poss[m][n]) - 1)
                        if v > oldV:
                            oldV = v
                            squareAndEle = [i, j, k]
    print(oldV)
    return squareAndEle


def isSolved(poss):
    sm = 0
    for i in poss:
        for j in i:
            if isinstance(j, list):
                return False
    for i in range(9):
        for j in range(9):
            if isinstance(poss[i][j], int):
                sm = sm + poss[i][j]
    if sm != 9 * 45:
        return False
    return True


def isSolvable(poss):
    for i in poss:
        for j in i:
            if isinstance(j, list):
                if len(j) == 0:
                    return False

    for i in range(9):
        colCheck = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        rowCheck = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for j in range(9):
            if isinstance(poss[i][j], int) and poss[i][j] in rowCheck:
                rowCheck.remove(poss[i][j])
            else:
                return False
            if isinstance(poss[j][i], int) and poss[j][i] in colCheck:
                colCheck.remove(poss[j][i])
            else:
                return False

    for i in range(3):
        for j in range(3):
            check = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for k in range(3 * i, 3 * i + 3):
                for l in range(3 * j, 3 * j + 3):
                    if isinstance(poss[k][l], int) and poss[k][l] in check:
                        check.remove(poss[k][l])
                    else:
                        return False
    return True


def takeAGuess(poss, l):
    l += 1
    c = copy.deepcopy(poss)
    used = list()

    while not isSolved(c):
        c = copy.deepcopy(poss)
        guess = valueSetter(c, used)
        c[guess[0]][guess[1]] = c[guess[0]][guess[1]][guess[2]]
        index = [(guess[0], guess[1])]
        while len(index) > 0:
            indexRefine(c, index)
            refinePossible(c)
            checkSubSquares(c)
            inferredLines(c)
            index = findSingles(c)

        if isSolvable(c):
            print('One level deeper!')
            takeAGuess(c, l)
            print('One level up!')
        elif l != 1:
            break
        used.append(guess)
    if isSolved(c):
        for i in range(9):
            for j in range(9):
                poss[i][j] = c[i][j]


txt = "020000801000006000470900200005040030700610000010008004000500003002000000060100007"

s = createSquare(txt)
for q in s:
    print(q)
p = initPossible(s)

refinePossible(p)
checkSubSquares(p)
inferredLines(p)
# boxInterplay(p)

ind = findSingles(p)
m = 0

while len(ind) > 0:
    indexRefine(p, ind)
    refinePossible(p)
    checkSubSquares(p)
    inferredLines(p)
    # boxInterplay(p)
    ind = findSingles(p)
    m += 1
    print(m)

takeAGuess(p, 0)

for q in p:
    print(q)
print("\n")

newSeed = createSeed(p)
newSquare = createSquare(newSeed)

for q in newSquare:
    print(q)
print(newSeed)
