import unittest
import requests
#coding: utf-8
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from collections import Counter
import os


class TestProject2(unittest.TestCase):
  def setUp(self):
    self.driver = webdriver.Chrome()
    self.driver.implicitly_wait(10)
    self.url = 'http://cc.ee.ntu.edu.tw/~farn/courses/BCC/NTUEE/2014.spring/index.htm'
    self.driver.get(self.url)


  def tearDown(self):
    response = requests.get(self.url)
    html_content = response.text
    file_path = "test_page.html"
    with open(file_path, 'w', encoding='utf-8') as file: #
        file.write(html_content)
        print(f"HTML content saved to {file_path}")
    self.driver.quit()
  
  def test_project2(self):
    checklist = ['a']
    cnt = Counter()
    #s = set()
    with open('result.txt', 'w') as file:
        
        for i in range(len(checklist)):
            
            elements = [(i,i.text , i.get_attribute("href")) for i  in self.driver.find_elements(By.TAG_NAME, checklist[i]) if i.is_displayed()]
            cnt['total'] = len(elements)
            
            for n,(t,text,except_href) in enumerate(elements,1):   
              try : 
                  response = requests.get(except_href,timeout= 3)
              except Exception as e:
                    file.write('reason: response too long \n')  
                    file.write('label:' + str(i) + '\n')  
                    file.write('href:' + str(except_href) + '\n')  
                    file.write('..........' + '\n')                    
                    cnt['response too long'] +=1
                    continue

              if response.status_code == 404:
                  file.write('reason:' + '404' + '\n')  
                  file.write('label:' + str(i) + '\n')  
                  file.write('href:' + str(except_href) + '\n')  
                  file.write('..........' + '\n')  
                  cnt['404 error'] +=1
                  continue
              

              try:            
                  t.click()

                  flag = False
                  for word in ['zip' , 'ppt']:
                    if word in except_href :
                      cnt['valid'] +=1
                      flag =True
                      break
                  if flag:
                    continue
                
                  if  except_href != self.driver.current_url:
                      self.assertＴrue(except_href != response.url)
                      cnt['redirect'] +=1
                  else:                 
                    self.assertＴrue(response.status_code == 200)
                    self.assertＴrue(self.driver.current_url == except_href)
                    cnt['valid'] +=1
                  self.driver.back()
              
              except Exception as e:
                  cnt['other'] +=1      
                  file.write('reason:' + str(e) + '\n')  
                  file.write('label:' + str(i) + '\n')  
                  file.write('href:' + str(except_href) + '\n')  
                  file.write('..........' + '\n')  


    for k,v in cnt.items():
       print('the number of  ' + str(k) + ' = ' + str(v))