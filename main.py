from Classes.Window import Window
from Classes.Game import Game
from Classes.SetInterval import SetInterval

global game
global fen

iteration = 0


def playCallBack():
    game.play()
    fen.buildGame()
    if game.isOver():
        fen.endGame(True)
    if game.defeat(game.moves_history):
        fen.endGame(False)


def playRolloutCallBack():
    game.playRollout(5)
    fen.buildGame()
    if game.isOver():
        fen.endGame(True)
    if game.defeat(game.moves_history):
        fen.endGame(False)


interval = SetInterval(playCallBack, 0.1)

game = Game()
fen = Window(interval, game.game)
fen.buildGame()
fen.window.mainloop()
