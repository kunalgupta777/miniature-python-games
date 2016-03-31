from tkinter import *

tol = 8
cell_size = 40
off_set = 10
circle_radian = 2
dot_off_set = off_set + circle_radian
game_height = 400
game_width = 400

class Player(object):

    def __init__(self, name, color="black"):
        self.score = 0
        self.str = StringVar()
        self.name = name
        self.color = color

    def update(self):
        self.str.set(self.name + ": %d" % self.score)

class my_frame(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.GO_font = font.Font(self, name="GOFont", family = "Times", weight="bold", size=36)
        self.canvas = Canvas(self, height = game_height, width = game_width)
        self.canvas.bind("<Button-1>", lambda e:self.click(e))
        self.canvas.grid(row=0,column=0)
        self.dots = [[self.canvas.create_oval(cell_size*i+off_set, cell_size*j+off_set, cell_size*i+off_set+2*circle_radian, cell_size*j+off_set+2*circle_radian, fill="black") for j in range(10)] for i in range(10)]
        self.lines = []
        self.info_frame = Frame(self)
        self.players = [Player(input("Player 1 : "),"blue"), Player(input("Player 2 : "),"red")]
        self.info_frame.players = [Label(self.info_frame, textvariable = i.str) for i in self.players]
        for i in self.info_frame.players:
            i.grid()
        
        self.turn = self.players[0]
        self.update_players()
        self.info_frame.grid(row = 0, column = 1, sticky = N)
        self.grid()

    def update_players(self):
        for i in self.players:
            i.update()

    def click(self, event):
        x,y = event.x, event.y
        orient = self.isclose(x,y)
        if(orient):
            if(self.line_exists(x,y, orient)):
                return
            l = self.create_line(x,y, orient)
            score = self.new_box_made(l)
            if(score):
                self.turn.score += score
                self.turn.update()
                self.check_game_over()
            else:
                index = self.players.index(self.turn)
                self.turn = self.players[1-index]
            self.lines.append(l)

    def create_line(self, x, y, orient):
        startx = cell_size * ((x-off_set)//cell_size) + dot_off_set
        starty = cell_size * ((y-off_set)//cell_size) + dot_off_set
        tmpx = (x-off_set)//cell_size
        tmpy = (y-off_set)//cell_size
        
        if(orient == HORIZONTAL):
            endx = startx + cell_size
            endy = starty
        else:
            endx = startx
            endy = starty + cell_size
        return self.canvas.create_line(startx,starty,endx,endy)
        
    def new_box_made(self, line):
        score = 0
        x0,y0,x1,y1 = self.canvas.coords(line)
        if(x0 == x1): # vertical line
            midx = x0
            midy = (y0+y1)/2
            pre = (x0 - cell_size/2, midy)
            post = (x0 + cell_size/2, midy)
        elif(y0 == y1): # horizontal line
            midx = (x0 + x1)/2
            midy = y0
            pre = (midx, y0 - cell_size/2)
            post = (midx, y0 + cell_size/2)
        
        if(len(self.find_lines(pre)) == 3):
            self.fill_in(pre)
            score += 1
        if(len(self.find_lines(post)) == 3):
            self.fill_in(post)
            score += 1
        return score

    def find_lines(self, coords):
        x, y = coords
        if(x < 0 or x > game_width):
            return []
        if(y < 0 or y > game_width):
            return []
        lines = [x for x in self.canvas.find_enclosed(x-cell_size,y-cell_size,x+cell_size,y+cell_size) if x in self.lines]
        return lines

    def fill_in(self, coords):
        x,y = coords
        self.canvas.create_text(x,y,text=self.turn.name, fill=self.turn.color)
        
    def isclose(self, x, y):
        x -= off_set
        y -= off_set
        dx = x - (x//cell_size)*cell_size
        dy = y - (y//cell_size)*cell_size
        
        if(abs(dx) < tol):
            if(abs(dy) < tol):
                return None
            else:
                return VERTICAL
        elif(abs(dy) < tol):
            return HORIZONTAL
        else:
            return None

    def line_exists(self, x,y, orient):
        id_ = self.canvas.find_closest(x,y,halo=tol)[0]
        if(id_ in self.lines):
            return True
        else:
            return False

    def check_game_over(self):
        total = sum([x.score for x in self.players])
        if(total == 81):
            self.canvas.create_text(game_width/2, game_height/2, text="GAME OVER", font="GOFont", fill="#888")

root = Tk()
root.f = my_frame(root)
root.mainloop()
