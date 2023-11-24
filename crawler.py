
from collections import deque
import string
import urllib.request
import re
from pymongo import MongoClient
from bs4 import BeautifulSoup

target_url = "https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml"

seed_url = "https://www.cpp.edu/sci/computer-science/"

target_heading = "Permanent Faculty"


# connect to mongodb
client = MongoClient(host=['localhost:27017'])
db_cur = client["corpus3"]
pages_col = db_cur["pages"]

# delete pages collection
pages_col.drop()

# parse html of given url
def fetch_page(url):
    try:
        response = urllib.request.urlopen(url)
        return response.read()
    except Exception as e:
        print("Error fetching" + url + e)
        return None

# extract links from html, make links absolute
def extract_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', href=True)
    abs_links = [urllib.parse.urljoin(base_url, link['href']) for link in links]
    return abs_links

# mongodb funcs
def storePage(url):
    newVisitedPage = {
        "url" : url,
    }
    pages_col.insert_one(newVisitedPage)
    
def checkIfVisitedPage(url):
    return not pages_col.find_one({url: url})

def checkForTarget(html):
    soup = BeautifulSoup(html, 'html.parser')
    heading = soup.find('h1').getText()
    
        
    return heading == target_heading


def web_crawler(frontier):
    
    while frontier:
        
        cur_url = frontier.popleft()
        print("Crawling: " + cur_url)
        cur_html = fetch_page(cur_url)
        
        storePage(cur_url)
        
        if checkForTarget(cur_html):
            print("TARGET FOUND")
            print("URL of target: " + cur_url)
            print(cur_url == target_url)
            frontier.clear()
        else:
            for link in extract_links(cur_html, seed_url):
                if checkIfVisitedPage:
                    frontier.append(link)
                    
        
        



frontier = deque()
frontier.append(seed_url)

web_crawler(frontier)