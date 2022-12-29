from random import randint


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
        index = 0
        nbrCard = 0
        for i in range(6, len(self.game)):
            index += 1
            for j in range(0, index):
                (nbr, color) = self.randomCard()
                faceup = 0
                if j == index - 1:
                    faceup = 1
                self.game[i].append((nbr, color, faceup))
                nbrCard += 1
        for i in range(nbrCard, 52):
            (nbr, color) = self.randomCard()
            self.game[0].append((nbr, color, 1))

    def randomCard(self):
        exists1 = True
        exists2 = True
        color = 0
        nbr = 0
        while not (exists1 == False and exists2 == False):
            color = self.__color[randint(0, 3)]
            nbr = randint(1, 13)
            exists1 = any((nbr, color, 0) in x for x in self.game)
            exists2 = any((nbr, color, 1) in x for x in self.game)
        return (nbr, color)

    def isOver(self):
        for i in range(2, 6):
            l = len(self.game[i])
            if l != 13:
                return False
            for j in range(0, l):
                if j + 1 != self.game[i][j][0]:
                    return False
        return True

    def heuristic(self, move):
        if (
            2 <= move[2] <= 5
                and (6 <= move[0] <= 13 or move[0] == 1)
        ):
            return 5
        if move[0] == 1 and 6 <= move[2] <= 13:
            return 5
        if 2 <= move[0] <= 5 and 6 <= move[2] <= 13:
            return -10
        return 0

    def differentiateHeuristic(self, move):
        if 6 <= move[0] <= 13 and move[2] >= 6 and move[2] <= 13:
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
            for j in range(0, len(self.game[i])):
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

        if len(self.available_moves) == 0:
            return False
        else:
            return True

    def evaluateMoves(self, moves_list):
        for move in moves_list:
            priority = self.heuristic([move[1], move[2], move[3], move[4]])
            move[0] = priority

        maxPriority = -1000
        for each in moves_list:
            if each[0] > maxPriority:
                maxPriority = each[0]

        tmp = []
        for each in moves_list:
            if each[0] == maxPriority:
                tmp.append(each)

        if len(tmp) > 1:
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

            tmp2 = []
            for each in tmp:
                if each[0] == maxPriority:
                    tmp2.append(each)
            return tmp2.copy()
        else:
            return tmp.copy()

    def play(self):
        if self.availableMoves():
            self.available_moves = self.evaluateMoves(self.available_moves)
            tmp = []
            for i in range(0, len(self.available_moves)):
                isRepetitive = self.repetitiveMove(self.available_moves[i])
                if not isRepetitive:
                    tmp.append(self.available_moves[i])
            self.available_moves = tmp.copy()
            if len(self.available_moves) > 0:
                if len(self.available_moves) > 1:  # if there's several maximums
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
        else:
            self.dealPile()
            self.moves_history.append([0, 0, 0, 0, 0])
        self.game_history.append(self.saveGame())

    def playRollout(self, depth):
        moves = []
        if self.availableMoves():
            moves = self.evaluateMoves(self.available_moves)
            self.available_moves.clear()
            tmp = []
            for i in range(0, len(moves)):
                isRepetitive = self.repetitiveMove(moves[i])
                if not isRepetitive:
                    tmp.append(moves[i])
            moves = tmp.copy()
            if len(moves) <= 0:
                moves.append([0, 0, 0, 0, 0])
        else:
            moves.append([0, 0, 0, 0, 0])

        for i in range(0, len(moves)):
            if moves[i] == [0, 0, 0, 0, 0]:
                self.dealPile()
            else:
                self.makeMove(moves[i])
            self.moves_history.append(moves[i])
            self.game_history.append(self.saveGame())
            self.rolloutCounter += 1
            self.iterationRollout(depth - 1, depth)
            self.resetPrevMove()

        maxI = -1
        maxV = -5000
        for i in range(0, len(self.rollout_moves_lists)):
            if self.rollout_moves_lists[i][-1] > maxV:
                maxI = i
                maxV = self.rollout_moves_lists[i][-1]

        for i in range(0, len(self.rollout_moves_lists[maxI]) - 1):
            if self.rollout_moves_lists[maxI][i] == [0, 0, 0, 0, 0]:
                self.dealPile()
            else:
                self.makeMove(self.rollout_moves_lists[maxI][i])
            self.moves_history.append(self.rollout_moves_lists[maxI][i].copy())
            self.game_history.append(self.saveGame())

        self.rollout_moves_lists.clear()

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
                self.evaluateGame(self.rollout_moves_lists[-1])
            )  # we append the value of the moves_list
            return

        moves = []
        if self.availableMoves():
            moves = self.evaluateMoves(self.available_moves)
            self.available_moves.clear()
            tmp = []
            for i in range(0, len(moves)):
                isRepetitive = self.repetitiveMove(moves[i])
                if not isRepetitive:
                    tmp.append(moves[i])
            moves = tmp.copy()
            if len(moves) <= 0:
                moves.append([0, 0, 0, 0, 0])
        else:
            moves.append([0, 0, 0, 0, 0])

        for i in range(0, len(moves)):
            if moves[i] == [0, 0, 0, 0, 0]:
                self.dealPile()
            else:
                self.makeMove(moves[i])
            self.moves_history.append(moves[i])
            self.game_history.append(self.saveGame())
            self.rolloutCounter += 1
            self.iterationRollout(depth - 1, maxDepth)
            self.resetPrevMove()
        return

    def evaluateGame(self, moves_list):
        count = 0
        for i in range(0, len(moves_list)):
            count += moves_list[i][0]
        return count

    def addRolloutMove(self, depth):
        self.rollout_moves_lists.append(self.moves_history[-depth:].copy())

    def resetPrevMove(self):
        for i in range(0, len(self.game_history[-2])):
            self.game[i] = self.game_history[-2][i].copy()
        del self.game_history[-1]
        del self.moves_history[-1]
        if len(self.newCard_history) > 0:
            del self.newCard_history[-1]

    def cardFacedUp(self, card):
        for i in range(0, len(self.game)):
            if (card[0], card[1], 1) in self.game[i]:
                return True
        return False

    def moveIsLegal(self, move):
        if 6 <= move[1] <= 12:
            if (
                    self.game[move[1]][move[2]][0] == 13
                    and move[2] == 0
                    and 6 <= move[3] <= 13
            ):
                return False
        if 6 <= move[3] <= 12:
            if len(self.game[move[3]]) == 0:
                return self.game[move[1]][move[2]][0] == 13
            else:
                return self.game[move[1]][move[2]][0] == self.game[move[3]][move[4]][
                    0
                ] - 1 and self.cardIsRed(
                    self.game[move[1]][move[2]][1]
                ) != self.cardIsRed(
                    self.game[move[3]][move[4]][1]
                )
        if move[3] >= 2 and move[3] <= 5:
            if move[2] == len(self.game[move[1]]) - 1:
                if len(self.game[move[3]]) == 0:
                    return self.game[move[1]][move[2]][0] == 1
                else:
                    return (
                        self.game[move[1]][move[2]][0]
                        == self.game[move[3]][move[4]][0] + 1
                        and self.game[move[1]][move[2]][1]
                        == self.game[move[3]][move[4]][1]
                    )
            else:
                return False

    def cardIsRed(self, card):
        return card == "D" or card == "H"

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
        else:
            if move[1] == 1:
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
            if t == (0, 0, 0, 0, 0):
                for i in range(1, 11):
                    if self.game_history[-i] != t:
                        return True
            if 6 <= t[1] <= 13 and t[3] >= 6 and t[3] <= 13:
                count = 0
                for i in range(1, len(self.moves_history) + 1):
                    prev = self.moves_history[-i]
                    if prev == (0, 0, 0, 0, 0):
                        count += 1
                    else:
                        if count >= 5:
                            if (t[1] == prev[1] and t[3] == prev[3]) or (
                                t[1] == prev[3] and t[3] == prev[1]
                            ):
                                return True
        count = 0
        anyFaceDown = False
        for i in range(6, len(self.game)):
            for j in range(0, len(self.game[i])):
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
        if 2 <= move[1] <= 13 and 2 <= move[3] <= 13:
            if len(self.moves_history) > 9:
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
        ret = []
        for each in self.game:
            ret.append(each.copy())
        return ret
