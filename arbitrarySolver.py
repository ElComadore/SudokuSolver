import copy
from numpy import sqrt


def createSquare(numEle, string):
    """
    Creates the square we are going to be working with from the seed provided
    :param numEle: size of n
    :param string: the seed for the puzzle
    :return: the puzzle
    """
    if len(string) != numEle * numEle:  # Sanity check
        print(len(seed))
        print('You fucked it!')
        exit(-1)

    square = [[0 for x in range(numEle)] for y in range(numEle)]

    for i in range(numEle):
        for j in range(numEle):
            if string[j + numEle * i] != 0:
                square[i][j] = string[j + numEle * i]  # Populate the matrix with seeded values
    return square


def createSeed(square):
    """
    Gives the seed to a given matrix
    :param square: the current puzzle
    :return: the seed of the puzzle
    """
    string = ""
    for i in square:
        for j in i:
            if isinstance(j, list):
                string = string + "0"  # Note that 0 is used as an empty square, which is really dumb!
            else:
                string = string + str(j)
    return string


def initPossible(elements, square):
    """
    Replace all the zeros with a list of the possible elements
    :param elements: which elements we are using
    :param square: the current puzzle
    :return: -
    """
    for i in range(len(elements)):
        for j in range(len(elements)):
            if square[i][j] == '0':
                square[i][j] = copy.deepcopy(elements)


def refinePossible(numEle, poss):
    """
    The basic horizontal/vertical checks and the sub-square checks
    :param numEle: size of n
    :param poss: the current state of the puzzle
    :return: -
    """
    s = int(sqrt(numEle))

    for i in range(numEle):
        for j in range(numEle):
            if not isinstance(poss[i][j], list):
                for k in range(numEle):
                    if isinstance(poss[i][k], list):  # Horizontal line checks
                        if poss[i][j] in poss[i][k]:
                            poss[i][k].remove(poss[i][j])

                    if isinstance(poss[k][j], list):  # Vertical line checks
                        if poss[i][j] in poss[k][j]:
                            poss[k][j].remove(poss[i][j])

                for k in range(i - i % s, i - i % s + s):  # Checks sub-squares
                    for l in range(j - j % s, j - j % s + s):
                        if isinstance(poss[k][l], list):
                            if poss[i][j] in poss[k][l]:
                                poss[k][l].remove(poss[i][j])


def findSingles(numEle, poss):
    """
    There are hot singles in your area! At least hopefully anyway._. Index all the len = 1 lists
    :param numEle: sie of n
    :param poss: the current state of the puzzle
    :return: the indices of the naked singles
    """
    index = list()
    for i in range(numEle):
        for j in range(numEle):
            if isinstance(poss[i][j], list):
                if len(poss[i][j]) == 1:
                    poss[i][j] = poss[i][j][0]      # Replaces list with the value as len = 1
                    index.append((i, j))
    return index


def checkSubSquares(elements, poss):
    """
    Checks to see if a number only has 1 valid place in a sub-square
    :param elements: which elements we are using
    :param poss: the current state of the puzzle
    :return: -
    """
    s = int(sqrt(len(elements)))
    for i in range(s):
        for j in range(s):
            for n in elements:  # Cycling through valid elements
                coords = list()
                amount = 0
                for k in range(s * i, s * i + s):  # Cycling through squares in sub-square
                    for l in range(s * j, s * j + s):
                        if isinstance(poss[k][l], list):
                            if n in poss[k][l]:
                                coords = [k, l]
                                amount += 1  # Counting number of valid places
                if amount == 1:
                    poss[coords[0]][coords[1]] = [n]  # If only 1 valid place, replace that list with a len = 1 list


# From here on out the methods get a bit wackier!

