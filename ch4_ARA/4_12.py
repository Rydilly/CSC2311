import math

def make_change_naive(coins, change):
    if change in coins:
        return 1
    min_coins = math.inf
    for i in [c for c in coins if c<=change]:#iterate through coins and makes a list of coins that are less then change then iterates through it
        coins_count = 1+make_change_naive(
            coins, change-i
        )
        min_coins = min(coins_count, min_coins)#if no sulutions at branch inf is the min
    return min_coins

def make_change_btr(coins, change, known_results):
    #we know the most possible coins for any config would be using 1's. 
    # But how do we know 1's are in coins? if they are not is it possible to return a impossible path? 
    # ex target 16 coins [2,15] would return 2 coins 15 and 1, no?
    
    #also passing a list means children only inherit results from parents, meaning nodes at the same level with different parents may have different known results
    min_coins = change
    if change in coins:
        known_results[change]=1
        return 1
    elif known_results[change]>0:
        return known_results[change]
    else:
        for i in [c for c in coins if c<=change]:
            num_coins = 1+make_change_btr(coins, change-i, known_results)
            if num_coins<min_coins:
                min_coins = num_coins
            known_results[change]=min_coins
    return min_coins

def make_change_btm_up(coins, change, min_coins):
    #simple wavefront approach
    #same problem as last func
    for cents in range(change+1):
        coin_count = cents#coin idx
        for j in [c for c in coins if c<=cents]:
            if min_coins[cents-j]+1<coin_count:#starts as 0. at 0 == cents is false(cant make change with 0 cents), 1 is min coins for t==1,... when min_coins[target-cur_coin]+1<target, coin_count which is currently == target becomes min_coins[...] and you check the rest of the coins for a better val at that min_coins.
                coin_count = min_coins[cents-j]+1
        min_coins[cents]=coin_count
    return min_coins[change]

def make_change_btm_up_v2(coins, change, min_coins, coins_used):
    for cents in range(change+1):
        coin_count = cents
        new_coin = 1
        for j in [c for c in coins if c<=cents]:
            if min_coins[cents-j]+1<coin_count:
                coin_count=min_coins[cents-j]+1
                new_coin=j
        min_coins[cents]=coin_count
        coins_used[cents]=new_coin
    return min_coins[change]

def print_coins(coins_used, change):
    coin = change
    while coin>0:
        this_coin = coins_used[coin]#access best coin at every index starting at target so works for targets<target when using btm_up_v2
        print(f"{this_coin} ")
        coin = coin-this_coin
    


def gcf_alg(val_a, val_b, cur_val=None):
    if cur_val is None:
        cur_val=min(val_a, val_b)
    if (val_a%cur_val==0) and (val_b%cur_val==0):
        return cur_val
    return gcf_alg(val_a, val_b, cur_val-1) 

def rev_list(in_list, out_list=[]):
    if len(in_list)<1:
        return out_list
    out_list.append(in_list.pop())
    return rev_list(in_list, out_list)

import turtle
def mountain(turd: turtle.Turtle, length=200):
    if length<5:
        turd.hideturtle()
        return
    turd.forward(length)
    turd.right(150)
    turd.forward(length/4)
    new_turd = turd.clone()
    turd.forward(length/4)
    turd.left(150)
    turd.forward(length/4)
    turd.right(150)
    turd.forward(length)
    new_turd.left(150)
    turd.hideturtle()
    return mountain(new_turd, 3*length/4)
    

def start_mountan():
    turd = turtle.Turtle()
    win = turtle.Screen()
    turd.up()
    turd.backward(200)
    turd.left(70)
    turd.backward(250)
    turd.down()
    mountain(turd)


def fib(n, memo = {}):
    #print(memo)
    if n<2:
        memo[n]=n
        return n
    elif n in memo:
        return memo[n]
    else:
        memo[n]= fib(n-1,memo)+fib(n-2,memo)
        return memo[n]
    
def tower_of_hanoi(height, A,B,C):
    if height<1:
        return
    tower_of_hanoi(height-1,A,C,B)
    print(f"Swapping {A} with {B}")
    tower_of_hanoi(height-1,C,B,A)


