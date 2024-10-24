class StudentPool:
    def __init__(self):
        self.table = {}     
    def assign(self,id,temp):
        if id not in self.table:
            self.table[id] = temp
        return

class Student:
    MAXNUM = 20  # Assuming MAXNUM is defined as a constant

    def __init__(self, name, id):
        self.name = name
        self.number = id
        self.total_credit = 0
        self.registeredclass = set()
    

    def register_class(self,course,pool):
        if course not in pool.table.values():
            print('the class is invalid')
            return 
        if course in self.registeredclass:
            print("You have already registered the class.")
            return 
        if self.total_credit + course.cc > self.MAXNUM:
            print("You have exceeded the maximum number of courses!")
            return 

        self.registeredclass.add(course)
        self.total_credit += course.cc
        course.student.add(self)
        
        return 
    
    
    def drop_class(self,course):
        if course not in self.registeredclass:
            print('you did not register this class before'  )
            return
        else:
            course.student.remove(self)
            self.registeredclass.remove(course)
            self.total_credit -= course.cc
            return

    