def inferredLines(elements, poss):
    """
    Looks at two sub-squares and checks if some lines are unavailable due to their interplay
    :param elements: the elements we are using
    :param poss: the current state of the puzzle
    :return: -
    """
    s = int(sqrt(len(elements)))
    for i in range(s):
        for j in range(s):
            for n in elements:
                coords = list()
                amount = 0
                for k in range(s * i, s * i + s):
                    for l in range(s * j, s * j + s):
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
                        for k in range(len(elements)):
                            if isinstance(poss[coords[0][0]][k], list) and (coords[0][0], k) not in coords:
                                if n in poss[coords[0][0]][k]:
                                    poss[coords[0][0]][k].remove(n)
                    if numCol == amount:
                        for k in range(len(elements)):
                            if isinstance(poss[k][coords[0][1]], list) and (k, coords[0][1]) not in coords:
                                if n in poss[k][coords[0][1]]:
                                    poss[k][coords[0][1]].remove(n)


def indexRefine(numEle, poss, index):
    """
    Uses the aforementioned findSingles method's return to then reduce possibilities of affected squares
    :param numEle: size of n
    :param poss: the current state of the puzzle
    :param index: the positions of the singles
    :return: -
    """
    s = int(sqrt(numEle))
    for i in index:
        for k in range(numEle):
            if isinstance(poss[i[0]][k], list):                     # Refine horizontally
                if poss[i[0]][i[1]] in poss[i[0]][k]:
                    poss[i[0]][k].remove(poss[i[0]][i[1]])
            if isinstance(poss[k][i[1]], list):                     # Refine vertically
                if poss[i[0]][i[1]] in poss[k][i[1]]:
                    poss[k][i[1]].remove(poss[i[0]][i[1]])
        for k in range(i[0] - i[0] % s, i[0] - i[0] % s + s):       # Refine sub-square wise
            for l in range(i[1] - i[1] % s, i[1] - i[1] % s + s):
                if isinstance(poss[k][l], list):
                    if poss[i[0]][i[1]] in poss[k][l]:
                        poss[k][l].remove(poss[i[0]][i[1]])


def valueSetter(numEle, poss, used=None):
    """
    Sets values for each of the possibilities in each unknown square
    :param numEle: how big is n?
    :param poss: the current state of the puzzle
    :param used: which positions we have looked at before
    :return: the highest value element in the puzzle
    """
    if used is None:
        used = list()

    s = int(sqrt(numEle))
    squareAndEle = list()
    oldV = 0

    for i in range(numEle):
        for j in range(numEle):
            if isinstance(poss[i][j], list):                        # Check each square
                for k in range(len(poss[i][j])):
                    if [i, j, k] not in used:                       # Check if we have guessed this possibility before
                        curOption = poss[i][j][k]
                        v = 0                                       # Initial value
                        for m in range(numEle):
                            if isinstance(poss[i][m], list):
                                if curOption in poss[i][m]:             # Summing along horizontal
                                    v = v + 1 / (len(poss[i][m]) - 1)
                            if m != i and isinstance(poss[m][j], list):
                                if curOption in poss[m][j]:             # Summing along vertical
                                    v = v + 1 / (len(poss[m][j]) - 1)
                        for m in range(i - i % s, i - i % s + s):       # Summing over sub-squares
                            for n in range(j - j % s, j - j % s + s):
                                if m != i and n != j and isinstance(poss[m][n], list):
                                    if curOption in poss[m][n]:
                                        v = v + 1 / (len(poss[m][n]) - 1)
                        if v > oldV:            # Setting new highest value
                            oldV = v
                            squareAndEle = [i, j, k]
    print(oldV)
    return squareAndEle


def isSolved(poss):
    """
    Checking if matrix is finished
    :param poss: the current state of the puzzle
    :return: True for solved, False for not solved
    """
    for i in poss:
        for j in i:
            if isinstance(j, list):
                return False
    return True


