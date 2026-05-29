
import java.util.ArrayList;


public class hw9pr4 {
    public sealed interface Order permits Lt, Gt, Eq{
    
    }
    public record Lt() implements Order {}
    public record Gt() implements Order{}
    public record Eq() implements Order{}

    public interface Ordering<T>{
        Order compare(T a, T b);
    }
    
    public static class Student{
        public final String name;
        public final Double gpa;
        public Student(String name, double gpa){
            this.name = name;
            this.gpa = gpa;
        }
    }

    public static class ByGpa implements Ordering<Student>{
        
        @Override
        public Order compare(Student a, Student b){
            double result = a.gpa-b.gpa;
            if (result<0){
                return new Lt();
            }
            if (result>0){
                return new Gt();
            }
            return new Eq();
        }
    }
    public static class ByName implements Ordering<Student>{
        public Order compare(Student a, Student b){
            int diff = a.name.compareTo(b.name);
         
            if (diff<0){
                return new Lt();
            }
            if (diff>0){
                return new Gt();
            }
            return new Eq();
        }
    }

    public static <T> void insertionSort(T[] arr, Ordering<T> ord){
        int len = arr.length;
        for (int i=0; i<len; i++){
            int temp_ind = i;
            for(int j=temp_ind-1;j>-1;j--){
                Order cmp = ord.compare(arr[temp_ind], arr[j]);
                switch (cmp) {
                    case Gt():
                        T temp_val = arr[j];
                        arr[j] = arr[temp_ind];
                        arr[temp_ind] = temp_val;
                        temp_ind--;
                    default:
                        break;
                }
            }
        }
    }

    public static void main(String[] args){
        Student[] students = new Student[10];
        students[0] = new Student("bob", 3);
        students[1] = new Student("billy", 5);
        students[2] = new Student("Joe", 1);
        students[3] = new Student("Riley", 3);
        students[4] = new Student("Frank", 1);
        students[5] = new Student("Diana", 4);
        students[6] = new Student("zoe", 3);
        students[7] = new Student("Alex", 2);
        students[8] = new Student("Mary", 1);
        students[9] = new Student("Alice", 6);

        insertionSort(students, new ByName());
        System.out.println("\nSORTED BY NAME:");
        for(int i=0; i<10;i++){
            System.out.println("GPA:" + students[i].gpa +"  Name:"+ students[i].name);
        }
        System.out.println("\nSORTED BY GPA");
        insertionSort(students, new ByGpa());
        for(int i=0; i<10;i++){
            System.out.println("GPA:" + students[i].gpa +"  Name:"+ students[i].name);
        }
        
    }
}
//*
// REFLECTION:
// It allows for multiple orderings.
// Inside a singular function that dos'nt filter dtypes or argument types to different operations like in this model.
//              Where Ordering Lives    |   Flexibility               |   Type Safety
// Python               __gt__         low- extensible and configurable,    high, type hinting helps and if you feed 
//                                    wrong data and get attribute error    
//                               It will get messy quick with its limited encapsulation
//                                              High
// C                 Comparitor Func extensible args/comparison funcs, reusable,                 
//                                        configurable, composable
//                                          passing ptrs and          Low, any ptr could enter the func and you may still 
//                                          returning ints              run incorrectly
// 
//                                             medium/low
//Gleam              is_less            reusable, config, composable      medium- Is type specific but you could sort all 
//                                                                      ints with the same method even if they are to be compared differently.  
// Java              Ordering.compare       med/High-extensible,        
//                                         configurable, composable     High, like py only the object is passed dynamic dispatch handles the rest       
//                                             substitution
//
//4)Eq results must not swap if the middle loop is iterating from the middle of the array or list to an end. If your middle loop is going from the end to the middle they must swap.
//   */