def make_quadrants(quad):    
    midpoint = [(quad[0][0]+quad[1][0])/2,(quad[0][1]+quad[1][1])/2]
    quad1=[[midpoint[0],midpoint[1]],[quad[1][0],quad[1][1]]]
    quad2=[[quad[0][0],midpoint[1]],[midpoint[0],quad[1][1]]]
    quad3=[[quad[0][0],quad[0][1]],[midpoint[0],midpoint[1]]]
    quad4=[[midpoint[0],quad[0][1]],[quad[1][0],midpoint[1]]]
    return[quad1,quad2,quad3,quad4]

def draw_n_conductor(quad):
    """
    makes the base case for any quadrant(or entire square if provided)
    """
    length = quad[1][0]-quad[0][0]#should be a square so fine for x and y
    #length is the length of one side of the quad

    turd = turtle.Turtle()
    quads = make_quadrants(quad)
    turd.hideturtle()

    turd.up()
    turd.goto(quads[2][0][0]+length/8,quads[2][1][1]-length/8)#going to quad 3 to start then 2, then 1 then 4
    turd.down()
    turd = draw_n(turd,length/4)

    turd.up()
    turd.goto(quads[2][0][0]+length/8,quads[2][1][1]-length/8)#a little hacky drawing all my n's the same way but it will work
    turd.down()
    turd.right(90)
    turd.forward(length/4)
    turd = draw_n(turd, length/4)

    turd.left(90)
    turd.forward(length/4)
    turd.left(90)
    turd = draw_n(turd, length/4)


    turd.forward(length/4)
    turd.up()
    turd.goto(quads[3][1][0]-length/8,quads[3][0][1]+length/8)
    turd.down()
    turd.right(90)
    turd = draw_n(turd, length/4)

def draw_lowest_order(turd: turtle.Turtle, length, turn1,turn2):
    #for the rotated quads feed in the x and y's backwards
    #for those cases x0 should be highest abs and y0 should be lowest abs and 

    turd.forward(length)
    turn1(90)
    turd.forward(length)
    turn1(90)
    turd.forward(length)
    turn2(90)

    turd.forward(length*2)
    turn2(90)
    turd.forward(length)
    turn2(90)
    turd.forward(length)
    turn1(90)

    turd.forward(length)
    turn1(90)
    turd.forward(length)
    turn2(90)
    turd.forward(length)
    turn2(90)

    turd.forward(length*2)
    turn2(90)
    turd.forward(length)
    turn1(90)
    turd.forward(length)
    turn1(90)
    turd.forward(length)
    


    return turd
    #when putting everything together note the outer x edge is always the one to connect

def hilbert_base(length,quad):
    sub_quads=make_quadrants(quad)
    for quad in sub_quads:
        draw_n(length/4, quad)

def draw_lowest_order_v2(turd: turtle.Turtle, length, turn1,turn2):
    #for the rotated quads feed in the x and y's backwards
    #for those cases x0 should be highest abs and y0 should be lowest abs and 

    turd.forward(length)
    turn1(90)
    turd.forward(length)
    turn1(90)
    turd.forward(length)
    #turn2(90)
    return turd