def isSolvable(elements, poss):
    """
    Checking if we are actually in a solvable position
    :param elements: elements we are using
    :param poss: the current state of the puzzle
    :return: True if puzzle is 'solvable', False otherwise
    """
    s = int(sqrt(len(elements)))
    for i in poss:
        for j in i:
            if isinstance(j, list):
                if len(j) == 0:         # Checking if we have any squares with no possibilities
                    return False

    for i in range(len(elements)):
        colCheck = copy.deepcopy(elements)
        rowCheck = copy.deepcopy(elements)
        for j in range(len(elements)):
            if not isinstance(poss[i][j], list) and poss[i][j] in rowCheck:     # Make sure rows are sane
                rowCheck.remove(poss[i][j])
            else:
                return False
            if not isinstance(poss[i][j], list) and poss[i][j] in colCheck:     # Make sure columns are sane
                colCheck.remove(poss[i][j])
            else:
                return False
    for i in range(s):
        for j in range(s):
            check = copy.deepcopy(elements)
            for k in range(s * i, s * i + s):
                for l in range(s * j, s * j + s):
                    if not isinstance(poss[k][l], list) and poss[k][l] in check:    # Make sure sub-squares are sane
                        check.remove(poss[k][l])
                    else:
                        return False
    return True


def takeAGuess(elements, poss, l):
    """
    Guesses a value based on which has the highest value
    :param elements: elements we are using
    :param poss: the current state of the puzzle
    :param l: the current layer
    :return: -
    """
    l += 1
    c = copy.deepcopy(poss)     # Make sure we have a copy of the step before
    used = list()

    while not isSolved(c):
        c = copy.deepcopy(poss)
        guess = valueSetter(len(elements), c, used)                 # Set the values and get the guess
        c[guess[0]][guess[1]] = c[guess[0]][guess[1]][guess[2]]     # Set the guess
        index = [(guess[0], guess[1])]                              # Get index for refinement

        while len(index) > 0:                                       # Standard reduction block
            indexRefine(len(elements), c, index)
            refinePossible(len(elements), c)
            checkSubSquares(elements, c)
            inferredLines(elements, c)
            index = findSingles(len(elements), c)

        if isSolvable(elements, c):             # Check if we can make another guess
            print('One level deeper!')
            takeAGuess(elements, c, l)          # Do it again!
            print('One level up!')
        elif l != 1:                            # If we can't, go one step back up
            break
        used.append(guess)

    if isSolved(c):                             # Checks if solved and applies the changes to the original matrix
        for i in range(len(elements)):
            for j in range(len(elements)):
                poss[i][j] = c[i][j]


def solveMe(elements, seed):
    """
    The standard code which attempts to solve a matrix without guesses
    :param elements: the elements we are using
    :param seed: the seed of the puzzle
    :return: the 'seed' of the completed square
    """
    p = createSquare(len(elements), seed)       # Initialise the square
    for q in p:
        print(q)

    initPossible(elements, p)                   # All initial possibilities

    refinePossible(len(elements), p)            # Initial refinement
    checkSubSquares(elements, p)
    inferredLines(elements, p)

    ind = findSingles(len(elements), p)         # Find our first singles
    m = 0

    while len(ind) > 0:                         # Repeat the above until we have no more singles
        indexRefine(len(elements), p, ind)
        refinePossible(len(elements), p)
        checkSubSquares(elements, p)
        ind = findSingles(len(elements), p)
        m += 1
        print(m)

    takeAGuess(elements, p, 0)              # Start taking guesses

    for q in p:
        print(q)
    print("\n")

    newSeed = createSeed(p)                             # Create a solved seed
    newSquare = createSquare(len(elements), newSeed)    # View the complete square

    for q in newSquare:
        print(q)
    print(newSeed)

    return newSeed


elements = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G']     # Change these
seed = "00AB000064030FC90040000000000000E10906000AD20800DC20G150BE00003A0DFE6A2050840001020000100060CEA0009C000E002B05843A50900B10E002F008600B09200503GC2EC057004000AD000BD10400090080509000EC0D08B621408F0000B602CG0A1300B0C3800050F0DG0000000000000B00G310D07F00009C60"

s = solveMe(elements, seed)
