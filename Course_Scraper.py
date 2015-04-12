import json
from lxml import html
import requests

import re
from bs4 import BeautifulSoup
import string
from HTMLParser import HTMLParser
from pprint import pprint
import xml
import sys


BASE_URL = "https://cesd3.oit.umass.edu/undergradguide/2014-2015/"
MAIN_PAGE = "Chapter2298.html"
major_map = {}
abrreviation_map = {}
requests.packages.urllib3.disable_warnings()

class Course_Scraper():
    def getMajors(self):
    	"""Gets majors from main page"""
       	page = requests.get(BASE_URL + MAIN_PAGE,verify=False)
        soup = BeautifulSoup(page.content)

        #populates major map with all links assosciated with each major
        for link in soup.find_all("a"):
        	links = "<a href='%s'>" %(link.get("href"))
        	major_map[link.text] = (str(links))[9:-2]

        #removes random links
        major_map.pop('departmental honors',None)
       	major_map.pop('',None)

       	#populates major_map with hashmap of courses
       	for course,link in major_map.items():
       		major_map[course] = self.getCourses(course,link)

    def getCourses(self,course,link):
    	"""Gets courses assosciated with given major"""
    	#navigates to course page
    	course_map = {}

    	page = requests.get(BASE_URL + link,verify=False)
    	soup = BeautifulSoup(page.content)

    	#finds all courses in major and puts them in a hashmap
    	coursePageLink = soup.find_all("li")
    	if coursePageLink:
    		link = str(coursePageLink[len(coursePageLink)-1])[54:-90]

    	page = requests.get(BASE_URL + link,verify=False)
    	soup = BeautifulSoup(page.content)
    	#printContent = soup.findAll('div', {"class" : "printcontent"})
    	regex = re.compile(r'<p><strong>(\w+)')
    	uniquedict = {}
    	normaldict = {}
    	for link in soup.find_all("p"):
    		print str(link) + "\n"
    		if '<br/><br/>' in str(link):
    			#print link
    			tup = self.uniqueCases(link)
    			if tup:
    				uniquedict = tup
    		elif re.match(regex,str(link)):
    			tup = normalCase = self.normalCase(link)
    			if tup:
    				uniquedict = tup
    			#course = str(link)[11:].strip('</strong>').strip('<strong>').strip('<br/>').strip('cr').strip('</p')
    			#course = ''.join(xml.etree.ElementTree.fromstring(str(link)).itertext()).encode('utf-8')
    			#courseNumber = re.search(r'([^\s]+)',course)
    			#if courseNumber:
    			#	courseNumber = courseNumber.group(0).strip()
    			#courseName = re.search(r'^[^\(]+',course.strip(courseNumber))
    			#if courseName:
    			#	courseName = courseName.group(0).strip()
    			#print course
    			#print courseNumber
    			#print courseName

    def uniqueCases(self,link):
    	#print str(link) + "\n"
    	for course in link.find_all('br'):
    		#print course
    		return self.normalCase(course)

    def normalCase(self,link):
    	#regex = re.compile(r'<p><strong>(\w+)')
    	#if re.match(regex,str(link)):
    		#course = str(link)[11:].strip('</strong>').strip('<strong>').strip('<br/>').strip('cr').strip('</p')
    	course = ''.join(xml.etree.ElementTree.fromstring(str(link)).itertext()).encode('utf-8')
    	courseNumber = re.search(r'([^\s]+)',course)
    	if courseNumber:
    		courseNumber = courseNumber.group(0).strip()
    		if not any(char.isdigit() for char in courseNumber):
    			return None
    	courseName = re.search(r'^[^\(]+',course.strip(courseNumber).strip('OIM').strip('- '))
    	if courseName:
    		courseName = courseName.group(0).strip()
    	#print courseNumber
    	#print courseName
    	#print course

    		


if __name__ == '__main__':
    scraper = Course_Scraper()
    scraper.getMajors()


