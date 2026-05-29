from pythonds3.basic import Stack
import random as r

def l_sum(l:list[int]):
    sum = 0
    for n in l:
        sum = sum+n
    return sum

def recursion_sum(l:list[int]):
    if l==[]:
        return 0
    else:
        return l[0] +recursion_sum(l[1:])
    


funcs = [l_sum, recursion_sum]

for f in funcs:
    print (f([]))
    print (f([1,3,7,9]))

"""
the 3 laws of recursion.
1_) must have a base case.
2) must change its state to approach the base case.
3) must call itself recursively
"""

def to_str(n, base):
    conversion = "0123456789ABCDEF"#the index of this string will be where the remainder of our current states next lsd
    if n<base:
        return conversion[n]
    return to_str(n//base, base)+conversion[n%base]

print(to_str(1453, 16))

def to_str_loop(n,base):
    r_stack = Stack()
    convert_key = "0123456789ABCDEF"
    while n>0:
        if n<base:
            r_stack.push(convert_key[n])
        else:
            r_stack.push(convert_key[n%base])
        n = n//base
    res = ""
    while not r_stack.is_empty():
        res = res+str(r_stack.pop())
    return res#feed chars into stack then read off stack by poping. filo

print(to_str_loop(1453, 16))



def rev_str(s):
    if s=="":
        return s
    else:
        return rev_str(s[1:])+s[0]
    
print(rev_str("Hello"))

def pali_check(stri, irts=None):#rts is str backwards 
    if irts==None:
        return pali_check(stri,rev_str(stri))
    if len(stri)<2:
        return True
    if stri[0]==irts[0]:
        return pali_check(stri[1:],irts[1:])#hindsight shouldnt have used str but it is what it is
    return False

print(pali_check("hello"))
print(pali_check("hellolleh"))


import turtle
"""
def draw_spiral(my_turtle:turtle, line_len):
    if line_len>0:
        my_turtle.forward(line_len)
        my_turtle.right(90)
        draw_spiral(my_turtle, line_len-5)

my_turd = turtle.Turtle()
my_win = turtle.Screen()
draw_spiral(my_turd, 100)
my_win.exitonclick()
"""
"""
def tree(branch_len, t):
    if branch_len>5:
        t.pensize(branch_len//2)
        t.forward(branch_len)
        t.right(20)#turn right 20 deg.
        tree(branch_len-15, t)
        t.left(40)
        tree(branch_len-15,t)
        t.right(20)
        t.backward(branch_len)
        #my prediction turtle will move forward then turn right 20 deg and keep doing that until len is <=5. 
        # after turd will teleport back to it pointing 20 degr to the right after the first forward and re iterate the rights after an initial left. 
        # every forward will reduce the subesequent and when turd teleports back it uses the len it had at that point of time.
        #at the end turd will go back to the head of the tree
        #WORKS AS EXPECTED

turd = turtle.Turtle()
my_win = turtle.Screen()
turd.left(90)
turd.up()
turd.backward(100)
turd.down()
turd.color("green")
tree(75,turd)
my_win.exitonclick()
"""

import math
import turtle

def sierpinski_triangle(turds, length):
    """
    mental model: draw the middle triagle with and init 90 deg turn to the left forward half len turn left 240 deg.
    forward full, left 240 deg forward full, left 240deg forward full.
    right 120deg, pass len as len//2.
    forwardfull right 240 forwrd... this is too complicated

    im going to use 3 turds that split into more smaller turds after every iteration of subtriaglgles top right left.
    all turds will start on the top of their sub triagle. after macro triagle is init the midpoit of each side will be the starting point for eery turd.
    the turds will coop to each draw one side of the subtri then go half that distace to start on each of the subtri's subtri and turn 90 to face inside. 
    One turd will not move 2 will turn 33.3deg one left one right and move for...

    final idea: 
    init
    start with 3 turds. 2 turn 123.3 deg right other left. 
    r1 will go forward half len turn left 90 deg
    r2 will go forward len turn right 123.3 deg forward len, reverse half len turn left 90 deg
    l1 will go forward len and reverse half, turn right 90 deg.
        by this point all 3 turds are at the half point of the triangles 3 sides facing outwards.
    now we can recurse with our 3 turds using the same alg but r2 will need to turn left on its 2nd and 3rd turn 
    ##note I will prob need to turn in rad so the turds makes a uniform isosceles triangle where the edges meet.
    """
    #print(length)
    if length<25:
        return
    r1turd, r2turd, l1turd = turds[0],turds[1],turds[2]
    
    r1turd.forward(length/2)
    r1turd.left(math.pi/2)
    r2turd.forward(length)
    r2turd.right((2/3)*math.pi)
    r2turd.forward(length)
    r2turd.backward(length/2)
    r2turd.left(math.pi/2)
    l1turd.forward(length)
    l1turd.backward(length/2)
    l1turd.right(math.pi/2)

    for t in turds:
        t.right(5*math.pi/6)
        t.forward(length/2)
        t.right(2*math.pi/3)
        t.forward(length/4)
        t.right(math.pi/2)
        new_turd_1 = t.clone()
        new_turd_2 = t.clone()
        t.right((5/6)*math.pi)
        new_turd_1.right((5/6)*math.pi)
        new_turd_2.left((5/6)*math.pi)
        sierpinski_triangle([t,new_turd_1,new_turd_2], length/4)


"""
r1turd = turtle.Turtle()
r2turd = turtle.Turtle()
l1turd = turtle.Turtle()
my_win = turtle.Screen()
length = 400

turds = [r1turd, r2turd, l1turd]
for t in turds:
    #t.hideturtle()
    #t.speed(0)
    t.left(90)
    t.up()
    t.forward((2/3)*length)

r1turd.radians()
r2turd.radians()
l1turd.radians()

r1turd.right((5/6)*math.pi)
r2turd.right((5/6)*math.pi)
l1turd.left((5/6)*math.pi)

for t in turds:
    t.down()

sierpinski_triangle(turds, length)


"""
def sierpinski_triangle_v2(turds, length, colours):
    """
    last version only wend inside on sub tris. this version will fill the 3 outside boxes with the 1 inside for every macro tri
    """
    if length<10:
        for t in turds:
            t.hideturtle()
        return
    turds[2].fillcolor(colours[0])
    turds[2].begin_fill()
    for j in range(len(turds)):
        for i in range(j+1):
            turds[j].right(2*math.pi/3)
            turds[j].forward(length)
        if j==2:
            turds[2].end_fill()
        turds[j].backward(length/2)
        temp_turd_1 = turds[j].clone()
        temp_turd_2 = temp_turd_1.clone()
        temp_turd_3 = temp_turd_2.clone()
        
        turds[j].hideturtle()
        sierpinski_triangle_v2([temp_turd_1,temp_turd_2,temp_turd_3],length/2,colours[1:])
    turds[2].hideturtle()
    return
"""
After finishing and looking at the books example they kind of cheated.
They didn't mention anywhere prior that I could just calc cords and move the turtle where I calculated.
I Think their version is harder to read but faster. I apparently needed the unit circle practice as I struggled figuring out what radians my turds needed to turn.
To be fair I kept calculating that pi would be straight instead of turning around which threw everything off. 
"""


turd1 = turtle.Turtle()
turd2 = turtle.Turtle()
turd3 = turtle.Turtle()
my_win = turtle.Screen()
length = 400
extra_colours = 10
colours = ["violet","yellow","white","green","red","blue",]+[(r.randint(0,1)+r.randint(0,9)/10) for _ in range(extra_colours)]

turds = [turd1, turd2, turd3]
for t in turds:
    t.up()
    t.speed(0)
    #t.hideturtle()
    t.left(90)
    t.forward(2*length/3)
    t.radians()
    t.right(math.pi/6)
    t.down()

sierpinski_triangle_v2(turds, length, colours)
