import random as r
import time as time

def insertion_sort(data: list[int])->list[int]:
    newL =[]
    
    for val in data:
        newL.append(val)
        #print(newL)
        for i in range(len(newL)-1,0,-1):
            if val<newL[i-1]:
                t = newL[i-1]
                newL[i-1]=newL[i]
                newL[i]=t
            else:
                #print(val, newL[i-1])
                break
    return newL

def hybrid_sort(data: list[int])->list[int]:
    if len(data)<17:
        newL =[]
        for val in data:
            newL.append(val)
            #print(newL)
            for i in range(len(newL)-1,0,-1):
                if val<newL[i-1]:
                    t = newL[i-1]
                    newL[i-1]=newL[i]
                    newL[i]=t
                else:
                    #print(val, newL[i-1])
                    break
        return newL
    
    else:
        pivot = r.randint(0,len(data)-1)
        right, left, eq = [],[],[]
        for i in range(len(data)):
            if data[i]<data[pivot]:
                left.append(data[i])
            elif data[i]>data[pivot]:
                right.append(data[i])
            else:    
                eq.append(data[i])

        return hybrid_sort(left)+[data[pivot]]+hybrid_sort(right)

"""
1)insertion is preferred for smaller lists because it has a low constant then quick while being O(n^2) when quick is amortized O(NlogN) meaning it beats quick with small lists but looses when the size exceeds a certain point.
2)Random pivots almost guarantee worst case behavior dos'nt happen and you can assume the alg will preform O(NlogN) amortized. worst case behavior is an instance when your pivot is the max or min of the list making the next recursive call barely an improvement. If this case reoccurs quick sort no longer represents a O(nlogn) amortized algorithm and closer resembles O(N^2) with a higher constant compared to insertion sort. 
If pivot was set to data[0] on a sorted list the alg would preform O(n^2) because every left would be empty and when the next right is used the same instance with 1 less element would occur. This would lead to worse performance then using insertion on a random list. Its a little difficult to compare sorted list time complexity, because insertion sort on an already sorted list is supper quick because every element only goes through 1 check so the asymptotic complexity matches more like O(N) because the inner loop would be O(1). 
For the purpose of my point I would predict insertion sort being more performant on reverse order lists then binary on sorted. Im using these comparisons because they are the worst case for both.In both cases the inner loop is triggered the same amount of times but insertion has a much lower overhead and higher cache locality. Meaning you would be better off just using insertion sort if you wanted to minimize your worst case and only knew how to binary sort with a fixed first index.
Update: insert and quicksort_fixed share worst case condition of descending data so It would've been more simple to compare that.
3)My insertion sort is stable because in my for i in range(len(data)) loop I go through the list from left to right and build my left right and eq from left to right of my data. In the case an element == my pivot val... it will be added to the eq list. once the pivot == i the eq will get the pivot value appended. after, all the values == to pivot value will be added to eq after pivot.
When insertion is called it also sorts stably. Unlike the version you had us make in the previous assignment, This version does not swap if val == newL[i]. If it did you would have stability issues because all equal values would be returned in reverse order.
"""

def in_place_insertion(data):
    for i in range(len(data)):
        cmp = data[i]
        for j in range(i-1,-1,-1):
            #print(data, cmp,">",data[j])
            if cmp>data[j]:
                break
            t=data[j]
            data[j]=data[j+1]
            data[j+1]=t


def partition(data, low, high):
    #returns index of pivot
    pivot_ind = r.randint(low,high)
    data[high], data[pivot_ind], pivot_ind = data[pivot_ind], data[high], high
    pivot_val = data[pivot_ind]
    #print(pivot_val)
    j = low
    for i in range(low,high+1):
        if data[i]<pivot_val:
            #print(data[i],"<->", data[j])
            data[i], data[j] = data[j], data[i]
            j+=1
        #print(data)
    data[j], data[pivot_ind] = data[pivot_ind], data[j]
    #print(data)
    return j
            


