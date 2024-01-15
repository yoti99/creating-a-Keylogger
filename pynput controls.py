from pynput.mouse import Controller
from pynput.keyboard import Controller

def mouseController():
    mouse = Controller()
    mouse.position = (1000,1000)

#mouseController()

def keyboardController():
    keyboard = Controller()
    keyboard.type("As we said new day, new things to be done!!!!")

keyboardController()

