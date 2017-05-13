global root, tiles, gamedata
import tkinter as tk
import random

root = tk.Tk()
root.title('Ballz')
root.config(bg='black')

class tile:
    def __init__(self, canvas, num, x, y):
        self.canvas = canvas
        self.num = num
        self.colour = 'green'
        self.x = x
        self.y = y
        self.obj = self.canvas.create_rectangle(x, y, x + self.width, y + self.height, fill=self.colour, outline=self.colour)
        self.text = self.canvas.create_text(x + (self.width / 2), y + (self.height / 2), text=str(self.num), fill='white', font=('', 12))
    def refresh(self):
        self.canvas.coords(self.obj, self.x, self.y, self.x + self.width, self.y + self.height)
        self.canvas.coords(self.text, self.x + (self.width / 2), self.y + (self.height / 2))
    height = 32
    width = height

def new_row():
    global gamedata
    gamedata.stage += 1
    for row in tiles:
        for t in row:
            t.y += 37
            t.refresh()
    tiles.insert(0, [])
    for i in range(5, 299, 37):
        if not random.randint(1, 9) in [1, 2]:
            if random.randint(1, 10) == 1:
                inc = 1
            else:
                inc = 0
            tiles[0].append(tile(canvas, gamedata.stage + inc, i, 5))

class gamedata:
    stage = 0

canvas = tk.Canvas(root, height=500, width=299, bg='black')

#####

tiles = []
for i in range(4):
    new_row()

#####

canvas.pack()

root.mainloop()
