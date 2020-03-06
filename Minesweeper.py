import tkinter as tk
import threading
import random

global width_final
global height_final
global num_col
global num_row

class Minesweeper(object):
    def __init__(self, master):
        self._master = master
        master.title('Minesweeper (Ready)')

        # Game variables
        self._mines = 0
        self._chosen_mines = 0
        self._game_on = False
        self._mineRatio = (1/3.5)
        self._game_seconds = 0
        self.looper = tk.Label(self._master,text="")
        self.looper.pack_forget()
        self.num_col = 0
        self.num_row = 0
        
        # Screen variables
        self._width = 15
        self._height = 50
        self._width_final = None
        self._height_final = None

        self.setup()

    def game_over(self):
        self._game_on = False
        app.game_over_text = tk.Label(app._canvas,text="Game Over!",font=("Arial",25))
        app.game_over_text.place(x=self._width_final/4,y=self._height_final/4)
        

    def check_game(self):
        #assume the game is over
        test = True
        for i in self._group:
            # test is something HAS NOT been clicked / flag pressed
            if i._flagged == False and not i._clicked:
                test = False
        return test

    def mouse_click(self,event):
        x = event.x
        y = event.y

        # find the square that has been clicked on and reveal it
        for i in range(len(self._group)):
            sqr = self._group[i]
            if (x > sqr._x and x < (sqr._x+sqr._width)
                and y > sqr._y and y < (sqr._y+sqr._height)
                and self._game_on):
                #print(sqr.nearby_mines)
                sqr.reveal()
                self.adj_mine_check(i)
                sqr._clicked = True
                #print("Current Row: ",sqr._row)
                #print("Current col: ",sqr._col)

        if self.check_game():
            self.game_over()
            
    def right_click(self,event):
        x = event.x
        y = event.y

        # find the square that has been clicked on and flag it
        for i in range(len(self._group)):
            sqr = self._group[i]
            if (x > sqr._x and x < (sqr._x+sqr._width)
                and y > sqr._y and y < (sqr._y+sqr._height) and not sqr._clicked
                and self._game_on):
                    if (not sqr._flagged):
                        app._canvas.create_rectangle(sqr._x,sqr._y,sqr._x+sqr._width,sqr._y+sqr._height,fill="yellow")
                    else:
                        app._canvas.create_rectangle(sqr._x,sqr._y,sqr._x+sqr._width,sqr._y+sqr._height,fill="gray")
                    sqr._flagged = not sqr._flagged
                    
        if self.check_game():
            self.game_over()              
        
    def setup(self):
        self._frame = tk.Frame(self._master)

        # Setting up to receive the number of mines from the user
        self._label = tk.Label(self._frame,text="Number of mines: ",font=("Arial",20))
        self._label.pack(side=tk.LEFT,padx=15)
        
        self._input = tk.Entry(self._frame,width=3)
        self._input.pack(side=tk.LEFT)

        self._submit = tk.Button(self._frame,text="Begin Game",command=self.begin_game)
        self._submit.pack(side=tk.LEFT,padx=15)

        self._frame.pack(side=tk.LEFT,pady=15)

    def game_timer(self):
        self._game_seconds += 1
        
        title = 'Minesweeper ('+str(self._game_seconds)+' sec)'
        app._master.title(title)

        if self._game_on:
            app.looper.after(1000, self.game_timer)

    def begin_game(self):
        self._group = []
        self._chosen_mines = 0
        self._game_on = True
        self._mines = int(self._input.get())
        self._frame.destroy()

        self.game_timer()
        
        # procedurally calculate the window dimensions using a factoring program
        self._totalsquares = round(self._mines / self._mineRatio)

        var = True
        self._n = 1
        self._k = 0
        self._factors = []

        # determine factors of the total square amount
        while True:
            while (self._k < (self._totalsquares // 2)):
                if (self._n * self._k == self._totalsquares):
                    # makes sure that both numbers are UNIQUE (a diff of 0 supersedes any actual dimensions)
                    if self._n not in self._factors:
                        self._factors.append(self._n)
                    if self._k not in self._factors:
                        self._factors.append(self._k)
                if self._n == 2:
                    self._k += 1
                if self._k != self._totalsquares:
                    if (self._n+1 > self._totalsquares):
                        self._n = 2
                    else:
                        self._n += 1
            # handles PRIME numbers
            if (len(self._factors) == 0):
                self._totalsquares += 1
            else:
                break


        # find the differences to find the two closest numbers
        self._differences = []
        
        i = 0
        j = 1
        while (True):
            try:
                first_num = self._factors[2*i]
                second_num = self._factors[(2*j)-1]
                self._differences.append(abs(first_num-second_num))
                i += 1
                j += 1
            except:
                break

        # find the smallest difference, map it 2 numbers, and transform them into dimensions
        magic_number = min(self._differences)
        index_num = self._differences.index(magic_number)*2
        num_a = self._factors[index_num]
        num_b = self._factors[index_num+1]

        if num_a > num_b:
            num_col = num_a
            num_row = num_b
            self.num_col = num_a
            self.num_row = num_b
        else:
            num_col = num_b
            num_row = num_a
            self.num_col = num_b
            self.num_row = num_a
            
        width_final = num_col*40
        height_final = num_row*40

        width_final += 1 #padding
        height_final += 1

        self._width_final = width_final
        self._height_final = height_final

        # setting up the canvas together w/ button presses/clicks
        self._canvas = tk.Canvas(self._master,bg="light blue",width=width_final,height=height_final)
        self._canvas.bind("<Button-1>",self.mouse_click)
        self._canvas.bind("<Button-2>",self.right_click)
        self._canvas.pack(side=tk.LEFT,expand=True,fill=tk.BOTH,pady=0,padx=0)

        # begin setup of new field
        for i in range(num_col):
            for j in range(num_row):
                self._group.append(self.Square(40*i,40*j))

        # Pick the mines on the field
        while (self._chosen_mines != self._mines):
            num = random.randint(0,len(self._group)-1)
            if (not self._group[num]._mine):
                self._group[num]._mine = True
                self._chosen_mines += 1
            
        for k in range(len(self._group)):
            sqr = self._group[k]
            sqr.draw()

            # find the number of nearby mines
            
            if (sqr._col != num_col): #check right               
                for n in range(len(self._group)):
                    sqr_two = self._group[n]
                    if (sqr_two._row == sqr._row
                        and sqr_two._col == sqr._col+1
                        and sqr_two._mine):
                        #print("Right mine found!\nRow: ",sqr_two._row,"\tCol: ",sqr_two._col)
                        #print("With orig at: ",sqr._row,"\tCol: ",sqr._col,"\n")
                        sqr.nearby_mines += 1
                       
            if (sqr._col != 1): #check left
                for n in range(len(self._group)):
                    if (self._group[n]._row == sqr._row
                        and self._group[n]._col == sqr._col-1
                        and self._group[n]._mine):
                        #print("Left mine found!\nRow: ",sqr_two._row,"\tCol: ",sqr_two._col)
                        #print("With orig at: ",sqr._row,"\tCol: ",sqr._col,"\n")
                        sqr.nearby_mines += 1

            if (sqr._row != num_row): #check bottom
                for n in range(len(self._group)):
                    if (self._group[n]._col == sqr._col
                        and self._group[n]._row == sqr._row+1
                        and self._group[n]._mine):
                        sqr.nearby_mines += 1

            if (sqr._row != 1): #check top
                for n in range(len(self._group)):
                    if (self._group[n]._col == sqr._col
                        and self._group[n]._row == sqr._row-1
                        and self._group[n]._mine):
                        sqr.nearby_mines += 1

            if (sqr._row != 1 and sqr._col != num_col): #check top right
                for n in range(len(self._group)):
                    if (self._group[n]._col == sqr._col+1
                        and self._group[n]._row == sqr._row-1
                        and self._group[n]._mine):
                        sqr.nearby_mines += 1

            if (sqr._row != num_row and sqr._col != num_col): #check bottom right
                for n in range(len(self._group)):
                    if (self._group[n]._col == sqr._col+1
                        and self._group[n]._row == sqr._row+1
                        and self._group[n]._mine):
                        sqr.nearby_mines += 1

            if (sqr._row != num_row and sqr._col != 1): #check bottom left
                for n in range(len(self._group)):
                    if (self._group[n]._col == sqr._col-1
                        and self._group[n]._row == sqr._row+1
                        and self._group[n]._mine):
                        sqr.nearby_mines += 1

            if (sqr._row != 1 and sqr._col != 1): #check top left
                for n in range(len(self._group)):
                    if (self._group[n]._col == sqr._col-1
                        and self._group[n]._row == sqr._row-1
                        and self._group[n]._mine):
                        sqr.nearby_mines += 1
            
        #for i in self._group:
            #i.reveal()

    def adj_mine_check(self,sqr_index):
        # grab the mine for easy reference
        sqr = self._group[sqr_index]
        num = sqr.nearby_mines

        print(num)

        #check for adjacent squares
        if (num == 0 and not sqr._clicked and not sqr._flagged
            and not sqr._mine):
            print("asd")
            if (sqr._col != self.num_col): #check right               
                for n in range(len(self._group)):
                    sqr_two = self._group[n]
                    if (sqr_two._row == sqr._row
                        and sqr_two._col == sqr._col+1
                        and self._group[n].nearby_mines == 0):
                        self.adj_mine_check(n)
                   
            if (sqr._col != 1): #check left
                for n in range(len(self._group)):
                    if (self._group[n]._row == sqr._row
                        and self._group[n]._col == sqr._col-1
                        and self._group[n].nearby_mines == 0):
                        self.adj_mine_check(n)

            if (sqr._row != self.num_row): #check bottom
                for n in range(len(self._group)):
                    if (self._group[n]._col == sqr._col
                        and self._group[n]._row == sqr._row+1
                        and self._group[n].nearby_mines == 0):
                        self.adj_mine_check(n)

            if (sqr._row != 1): #check top
                for n in range(len(self._group)):
                    if (self._group[n]._col == sqr._col
                        and self._group[n]._row == sqr._row-1
                        and self._group[n].nearby_mines == 0):
                        self.adj_mine_check(n)

            if (sqr._row != 1 and sqr._col != self.num_col): #check top right
                for n in range(len(self._group)):
                    if (self._group[n]._col == sqr._col+1
                        and self._group[n]._row == sqr._row-1
                        and self._group[n].nearby_mines == 0):
                        self.adj_mine_check(n)

            if (sqr._row != self.num_row and sqr._col != self.num_col): #check bottom right
                for n in range(len(self._group)):
                    if (self._group[n]._col == sqr._col+1
                        and self._group[n]._row == sqr._row+1
                        and self._group[n].nearby_mines == 0):
                        self.adj_mine_check(n)

            if (sqr._row != self.num_row and sqr._col != 1): #check bottom left
                for n in range(len(self._group)):
                    if (self._group[n]._col == sqr._col-1
                        and self._group[n]._row == sqr._row+1
                        and self._group[n].nearby_mines == 0):
                        self.adj_mine_check(n)

            if (sqr._row != 1 and sqr._col != 1): #check top left
                for n in range(len(self._group)):
                    if (self._group[n]._col == sqr._col-1
                        and self._group[n]._row == sqr._row-1
                        and self._group[n].nearby_mines == 0):
                        self.adj_mine_check(n)
        sqr.reveal()
        
                
                
            
    class Square():
        def __init__(self,x,y):
            self._x = x+3
            self._y = y+3
            self._width = 40
            self._height = 40

            self._col = round((self._x-3)/40)+1
            self._row = round((self._y-3)/40)+1
            
            self._mine = False
            self._flagged = False
            self._clicked = False
            self.nearby_mines = 0

            self._label_dim = 5

        def reveal(self):
            if (not self._flagged):
                if (self._mine):
                    app._canvas.create_rectangle(self._x,self._y,self._x+self._width,self._y+self._height,fill="red")
                else:
                    app._canvas.create_rectangle(self._x,self._y,self._x+self._width,self._y+self._height,fill="white")
                    if self.nearby_mines != 0:
                        self.mine_label = tk.Label(app._canvas,text=self.nearby_mines,font=("Arial",14))
                        self.mine_label.place(x = self._x+self._label_dim, y = self._y+self._label_dim, width=self._width-self._label_dim,height=self._height-self._label_dim)
                self._clicked = True
                
        def draw(self):
            app._canvas.create_rectangle(self._x,self._y,self._x+self._width,self._y+self._height,fill="gray")
            
root = tk.Tk()
app = Minesweeper(root)
root.mainloop()

'''
Factoring program:
    - Find all the factors of the SQUARE amount (mines*5=c)
    - See which numbers multiply to what
    - The 2 numbers with the least difference are used as reference
    - If no two numbers exist 


'''



# a * height = screen_height
# b * width = screen_width

# a * b = c #total num. of squares
# mines * 5 = c

'''
497 * b = c
24.85 * b = c

mines * 5 = c
10 * 5 = 50 (c)

Therefore, b = 1
'''

#497 screen_height px

    #497 / 40 = 12

#797 width px

    #797 / 40 = 66
    
