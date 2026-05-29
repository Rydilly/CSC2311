import time
import numpy as np
#import math
import matplotlib.pyplot as plt

def insertion_sort(L:list)->list:
    for i in range(1,len(L)):
        cur_pos = i
        cur_val = L[i]
        while cur_val<L[cur_pos-1] and cur_pos > 0:
            L[cur_pos] = L[cur_pos-1]
            cur_pos-=1
        L[cur_pos] = cur_val
    return L

def np_insertion_sort_naive(L: np.ndarray)->np.ndarray:
    for i in range(1,len(L)):
        cur_pos = i
        cur_val = L[i]
        while cur_val<L[cur_pos-1] and cur_pos > 0:
            L[cur_pos]=L[cur_pos-1]
            cur_pos-=1
        L[cur_pos] = cur_val
    return L

def np_insertion_sort_fast(L: np.ndarray)->np.ndarray:
    for i in range(1,len(L)):
        cur_val = L[i]
        insert_ind = find_insert_pos(L, cur_val, i)
        L[insert_ind+1:i+1]=L[insert_ind:i]
        L[insert_ind] = cur_val
        #print(L)
    return L
#No iterations are being replaced it only seems that way because we added a layer of indirection. we still have an inner loop checking for the index the vectorized shift will occur at. 
#The final state of the array is identical because the logic is identical the only difference is in this version we are lazily waiting to preform the shift until we know all the values that need shifting per outer iteration.
    

def find_insert_pos(L, val, k)->int:  #not sure why we want left of. wouldn't this make an unstable sorting alg?
    start = 0
    while start<k:
        #print(L[start:k])
        mid = (k+start)//2
        if L[mid]<val:
            start= mid+1
            #print(k)
        else:
            k = mid
    #print (start)
    return start
"""
Part5: the inner loop is the slice assignment. We should be able to get rid of it and just call find_insert_pos in our new version.
"""



def benchmark():
    sizes = [10, 125, 250, 500, 1000, 2000, 4000, 8000]
    n_trials = 5
    list_times =[]
    naive_np_times = []
    fast_np_times = []

    for n in sizes:
        base_list = list(np.random.randint(0,n*10,size=n))
        base_np = np.array(base_list)
        fast_np = np.array(base_list)
        times_plain, times_np, times_np_fast = [], [], []
        

        for _ in range(n_trials):
            t0 = time.perf_counter()
            insertion_sort(base_list.copy())
            times_plain.append(time.perf_counter()-t0)

            t0 = time.perf_counter()
            np_insertion_sort_naive(base_np.copy())
            times_np.append(time.perf_counter()-t0)

            t0 = time.perf_counter()
            np_insertion_sort_fast(fast_np.copy())
            times_np_fast.append(time.perf_counter()-t0)

        list_times.append(1000*((sum(times_plain)/n_trials)))
        naive_np_times.append(1000*((sum(times_np)/n_trials)))
        fast_np_times.append(1000*((sum(times_np_fast)/n_trials)))
        #print(fast_np_times)

        print("At Size ", n, "...\nPython Lists Avg:        ", f"{1000*(sum(times_plain)/n_trials)}ms", "\nNaive NP Arrays Avg:     ", f"{1000*(np.average(times_np)/n_trials)}ms" "\nFast NP Arrays Averaged: ", f"{(1000*np.average(times_np_fast))}ms")
    print(fast_np_times)
    plt.plot(sizes, list_times, marker='o', label = "Python lists")
    plt.plot(sizes, naive_np_times, marker = "s", label = "Naive NP")
    plt.plot(sizes, fast_np_times, marker = "+", label = "Fast NP")
    plt.title("Py_List:o, Naive_NP:s, Fast_NP:+")
    plt.xscale('log')
    plt.show()