def hybrid_sort_inplace(data: list[int], low=0, high=None)->None:
    if high == None:
        high = len(data)-1
    if high-low < 17:
        for i in range(low+1, high+1):
            cmp = data[i]
            for j in range(i-1,-1,-1):
                #print(data, cmp,">",data[j])
                if cmp>data[j]:
                    break
                t=data[j]
                data[j]=data[j+1]
                data[j+1]=t
        return

    else:
        pivot_ind = r.randint(low,high)
        data[high], data[pivot_ind], pivot_ind = data[pivot_ind], data[high], high
        pivot_val = data[pivot_ind]

        j = low
        for i in range(low,high+1):
            if data[i]<pivot_val:
                data[i], data[j] = data[j], data[i]
                j+=1
        data[j], data[pivot_ind] = data[pivot_ind], data[j]
        hybrid_sort_inplace(data,low, j-1)
        hybrid_sort_inplace(data, j+1, high)



def quicksort_fixed(data: list[int], low = 0, high = None)->None:
    if high == None:
        high = len(data)-1
    if high-low>0:
        split = fixed_partition(data, low, high)
        quicksort_fixed(data, low, split-1)
        quicksort_fixed(data, split+1, high)

def fixed_partition(data:list[int], low, high):
    pivot_val = data[low]
    pivot_ind = low
    low = low+1

    while low<high:
        while not low>high and not data[low]>pivot_val:
            low+=1
        while not low>high and not data[high]<pivot_val:
            high-=1
        if low<high:#when high < piv and low >.
            data[low], data[high]=data[high], data[low]#note if 
    data[pivot_ind], data[high] = data[high], data[pivot_ind]
    return high


        
def quicksort_random(data:list[int], low=0, high = None):
    if high==None:
        high=len(data)-1
    if high-low>0:
        pivot = partition(data, low, high)#my random alg using a for loop and goes through 1 end to the other so that my effect performance.
        quicksort_random(data, low, pivot-1)
        quicksort_random(data, pivot+1, high)
    
"""
ANALYSIS QUESTIONS:
1) quicksort fixed performs much worse on ascending and descending list because both types are its worst case. When the pivot can only be the first element in the list and the list is sorted the left or right depending how your sorting and how the data is sorted will be empty while the other will be k-1 with k being the current low to high indexes.
2) randomized makes worst case behavior extremely unlikely. for every iteration of the list (Log_2(n)) every randomly selected element must be the max or the min of the local selected group. the likelyhood of this happening raises as the local list decreases in size. The first chance is 2/n next is 2*2/(n/2) (assuming last pivot was the middle val) or 4/n then 8/n for log_(2)n times. the end case is when len(k)==0.
What im getting at is the worst case grows in likelyhood as the difference in computation decreases. For example a list at size 40 has a low likelyhood and picking the min would have a great impact because you would be forced to iterate through n-1 at the next depth, but the likelyhood of selecting the min or max twice is 2/n*2/n-1.In this case it changes from a probability of .05 to .0026 to .00013 at 3rd depth. Reaching full depth only hitting worst case calculates to aprox. 1.35*10^-36(divided by 2 I think I might've included n==1 which is impossible), so yes it is possible but highly improbable.  
When our k has shrank to say 5 the likelyhood has grown to .4 for that instance. This may seem like an issue but remember that k=5. This means worst case the list is still shrinking by 20% (5-4) where if the worst case for n would be a decrease of only 2.5%. This relationship fits perfectly with a amortized time relationship because as the likely of a worst case pivot grows that impact of that case decreases.
3)I wouldn't say insertion beats quicksort at any particular size but, I would say insertion always beats qucick when the data is almost already organized for any size. This is because if the next value is already in the correct order insertions inner loop breaks and moves to asses the next element. quicksort must reasses every element multiple times even if they are in the correct order from a previous iteration. this is where an algorithm like tim sort would really shine because it has the ability to section data that is or almost is already sorted.
4)At all sizes quicksort inplace was noticibly faster then construction with all sizes with descending data at 100 and 10000 the averaged differential was around a 40% decrease in performance. So the lesson here is if you have a hot spot sorting in your code you should use mutation if possible. I'm honestly surprised even at low values construction had a noticable disadvantage. I asked genai which explaned the disadvantage is due to concatenation/allocation which is O(n). applying what I already know this adds O(nlogn) operations because the concationation needs to occur logn times.  
With concationation being O(nlogn) + hybridsort being O(nlogn) makes our new alg O(logn) with a higher coefficient always pushing constructions time complexity a multiple higher then mutation. I would guess the coeficent difference of concationation in relation to mutation is about 1.6.
5)Insertion sort kills everything with sorted data at all sizes however it sturggles badly with other data imputs. These issues can be minimized with relatively minimal impact to sorted speed by implementing a hybrid. Hybrids goal is get the consistency of quicksort for all data types while utilizing insertions speed for small and sorted inputs.
6) a good hybrid alg is not about maximizing strengths, but about minimizing weaknesses/getting the fastest time with inconsistent inputs.
"""






