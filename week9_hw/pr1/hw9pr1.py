class FullHashMapError(Exception): pass

class TombStone:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class HashMap:
    def __init__(self, cap=101):
        self._buffer = [None] * cap
        self._cap = cap
        self._size = 0
        self._insertions = []

    def _findKey(self, k_ind, key):
        """Probe for key. Returns the index where search terminates:
        - matching slot if key exists
        - first None slot otherwise — a proof of absence, but only
          when tombstones are handled correctly (see Parts 2-4).
          In a table with naive deletions, a None slot is no longer
          a reliable witness.
        """
        for shift in range(self._cap):#looping through buffer starting at the hash index using linear search to find none or key. We dont replace tombstones because we want the data to stay in the order it was added in
            new_ind = (k_ind + shift) % self._cap
            slot = self._buffer[new_ind]
            if slot is None:
                return new_ind
            elif slot is TombStone():
                pass
            elif key == slot[0]:
                return new_ind
        raise FullHashMapError("HashMap is full")
    
    def delKey(self, key):
        key_ind = self._calc_ind(key)
        key_ind = self._findKey(key_ind, key)
        match self._buffer[key_ind]:
            case None:
                raise KeyError
            case TombStone():
                raise(KeyError())
            case _:
                self._size-=1
                self._buffer[key_ind] = TombStone()

    def _findSlotForInsert(self, k_ind, key):
        #we cant use the first found tombstone because the key may already exist somewhere
        ind_if_no_key = -1
        for shift in range(self._cap):
            new_ind = (k_ind + shift)%self._cap
            slot = self._buffer[new_ind]
            if slot is None:
                if ind_if_no_key<0:
                    return new_ind
                return ind_if_no_key
            elif slot is TombStone():
                if ind_if_no_key<0:
                    ind_if_no_key=new_ind
            elif slot[0]==key:
                return new_ind
        if ind_if_no_key<0:
            raise FullHashMapError("HashMap is full")
        return ind_if_no_key
    
    def _clean_insertions(self):
        out =[]
        #print(self._insertions)
        for i in self._insertions:
            #print(i)
            if self._buffer[i] is not TombStone():
                out.append(i)
        self._insertions=out

    def _calc_ind(self, key):
        return hash(key) % self._cap

    def add(self, key, val):
        key_ind = self._calc_ind(key)
        key_ind = self._findSlotForInsert(key_ind, key)
        slot = self._buffer[key_ind]

        
        if slot is None:
            self._size += 1
            self._insertions.append(key_ind)
            self._buffer[key_ind] = (key, val)
        elif slot is TombStone():#this is probably wrong now that clean_insertions exists
            self._size+=1
            self._buffer[key_ind] = (key, val)
            if key_ind not in self._insertions:#this is stupid now because in uses iter so it will never be False
                #insertion already exists at this Tombstone 
                #if cant find the tombstone in insertions
                self._insertions.append(key_ind)
        else:
            self._buffer[key_ind]=(key,val)

    def __setitem__(self, key, val):
        self.add(key, val)

    def getVal(self, key):
        key_ind = self._calc_ind(key)
        key_ind = self._findKey(key_ind, key)
        if self._buffer[key_ind] is None:
            raise KeyError(f"{key} is not in the HashMap")
        return self._buffer[key_ind][1]

    def __getitem__(self, key):
        return self.getVal(key)

    def __len__(self):
        return self._size

    def __iter__(self):
        self._clean_insertions()
        for i in self._insertions:
            yield self._buffer[i][0]

    def hasKey(self, key):
        key_ind = self._calc_ind(key)
        key_ind = self._findKey(key_ind, key)
        return self._buffer[key_ind] is not None

    def __repr__(self):
        self._clean_insertions()
        tmp = [self._buffer[i] for i in self._insertions]
        sl = [f"{stringy(key)}: {stringy(val)}" for key, val in tmp]
        s = ', '.join(sl)
        return f"{{{s}}}"


def stringy(obj):
    if isinstance(obj, str):
        return f"'{obj}'"
    return obj

class RileyError(Exception):
    pass

def main():
    pass