if __name__ == "__main__":
    A = np.array([1, 3, 5, 7, 9, 0, 0, 0])  # sorted front of length 5
    assert find_insert_pos(A, 0, 5) == 0
    assert find_insert_pos(A, 4, 5) == 2
    assert find_insert_pos(A, 9, 5) == 4
    assert find_insert_pos(A, 10, 5) == 5
    print("All tests passed.") 

"""
PART 1:
Yes, if the only operation being accounted for is insertion sort then numpy will always be faster. 
At some point you will probably want to extract the data and when you do you need to convert to a python type. Unwrapping is the main downside of using np arrays.
In insertion sort only 2 points are being operated on at any given point, leading me to believe that the main operating cost comes from copying the lists.
When testing if the performance changed if I moved the copy operation outside the test my results barely change so there must be some optimization happening in the operation.
since only 2 elements have an operation applied at any given point my guess is that cache locality is the main driver of np's performance boost, arrays vs lists.
"""
"""
Part 2:
Insertion sort is the process of growing a (L)ist/array starting at 1 by adding 1 element from a (U)nsorted list/array. Its common practice to have L and U share 1 contiguious section of memory with L taking slots from U as it grows.   
For every (e)lement added, e gets compared with every element in L starting at the right end of L and when it is less then L[i], L[i] e and U[0]= L[i], U[0] = U[1]. Or to simplify things you Could use L with 2 seperate indexes but the same thing is happening under the hood.
L[i] and everything to the right of it must be shifted to fit e. the process continues until every e in U has been evaluated in L.

The sorted front refers to L where L and U are 2 seperate pointers in 1 contiguious block of memory marking where L and u is currently at. L is index 0 and u is wherever the sorted fron ends to the end of the array.

The logical operations in the outer loop of your insertion sorts are: an element swap, an increment for i, a comparison if i>len(L) a variable assignment for i, a variable assignment for L[i]

In the naive implementation the index is used to swap every element with its prior value so long as the prior value is < current val. current index is also being used to compare current val with L[current index] for the < check. current index is also being used to check if the beginning of L has been reached which is annother terminating condition. after 1 itteration i is reduced by 1. After the inner loop is complete i is reassigned to what it was last time it was in the outer loop +1 and current val is the next element to the right.
"""

"""
Part 3:
a) NP array shifts are faster because the shifts are more eager meaning rather then shifing 1 element at a time 100 times we would be shifing 100 elements 1 time with the power of vectorization. I would guess under the hood it is applying an index assignment to a shift of the pointer. ptr[x+2*sizeof(it) from i to j] for all element i to j. Its a little magic that multiple operations can happen at the same time and you wont run into the issue one slot has already been written befor it has been read. It looks like from what I see online it will grap a hunk of 32 or 64 bytes and move them all at the same time. To avoid the issue I stated I would assume it just needs to make sure the side it starts its copy from is the side closer to the to location.
Also a big benefit is that it dosnt try to evaluate the slots or understand what its really doing i just grabs a hunk of bytes and moves them to.a new address.

b) From the way you put it yes. From what I just stated in a no. If the elements all truly moved at the same time it would be O(1) but thats not how memmove works. memmove usually moves 64 or 32 bits at a time meaning its linear with a much lower constant.

c)The naive logic structure is more eager. It moves every element when it knows the element should be in a shifted position rather then applying 1 shift to several elements at the same time in unison when it is know which elements need to shift.

d)I would argue it is still insertion sort because the same operations are being applied the only difference is the conservation of computation using lazy evaluation. the same comparison logic is being applied the same shifting operations are still being applied. The only difference is when we shift which will probably be in the outer loop all at the same time.
"""
"""
Part 4:
Prediction: I think there will be a noticable speedup over huge lists but small lists will actually slow down because cache misses will overshadow the difference in comparisons. Over massive lists/arrays there will be a huge improvement becasue for a list of 10000, 130,000 is way smaller then 100,000,000. Even if every individual operation is more expesive for binary, binary will eventually win.
"""

