def sequential_search(list, item):
    pos=0
    while pos<len(list):
        if list[pos]==item:
            return True
        pos+=1
    return False

def binary_search(list,item):
    first=0
    last = len(list)-1

    while first<last:
        midpoint=(first+last)//2
        if list[midpoint]==item:
            return True
        elif item<list[midpoint]:
            last=midpoint-1
        else:
            first=midpoint+1
    return False


#folding method involves compressing data to have a smaller defined possible input pool for the hash

#mid-square: square the item then extract part of the result like only the last 2 digits.

#for word based strings I would only hash the first and last 2 chars because they are almost as unique as the entire char ensamble
#but this method only involves 1 hashing so it might be more performant. I would like to benchmark and see the collision rate 


def hash_str(a_str, table_size):
    return sum([ord(c) for c in a_str])%table_size

#open addressing:trying to find a slot in a hash after a collision

#quadratic addressing: rehashing using a quadratic equation in effort to reduce collisions

#chaining: using buckets at each hash and the buckets are appended to then searched through linearly

class HashTable:
    def __init__(self):
        self.size=11
        self.slots=[None]*self.size
        self.data=[None]*self.size

    def hash_function(self, key, size):
        return key%size
    
    def rehash(self, old_hash, size):
        return(old_hash+1)%size
    
    def put(self, key, data):
        hash_value = self.hash_function(key, len(self.slots))

        if self.slots[hash_value] is None:
            self.slots[hash_value]=key
            self.data[hash_value]=data
        else:
            if self.slots[hash_value]==key:
                self.data[hash_value]=data
            else:
                next_slot=self.rehash(hash_value, len(self.slots))
                while(
                    self.slots[next_slot] is not None#I need to start doing this duel line arg format for whiles
                    and self.slots[next_slot]!=key
                ):
                    next_slot=self.rehash(next_slot,len(self.slots))#this never stops on the condition the hash is 100%full!

                if self.slots[next_slot] is None:
                    self.slots[next_slot] = key
                    self.data[next_slot]=data

                else:
                    self.data[next_slot]=data#if key already exists

    def get(self, key):
        start_slot = self.hash_function(key, len(self.slots))

        position = start_slot
        while self.slots[position]==key:
            if self.slots[position] is not None:
                return self.data[position]
            else:
                position==self.rehash(position, len(self.slots))
                if position==start_slot:
                    return None
                
    def __getitem__(self, key):
        return self.get(key)
    
    def __setitem__(self, key, value):
        self.put(key, value)
        
        
"""
avg number of comparisons = (1/2)(1+(1/(1-load_factor))#as the load factor approaches 1 the numb of cmp approaches inf

avg numb of cmp for seach of somthing not in hash = (1/2)(1+(1/(1-load_factor)^2). scales exponentially because clusters merge at higher loads leading to even longer runs before finding a none
"""