if __name__=="__main__":
    hm = HashMap(11)
    hm["listen"] = 1
    hm["silent"] = 2
    hm["enlist"] = 3

    hm.delKey("listen")
    #print(hm["silent"])        # should work now
    #print(hm["enlist"])        # should work now
    #print(hm.hasKey("listen")) # should be False


    hm = HashMap(7)
    for i in range(6):
        hm[f"key{i}"] = i
    for i in range(6):
        hm.delKey(f"key{i}")
    print(hm._buffer)
    hm["new_key"] = 99   # what happens?
    print(hm["new_key"])
    #[(0, t), (1, t), (2, t), none, (4, t), (5, t), (6,t)]
    print(hm._calc_ind("new_key"))#new_key hash index is 2(can change)
    #[(0, t), (1, t), (2, t), ('new_key', 99), (4, t), (5, t), (6,t)]
    print(hm._buffer)

    h = HashMap(11)
    h["a"]=1
    h["b"]=2
    h["c"]=3
    
    h.delKey("b")
    print(h.hasKey("b"))
    print(h["a"])
    print(h["c"])
    print(h)

    for i in range(30):
        h[f"x{i}"]=i
        h.delKey(f"x{i}")

    h["d"]=4
    print(h["d"])
    print(len(h))
    print(h)
    

