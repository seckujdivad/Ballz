#no. 9 large
global root, tiles, gamedata, new_row, slabel, settings, canvas
import tkinter as tk
from tkinter import messagebox
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
        if self.num == 'BALL':
            tsize = 8
        else:
            tsize = 12
        self.obj = self.canvas.create_rectangle(x, y, x + self.width, y + self.height, fill=self.colour, outline=self.colour)
        self.text = self.canvas.create_text(x + (self.width / 2), y + (self.height / 2), text=str(self.num), fill='white', font=('', tsize))
        self.refresh()
    def refresh(self):
        if not self.num == 'BALL':
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
        if self.num != 'BALL' and self.num < 1:
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
            if random.randint(1, 7) == 1:
                string = 'BALL'
            else:
                string = gamedata.stage + inc
            tiles[0].append(tile(canvas, string, i, 5 * 2 + 32))

class onclick:
    def __init__(self, balls, canvas, tiles):
        self.startx = gamedata.width / 2
        self.starty = gamedata.height - 50
        self.balls = balls
        self.tiles = tiles
        self.canvas = canvas
    def bind(self, event):
        if (not self.running) and (not self.stop):
            self.event = event
            threading.Thread(target=self.ball_move, args=[event], name='Ball movement', daemon=True).start()
    def ball_move(self, event):
        self.running = True
        import time, math
        balls = self.balls
        canvas = self.canvas
        tiles = self.tiles
        dx = self.startx - event.x
        dy = self.starty - event.y
        angle = math.atan(dy / dx)
        ndx = float(math.cos(angle) * self.maxmove)
        ndy = float(math.sin(angle) * self.maxmove)
        if dx > 0:
            ndx = 0 - ndx
        ndy = 0 - abs(ndy)
        if self.score == 0:
            balls.append(ball(canvas, gamedata.width / 2, gamedata.height - 50, ndx, ndy))
        else:
            for i in range(self.ballsnextround):
                balls.append(ball(canvas, gamedata.width / 2, gamedata.height - 50, ndx, ndy))
        for b in balls:
            b.dx = ndx
            b.dy = ndy
            b.x = gamedata.width / 2
            b.y = gamedata.height - 50
            b.enabled = False
        running = True
        lsince = 9
        self.ballsnextround = 0
        while running:
            lsince += 1
            still = False
            for b in balls:
                if lsince == 10 and not b.enabled:
                        lsince = 0
                        b.enabled = True
                if b.enabled:
                    still = True
                    b.x += b.dx
                    b.y += b.dy
                    clipx = b.x + b.radius > gamedata.width or b.x - b.radius < 0
                    clipy = b.y - b.radius < 0
                    if b.y + b.radius > gamedata.height:
                        b.enabled = False
                    for row in tiles:
                        if row == []:
                            tiles.remove(row)
                        for t in row:
                            cx = (b.x - b.radius < t.x + t.width and b.x + b.radius > t.x)
                            cy = (b.y - b.radius < t.y + t.height and b.y + b.radius > t.y)
                            if cx and cy:
                                if t.num == 'BALL':
                                    t.num = -1234
                                else:
                                    t.num -= 1
                                t.refresh()
                                centrex = t.x + (t.width / 2)
                                centrey = t.y + (t.height / 2)
                                dx = abs(b.x - centrex)
                                dy = abs(b.y - centrey)
                                if t.num == -1234:
                                    self.ballsnextround += 1
                                else:
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
            if still:
                running = True
            else:
                running = False
            time.sleep(settings.physics_delay_value)
        for row in tiles:
            for t in row:
                if t.y > 340:
                    self.stop = True
                    canvas.create_text(gamedata.width / 2, gamedata.height / 2, text='GAME OVER', font=('', 20), fill='white')
        for b in balls:
            b.x = gamedata.width / 2
            b.y = gamedata.height - 50
            #b.enabled = True
            b.refresh()
        new_row()
        self.score += 1
        slabel.increment(1)
        self.running = False
    maxmove = 4
    running = False
    stop = False
    ballsnextround = 0
    score = 0

def refreshloop():
    import time
    obj = ''
    while True:
        start = time.time()
        for b in balls:
            b.refresh()
        delay = (1 / int(settings.frame_cap_value)) - (time.time() - start)
        if delay > 0:
            time.sleep(delay)

class scorelabel:
    def __init__(self):
        self.widget = tk.Label(root, text='----', bg='black', fg='snow1', font=('', 20))
    def increment(self, inc):
        self.score += inc
        self.widget.config(text=str(self.score))
    score = 0

class gamedata:
    stage = 0
    height = 500
    width = 299

slabel = scorelabel()
canvas = tk.Canvas(root, height=gamedata.height, width=gamedata.width, bg='black', highlightthickness=0)

class settings_class:
    def __init__(self):
        self.open_button = tk.Button(root, text='⚙', font=('', 15), command=self.make, relief=tk.FLAT, bg='black', fg='white', overrelief=tk.RIDGE, activeforeground='white', activebackground='black')
    def make(self):
        if self.running:
            self.window.destroy()
            self.running = False
        else:
            self.running = True
            self.window = tk.Frame(root)
            self.labels = tk.Frame(self.window)
            self.inputs = tk.Frame(self.window)
            self.frame_cap_label = tk.Label(self.labels, text='FPS Cap')
            self.frame_cap = tk.Spinbox(self.inputs, increment=2, from_=1, to=60, command=self.update_frame_cap, highlightthickness=0)
            self.physics_delay_label = tk.Label(self.labels, text='Physics Tick Delay (ms)')
            self.physics_delay = tk.Spinbox(self.inputs, increment=0.5, from_=0, to=10, command=self.update_physics_delay)
            ####
            self.frame_cap_label.pack(fill=tk.X, anchor='nw')
            self.physics_delay_label.pack(fill=tk.X, anchor='nw')
            ####
            self.frame_cap.pack(fill=tk.X, anchor='nw', expand=True)
            self.physics_delay.pack(fill=tk.X, anchor='nw', expand=True)
            ####
            self.frame_cap.delete(0, tk.END)
            self.physics_delay.delete(0, tk.END)
            self.frame_cap.insert(0, self.frame_cap_value)
            self.physics_delay.insert(0, self.physics_delay_value * 1000)
            ####
            self.labels.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.inputs.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            self.window.pack(side=tk.BOTTOM, fill=tk.BOTH)
    def update_frame_cap(self):
        try:
            self.frame_cap_value = float(self.frame_cap.get())
        except:
            pass
    def update_physics_delay(self):
        try:
            self.physics_delay_value = float(self.physics_delay.get()) / 1000
        except:
            pass
    threadhash = 0
    frame_cap_value = 50
    physics_delay_value = 0.004
    running = False
settings = settings_class()


#####

tiles = []
new_row()

balls = []

onclick_b = onclick(balls, canvas, tiles)
canvas.bind('<Button-1>', onclick_b.bind)
threading.Thread(target=refreshloop, name='Refresh', daemon=True).start()

#####

slabel.widget.pack()
canvas.pack()
settings.open_button.pack(fill=tk.BOTH, side=tk.TOP)

root.mainloop()