if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(50000)#quicksort breaks with 10,000 vals worst case

    sizes = [100, 1000, 10000]
    iterations = 10
    functions = [insertion_sort, quicksort_fixed, quicksort_random, hybrid_sort, hybrid_sort_inplace]
    

    for s in sizes:
        inputs = [r.randint(-2**31,(2**31)-1) for _ in range(s)],[x for x in range(s)],[y for y in range(s-1,-1,-1)]
        #print(inputs)
        print("-------------------------------------------------")
        print(f"AT SIZE {s})")
        for f in range(len(functions)):   
            print("++++++++++++++") 
            print(f"    FOR FUNCTION {functions[f]}")    
            for dtype in range(3):
                results = []
                match dtype:
                    case 0: print("         With Random Data...")
                    case 1: print("         With Ascending Data...")
                    case 2: print("         With Descending Data..")

                for _ in range(iterations):
                    t0 = time.perf_counter()    
                    functions[f](inputs[dtype].copy())
                    results.append(time.perf_counter()-t0)
                print(f"            Averaged: {sum(results)*1000/iterations}(s)")
                
                    
                    






  
"""
1)Direct order is lost when an equal element gets swapped for one that is less then.
pivot = 4 for [4,10,4,3,8,1], eventually you will get to [3,4,10,4,8,1]. the next check is data[5]<pivot_val, True.
[3,1,10,4,8,4] as you can see the 4 that was once at ind 2 is now at ind 5 while the 4 at ind 3 is no longer to the right of the 4 at ind 5
2) The main benefit I see is reduced memory usage without a significant time difference. The space complexity changes from O(NLogN) to O(Logn) because before every iteration held a new list of size n with amortized logN iterations resulting in NlogN.
The inplace mutation is O(1) per instance across log(n) instances == O(LogN). I think the cache behavior is neglegable for most sizes because of the limitations of caches related to jumping indexs. I think our mutation verson will have an edge when all the data of our first version cant fit in the l1 but the mutation still can but that advantage should only be brief.
Actually scratch that I asked claude and most L1's hold at minimum 32kb. With the space complexity scaling at log2(N)=32000->N=2^32000 which == overflow, I asked claude what it would be and it said somthing just below 2^15 compared to something that grows a little faster then linear. I also know from making my cuckoo filter that the cost of cache needing to fetch data can cost around 100 cpu cycles. My final answer to what i predict performance will look like is farily equal on low sized lists with a huge difference in costs with large lists.
they should be fairly close until C*NlogN>(l1 cap). I have no idea what the constant would be because python usually carrys extra bloat with variables and im sure the same applies when storing instances of functions.
3)Depends on the application. I could see cases where you might need the data organized in a stable way but if its not necessary or you can find a cheaper work around like resorting small chuncks of data as its accessed while keeping strict space complexity on sotring the whole you could probably get a nice compromise. 
"""
   

            

