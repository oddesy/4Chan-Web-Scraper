from asyncore import write
from operator import index
import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# imports classes Post and Thread
from Post import Post 
from Thread import Thread

# imports datetime to store time data in objects
from datetime import datetime


# type this into the anaconda prompt
# python C:\Users\jacks\OneDrive\Desktop\Coding\4Chan-Web-Scraper\main.py


# main function of the file
def main ():
    
    # the url we are using to draw text data
    url = "https://boards.4chan.org/pol/"

    # gets the soup of the page
    soup = get_soup_from_page(url)

    # gets the data into a NumPy array
    array = scrape_to_numpy(soup)

    # check for duplicate threads in the NumPy array and the dataset
    array = check_duplicates(array)

    # add NumPy array to the dataset file
    write_to_dataset(array)





    # iterate over multiple pages
    # iterates over several webpages ____ many times or until ______
    # url goes from the first page of pol being /pol/ to /pol/2 and ends at /pol/10




# creates the scrape_to_numpy function that scrapes data from the given 
# Beautiful soup object of the web page
def scrape_to_numpy (soup):

    # filters the page, so that only the threads are left
    page = soup.find_all('div', class_='thread')


    # creates a list to store lists of Post objects in each thread
    THREADS = []
    POSTS = []

    # iterates through each thread and 
    for thread in page:
        
        # to find the title I need to navigate to the span nameBlock of the OP
        nameBlock = thread.find("span", class_="nameBlock")

        # then need to navigate to the span subject portion
        title = nameBlock.find("span", class_="subject").text

        # create a thread with the title
        t = Thread(title)


        # create a new soup because of issues with grabbing
        #thread_soup = BeautifulSoup(thread, "html.parser")

        # iterates through each post in the thread and 
        for post in soup.find_all('div', class_= ['postContainer opContainer','postContainer replyContainer']):


            # find the variables needed to instantiate a Post object
            
            # to find the time and country of origin I need to navigate to the 
            # span nameBlock of the post
            nameBlock = post.find("span", class_="nameBlock")

            # then need to navigate to the span dateTime postNum part
            time = str(post.find("span", class_="dateTime postNum").text)
            
            #removes the user id from the end
            time = time[:21]

            # turn this into Python datetime objext using string methods
            date_object = datetime(2000 + int(time[6:8]), int(time[:2]), int(time[3:5]), int(time[13:15]), int(time[16:18]), int(time[19:21]))

            

            
            # str parse through nameBlock until I find the span with the title
            #containing the country 
            parse = str(nameBlock.span.find_next_sibling().find_next_sibling())        
            
            # iterate over string
            quotation_index = []
            index = 0
            while (index < len(parse)):
                if (parse[index] == '"'):
                    quotation_index.append(index)
                index = index + 1
            
            # parses the country from the parse variable
            countryOfOrigin = parse[quotation_index[2] + 1 : quotation_index[3]]
            



            # finding the text 
            text = post.find("blockquote", class_="postMessage").text

            # cut out first eleven characters of each new line (cuttting out the user id)
            # if it has ">>" at the start
            while (text[:2] == ">>"):
                text = text[11:]

            text = str(text).replace('>', '')




            # instantiate a Post object
            p = Post(countryOfOrigin, date_object, text)

            # append the Post object to my thread
            t.posts.append(p)
        
        
        # append thread to the list THREADS before loop ends
        THREADS.append(t)




    # creating an empty NumPy array for the dataset
    arr = np.empty((1, 4), object)


    # looping through each thread in the THREADS list 
    for thread in THREADS:

        # storing the thread title
        thread_title = thread.title

        # looping through each post in the posts list of the thread object
        for post in thread.posts:

            # storing the post data
            post_country = post.country
            post_time = post.time
            post_text =  post.text

            # adds the information into a placeholder array (a little redundant)
            new_array = np.array([[thread_title, post_country, post_time, post_text]])

            # adds the information to the NumPy array to create the dataset
            arr = np.append(arr, new_array, axis= 0)
            
            


    # removes the row of [None, None, None, None] from the NumPy arr
    if (arr[0, 0] == None):
        arr = np.delete(arr, 0, 0)


    print (arr.shape)

    print (arr)
    



# gets a soup of the /pol forum
def get_soup_from_page (url):
    
    # Only use US websites
    headers = {
        "Accept-Language": 
        "en-US, en;q=0.5"
    }
    
    # defining and inititalizing requests varaible to hold the text information of the webpage
    results = requests.get(url, headers=headers)

    # first filtering of data
    soup = BeautifulSoup(results.text, "html.parser")

    return soup



# ensures there are no duplicates of threads/data in the dataset   
def check_duplicates (array):

    # loop through the NumPy array of scraped data
    #for x in array:

    print("Hello")

    #check for duplicates in the saved dataset


    # if duplicate is spotted, remove duplicate thread from the dataset or the NumPy array



    return array




# writes the correct NumPy array of data to the dataset file
def write_to_dataset (array):

    # iterates through the dataset and writes it in the dataset file
    print("text")

 


# runs the main function if this is the file being run
if __name__=="__main__":
    main()









































"""
urls = ["https://boards.4chan.org/pol/", "https://boards.4chan.org/pol/2", "https://boards.4chan.org/pol/3", 
"https://boards.4chan.org/pol/4", "https://boards.4chan.org/pol/5", "https://boards.4chan.org/pol/6", 
"https://boards.4chan.org/pol/7", ,"https://boards.4chan.org/pol/8", "https://boards.4chan.org/pol/9", 
"https://boards.4chan.org/pol/10"]
"""


# there is a 3-day archive for last 3,000 threads, but it's not worth it to scrape 







    
"""   
original_post = thread.find("div", class_="postContainer opContainer")

post = postInfo(original_post)

#print(findCountryOfOrigin(post))
#print(findTitle(post))
#print(findTime(post))

reply_posts = thread.find("div", class_="postContainer replyContainer")










# "postInfoM mobile" has the country of origin and time of posting
def postInfo(post):
    post_info = post.find("div", class_="postInfoM mobile")
    return post_info

def findCountryOfOrigin(post):
    nameBlock = post.find("span", class_="nameBlock")
    country = nameBlock.next_element.next_element.next_element
    return country

def findTime(post):
    time = post.find("span", class_="dateTime")
    formatted_time = time.text
    return formatted_time




def findTitle(post):
    title = post.find("div", class_="subject")
    #formatted_title = title.text
    #return formatted_title
    return title



"""
















#THREAD_TITLES






#MESSAGES

#div.post blockquote.postMessage {
#    display: block;
#}

#<blockquote class="postMessage" id= ""> </blockquote>

#<div class="postContainer replyContainer" id=""> </div>







"""
# initialize empty lists where you'll store data
thread_titles = []
time = []
op_post_message = []
post_messages = []
images = []
links = []


TITLES = soup.find_all('div', class_='subject')

TIME = soup.find_all('span', class_='dateTime')

OPMESSAGE = soup.find_all('div', class_='postContainer opContainer')

REPLIES = soup.find_all('div', class_='postContainer replyContainer')

IMAGES = soup.find_all('a', class_='fileThumb')

LINKS = soup.find_all('a', class_='quotelink')
"""