"""
Part 1:
I get a notImplemented air on add because I need to define _findSlotForInsert

1)The function acted as expected listen returned 1, silent 2, enlist 3, after del silent i got a key error trying to return. 
Everything worked fine. I'm guessing I was supposed to get a problem because I used none rather then a tombstone and if all 3 vals hashed to the say index find would stop before finding enlist becasuse the 2nd "local index" would be a none indicating the linear implementation has reached its end when in reality enlist is in the next slot.

2)Because with a linear search it terminates once it reaches a slot that indicates no more values are after it. I just realized when the program reaches higher capacity percentages there is an increased likelyhood that the end of one index reaches the beginning of a different one forcing search to look through 2 hash indexes instead of just 1. 
Could probably fix for the most part using robinhood hashing but you probably wanted to keep thing as simple as possible.

3)It fails when lookup is searchng for a value expected to be at that hash index but is after any deletion (assuming a new value hasnt been added). If after every deletion a new value is added to the hash index deletion occured the implementation would work as expected because every gap would be filled.

Part 2:
1) findkey goes to the next slot when it finds a tombstone because tombstone()!=key or None

2) I think it would perform normaly because the condition does nothing. if anything it might be a little more correct if you dont want to allow the retreval of the nearest tombstone which seems like a negative feature to me because to save space you would probably want to fill tombstones before nones.
It would make findkey a little slower too just because findkey will need to do an unessesary check.
The invariant lies in the termination condition because we will check every val from the hash ind until we run into the key or a none in both cases.

3)[0,1,2,3,4,5,6]-del(4)->[0,1,2,3,t,5,6]-add 5->[0,1,2,3,5,5,6] never finds the 5 key so we get duplicates
[0,1,2,3,4,5,6]-del(4)->[0,1,2,3,t,5,6]-hasKey(300)->True (tombstone is not none)
add should work fine though.

4) The problem is space. when we delete an entry the tombstone is taking up space that we never get back. We need a function that compresses after a certain number of tombstones are at a particualer hash index or else we may run into the problem of having a full hash table with only tombstones and no real values.
find key 5: [1,2,(3),4]->[1,2,3,(4)]->[(1),2,3,4]->[1,(2),3,4]. has itered its cap raise(fullhasherror)


Part 3)
1) The tombstone problem occures when t:number of total tombstones + s: the number of slots that hold a value = c: the hash's capacity.
When key is not an existing key and the number of None's ==0.

2)My map behaves like our current hash except when len(self.insertions==self.cap) we remove all the tombstones. We dont need to worry about local index hashes because the hash index is mod cap meaning a key can be hashed to any index.
[n,n,n,n,n,n,n]->[n,n,n,(3,3),n,n,n]->[n,n,(2,2),(3,3),n,n,n]->[n,(1,1),(2,2),(3,3),n,n,n]->[(0,0)(1,1),(2,2),(3,3),n,n,n]->[(0,0)(1,1),(2,2),(3,3),(4,4),n,n,n]->[(0,0)(1,1),(2,2),(3,3),(4,4),(5,5),n,n]->[(0,0)(1,1),(2,t),(3,3),(4,4),(5,5),n]->[(0,0)(1,1),(2,t),(3,3),(4,4),(5,t),n]->[(0,0)(1,1),(2,t),(3,3),(4,4),(5,t),(6,6)]-buffer is full time to remove tombstones>[(0,0)(1,1),(2,t),(3,3),(4,4),n,(6,6)]

3) In the case our hash is full of values and then we start deleting. the has would have no none values and you search for a key not inside the buffer you will loop around the entire buffer before the for loop ends and you would get a fullhashmap error rather then a false which could be tweaked but the has search and add time compexity becomes O(n).

4)This is a more robust solution because it has a solution to all edge cases besides there is no more space on the system. rehashing costs a fraction of initial hashing because most keys should already be in the right place unless you are over doubling the cap. but sill some vals wont move index although everything gets concat. You would end up doing an O(n) because when you fill in the new buffer every element needs its hash reevaluated when you rehash from element 0 to n ignoring the tombstones the shifting and index transfer logic is done automaticly so relocated values carry the same weight as values that keep their index.


LAZY vs EAGER:
1) Every case of del would increase by O(n) the actual time increment is whatever the size of insertions is at that given time, because you need to loop through increments until you find the key you deleted. worst case insertions len(increments) is n. delKeys is O(n) right now so O(n)+O(n)=O(n).
2)del key is O(n) because the hash func it call is O(1) the search function it calls is O(n) and the match case inside of it is O(1). we dont preserve any asymtotic complexity only the constant decreases. 
3)If delete is only being called once it should preform quicker then clean_insertions because it is able to stop once it finds the one tombstone index it contains. Its also saving total computation another way which is when it needs to search through its list even when there are no tombstone when iter is called cleaninsertions is always triggered. 
The last trade off is stability. As I've already hinted at prior when cleaninsertions is lazy it has to compute more but less frequently. This means you are trading stability for reduced computations.
4)amortized evaluation


4D)
1) buffers invariants are its size and its hash indexs because those values only change when you resize and our hash does not have that feature. When the hash is initilaized the space is prealloced and static. Every cell satisfies the condition of it containing a none, (idx,TombStone) or, (idx,val). 
2) At all times insertions will contain the indexes to every key and sometimes also contain the index to a tombstone. the live values are the stronger invariants while the tombstones are weaker because they are wiped every time cleaninsertions is called.
insertions must only cointain live items when it is iterated through because computation will be wasted on checking if self.buffer[insertion[i]] is a real pair or tombstone. the same applies when getting a string of live indexes. If the string returned could also contain tombstones the string of live key indexs would get muddied up by tombstones yet to be cleared.
insertions do not need to be cleared when adding because it does not provide utility to every case in add. If the key already exists or is none insertions does'nt need to loop through all of its elements. every none satisfies the condition insertion.append(index), every existing key satisfies the condition to leave insertion unchanged, on the condition the index we are using is a tombstone there are 2 possibilities.
Possibility A the tombstone still exists in insertions in which case we do nothing to insertions. Possibility B tombstones does not exist in insertions and insertions needs to append it. This is where I think this code is flawed. It would be much more efficient if our hash held a bool metadata signifiying insertions have been wiped which swaps to false when delete is done helping the program know if the current wipe is redundant.
3)
Invariants: (b)uffer- having the cap number of slots, having no duplicate keys , each slot must contain a none, (key,val,) or (ind,tombstone) (s)ize-value being an invariant through out the lifetime of the hash map, (i-)weak insertions- live i+, and the possibility of tombstones in insertions (i+)strong insertions-live key,value indexs in insertions, 
at all times add relies on _calc_ind, findslotsforinserts, tombstone to be defined. at all times add relies on b,s,i- and maintains i+(iter)
at all times delKey relies on calc_ind, tombstone, and find_key being defined and being an invariant. at all times delkey relies on b,s,i-
at all times getVal relise on calc ind and find key to be defined and being an invariant. at all times getval relies on b
at all times hasKey relies on calc ind and findkey bing defined and also an invariant. at all times b
at all times iter relies on clean_insertions being defined. at all times iter relies on b,i- and maintains i+
at all times repr relies on clean_insertions, and tombstone being defined. at all times repr relies on b,i- and maintains i+

"""