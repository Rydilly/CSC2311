from pythonds3.basic import Stack


def move_tower(height, from_pole, to_pole, with_pole):
    if height <1:
        return
    move_tower(height-1, from_pole, with_pole, to_pole)
    move_disk(from_pole, to_pole)
    move_tower(height-1, with_pole, to_pole, from_pole)

def move_disk(from_pole, to_pole):
    print("moving disk", from_pole, "to", to_pole)
    to_pole.push(from_pole.pop())

a = Stack()
for i in range(10-1,-1,-1):
    a.push(i)

b = Stack()
c = Stack()
stack_list=[a,b,c]

move_tower(10, a,b,c)

for s in range(len(stack_list)): 
    print(f"Stack {s}")
    while not stack_list[s].is_empty():
        print(stack_list[s].pop())

"""
Im surprised they didn't go into memoizing with this problem.
"""





import turtle
import math
#import fileio

START = "S"
OBSTACLE ="+"
TRIED = "."
DEAD_END = "-"
PART_OF_PATH="O"


class Maze:
    def __init__(self, maze_filename):
        with open(maze_filename, 'r') as maze_file:
            self.maze_list = [
                [ch for ch in line.rstrip("\n")]#is line just a line from the file?
                for line in maze_file.readlines()#line is declared here. easy to miss because it seems like a new line at first glance
            ]
        self.rows_in_maze = len(self.maze_list)
        self.columns_in_maze = len(self.maze_list[0])
        for row_idx, row in enumerate(self.maze_list):
            if START in row:
                self.start_row = row_idx
                self.start_col = row.index(START)#finds the index of START aka "S"
                break
    
        self.x_translate = -self.columns_in_maze/2
        self.y_translate = self.rows_in_maze/2
        self.turd = turtle.Turtle()
        self.turd.shape("turtle")
        self.window = turtle.Screen()
        self.window.setworldcoordinates(
            -(self.columns_in_maze-1)/2-.5,#number of gaps +1
            -(self.rows_in_maze-1)/2-.5,
            (self.columns_in_maze-1)/2+.5,
            (self.rows_in_maze-1)/2+.5
        )

    def draw_maze(self):
        self.turd.speed(10)
        self.window.tracer(0)
        for y in range(self.rows_in_maze):
            for x in range(self.columns_in_maze):
                if self.maze_list[y][x]==OBSTACLE:
                    self.draw_centered_box(
                        x+self.x_translate, -y+self.y_translate,"orange"
                    )#where is start?
        self.turd.color("black")
        self.turd.fillcolor("blue")
        self.window.update()
        self.window.tracer(1)

    def draw_centered_box(self,x,y,color = "brown"):
        """
        draws a 1x1 box at a cell
        """
        self.turd.up()
        self.turd.goto(x-.5,y-.5)
        self.turd.color(color)
        self.turd.fillcolor(color)
        self.turd.setheading(90)
        self.turd.down()
        self.turd.begin_fill()
        for i in range(4):
            self.turd.forward(1)
            self.turd.right(90)
        self.turd.end_fill()

    def update_position(self, row, col, val=None):
        if val:
            self.maze_list[row][col]=val
        self.move_turtle(col,row)

        if val == PART_OF_PATH:
            color = "green"
        elif val == OBSTACLE:
            color="red"
        elif val==TRIED:
            color="brown"
        elif val == DEAD_END:
            color="red"
        else:
            color = None

        if color:
            self.drop_bread_crumb(color)

    
    def move_turtle(self, x, y):
        """
        points to box then jumps to it
        box is expected to be touching turd
        """
        self.turd.up()
        self.turd.setheading(self.turd.towards(x+self.x_translate,-y+self.y_translate))
        self.turd.goto(x+self.x_translate,-y+self.y_translate)

    def drop_bread_crumb(self, color):
        self.turd.dot(10, color)

    def is_exit(self, row, col):
        """
        if turd is touching an edge
        """
        return(
            row==0
            or row == self.rows_in_maze-1
            or col == 0
            or col == self.columns_in_maze-1
        )
    def __getitem__(self, key):
        return self.maze_list[key]

def search_from(maze, row, column):
    """
    returns true if row, col cell is a valid move
    """
    maze.update_position(row, column)#turd will go to cell and fill the cell a color based on what it sees

    if maze[row][column]==OBSTACLE:
        return False
    if maze[row][column] in [TRIED, DEAD_END]:
        return False
    if maze.is_exit(row,column):
        maze.update_position(row, column, PART_OF_PATH)
        return True
    maze.update_position(row,column,TRIED)#actively exploring from here or its descendents
    found = (#looks like turd can only move up down left or right
        search_from(maze, row-1, column)
        or search_from(maze, row, column-1)
        or search_from(maze, row+1, column)
        or search_from(maze, row, column+1)
        )
    if found:
        maze.update_position(row,column, PART_OF_PATH)
    else:
        maze.update_position(row, column, DEAD_END)
    return found

the_maze = Maze("maze1.txt")
the_maze.draw_maze()
the_maze.update_position(the_maze.start_row, the_maze.start_col)

search_from(the_maze, the_maze.start_row, the_maze.start_col)


