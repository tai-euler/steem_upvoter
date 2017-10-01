# needs to change interpreter to python 2.7

import re
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox(executable_path=r'/home/superuser/Documents/geckodriver')
browser.get("https://steemit.com/login.html")
linkElem= browser.find_element_by_name('username')
linkElem.send_keys('your_username')

passElem= browser.find_element_by_name('password')
passElem.send_keys('your_password')
passElem.submit()
sleep(5)

browser.get("https://steemit.com/hot")
sleep(5)

# endless loop for checking posts and upvoting relevant posts on steemit.com
while True:
    #loop for 5x down key pressing and getting content with 4 seconds pause between
    kk = 11
    while kk > 0:
        bodyElem = browser.find_element_by_tag_name('body')
        bodyElem.send_keys(Keys.PAGE_DOWN)
        #wait between Page_Down random 4, 5 or 6 seconds
        sleep(random.randint(4, 6))
        kk = kk - 1


    # find every element and inside check money and post time (minutes) and give upvote if relevant post
    for s in browser.find_elements_by_xpath("//div[@class='PostSummary__footer']"):

            # find the value of Post, just the integer value
            postValue = int(s.find_element_by_xpath(".//span[@class='integer']").text)

            #find when it was updated -> look after minutes
            #extract integer from string and convert to integer the num string
            postTime = s.find_element_by_xpath(".//span[@class='updated']").text
            #default value
            minutesString = 'minutes'
            #default value, it is corrected in the if loop, when we have minutes
            #otherwise we have hours and in the try block it should NOT be upvoted
            postTimeInt = 31
            # when minutes is in string, extract minutes as integer
            if minutesString in postTime:
                postTime = postTime.strip()
                postTimeInt = re.match(r'\d+', postTime).group(0)
                postTimeInt = int(postTimeInt)
            upvoted = 1
            # if post has already collected at least 30 dollar and was posted between 5-30 minutes
            #give a upvote
            try:
                if (postValue >= 40) and (postTimeInt >= 5 and postTimeInt <= 30):

                    # if 'Remove_vote' found in html, than dont upvote, because its upvoted
                    try:
                        s.find_element_by_xpath(".//a[@title='Remove Vote']")
                        continue
                    # otherwise upvote
                    except Exception as msg:
                        #print msg #optional
                        upvote = s.find_element_by_class_name('Voting__button-up')
                        upvote.click()
                        # after upvoting sleep for 2.5 hour to fully recover steem voting power to 100 %
                        sleep(9000)

            except Exception as msg:
                #print msg
                continue
    #refresh page and wait random time between 1 and 3 minutes to continue
    browser.refresh()
    sleep(random.randint(60, 180))







