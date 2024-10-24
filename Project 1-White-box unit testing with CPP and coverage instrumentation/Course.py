# Course.py
from Student import Student
#課程管理
class CoursePool:
    def __init__(self):
        self.table = {}     

    def assign(self,id,temp):     
        if id not in self.table:
            self.table[id] = temp
        return
class Course:
    def __init__(self, name,cc,id):
        self.name = name
        self.cc = cc #cc stand for course credits 
        self.id = id
        self.student = set()

    def canceltheclass(self,stu,pool):
        for k,v in stu.table.items():
            if self in v.registeredclass:
                v.registeredclass.remove(self)
                v.total_credit -=self.cc
        self.student.clear()
        del pool.table[str(self.id)]
        return


    