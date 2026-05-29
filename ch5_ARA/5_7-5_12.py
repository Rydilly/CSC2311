def bubble_sort(l):
    for i in range(len(l)-1,0,-1):#skipps ele 0 because it should be sorted if everything else is
        for j in range(i):
            if l[j]<l[j+1]:
                l[j], l[j+1]=l[j+1],l[j]
#they just noted simultaneous assignment and used a temp value in their example smh

#bubble sort has the the fastest runtime on lists that are 100% sorted because on its first pass it iterates through n elements unlike the other search algs.

def bubble_short(l):
    for i in range(len(l)-1,0,-1):
        exchanges=False
        for j in range(i):
            if l[j]>l[j+1]:#ascending this time
                exchanges=True
                l[j],l[j+1]=l[j+1],l[j]
        if not exchanges:
            break

#selection sort is bubble with 1 swap per outer loop

def selection_sort(l):
    for i in range(len(l)):
        max_ind = 0
        for j in range(len(l)-i):
            if l[j]>l[max_ind]:
                max_ind=j
            if max_ind!=len(l)-i-1:#when you reach the last element of the list you dont want to write max_ind to unallocated memory
                new_end=len(l)-i-1
                l[max_ind],l[new_end]=l[new_end],l[max_ind]
#I wonder if selection sort would lead to better results for our hybrid sort
#probably not because the sublists are going to be the avg case for random data

#shifts are 3 times quicker then swaps
def insertion_sort(l):
    for i in range(1,len(l)):
        cur_val=l[i]
        cur_pos=i

        while cur_pos>0 and l[cur_pos-1]>cur_val:
            l[cur_pos]=l[cur_pos-1]
            cur_pos-=1
        l[cur_pos]=cur_val#the lowest val still needs to get swapped at pos i. nvm I was wrong


#we should've tried shell sort to compare with binary for our hybrid

def gap_insertion_sort(l, start, gap):
    for i in range(start+gap, len(l),gap):
        cur_val=l[i]
        cur_pos=i#ex has >=gap below but I think this is a little easier to read
        while cur_pos>start and l[cur_pos-gap]>cur_val:#while the next left val is gt curval
            l[cur_pos]=l[cur_pos-gap]
            cur_pos-=gap
        l[cur_pos]=cur_val#set start or last ind thats gt

def shell_sort(l):
    sublist_count = len(l)//2
    while sublist_count>0:
        for start_ind in range(sublist_count):
            gap_insertion_sort(l,start_ind,sublist_count)
        print(f"at {sublist_count} sublist's, the list looks like... \n{l}\n")
        sublist_count//=2


#the text mentions mergesort is our first divide and conq approach... how is shell sort not divide and conq.
def merge_sort(l):
    print(f"SPLITTING, {l}")
    if len(l)>1:
        mid = len(l)//2
        left_half = l[:mid]
        right_half = l[mid:]

        merge_sort(left_half)#I honestly thought this made new lists without numpy views
        merge_sort(right_half)#update. It does.

        print(f"MERGING, {l}")
        i,j,k=0,0,0
        while i<len(left_half) and j<len(right_half):
            if left_half[i]<=right_half[j]:
                l[k]=left_half[i]
                i+=1
            else:
                l[k]=right_half[j]
                j+=1
            k+=1

        while i<len(left_half):
            l[k]=left_half[i]
            i+=1
            k+=1
        while j<len(right_half):
            l[k]=right_half[j]
            j+=1
            k+=1

    
def quicksort(l):
    quicksort_hlpr(l,0,len(l)-1)

def quicksort_hlpr(l, first, last):
    if first<last:
        split = partition(l,first,last)#why are we sorting the entire list before splitting?
        quicksort_hlpr(l,first,split-1)
        quicksort_hlpr(l,split+1,last)

def partition(l,first,last):
    pivot = l[first]
    left_ind = first+1#im guessing the +1 is for the privot being at ind0
    right_ind = last
    done = False

    while not done:#pushing ind to 2 vals that are on the wrong sides of the pivot then swaps them
        while left_ind<=right_ind and l[left_ind]<=pivot:
            left_ind+=1
        while left_ind<=right_ind and l[right_ind]>=pivot:
            right_ind-=1
        if right_ind<left_ind:
            done=True
        else:
            l[left_ind],l[right_ind]=(
                l[right_ind],
                l[left_ind]
            )
    l[first],l[right_ind]=l[right_ind],l[first]#yes, first is the pivot so it swaps at the mid

    print(l, first, last)
    return right_ind
