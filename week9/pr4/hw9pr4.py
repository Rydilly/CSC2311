import random as r


class Student:
    def __init__(self, name:str, gpa:float):
        self.name = name
        self.gpa = gpa

    def __gt__(self, other: "Student")->bool:
        #print(self.gpa,">" ,other.gpa)
        #print(self.gpa>other.gpa)
        return self.gpa > other.gpa
    
    
def gpa_sort(students):
    for i in range(len(students)):
        tmp_i = i
        #print(students[i].gpa, "cmp")
        for j in range(tmp_i-1,-1,-1):
            
            #print(students[j],">",students[tmp_i])
            if students[tmp_i]>students[j]:
                students[tmp_i], students[j] = students[j], students[tmp_i]
                tmp_i-=1
            else:
                #print(students[j].gpa,">=")
                break
        #print(i,"inner loop end")
        #print(students[tmp_i].gpa)

def name_sort(students = list("Student"))->list("Student"):
    for i in range(len(students)):
        tmp_i=i
        for j in range(i-1,-1,-1):
            if students[tmp_i].name>students[j].name:
                students[tmp_i].name, students[j].name = students[j].name, students[tmp_i].name
                tmp_i-=1
            else:
                break

def sort_students(list_o_students: list("Student"))->list("Student"):
    pass

if __name__ == "__main__":
    size = 1000
    los = [Student(str(r.randint(10,500)),r.randint(0,100)) for _ in range(size)]#names will be strings of numbers to easily tell if instability is taking place 
    
    gpa_sort(los)
    print([los[x].gpa for x in range(len(los))])
    name_sort(los)
    print([los[x].name for x in range(len(los))])
    for s in range(len(los)-1):
        print(f"comparing names: {los[s].name} >= {los[s+1].name} and gpa's: {los[s].gpa} >= {los[s+1].gpa}")
        assert los[s].gpa >= los[s+1].gpa#these cmp should work bc they are accessing py types in the class
        if los[s].gpa == los[s+1].gpa:
            assert los[s].name >= los[s+1].name
    print("sort is stable!")
    
"""
Yes, I am able to sort by name and gpa it was a little dirty accessing the object data outside the class but all the object data is public. The ordering logic of gpa is in the Student class while the ordering of name is in the string type/class. This design does support multiple orderings.

The ordering logic of the c design lives in a directly declared function that evaluates the difference of 2 values. Comparator uses a void pointer so the comparison is of x bytes, this means that every data type is can be compared with one another because bytes are the base data type. 
I dont think the compiler can check what type is coming in so if you send in a double and the function is expecting an int the comparison will ignore the second half of the bytes of each double. or even undefined behavior if the incoming bytes are shorter then what is expected so it reads past the byte into unrelated memory blocks.


"""