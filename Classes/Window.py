from tkinter import *


class Window:

    imgList = []
    symbDic = {"S": "\u2660", "H": "\u2665", "D": "\u2666", "C": "\u2663"}
    __characters = {1: "A", 11: "J", 12: "Q", 13: "K"}
    game = []

    def __init__(self, callBackButton, game=None):
        self.window = Tk()
        self.window.geometry("1000x700")
        self.window.resizable(width=False, height=False)
        self.B = Button(self.window, text="Зробити крок", command=callBackButton)
        self.B.pack()
        self.createGame()
        if game == None:
            self.game.append(
                [
                    (3, "D", 0),
                    (5, "H", 0),
                    (5, "H", 0),
                    (2, "S", 0),
                    (3, "D", 0),
                    (5, "H", 0),
                    (2, "S", 0),
                    (3, "D", 0),
                    (5, "H", 0),
                    (5, "H", 0),
                    (2, "S", 0),
                    (3, "D", 0),
                    (5, "H", 0),
                    (2, "S", 0),
                    (3, "D", 0),
                    (5, "H", 0),
                    (2, "S", 0),
                    (3, "D", 0),
                    (5, "H", 0),
                    (5, "H", 0),
                    (2, "S", 0),
                    (3, "D", 0),
                    (5, "H", 0),
                    (2, "S", 0),
                ]
            )  # 24
            self.game.append([(3, "D", 1), (3, "D", 1), (3, "D", 1)])
            self.game.append([(3, "D", 1)])
            self.game.append([(3, "D", 1)])
            self.game.append([(3, "D", 1)])
            self.game.append([(3, "D", 1)])
            self.game.append([(2, "S", 1)])
            self.game.append([(3, "D", 0), (5, "H", 1)])
            self.game.append([(3, "D", 0), (5, "H", 0), (5, "H", 1)])
            self.game.append([(3, "D", 0), (5, "H", 0), (2, "S", 0), (3, "D", 1)])
            self.game.append(
                [
                    (3, "D", 0),
                    (5, "H", 0),
                    (5, "H", 0),
                    (2, "S", 0),
                    (3, "D", 1),
                ]
            )
            self.game.append(
                [
                    (3, "D", 0),
                    (5, "H", 0),
                    (3, "D", 0),
                    (5, "H", 0),
                    (2, "S", 0),
                    (2, "S", 1),
                ]
            )
            self.game.append(
                [
                    (3, "D", 0),
                    (5, "H", 0),
                    (5, "H", 0),
                    (2, "S", 0),
                    (3, "D", 0),
                    (5, "H", 0),
                    (2, "S", 1),
                ]
            )  # 28
        else:
            self.game = game
        self.buildGame()

    def createGame(self):
        self.canvas = Canvas(self.window, bg="black", borderwidth=5)
        self.canvas.pack(fill="both", expand="yes")

    def drawCard(self, pos, card):
        assert (
            type(card) == type((1, "a", 1))
            and type(pos) == type((1, 1))
            and len(card) == 3
            and len(pos) == 2
        )
        fill = "white"
        outline = "black"
        if card[2] == 0:
            fill = "blue"
            outline = "white"

        self.canvas.create_rectangle(
            pos[0], pos[1], pos[0] + 100, pos[1] + 140, fill=fill, outline=outline
        )
        if card[2] == 0:
            return
        if card[1] == "D" or card[1] == "H":
            color = "Red"
        else:
            color = "Black"
        nbr = ""
        if card[0] == 1 or card[0] > 10:
            nbr = self.__characters[card[0]]
        else:
            nbr = card[0]

        self.canvas.create_text(
            pos[0] + 15, pos[1] + 15, fill=color, font="Arial 12 bold", text=nbr
        )
        self.canvas.create_text(
            pos[0] + 80,
            pos[1] + 15,
            fill=color,
            font="Arial 14 bold",
            text=self.symbDic[card[1]],
        )
        self.canvas.create_text(
            pos[0] + 15,
            pos[1] + 30,
            fill=color,
            font="Arial 14 bold",
            text=self.symbDic[card[1]],
        )
        self.window.update()

    def buildGame(self):
        self.canvas.delete("all")
        color = "blue"
        if not self.game[0]:
            color = "black"

        if len(self.game[0]) >= 1:
            self.canvas.create_rectangle(10, 10, 110, 150, fill=color, outline="white")
        else:
            self.canvas.create_rectangle(10, 10, 110, 20, fill="green", outline="white")
            self.canvas.create_oval(
                35, 45, 85, 95, fill="green", outline="forestgreen", width=4
            )
        if len(self.game[1]) == 0:
            self.canvas.create_rectangle(
                130, 10, 230, 150, fill="green", outline="white"
            )
        else:
            i = 1
            for each in self.game[1]:
                self.drawCard((130 + i * 25, 10), each)
                i += 1

        for i in range(2, 6):
            if len(self.game[i]) == 0:
                self.canvas.create_rectangle(
                    i * 120 + 130, 10, i * 120 + 230, 150, fill="green", outline="white"
                )
            else:
                self.drawCard((120 * i + 120, 10), self.game[i][-1])

        for i in range(6, len(self.game)):
            if len(self.game[i]) > 0:
                for j in range(0, len(self.game[i])):
                    self.drawCard((10 + 120 * (i - 6), 200 + j * 25), self.game[i][j])
            else:
                self.canvas.create_rectangle(
                    10 + 120 * (i - 6),
                    200,
                    110 + 120 * (i - 6),
                    340,
                    fill="green",
                    outline="white",
                )

    def endGame(self, isVictory):
        if isVictory:
            color = "green3"
            text = "VICTORY"
        else:
            color = "orange"
            text = "DEFEAT"
        self.B.pack_forget()
        self.canvas.create_text(500, 600, fill=color, font="Arial 30 bold", text=text)
