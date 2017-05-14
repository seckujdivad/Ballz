global root, tiles, gamedata
import tkinter as tk
import random, threading

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

class ball:
    def __init__(self, canvas, x, y, dx, dy):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.obj = self.canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius, outline='white', fill='white')
    def refresh(self):
        self.canvas.coords(self.obj, self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius)
    radius = 8

def new_row():
    global gamedata
    gamedata.stage += 1
    for row in tiles:
        for t in row:
            t.y += 37
            t.refresh()
    tiles.insert(0, [])
    for i in range(5, gamedata.width, 37):
        if not random.randint(1, 9) in [1, 2]:
            if random.randint(1, 10) == 1:
                inc = 1
            else:
                inc = 0
            tiles[0].append(tile(canvas, gamedata.stage + inc, i, 5))

def ball_move(canvas, balls):
    import time
    while True:
        for b in balls:
            b.x += b.dx
            b.y += b.dy
            clipx = b.x + b.radius > gamedata.width or b.x - b.radius < 0
            clipy = b.y + b.radius > gamedata.height or b.y - b.radius < 0
            for row in tiles:
                for t in row:
                    cx = (b.x - b.radius < t.x + t.width and b.x + b.radius > t.x)
                    cy = (b.y - b.radius < t.y + t.height and b.y + b.radius > t.y)
                    if cx and cy:
                        centrex = t.x + (t.width / 2)
                        centrey = t.y + (t.height / 2)
                        dx = abs(b.x - centrex)
                        dy = abs(b.y - centrey)
                        if dx > dy:
                            clipx = True
                        elif dx < dy:
                            clipy = True
                        else:
                            clipx = True
                            clipy = True
            if clipx or clipy:
                b.x -= b.dx
                b.y -= b.dy
            if clipx:
                b.dx = 0 - b.dx
            if clipy:
                b.dy = 0 - b.dy
            b.refresh()
        time.sleep(0.015)

class gamedata:
    stage = 0
    height = 500
    width = 299

canvas = tk.Canvas(root, height=gamedata.height, width=gamedata.width, bg='black')

#####

tiles = []
for i in range(4):
    new_row()

balls = []
for i in range(1):
    balls.append(ball(canvas, 100, 300, -2, -4))

threading.Thread(target=ball_move, args=[canvas, balls], name='Ball movement').start()

#####

canvas.pack()

root.mainloop()
