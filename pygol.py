import curses
import time
plays = set()
edits = set()
next_edits = set()
class cell:
    def __init__(self,grid) -> None:
        self.grid = grid
        self.sides = {'u':None,'d':None,'l':None,'r':None,'ul':None,'ur':None,'ul':None,'ur':None,}
        self.__val = 0
        self.__oldval = 0
        self.played = 0
        self.next_val=0
    def next(self):
        self.__oldval = self.__val
        self.__val = self.next_val
        self.next_val=0
        self.played = 0
    def switch(self):
        self.__val ^= 1
        edits.add(self.play)     
    def play(self):
        if self.played:
            return
        self.played = 1
        s = 0
        alltrue=True
        for i in self.sides.values():
            if i.__val == i.__oldval:
                alltrue = False
            s+= i.__val
        if alltrue:
            self.next_val=self.__val
            return
        else:
            for i in self.sides.values():
                next_edits.add(i.play)
        if self.__val:
            if s in [2,3]:
                self.next_val=1
            else:
                self.next_val=0
        else:
            if s==3:
                self.next_val=1
            else:
                self.next_val=0
        plays.add(self.next)
              
    def __str__(self) -> str:
        return str(('#'*self.__val+' ')[:1])
    def __repr__(self) -> str:
        return str(self)
from curses import wrapper
def main(stdscr):
    global edits,plays,next_edits
    height ,width = stdscr.getmaxyx()
    height-=1
    width-=1
    curses.curs_set(0)
    board = []

    for i in range(height):
        board.append([])
        for j in range(width):
            board[i].append(cell((i,j)))
    for i in range(height):
        for j in range(width):
            imo = (i-1)%height
            ipo = (i+1)%height
            jmo = (j-1)%width
            jpo = (j+1)%width
            board[i][j].sides = {
                'u':board[imo][j],'d':board[ipo][j],'l':board[i][jmo],'r':board[i][jpo],
            'ul':board[imo][jmo],'ur':board[imo][jpo],'dl':board[ipo][jmo],'dr':board[ipo][jpo],}

    with open('pattern.txt') as f:
        speed, *data = f.read().split('\n')
    
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j]=='X':
                board[i][j].switch()
    stdscr.clear()
    for i in board:
        for j in i:
            stdscr.addstr(*j.grid,str(j))
    stdscr.refresh()
    stdscr.getch()

    while True:
        for i in board:
            for j in i:
                j.play()
        for i in  edits:
            i()
        edits = next_edits
        next_edits.clear()
        edits.clear()
        for i in  plays:
            i()
        plays.clear()

        stdscr.clear()
        for i in board:
            for j in i:
                stdscr.addstr(*j.grid,str(j))
        stdscr.refresh()
        time.sleep(float(speed))
wrapper(main)