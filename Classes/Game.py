from random import randint

EMPTY_MOVE = (0, 0, 0, 0, 0)


def heuristic(move):
    if 2 <= move[2] <= 5 and (6 <= move[0] <= 13 or move[0] == 1):
        return 5
    if move[0] == 1 and 6 <= move[2] <= 13:
        return 5
    return -10 if 2 <= move[0] <= 5 and 6 <= move[2] <= 13 else 0


def evaluateGame(moves_list):
    return sum(moves_list[i][0] for i in range(len(moves_list)))


def cardIsRed(card):
    return card in ["D", "H"]


class Game:
    game = [[] for i in range(13)]
    game_history = []
    moves_history = []
    newCard_history = []
    rollout_moves_lists = []
    rolloutCounter = 0
    __color = ["S", "H", "C", "D"]
    available_moves = []

    def __init__(self):
        self.generateStart()
        self.game_history.append(self.game)

    def generateStart(self):
        nbrCard = 0
        for index, i in enumerate(range(6, len(self.game)), start=1):
            for j in range(index):
                (nbr, color) = self.randomCard()
                faceup = 0
                if j == index - 1:
                    faceup = 1
                self.game[i].append((nbr, color, faceup))
                nbrCard += 1
        for _ in range(nbrCard, 52):
            (nbr, color) = self.randomCard()
            self.game[0].append((nbr, color, 1))

    def randomCard(self):
        exists1 = True
        exists2 = True
        color = 0
        nbr = 0
        while exists1 or exists2:
            color = self.__color[randint(0, 3)]
            nbr = randint(1, 13)
            exists1 = any((nbr, color, 0) in x for x in self.game)
            exists2 = any((nbr, color, 1) in x for x in self.game)
        return nbr, color

    def isOver(self):
        for i in range(2, 6):
            l = len(self.game[i])
            if l != 13:
                return False
            for j in range(l):
                if j + 1 != self.game[i][j][0]:
                    return False
        return True

    def differentiateHeuristic(self, move):
        if 6 <= move[0] <= 13 and 6 <= move[2] <= 13:
            if len(self.game[move[0]][:-1]):
                return 1
            if self.game[move[0]][move[1] - 1][2] == 0:
                return len(self.game[move[0]][:-1]) + 1
        if move[0] == 1 and 6 <= move[2] <= 13:
            if self.game[move[0]][move[1]][0] != 13:
                return 1
            if self.game[move[0]][move[1]][0] == 13 and self.cardFacedUp(
                (12, self.game[move[0]][move[1]][1])
            ):
                return 1
            if self.game[move[0]][move[1]][0] == 13:
                return -1
        return 0

    def availableMoves(self):
        for i in range(6, len(self.game)):
            for j in range(len(self.game[i])):
                if self.game[i][j][2]:
                    for k in range(2, len(self.game)):
                        if k != i:
                            mv = [0, i, j, k, len(self.game[k]) - 1]
                            if self.moveIsLegal(mv):
                                self.available_moves.append(mv)

        if len(self.game[1]) > 0:
            for k in range(2, len(self.game)):
                mv = [0, 1, len(self.game[1]) - 1, k, len(self.game[k]) - 1]
                if self.moveIsLegal(mv):
                    self.available_moves.append(mv)

        return len(self.available_moves) != 0

    def evaluateMoves(self, moves_list):
        for move in moves_list:
            priority = heuristic([move[1], move[2], move[3], move[4]])
            move[0] = priority

        maxPriority = -1000
        for each in moves_list:
            if each[0] > maxPriority:
                maxPriority = each[0]

        tmp = [each for each in moves_list if each[0] == maxPriority]
        if len(tmp) <= 1:
            return tmp.copy()
        for move in tmp:
            priority = (
                move[0]
                + self.differentiateHeuristic([move[1], move[2], move[3], move[4]])
                + move[0]
            )
            move[0] = priority
        maxPriority = -1000
        for each in tmp:
            if each[0] > maxPriority:
                maxPriority = each[0]

        tmp2 = [each for each in tmp if each[0] == maxPriority]
        return tmp2.copy()

    def play(self):
        if self.availableMoves():
            self.makeRandomMove()
        else:
            self.dealPile()
            self.moves_history.append([0, 0, 0, 0, 0])
        self.game_history.append(self.saveGame())

        print("Moves in game_history: ", end="")
        print(len(self.game_history))
        print()

    def makeRandomMove(self):
        self.available_moves = self.evaluateMoves(self.available_moves)
        tmp = []
        for i in range(len(self.available_moves)):
            isRepetitive = self.repetitiveMove(self.available_moves[i])
            if not isRepetitive:
                tmp.append(self.available_moves[i])
        self.available_moves = tmp.copy()
        if self.available_moves:
            if len(self.available_moves) > 1:
                rdmNbr = randint(0, len(self.available_moves) - 1)
                maxMove = rdmNbr
            else:
                maxMove = 0
            self.makeMove(self.available_moves[maxMove])
            self.moves_history.append(self.available_moves[maxMove])
        else:
            self.dealPile()
            self.moves_history.append([0, 0, 0, 0, 0])
        self.available_moves.clear()

    def playRollout(self, depth):
        moves = []
        if self.availableMoves():
            moves = self.getNotRepetitiveMoves()
        else:
            moves.append([0, 0, 0, 0, 0])

        for move in moves:
            self.makeRolloutMove(move, depth, depth)
        maxI = -1
        maxV = -5000
        for i in range(len(self.rollout_moves_lists)):
            if self.rollout_moves_lists[i][-1] > maxV:
                maxI = i
                maxV = self.rollout_moves_lists[i][-1]

        for i in range(len(self.rollout_moves_lists[maxI]) - 1):
            if self.rollout_moves_lists[maxI][i] == [0, 0, 0, 0, 0]:
                self.dealPile()
            else:
                self.makeMove(self.rollout_moves_lists[maxI][i])
            self.moves_history.append(self.rollout_moves_lists[maxI][i].copy())
            self.game_history.append(self.saveGame())

        self.rollout_moves_lists.clear()

    def getNotRepetitiveMoves(self):
        result = self.evaluateMoves(self.available_moves)
        self.available_moves.clear()
        tmp = []
        for i in range(len(result)):
            isRepetitive = self.repetitiveMove(result[i])
            if not isRepetitive:
                tmp.append(result[i])
        result = tmp.copy()
        if len(result) <= 0:
            result.append([0, 0, 0, 0, 0])
        return result

    def iterationRollout(self, depth, maxDepth):
        if self.isOver():
            self.addRolloutMove(maxDepth)
            self.rollout_moves_lists[-1].append(1000)
            return

        if self.defeat(self.moves_history):
            self.addRolloutMove(maxDepth)
            self.rollout_moves_lists[-1].append(-1000)
            return

        if depth <= 0:
            self.addRolloutMove(maxDepth)
            self.rollout_moves_lists[-1].append(
                evaluateGame(self.rollout_moves_lists[-1])
            )  # we append the value of the moves_list
            return

        moves = []
        if self.availableMoves():
            moves = self.getNotRepetitiveMoves()
        else:
            moves.append([0, 0, 0, 0, 0])

        for move in moves:
            self.makeRolloutMove(move, depth, maxDepth)
        return

    def makeRolloutMove(self, move, depth, maxDepth):
        if move == [0, 0, 0, 0, 0]:
            self.dealPile()
        else:
            self.makeMove(move)
        self.moves_history.append(move)
        self.game_history.append(self.saveGame())
        self.rolloutCounter += 1
        self.iterationRollout(depth - 1, maxDepth)
        self.resetPrevMove()

    def addRolloutMove(self, depth):
        self.rollout_moves_lists.append(self.moves_history[-depth:].copy())

    def resetPrevMove(self):
        for i in range(len(self.game_history[-2])):
            self.game[i] = self.game_history[-2][i].copy()
        del self.game_history[-1]
        del self.moves_history[-1]
        if len(self.newCard_history) > 0:
            del self.newCard_history[-1]

    def cardFacedUp(self, card):
        return any((card[0], card[1], 1) in self.game[i] for i in range(len(self.game)))

    def moveIsLegal(self, move):
        if 6 <= move[1] <= 12 and (
            self.game[move[1]][move[2]][0] == 13 and move[2] == 0 and 6 <= move[3] <= 13
        ):
            return False
        if 6 <= move[3] <= 12:
            if len(self.game[move[3]]) == 0:
                return self.game[move[1]][move[2]][0] == 13
            else:
                return self.game[move[1]][move[2]][0] == self.game[move[3]][move[4]][
                    0
                ] - 1 and cardIsRed(self.game[move[1]][move[2]][1]) != cardIsRed(
                    self.game[move[3]][move[4]][1]
                )
        if 2 <= move[3] <= 5:
            if move[2] != len(self.game[move[1]]) - 1:
                return False
            if len(self.game[move[3]]) == 0:
                return self.game[move[1]][move[2]][0] == 1
            else:
                return (
                    self.game[move[1]][move[2]][0] == self.game[move[3]][move[4]][0] + 1
                    and self.game[move[1]][move[2]][1] == self.game[move[3]][move[4]][1]
                )

    def makeMove(self, move):
        self.game[move[3]].extend(self.game[move[1]][move[2] :])
        del self.game[move[1]][move[2] :]
        if 6 <= move[1] <= 12:
            if len(self.game[move[1]]) > 0:
                tmp = self.game[move[1]][move[2] - 1]
                del self.game[move[1]][move[2] - 1]
                self.game[move[1]].append((tmp[0], tmp[1], 1))
                if tmp[2] == 0:
                    self.newCard_history.append(1)
                else:
                    self.newCard_history.append(0)
        elif move[1] == 1:
            self.newCard_history.append(1)
        else:
            self.newCard_history.append(0)

    def dealPile(self):
        if len(self.game[1]) > 0:
            self.game[0] = self.game[1][::-1] + self.game[0]
            self.game[1].clear()
        self.game[1].extend(self.game[0][::-1][:3])
        del self.game[0][-3:]
        self.newCard_history.append(0)

    def defeat(self, moves_list):
        if len(self.moves_history) > 11:
            t = moves_list[-1]
            if t == EMPTY_MOVE:
                for i in range(1, 11):
                    if self.game_history[-i] != t:
                        return True
            if 6 <= t[1] <= 13 and 6 <= t[3] <= 13:
                count = 0
                for i in range(1, len(self.moves_history) + 1):
                    prev = self.moves_history[-i]
                    if prev == EMPTY_MOVE:
                        count += 1
                    elif count >= 5 and (
                        (t[1] == prev[1] and t[3] == prev[3])
                        or (t[1] == prev[3] and t[3] == prev[1])
                    ):
                        return True
        count = 0
        anyFaceDown = False
        for i in range(6, len(self.game)):
            for j in range(len(self.game[i])):
                if self.game[i][j][-1] == 0:
                    anyFaceDown = True

        if anyFaceDown == True and len(self.game[0]) >= 0:
            for i in range(1, len(self.newCard_history) + 1):
                if self.newCard_history[-i] == 1:
                    return False
                else:
                    count += 1

                if count >= 20:
                    return True

        return False

    def repetitiveMove(self, move):
        if 2 <= move[1] <= 13 and 2 <= move[3] <= 13 and len(self.moves_history) > 9:
            for i in range(1, 8):
                prevMove = self.moves_history[-i]
                if (
                    move[1] == prevMove[3]
                    and move[2] == prevMove[4] + 1
                    and move[3] == prevMove[1]
                    and move[4] == prevMove[2] - 1
                ):
                    prevGame = self.game_history[-i - 1]
                    if (
                        prevGame[prevMove[1]][prevMove[2]]
                        == self.game[move[1]][move[2]]
                    ):
                        return True
        return False

    def saveGame(self):
        return [each.copy() for each in self.game]
