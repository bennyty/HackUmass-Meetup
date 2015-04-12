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
import itertools


BASE_URL = "https://cesd3.oit.umass.edu/undergradguide/2014-2015/"
MAIN_PAGE = "Chapter2298.html"
ABBR_PAGE = "http://www.umass.edu/ug_programguide/academicinfo/abbreviationsforcourses.html"
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
       	#populates abrreviation_map with hashmap of abbreviations
       	abrreviation_map = self.getAbbreviation()
       	print abrreviation_map
       	for major,link in major_map.items():
       		major_map[major] = self.getCourses(major,link)

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
    	uniqueTup = []
    	normalTup = []
    	courseList = []
    	for link in soup.find_all("p"):
    		#print str(link) + "\n"
    		if '<br/><br/>' in str(link):
    			#print link
    			tup = self.uniqueCases(link)
    			if tup:
    				uniqueTup = tup
    		elif re.match(regex,str(link)):
    			tup = normalCase = self.normalCase(link)
    			if tup:
    				normalTup = tup
    		courseTuple = uniqueTup + normalTup
    		#if courseTuple
    		courseList.append(courseTuple)
    	return courseList
    		#return courseTuple
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
    		courseNumber = [courseNumber.group(0).strip()]
    		commaCase = re.search(r'\d*[,]\d*',courseNumber[0])
    		if not any(char.isdigit() for char in courseNumber):
    			return None
    		elif commaCase:
    			multipleCourseNumList = course.split(',')
    			for number in multipleCourseNumList[:-1]:
    				courseNumber.append(number.strip(','))
    				#print courseNumber
    			lastNumber = re.search(r'([^\s]+)',multipleCourseNumList[len(multipleCourseNumList)-1])
    			if lastNumber.group(0):
    				courseNumber.append(str((lastNumber).group(0)).strip())
    				#print courseNumber

    			#courseNumber.append(lastNumber)
    			#print commaCase.group(1)
    	courseStripped = None
    	courseName = None
    	#courseNumber = [courseNumber]
    	#print courseNumber
    	if courseNumber:
    		#print courseNumber
    		#print courseNumber
    		for stripVal in courseNumber:
    			#print stripVal
    			courseStripped = course.strip(stripVal)
    	#print courseStripped
    	if courseStripped:
    		courseName = re.search(r'^[^\(]+',courseStripped)
    	if courseName:
    		if courseName.group(0):
    			courseName = courseName.group(0).strip('OIM').strip('- ').strip()
    			courseName = filter(lambda x: x in string.printable, courseName)
    	#print courseName
    	#print courseNumber
    	if courseName and courseNumber:
    		return zip(courseNumber,[courseName])
    	#print course

    def getAbbreviation(self):
       	page = requests.get(ABBR_PAGE,verify=False)
        soup = BeautifulSoup(page.content)

        #populates major map with all links assosciated with each major
        abbrev_map = {}
        for link in soup.find_all("p"):
    		link = ''.join(xml.etree.ElementTree.fromstring(str(link)).itertext()).encode('utf-8')
    		abbrevPair = link.split()
    		abbrev_map = dict(itertools.izip_longest(*[iter(abbrevPair)] * 2, fillvalue=""))
    		return abbrev_map
    

    		


if __name__ == '__main__':
    scraper = Course_Scraper()
    scraper.getMajors()