"""
Part 7:
a)Yes, I was right. at high values of size fast_np outperforms naive and at lower sizes naive outperforms fast because of cache locality and issues relating to binary search. py outperforms both at low values because of unboxing overhead.

b)I would say its a clear winner at 10^3rd elements. there is a crossover because the functions scale differently. The only thing asymtotic time complexity shows is how data scales with size(per element overhead) it dos'nt share any information on the constant being applied to it.

c)
a. partially correct, the algorithm is still insertion sort. for it to be a different algorithm the abstract approach of sorting data would have to change. I could see an argument for it being closer to bubble sort then insertion because the same operations for bubble sort are applied in the naive version just in a different order... the insertion order.
b. wrong, the same np array is being fed as an argument in both cases.
c. correct, in the naive version the shifing work is applied eagerly leading to increased time. I dont think at any size this approach is faster so I would swap it out and add a conditional to apply linear or binary based on the size.
"""

"""
Part 8:
Versions       search cost          shift cost         Total Complexity
insertion       O(k)                    O(k)               O(k)
np_naive        O(k)                    O(k)               O(k)
np_fast         log(k)                  O(k)               O(k)

a) The outer loop needing to iterate n times. I saw a video of someone benchmarking different function and perf report seemed like a pretty powerful tool for this but Im not running linux.
The difference of 4000 to 8000 was 7 to 18 we know some part scaled linear and some part scaled logrimicaly so we could fit a function 
our func is still increasing at a decent rate at extreme values meaning its still getting impacted by somthing with a constant or higher aymtotic complexity.

b)Its because the alg isnt truely Nlogn its n^2logn. we are treating the shift cost O(1) because its tiny but its still scaling constantly

c)because after decoupling the search area of our alg changes from O(n) to O(logn)

d)You could increase your cache so you could vectorize more elements in 1 shift operation. You could also compress the data to repeated numbers only show up once. 
You could also reduce the bit size of your elements if you know you dont need to use the entire 4 byte space. Theres probably other improvements you can make by making other assumtipins about the data your dealing with.

e) Yes because this would change one N coefficient. The formula A*N+B*LogN would become C*N * B*LogN or for naive A*N * B*N to C*N * B*N. If C<A the difference in functions still changes by a multiple and not a constant
"""
"""
They do the same amount of swaps. the numpy swap operation is faster because numpy views the data as contiguious bytes while python views the data as python byte code but the c overhead evens out the cost. 
The binary search is an improvement but if that improvement is cold on the heatmap its going to make a small difference in overall performance. doubling the speed of walking to your car when you have to commute 8 hours isnt a noticalbe difference.
The cost of swapping back and forth between python and c has a pretty heavy usually order n
"""
"""
Asytotic time complexity is only part of the entire picture. When you decide what alg to use for a given problem you need to make assumtions of what kind of data and how much will travel through it. If your implementation will rarely be used and take in low ammounts of data you probably have better things to optimize.
If the thing your working on is a bottleneck you should look at your entire codebase for times the data is converted to different types or filtered to see if the data at that point is more effective for what you want to do so you dont need to pay the cost of converting data.
Vectorization is extremely useful for big data but it can be costly for multiple instances of small data. Gpu computing probably follows the same suit because to my understanding its like a 2nd cpu that is very good at vectoring. when storing your data say in a sql query its also important to make assumptions of how the data may be used.
A good example that isnt directly related to this assignment has to do with hashing strings. You can speed up performance of the hashing functions if you reduce the strings to their first and last 2 chars because the function needs to iterate through every char. the same logic can be applies to python types and nparrays being stored.
"""

"""
Its not faster at all values fast has a better asymptotic complexity so its is better the eventually as input grows but you can make assumptions about data to actually know what will be the fastest.
Numpy supports vectorization which is a game changer when it comes to operating on large contiguous data but falls short when data is small and type conversion cost more then the benefits of vectorization.
"""
