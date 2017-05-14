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
        self.refresh()
    def refresh(self):
        if self.num < 5:
            self.colour = '#c6a500' #yellow
        elif 5 <= self.num < 10:
            self.colour = 'green'
        elif 10 <= self.num < 20:
            self.colour = 'blue'
        elif 20 <= self.num < 30:
            self.colour = 'purple'
        else:
            self.colour = 'pink'
        self.canvas.itemconfig(self.obj, fill=self.colour, outline=self.colour)
        self.canvas.itemconfig(self.text, text=str(self.num))
        if self.num < 1:
            self.canvas.delete(self.obj)
            self.canvas.delete(self.text)
        else:
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
    enabled = True

def new_row():
    global gamedata
    gamedata.stage += 1
    for row in tiles:
        for t in row:
            t.y += 37
            t.refresh()
    tiles.insert(0, [])
    for i in range(5, gamedata.width, 37):
        if not random.randint(1, 9) in [1, 2, 3, 4]:
            if random.randint(1, 7) == 1:
                inc = 1
            else:
                inc = 0
            tiles[0].append(tile(canvas, gamedata.stage + inc, i, 5))

class onclick:
    def __init__(self, balls, canvas, tiles):
        self.startx = gamedata.width / 2
        self.starty = gamedata.height
        self.balls = balls
        self.tiles = tiles
        self.canvas = canvas
    def bind(self, event):
        if not self.running:
            print('click')
            self.event = event
            threading.Thread(target=self.ball_move, args=[event], name='Ball movement').start()
    def ball_move(self, event):
        self.running = True
        import time, math
        balls = self.balls
        canvas = self.canvas
        tiles = self.tiles
        dx = self.startx - event.x
        dy = self.starty - event.y
        angle = math.atan(dy / dx)
        ndx = math.cos(angle) * self.maxmove
        ndy = math.sin(angle) * self.maxmove
        if dx > 0:
            ndx = 0 - ndx
        ndy = 0 - abs(ndy)
        balls.append(ball(canvas, gamedata.width / 2, gamedata.height - 50, ndx, ndy))
        gap = 0
        for b in balls:
            gap += 5
            b.x = gamedata.width / 2 + (ndx * gap)
            b.y = gamedata.height - 50 + (ndy * gap)
            b.dx = ndx
            b.dy = ndy
            b.enabled = True
        running = True
        while running:
            still = False
            for b in balls:
                if b.enabled:
                    still = True
                    b.x += b.dx
                    b.y += b.dy
                    clipx = b.x + b.radius > gamedata.width or b.x - b.radius < 0
                    clipy = b.y - b.radius < 0
                    if b.y + b.radius > gamedata.height:
                        b.enabled = False
                    for row in tiles:
                        for t in row:
                            cx = (b.x - b.radius < t.x + t.width and b.x + b.radius > t.x)
                            cy = (b.y - b.radius < t.y + t.height and b.y + b.radius > t.y)
                            if cx and cy:
                                t.num -= 1
                                t.refresh()
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
                                if t.num < 1:
                                    row.remove(t)
                    if clipx or clipy:
                        b.x -= b.dx
                        b.y -= b.dy
                    if clipx:
                        b.dx = 0 - b.dx
                    if clipy:
                        b.dy = 0 - b.dy
                    b.refresh()
            if still:
                running = True
            else:
                running = False
            time.sleep(0.015)
        for b in balls:
            b.x = gamedata.width / 2
            b.y = gamedata.height - 50
            b.refresh()
        self.running = False
        print('end')
    maxmove = 4
    running = False

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

onclick_b = onclick(balls, canvas, tiles)
canvas.bind('<Button-1>', onclick_b.bind)

#####

canvas.pack()

root.mainloop()