def hilbert_curve_hlpr(turd:turtle.Turtle,order,quad,length,turn1=None, turn2=None):
    """
    break down the curve into subproblems of order 1 hilbert curves and construct
    order is expected to be 1 at min
    I want to memoize subproblems and paste somthing the turtle has already made but i dont think its possible
    """

    """
    Working order 2
    draw_lowest_order(turd,500/8, turd.right, turd.left)
    turd.forward(500/8)
    turd.right(90)
    draw_lowest_order(turd,500/8, turd.left, turd.right)
    turd.forward(500/8)
    draw_lowest_order(turd,500/8, turd.left, turd.right)
    turd.right(90)
    turd.forward(500/8)
    draw_lowest_order(turd,500/8, turd.right, turd.left)
    

    note bot quads or the first and last use right,left while top use left,right
    i need to refactor to use u as base...
    """

    if turn1==None:
        turn1=turd.left
        turn2=turd.right

    
    #start should be in quad 3

    if order <2:
        #R,l,f,L,r,f,r,L,f,l,R; or...
        #L,r,f,R,l,f,l,R,f,r,L; Note after every n the opp. turn time is done to make an l
        #if i did this again i would try starting at the midpoint and having 2 turds mirror each other

        #turd.up()
        #turd.goto(new_quad[2][0][0]+length/8, new_quad[2][0][1]+length/8)
        #turd.down()
        #print(length)

        draw_lowest_order_v2(turd,length, turn2, turn1)
        
        #as you can see the calls mirror 

    elif order%2==0:
        quads = make_quadrants(quad)
        
        hilbert_curve_hlpr(turd,order-1,quads[2],length,turn2,turn1)
        turn2(90)
        turd.forward(length)
        
        hilbert_curve_hlpr(turd,order-1,quads[1],length,turn1,turn2)
        turn1(90)

        turd.forward(length)

        turn1(90)
        hilbert_curve_hlpr(turd,order-1,quads[0],length,turn1,turn2)
        
        turd.forward(length)
        turn2(90)
        #turd.right(180)#honestly have no idea why I need to do this I just adjusted to fix what I saw
        
        hilbert_curve_hlpr(turd,order-1,[quads[3][1],quads[3][0]],length,turn2,turn1)#note for all quads but the last the starting index refrenced the lowest x/y pair. for the 4th quadrant we need to use the highest
    else:
        quads = make_quadrants(quad)
        
        hilbert_curve_hlpr(turd,order-1,quads[2],length,turn2,turn1)
        turd.forward(length)
        turn2(90)

        hilbert_curve_hlpr(turd,order-1,quads[1],length, turn1,turn2)
        

        turd.forward(length)

        hilbert_curve_hlpr(turd,order-1,quads[0],length, turn1,turn2)
        
        
        
        #turn2(90)
        #turd.right(180)#honestly have no idea why I need to do this I just adjusted to fix what I saw
        turn2(90)
        turd.forward(length)
        hilbert_curve_hlpr(turd,order-1,[quads[3][1],quads[3][0]],length, turn2,turn1)#note for all quads but the last the starting index refrenced the lowest x/y pair. for the 4th quadrant we need to use the highest
                


def hilbert(order):
    turd = turtle.Turtle()
    win = turtle.Screen()
    ##quad 3 and 4 need to rotate outwards(quad4: counter, quad3:clock)
    #can be done with setting x==y and y==x 
    #how do I want to sort the points?
    #I think in order of lowest x would be easiest to follow

    quad1= [[0,0],[250,250]]
    quad2=[[-250,0],[0,250]]
    quad3=[[-250,-250],[0,0]]
    quad4=[[0,-250],[250,0]]
    quads=[quad1,quad2,quad3,quad4]

    #constructing outer square
    turd.up()
    turd.goto(-250,-250)
    turd.down()
    turd.goto(-250, 250)
    turd.goto(250,250)
    turd.goto(250,-250)
    turd.goto(-250,-250)
    

    #turd.hideturtle()
    turd.speed(0)
    turd.up()
    turd.goto(quad3[0][0]+250/(2**order),quad3[0][1]+250/(2**order))
    turd.down()
    
    if order%2==1:
        turd.left(90)

    length = 500/(2**order)
    
    hilbert_curve_hlpr(turd, order, [[-250,-250],[250,250]],length)
    

"""
    #proof of concept
    draw_lowest_order(turd,500/8, turd.right, turd.left)
    turd.forward(500/8)
    turd.right(90)
    draw_lowest_order(turd,500/8, turd.left, turd.right)
    turd.forward(500/8)
    draw_lowest_order(turd,500/8, turd.left, turd.right)
    turd.right(90)
    turd.forward(500/8)
    draw_lowest_order(turd,500/8, turd.right, turd.left)
    #works! now i have to scale it...

    #draw_n_conductor([[-250,-250],[250,250]])
    #hilbert_curve_hlpr()
"""