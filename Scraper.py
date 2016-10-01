import time
import sys
import os
import re
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import html2text

from selenium import webdriver
from splinter import Browser
url = 'https://www.instagram.com/accounts/login/'

driver = webdriver.PhantomJS()
driver.set_window_size(1120, 550)
driver.get(url)
print driver


"""
browser = mechanize.Browser()

cj = cookielib.LWPCookieJar()
browser.set_cookiejar(cj)
# Browser options
browser.set_handle_equiv(True)
browser.set_handle_gzip(False)
browser.set_handle_redirect(True)
browser.set_handle_referer(True)
browser.set_handle_robots(False)
browser.set_handle_robots(False)   # ignore robots
browser.set_handle_refresh(False)  # can sometimes hang without this
browser.addheaders = [('User-agent', 'Firefox')]

html = browser.open('https://www.instagram.com/accounts/login/').read()
print list(browser.forms())
"""



"""
self.browser.select_form(nr=0)
self.browser.form['ctl00$pageContent$userNameText'] = userName
self.browser.form['ctl00$pageContent$passwordText'] = password
self.browser.find_control('ctl00$pageContent$CredentialCheckBox').items[0].selected=True
self.browser.submit()

    #-----------------------------------------------------------------------------------
    #Changes the quarter on the schedule page
    #Takes in the string and int for quarter and year and
    #formats the desired quarter, should be the year + a number
    #for example: quarter: "spring", year: "2014" becomes "20141"
    #-----------------------------------------------------------------------------------
    def changeQuarter(self, quarter, year):
        goldformattedQuarter = str(year) + (self.goldQuarters[quarter.upper()])

        self.browser.select_form(nr=0)
        #goldFormattedQuarter = '20142'
        self.browser.form['ctl00$pageContent$quarterDropDown'] = [goldformattedQuarter]
        self.browser.submit()

    #-----------------------------------------------------------------------------------
    #Prints out GOLD schedule
    #-----------------------------------------------------------------------------------
    def printSchedule(self):

		#Finding the quarter that is selected in GOLD
        quarterList = ['']
        self.browser.select_form(nr=0)
        for control in self.browser.form.controls:
                #For printing all controls:
                #print "type=%s, name=%s value=%s" % (control.type, control.name, self.browser[control.name])
                if (control.name == 'ctl00$pageContent$quarterDropDown'):
                    quarterList = self.browser[control.name]

        currentQuarter = 0
        currentQuarter = quarterList[0][4:5]

		#Finding the season also
        currentSeason = ""
        try:
            currentSeason = (key for key, value in self.goldQuarters.iteritems() if value.upper() == currentQuarter).next()
        except:
            pass
        currnetYear = ""
        currentYear = quarterList[0][0:4]

        #Putting this also together to print it with the schedule
        scheduleTitle = currentSeason + " " + currentYear


        print "######################################"
        #IF statement b/c on first run cannot find the quarter properly
        if (scheduleTitle == " "):
			pass
        else:
        	print scheduleTitle, "\n----"
        self.html = self.browser.open('https://my.sa.ucsb.edu/gold/StudentSchedule.aspx').read()
        soup = BeautifulSoup(self.html)
        str(soup)
        soup2 = (soup.findAll('td', style="padding:3px;"))
        skip = 0
        for i in range(len(soup2)):
            for j in soup2[i]:
                if (skip == 0):
                    print j
                    skip = 1
                else:
                    skip = 0
        print "######################################\n"

    #-----------------------------------------------------------------------------------
    #Counts the number of "full" words in a html page.
    #-----------------------------------------------------------------------------------
    def countFulls(self, inputSoup, numFulls):
        soupString = str(inputSoup)
        self.htmlStrings = soupString.split()
        for line in self.htmlStrings:
            if (line.find('Full')) != -1:
                numFulls = numFulls + 1
        return numFulls

    #-----------------------------------------------------------------------------------
    #Adds the a course for the scraper to look for
    #-----------------------------------------------------------------------------------
    def addCourseToSearch(self, newCourse):
		self.courses.append(newCourse)

    #-----------------------------------------------------------------------------------
    #Attempts to add whatever is in the list
    #-----------------------------------------------------------------------------------
    def attemptAdd(self, courseNumList):
        for courseNum in courseNumList:
            self.html = self.browser.open('https://my.sa.ucsb.edu/gold/StudentSchedule.aspx').read()
            self.browser.select_form(nr=0)
            self.browser.form['ctl00$pageContent$EnrollCodeTextBox'] = courseNum
            response = self.browser.submit('ctl00$pageContent$AddCourseButton')
            self.html = self.browser.open('https://my.sa.ucsb.edu/gold/AddStudentSchedule.aspx').read()

            soup = BeautifulSoup(self.html)
            if (soup.findAll('span', style="color:Red")):
                self.html = self.browser.open('https://my.sa.ucsb.edu/gold/StudentSchedule.aspx').read()
                #print "Tried code: " + courseNum
                return false
            else:
                self.browser.select_form(nr=0)
                response = self.browser.submit('ctl00$pageContent$AddToScheduleButton')
                print "Success"
                return true

"""
