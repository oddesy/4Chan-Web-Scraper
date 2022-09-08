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

# imports the libraries needed to work with csv files
import csv
import os

# imports libraries needed to run program every hour
import time
import schedule


# to run this program, type this into the anaconda prompt:
# python C:\Users\jacks\OneDrive\Desktop\Coding\4Chan-Web-Scraper\main.py


# TO ADD:

    # do data analytics






# runs the main
def data_from_pol_to_csv ():
    
    # tells users that it is running again
    print("Scanning /pol for new posts...")



    # the url we are using to draw text data
    url = "https://boards.4chan.org/pol/"

    # gets the soup of the page
    soup = get_soup_from_page(url)

    # gets the data into a NumPy array
    array = scrape_to_numpy(soup)

    # check for duplicate threads in the NumPy array and the dataset
    remove_duplicates(array)

    # add NumPy array to the dataset file
    write_to_dataset(array)




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




# creates the scrape_to_numpy function that scrapes data from the given 
# Beautiful soup object of the web page
def scrape_to_numpy (soup):

    # filters the page, so that only the threads are left
    page = soup.find_all('div', class_='thread')


    # creates a list to store lists of Post objects in each thread
    THREADS = []

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
            # containing the country 
            parse = str(nameBlock.span.find_next_sibling().find_next_sibling())        
            
            # iterate over string
            quotation_index = []
            index = 0
            while (index < len(parse)):
                if (parse[index] == '"'):
                    quotation_index.append(index)
                index = index + 1
            

            # parses the country from the parse variable and the number of quotation marks
            if (len(quotation_index) == 4):
                countryOfOrigin = parse[quotation_index[2] + 1 : quotation_index[3]]
            elif (len(quotation_index) > 4):
                countryOfOrigin = "Moderator"
            else:
                countryOfOrigin = "<br> (Error)"


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

    # returns the array of the data for this page
    return arr    




# ensures there are no duplicates of threads/data in the dataset
def remove_duplicates (array):

    # opening the dataset file
    reader_file = open(r"C:\Users\jacks\OneDrive\Desktop\Coding\4Chan-Web-Scraper\Pol_Forum_Dataset.csv", 'r', encoding='utf-8')

    # reading the CSV file
    reader = csv.reader(reader_file)


    # when the last duplicate in the array appears
    last_row_duplicate_index = 0
    
    # the index iterator keeping track of which line of the dataset file is being examined
    index = 0


    # number of rows in the NumPy array
    rows_in_NumPy_array = int((array.size) / 4)
    #print(rows_in_NumPy_array)


    # searches through the dataset file only the length of the array 
    for lines in reader:

        # defines the formatted_lines variable
        formatted_lines = ""

        # checks if the lines variable (the current line) is an empty list (whitespace)
        # if not, sets formatted_lines to be a string concatenation of the list values
        if (len(lines) != 0):
            formatted_lines = "[" + str(lines[0]) + ", " + str(lines[1]) + ", " + str(lines[2]) + ", " + str(lines[3]) + "]"
        #else:
        #    print("empty")
        #print(lines)
        #print(formatted_lines)


        # searches through the array for duplicate posts
        for row in array:
            
            #print(row)
            # makes the the NumPy rows 32formatted the same as the csv lines so that they may be tested for equality
            formatted_row = "[" + str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + ", " + str(row[3]) + "]"
            #print(formatted_row)
            
            
            # tests for duplicates
            if (formatted_row == formatted_lines):
                
                #print("Found a duplicate!")
                # sets the last duplicate to the current index
                last_row_duplicate_index = index
            


        #print("Rows left is " + str(rows_in_NumPy_array))
        # decrementing the rows_in_NumPy_array variable by 1
        rows_in_NumPy_array = rows_in_NumPy_array - 1
        

        #print("Index is " + str(index))
        # increments the index variable by 1
        index = index + 1
        

        # detect if the search is exceeding the possible limit of duplicates
        if (rows_in_NumPy_array < 0):
            #print("Break")
            break
        

    

    # closes the reader
    reader_file.close()


    # removes every duplicate thread including the current one and after 
    # for example if array has a duplicate at thread index 20, 
    # remove the threads 20-end in the array from the dataset


    # prints the number of posts added to the database file
    num_added_posts = index - last_row_duplicate_index
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Added " + str(num_added_posts) + " posts to csv file at time: " + current_time + ".\n")


    # holds the rows to be removed
    row_numbers_to_remove = []

    #print(last_row_duplicate_index)
    # populating the variable with the range of rows from the beginning to the row at the index
    # its twice the last_row_duplicate_index because of the whitespace after every entry and + 1 because
    # the range returns a list from [0, ..., n-1] and we want it to be from [0, ..., n]
    for num in range((2 * last_row_duplicate_index) + 1):
        row_numbers_to_remove.append(num)


    # holds the rows that aren't deleted from the dataset file
    lines = list()
    

    # reads the csv file and adds the rows that aren't being removed to a list
    with open(r"C:\Users\jacks\OneDrive\Desktop\Coding\4Chan-Web-Scraper\Pol_Forum_Dataset.csv", 'r', encoding='utf-8') as read_file:
        reader = csv.reader(read_file)
        for row_number, row in enumerate(reader, start=1):
            
            # rows that are being removed and don't include empty rows
            if((row_number not in row_numbers_to_remove) and (row != [])):
                lines.append(row)


    # remove everything in the original csv file.
    file = r"C:\Users\jacks\OneDrive\Desktop\Coding\4Chan-Web-Scraper\Pol_Forum_Dataset.csv"

    if(os.path.exists(file) and os.path.isfile(file)):
        os.remove(file)
        #print("File deleted")
    else:
        print("File not found")


    # writes the rows of data that aren't being removed to the csv file
    with open(r"C:\Users\jacks\OneDrive\Desktop\Coding\4Chan-Web-Scraper\Pol_Forum_Dataset.csv", 'w', encoding='utf-8') as write_file:
        writer = csv.writer(write_file)
        writer.writerows(lines)




# writes the correct NumPy array of data to the dataset file
def write_to_dataset (array):

    # opening the dataset file
    writer_file = open(r"C:\Users\jacks\OneDrive\Desktop\Coding\4Chan-Web-Scraper\Pol_Forum_Dataset.csv", 'a', encoding='utf-8')

    # creating the writer for the csv file 
    writer = csv.writer(writer_file)
    
    # iterates through the dataset and writing the NumPy array to the dataset file
    for row in array:
        writer.writerow(row)

    # closing the file
    writer_file.close()




# runs the main function if this is the file being run
if __name__=="__main__":
    
    # runs the main program once at the beginnning:   
    print("Starting Program: \n\n") 


    # runs the main program once every minute
    schedule.every().minute.do(data_from_pol_to_csv) 
    
    # loops and runs the scheduled job indefinitely 
    while True:  
        schedule.run_pending()
        time.sleep(1)









































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

"""
#THREAD_TITLES


#MESSAGES

#div.post blockquote.postMessage {
#    display: block;
#}

#<blockquote class="postMessage" id= ""> </blockquote>

#<div class="postContainer replyContainer" id=""> </div>
"""
