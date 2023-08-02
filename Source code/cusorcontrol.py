from pynput.mouse import Button,Controller
mouse = Controller()
import pyautogui as pg

#take the position of the mouse
pos = mouse.position
x = int(input("Give the x coordinate of the mouse: "))
y = int(input("Give the y coordinate of the mouse: "))

##mouse.move(x,y)
#print(pos)

# click the mouse
time = 1         # time the button clicks
#mouse.click(Button.right, time)
#mouse.click(Button.left, time)

'''
# click nonstop
mouse.press(Button.right)
mouse.release(Button.right)
'''

#pg.scroll(0,-100)
#pg.scroll(-1000)

str