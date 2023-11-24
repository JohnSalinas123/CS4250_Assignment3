from collections import deque
import string
import urllib.request
import re
from pymongo import MongoClient
from bs4 import BeautifulSoup
import bson

# connect to mongodb
client = MongoClient(host=['localhost:27017'])
db_cur = client["corpus3"]
pages_col = db_cur["pages"]

professor_col = db_cur["professors"]


professor_col.drop()


def parse_faculty(html):
    soup = BeautifulSoup(html, 'html.parser')
    for faculty_div in soup.find_all('div', class_ = "clearfix"):
        
        if not faculty_div.find('h2'):
            continue
    
        faculty_name = faculty_div.find('h2')
        if faculty_name:
            faculty_name = faculty_name.text
        else:
            continue
        
        faculty_p = faculty_div.find('p')
        faculty_title = faculty_p.find('strong', string=re.compile("Title"))
        if faculty_title:
            faculty_title = faculty_title.next_sibling.strip()
        else:
            continue
        
        
        faculty_office = faculty_p.find('strong', string=re.compile("Office"))
        if faculty_office:
            faculty_office = faculty_office.next_sibling.strip()
            faculty_office = re.search(r'\d+-\d+', faculty_office).group()
        else:
            continue
        
    
        faculty_email = faculty_p.find('strong', string=re.compile("Email"))
        if faculty_email:
            faculty_email = faculty_email.find_next_sibling('a').text
        else:
            continue

        
        

        new_prof = {
            "name" : faculty_name,
            "title" : faculty_title,
            "office" : faculty_office,
            "email" : faculty_email,
            
        }
        print(new_prof)
        professor_col.insert_one(new_prof)
    
    
doc = pages_col.find_one({ "url" : "https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml"})
html = doc['html_content']
#print(html)
new_prof = parse_faculty(html)