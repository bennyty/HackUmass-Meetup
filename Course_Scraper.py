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

#TODO - fix hardcoded urls
BASE_URL = "https://cesd3.oit.umass.edu/undergradguide/2014-2015/"
MAIN_PAGE = "Chapter2298.html"
ABBR_PAGE = "http://www.umass.edu/ug_programguide/academicinfo/abbreviationsforcourses.html"
major_map = {}
abbreviation_map = {}
#ignores SSL warnings cause they're fucking annoying
requests.packages.urllib3.disable_warnings()


class Course_Scraper():
    def getMajors(self):
    	"""Gets majors from main page"""
       	page = requests.get(BASE_URL + MAIN_PAGE,verify=False)
        soup = BeautifulSoup(page.content)

        abbreviationList = []
        majorList = []

        #populates major map with all links assosciated with each major
        for link in soup.find_all("a"):
        	links = "<a href='%s'>" %(link.get("href"))
        	major_map[link.text] = (str(links))[9:-2]

        #removes random links
        major_map.pop('departmental honors',None)
       	major_map.pop('',None)

       	#json_data = open("document.json").read()
       	#data = json.loads(json_data)

       	#list = (data["CMPSCI"].keys())
       	#Sprint type(list[0][1])
       	#populates major_map with hashmap of courses
       	#populates abrreviation_map with hashmap of abbreviations
       	abbreviation_map = self.getAbbreviation()
       	for major,link in major_map.items():
       		#if str(major) in abbreviation_map.keys():
       			#abbreviationList.append(abbreviation_map[str(major)])
       		if major in major_map.keys():
       			if str(major) in abbreviation_map.keys():
       				abbreviation = abbreviation_map[major]
       			courseList = self.getCourses(major,link,abbreviation)
       			if courseList:
       				majorList.append(courseList)
       	majorList = [x for x in majorList if x] 
       	#pprint(majorList)
       	#pprint(major_map)
       	#pprint(abbreviationList)
       	with open('UMass.json', 'w') as outfile:
       		json.dump(majorList, outfile)
       	outfile.close
       	#json.write(majorList,indent=4, sort_keys=True)
       	#self.writeBlob()


    def getCourses(self,course,link,abbrev):
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
    	regex = re.compile(r'<p><strong>(\w+)')
    	uniqueTup = []
    	normalTup = []
    	courseList = []

    	#
    	for link in soup.find_all("p"):

    		#special cases
    		if '<br/><br/>' in str(link):
    			#tuple {major:[course_number,name]}
    			tup = self.uniqueCases(link)
    			if tup:
    				uniqueTup = tup
    		#standard case
    		elif re.match(regex,str(link)):
    			#tuple {major:[course_number,name]}
    			tup = normalCase = self.normalCase(link)
    			if tup:
    				normalTup = tup
    		#puts same major tuples under 1 major
    		courseTuple = uniqueTup + normalTup
    		if courseTuple:
    			courseTuple[0] = courseTuple[0] + ("Department: " + abbrev,)
    			courseList.append(courseTuple)
    	return courseList

    #runs normal case after splitting special case into seperate courses
    def uniqueCases(self,link):
    	for course in link.find_all('br'):
    		return self.normalCase(course)

    def normalCase(self,link):
    	#removes html tags
    	course = ''.join(xml.etree.ElementTree.fromstring(str(link)).itertext()).encode('utf-8')
    	courseNumber = re.search(r'([^\s]+)',course)
    	if courseNumber:
    		courseNumber = [courseNumber.group(0).strip()]
    		
    		commaCase = re.search(r'\d*[,]\d*',courseNumber[0])
    		#if no course number, ignore
    		if not any(char.isdigit() for char in courseNumber):
    			return None
    		elif commaCase:
    			multipleCourseNumList = course.split(',')
    			#split up list by comma except for last number which is attached to the course name
    			for number in multipleCourseNumList[:-1]:
    				courseNumber.append(number.strip(','))
    			#special parses for last name in list
    			lastNumber = re.search(r'([^\s]+)',multipleCourseNumList[len(multipleCourseNumList)-1])
    			if lastNumber.group(0):
    				courseNumber.append(str((lastNumber).group(0)).strip())
    	courseStripped = None
    	courseName = None
    	#if a course number exists strip all the course numbers, could be 1 or many
    	if courseNumber:
    		for stripVal in courseNumber:
    			courseStripped = course.strip(stripVal)
    	if courseStripped:
    		courseName = re.search(r'^[^\(]+',courseStripped)
    	#gets course name if exists
    	if courseName:
    		if courseName.group(0):
    			#fix special cases
    			courseName = courseName.group(0).strip('OIM').strip('- ').strip()
    			courseName = "Course Name: " + filter(lambda x: x in string.printable, courseName)
    	#returns tuple of courseNumber and courseName
    	if courseName and courseNumber:
    		courseNumber = ['Course Number: {0}'.format(i) for i in courseNumber]
    		return zip(courseNumber,[courseName])

    def getAbbreviation(self):
       	page = requests.get(ABBR_PAGE,verify=False)
        soup = BeautifulSoup(page.content)
        #creates dictionary of abbreviation
        normal_map = {}
        unique_map = {}
        for link in soup.find_all("p"):
    		link = ''.join(xml.etree.ElementTree.fromstring(str(link)).itertext()).encode('utf-8')
    		prevLink = None
    		for link in link.split("\n"):
    			abbrevPair = link.split("\t",1)
        		#puts abbreviations into tuple and returns it
        		if len(abbrevPair) == 2:
        			if(abbrevPair[1] == "Bachelor\xe2\x80\x99s Degree with "):
        				abbrevPair[1] = abbrevPair[1].replace("\xe2\x80\x99","'")
        			prevLink = abbrevPair[1]
        			normal_map[abbrevPair[1]] = abbrevPair[0].strip()
    			elif len(abbrevPair) == 1:
    				abbrevPair[0] = abbrevPair[0].strip()
    				unique_map[prevLink + abbrevPair[0]] = normal_map.pop(prevLink)
    		abbrev_map = dict(normal_map,**unique_map)
    		return abbrev_map
    
    #def writeBlob(self):
    #	with open('catalog.json')

if __name__ == '__main__':
    scraper = Course_Scraper()
    scraper.getMajors()


