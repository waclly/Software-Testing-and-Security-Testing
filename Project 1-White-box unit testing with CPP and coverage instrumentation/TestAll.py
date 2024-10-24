# Test_Student.py
import unittest
from Student import *  # Import the Student class from student.py
from Course import * 
# py -3.11 -m coverage  run -m pytest TestAll.py
# py -3.11 -m coverage report -m

def student_test(student , course_set):
    #course 為 student目前該有且僅有的課程
    total = 0
    #應該有的課程卻沒有
    for i in course_set:
        if i not in student.registeredclass: return False
            
        total += i.cc
    #多課程
    if len(course_set) != len(student.registeredclass): return False
    #學分錯誤
    if total != student.total_credit: return False

    return True

def course_test(course , student_set , pool):
    #如上
    if course.id not in pool.table:   return True
    for i in student_set:
        if i not in course.student:  return False
    if len(course.student) != len(student_set):         return False

    
    return True
class AllTest(unittest.TestCase):
    
    #前處理 課程建立 人員建立
    def setUp(self):
        
        self.pool = CoursePool()
        self.stu = StudentPool()
        
        k = 0
        for i in ['CS','EE']:
            for j in range(1,5):
                temp = Course(i+str(j),3,str(k))
                self.pool.assign(str(k),temp)
                k +=1

        self.stu.assign('0001',Student("Wu", "0001"))
        self.stu.assign('0002',Student("Fu", "0002"))
        
    #後處理 garbage collection
    def tearDown(self):
        for k,v in self.stu.table.items():
            del v 
        self.stu.table.clear()
        del self.stu
        
        for k,v in self.pool.table.items():
            del v 
        self.pool.table.clear()
        del self.pool

    def test_student_pool_check(self):
        before = self.stu.table['0001']
        same_id_obj = Student("Liang", "0001")
        self.stu.assign('0001',same_id_obj)
        after = self.stu.table['0001']
        self.assertTrue((before.name) == after.name)
        
        # for k,v in self.stu.table.items():
        #     print(v.name)
    
    def test_course_pool_check(self):
        before = self.pool.table['0']
        same_id_obj = Course('MED1',3,'0')
        self.pool.assign('0',same_id_obj)
        after = self.pool.table['0']
        self.assertTrue(before.name == after.name)

        # for k,v in self.pool.table.items():
        #     print(v.name)
    
    #初值確認   
    def test_setup(self):
        flag = True
        for i in range(8):
            flag &= str(i) in self.pool.table
               
        self.assertTrue(flag)     
        self.assertTrue((len(self.pool.table) == 8 ))

        
        flag = True
        flag &= '0001' in self.stu.table
        flag &= '0002' in self.stu.table
        
        self.assertTrue(flag)
        self.assertTrue(len(self.stu.table) == 2)
         
    def test_register_check(self):
        cr1 = self.pool.table['0']
        st1 = self.stu.table['0001']
        st1.register_class(cr1,self.pool)

        st1_current_class = set([cr1])
        self.assertTrue(student_test(st1 ,st1_current_class))
        self.assertTrue(course_test(cr1 , set([st1]),self.pool))

        st2 = self.stu.table['0002']
        st2.register_class(cr1,self.pool)
        st2_current_class = set([cr1])

        self.assertTrue(student_test(st2 ,st2_current_class))
        cr1_current_student = set([st1,st2])
        self.assertTrue(course_test(cr1 , cr1_current_student,self.pool))
        

    #register the same class
    def test_repeat(self):
        cr1 = self.pool.table['0']
        st1 = self.stu.table['0001']
        st1.register_class(cr1,self.pool)
        st1.register_class(cr1,self.pool) 
        
        st1_current_class = set([cr1])
        self.assertTrue(student_test(st1 , st1_current_class))
        cr1_current_student = set([st1])
        self.assertTrue(course_test(cr1 , cr1_current_student,self.pool))
    
    #課程超過20學分
    def test_credit_over20(self):
        for i in range(8):
            self.stu.table["0001"].register_class(self.pool.table[str(i)],self.pool)
        self.assertTrue(self.stu.table["0001"].total_credit <= 20)
    
    #限修課程
    def test_insert_unvalidclass(self):
        cr1 = Course('MED1',3,9)
        st1 = self.stu.table['0001']
        st1.register_class(cr1,self.pool)
        
        self.assertTrue(cr1 not in st1.registeredclass)
        self.assertTrue(student_test(st1 , set()))
        self.assertTrue(cr1 not in self.pool.table)

    def test_cancel_the_class(self):
        to_be_removed = '0'
        remain = '1'
        cr1 = self.pool.table[to_be_removed]
        cr2 = self.pool.table[remain]
        st1 = self.stu.table['0001']
        st2 = self.stu.table['0002']
        st1.register_class(cr1,self.pool)
        st1.register_class(cr2,self.pool)
        st2.register_class(cr1,self.pool) 
        cr1.canceltheclass(self.stu,self.pool)
        self.assertTrue(student_test(st1 , set([cr2])))
        self.assertTrue(student_test(st2 , set()))
        self.assertTrue(course_test(cr1 , set([st1,st2]) , self.pool))
        

    def test_student_drop(self):
        #register
        to_be_removed = '0'
        cr1 = self.pool.table[to_be_removed]
        st1 = self.stu.table['0001']
        st1.register_class(cr1,self.pool)
        st1.drop_class(cr1)
        self.assertTrue(student_test(st1 , set([])))
        self.assertTrue(course_test(cr1 , set([]) , self.pool))


        #non register
        current_register_course = set()
        for i in range(1,5):
            st1.register_class(self.pool.table[str(i)],self.pool)
            temp = self.pool.table[str(i)]
            current_register_course.add(temp)
            self.assertTrue(course_test(temp, set([st1]) , self.pool))
        st1.drop_class(cr1) 
        self.assertTrue(student_test(st1 ,current_register_course))
        self.assertTrue(course_test(cr1 , set([]) , self.pool))

