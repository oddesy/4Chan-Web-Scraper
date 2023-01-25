from bs4 import BeautifulSoup
import numpy as np

# imports classes Post and Thread
from Post import Post 
from Thread import Thread

# imports datetime to store time data in objects
from datetime import datetime

# imports the libraries needed to work with csv files
import csv

# imports libraries needed to run program every hour
import time
import schedule

# allows resolution of the following error:     Max retries exceeded with url: 
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# to deal with string splicing
import re 





# to run this program, type this into the anaconda prompt:
# python C:\Users\Jackson\Documents\Coding\4Chan-Web-Scraper\main.py






"""
PROBLEM - Fix country of origin


RESOLVED Duplicates - Potential solution is to only output a thread and its posts to the csv file if that thread was no longer found on 
                the first ten pages of the /pol. This means that it would become archived. Thus, I wouldn't need to run a differnt
                program to check for duplicates because I would only ever output the thread (and associated posts) to the csv file
                until I knew the program wouldn't need them again. 


RESOLVED - Test whether the program catches forum replies underneath the [+] icon. # replies and # images omitted. Click here to view.
NOTES - Yes, it does. It catches all of the replies because although they are initially hidden from the user, the html which the 
        program scrapes catches them all
"""















# runs the main
def data_collection_and_processing ():
    
    # tells users that it is running again
    print("\nScanning /pol for new posts...")
    

    urls = ["https://boards.4chan.org/pol/", "https://boards.4chan.org/pol/2", "https://boards.4chan.org/pol/3", 
    "https://boards.4chan.org/pol/4", "https://boards.4chan.org/pol/5", "https://boards.4chan.org/pol/6", 
    "https://boards.4chan.org/pol/7", "https://boards.4chan.org/pol/8", "https://boards.4chan.org/pol/9", 
    "https://boards.4chan.org/pol/10"]


    # creates a list to hold the html extracts of each url
    soups = []

    # loops through each of the urls in the list of urls
    for url in urls:

        # add the extracted html of the url into the soups list
        soups.append(get_soup_from_page(url))

    
    # contains a list of all threads from the urls and each post within each thread
    total_list_of_threads = []

    # iterates through each html extract
    for soup in soups:

        # scrapes the html into a list of Thread objects
        list_of_threads = scrape_to_list(soup)

        # loops through each Thread object in the list_of_threads 
        for thread in list_of_threads:

            # adds each Thread object into the total_list_of_threads
            total_list_of_threads.append(thread)


    # removes duplicate posts from duplicate Threads using the previous list of threads 
    # and the newly scraped list of threads.
    non_duplicate_list = remove_duplicate_threads_and_posts(total_list_of_threads, previous_thread_additions_to_csv_file)


    """
    # prints the number of posts that are now in the previous thread list

    size = 0
    for thread in previous_thread_additions_to_csv_file:

        for post in thread.posts:

            size += 1
    
    print ("\nThe comparator for the past iteration has been updated to include a total of " + str(size) + " posts.\n")
    """

    # transforms the non_duplicate_list into an array
    array = list_to_NumPy_array(non_duplicate_list)

    # add NumPy array to the dataset file
    write_to_dataset(array)




# gets a soup of the /pol forum
def get_soup_from_page (url):
    
    # Only use US websites
    headers = {
        "Accept-Language": 
        "en-US, en;q=0.5"
    }
    

    # applies the backoff factor to the requesting of the url an unlimited number of times
    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=3)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    # extracts the data from the url
    results =  session.get(url, headers=headers)

    # specifies the html text to be stored
    soup = BeautifulSoup(results.text, "html.parser")

    # returns the text of the webpage
    return soup




# appends Post Objects to a Thread Object from the url of a specific Thread (that has more than 5 replies)
def get_posts_from_single_thread (thread_url):

    # gets the soup of the page
    soup = get_soup_from_page(thread_url)

    # a list that holds all of the posts in the thread as Post objects
    posts = []

    # filters the page, so that only the threads are left
    # in this case, there is only one thread on the page because we are viewing an expanded
    # thread and are not on the homepage. 
    list_of_threads = soup.find_all('div', class_='thread')



    #print("There are " + str(len(list_of_threads)) + " threads in the html from the url.")
    #print("There are " + str(len(list_of_threads[0].find_all('div', class_= ['postContainer opContainer','postContainer replyContainer']))) + " posts in the html from the url.")


    # checks if there is at least one thread in the html
    if (len(list_of_threads) > 0):

        # iterates through each post in the thread and 
        for post in list_of_threads[0].find_all('div', class_= ['postContainer opContainer','postContainer replyContainer']):

            # find the variables needed to instantiate a Post object
            # to find the time and country of origin I need to navigate to the 
            # span nameBlock of the post
            nameBlock = post.find("span", class_="nameBlock")



            # finding the time of the Post
            # then need to navigate to the span dateTime postNum part
            time = str(post.find("span", class_="dateTime postNum").text)
            
            # removes the user id from the end
            time = time[:21]

            # turn this into Python datetime objext using string methods
            date_object = datetime(2000 + int(time[6:8]), int(time[:2]), int(time[3:5]), int(time[13:15]), int(time[16:18]), int(time[19:21]))


            # FIX
            # finding the Country of the Post
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

            # append the Post object to the posts list
            posts.append(p)


    # returns the list of Post objects
    return posts


# appends Post Objects to a Thread Object given the html of the homepage of 4Chan (that has under 6 replies)
def get_posts_from_homepage (thread):
    
    # a list that holds all of the posts in the thread as Post objects
    posts = []

    # iterates through each post in the thread and 
    for post in thread.find_all('div', class_= ['postContainer opContainer','postContainer replyContainer']):



        # find the variables needed to instantiate a Post object

        # to find the time and country of origin I need to navigate to the 
        # span nameBlock of the post
        nameBlock = post.find("span", class_="nameBlock")



        # finding the time of the Post
        # then need to navigate to the span dateTime postNum part
        time = str(post.find("span", class_="dateTime postNum").text)
        
        # removes the user id from the end
        time = time[:21]

        # turn this into Python datetime objext using string methods
        date_object = datetime(2000 + int(time[6:8]), int(time[:2]), int(time[3:5]), int(time[13:15]), int(time[16:18]), int(time[19:21]))


        # FIX
        # finding the Country of the Post
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

        # append the Post object to the posts list
        posts.append(p)


    # returns the list of Post objects
    return posts
    

# creates the scrape_to_list function that scrapes data from the given 
# Beautiful soup object of the web page to a List of Thread Objects
def scrape_to_list (soup):

    # filters the page, so that only the threads are left
    page = soup.find_all('div', class_='thread')


    # creates a list to store each Thread object and its list of Post objects underneath it
    THREADS = []

    # iterates through each thread in the page
    for thread in page:

        # finds the thread title
        # to find the title I need to navigate to the span nameBlock of the OP
        nameBlock = thread.find("span", class_="nameBlock")

        # then need to navigate to the span subject portion
        title = nameBlock.find("span", class_="subject").text

        

        # gets the full thread from the html of the page 
        # this only selects the non-pinned threads like the logical falacies one and the 
        # check this catalog before posting one. The "summary desktop" is responsible for
        # this.
        thread_link = str(thread.find("span", class_="summary desktop"))

        #print(thread_link)

        # the index of where the thread number appears in the html
        index_of_thread_number = thread_link.find("thread/") + 7

        # splits the html string to find the thread number 
        thread_number = re.split('"', thread_link[index_of_thread_number:])


        

        # if the program doesn't find the thread number from the html, the list 
        # thread_number will have only one value: [None]. Otherwise, if the program 
        # does find the thread number fromm the html, the list thread_number will 
        # have two values, with the first being the thread_number. 

        

        # there are two situations if the thread_number isn't found. One is that the 
        # thread has less than six replies, thus it doesn't need to be expanded by 
        # clicking the [+] button to reveal the remaining replies. Another is that
        # the thread has no replies because it is one of the two pinned threads by
        # the moderators. Those two are: the Logical Fallacies one and the Check 
        # this before posting. 

        # stores the list of Post objects from the html of whichever page of 4Chan/pol
        # it was sourced from 
        new_posts = []
        
        # if the thread_number exists and is equal to 2, there is an expanded thread
        # waiting to be explored
        if (len(thread_number) == 2):

            thread_url = "https://boards.4chan.org/pol/thread/" + str(thread_number[0])
            #print(thread_url)

            #print("single thread")
            # extracting the html text from the full thread page and putting the list of 
            # Post objects into the new_posts list 
            new_posts = get_posts_from_single_thread(thread_url)

        # if the thread_number is not found, there is entirity of the thread is on the 
        # homepage
        else:
            
            #print("from homepage")
            # gets the list of Post objects from the html text in the thread variable and 
            # puts them in the new_posts list 
            new_posts = get_posts_from_homepage(thread)

            

            
        # create a Thread object with the title
        t = Thread(title, new_posts)

        # append thread to the THREADS list after completely instaniating a Thread 
        # Object with all of its posts
        THREADS.append(t)


    # returns the list of Thread Objects
    return THREADS




# ensures there are no duplicates threads in the dataset
def remove_duplicate_threads_and_posts (new_list, previous_thread_list):


    """
    # prints the number of posts in the previous_thread_list

    size = 0
    for thread in previous_thread_list:

        for post in thread.posts:

            size += 1

    print ("The previous_thread_list has " + str(size) + " posts.\n")
    """

    """
    # prints the number of posts in the new_list 

    size = 0
    for thread in new_list:

        for post in thread.posts:

            size += 1

    print ("The new_list of threads has " + str(size) + " posts.\n")
    """
    
    
    """
    #
    # everything after this line and until this line:
    # 
    # list_without_duplicates = []
    # 
    # is responsible for updating the previous_threads_list
    """

    # tracks which old_threads are not present in the list of new threads
    indexes_of_old_threads_not_in_new_threads = []

    # sets up an index variable to track which old_thread is being iterated through
    old_thread_index = 0

    # loops through the Thread objects in previous_thread_list (old_list)
    for old_thread in previous_thread_list:

        # tracks whether or not the old thread has appeared in the list of new threads 
        found_old_thread_in_new_list = False

        # checks if there are any posts inside the old thread before getting into it
        if (len(old_thread.posts) > 0):

            # 
            formatted_old_first_post_of_thread = "[" + str(old_thread.title) + ","  + str(old_thread.posts[0].country) + "," + str(old_thread.posts[0].time) + "," + str(old_thread.posts[0].text) + "]"

            # loops through the Thread objects in new_list
            for new_thread in new_list:
                
                # checks if there are any posts inside the old thread before getting into it
                if (len(new_thread.posts) > 0):

                    # gets a formatted string of the first post of the thread
                    formatted_new_first_post_of_thread = "[" + str(new_thread.title) + ","  + str(new_thread.posts[0].country) + "," + str(new_thread.posts[0].time) + "," + str(new_thread.posts[0].text) + "]"

                    # checks if the two Threads are the same (this is done by comparing the original post of each
                    # thread by looking at the first post in each Thread.posts list)
                    # can't check if the Thread titles (Thread.titles) are the same because often times thread 
                    # titles are blank ("" == "") could be true for completely different threads
                    if (formatted_new_first_post_of_thread == formatted_old_first_post_of_thread):

                        # sets the bool to be True denoting that this old thread exists in the list of new threads
                        found_old_thread_in_new_list = True
            
            # if the old thread was not found at all in the list of new threads, then add the index of the 
            # old thread to a list to be removed from the list of old threads later on
            if (found_old_thread_in_new_list == False):
                
                #print("\nDidn't find old thread in list of new threads!")

                # notes down which old_threads are not in the new_list of Thread objects
                indexes_of_old_threads_not_in_new_threads.append(old_thread_index)

            # increments the index variable
            old_thread_index += 1




    non_duplicate_new_thread_post_size = 0
    
    
    
    
    # tracks which new_threads are not present in the list of old threads
    indexes_of_new_threads_not_found_in_old_threads = []

    # sets up an index variable to track which new_thread is being iterated through
    new_thread_index = 0

    # searches through the Thread objects in new_list 
    for new_thread in new_list:
        
        # tracks whether or not the new thread has appeared in the list of old threads 
        found_new_thread_in_old_list = False

        # iterates through the Thread objects in previous_thread_list 
        for old_thread in previous_thread_list:

            # checks if there are any posts inside the threads before getting into them
            if (len(old_thread.posts) > 0 and len(new_thread.posts) > 0):

                # sets the two formatted strings of each post 
                formatted_new_first_post_of_thread = "[" + str(new_thread.title) + ","  + str(new_thread.posts[0].country) + "," + str(new_thread.posts[0].time) + "," + str(new_thread.posts[0].text) + "]"
                formatted_old_first_post_of_thread = "[" + str(old_thread.title) + ","  + str(old_thread.posts[0].country) + "," + str(old_thread.posts[0].time) + "," + str(old_thread.posts[0].text) + "]"

                # checks if the two Threads are the same (this is done by comparing the original post of each
                # thread by looking at the first post in each Thread.posts list)
                # can't check if the Thread titles (Thread.titles) are the same because often times thread 
                # titles are blank ("" == "") could be true for completely different threads
                if (formatted_new_first_post_of_thread == formatted_old_first_post_of_thread):

                    #print("\nFound new thread in list of old threads!")
                    
                    # sets the bool to be True denoting that this new thread exists in the list of old threads
                    found_new_thread_in_old_list = True
                    

                    #print(str(len(new_thread.posts)) + " posts in the new thread.")
                    #print(str(len(old_thread.posts)) + " posts in the old thread.")


                    # a list that holds all of the posts that are present in both of Thread.posts lists
                    list_of_duplicate_posts = []

                    # a list that holds all the posts that are present in only one of the Thread.posts lists
                    list_of_non_duplicate_posts = []
                    
                    # this will be the combination of the two lists above (duplicates + non_duplicates)
                    list_of_all_posts = []


                    # loops through the posts in the new thread
                    for new_post in new_thread.posts:
                        
                        # tracks whether or not the new post has appeared in the list of old threads 
                        found_new_post_in_old_list = False

                        # a String that holds the String concatenation of the instance variables of the  
                        formatted_new_thread_post = "[" + str(new_thread.title) + ","  + str(new_post.country) + "," + str(new_post.time) + "," + str(new_post.text) + "]"


                        # loops through the posts in the old thread
                        for old_post in old_thread.posts:

                            # formats the post from the old thread
                            formatted_old_thread_post = "[" + str(old_thread.title) + ","  + str(old_post.country) + "," + str(old_post.time) + "," + str(old_post.text) + "]"


                            # checks if the post is in both the new and old lists
                            # if post is in both, it is a duplicate, and it can be deleted from the new_list
                            # if post is only in the new, it remains in the Thread.posts list of for the 
                            # additions
                            if (formatted_new_thread_post == formatted_old_thread_post):

                                #print("Found a duplicate post!")

                                # adds the current duplicate post to the list of duplicate posts
                                list_of_duplicate_posts.append(old_post)

                                # sets found_new_post_in_old_list to True if the new_post is in the list of old posts 
                                found_new_post_in_old_list = True


                        # checks if the new post was found in the list of old posts, if not it adds it to the
                        # list of non-duplicates 
                        if (found_new_post_in_old_list == False):

                            #print("Found a NON-DUPLICATE post!")

                            # adds the current non-duplicate post to the list of duplicate posts
                            list_of_non_duplicate_posts.append(new_post)




                    # first, sets the list_of_all_posts to the list_of_duplicate_posts
                    list_of_all_posts = list_of_duplicate_posts 
                   
                    # second, adds each non-duplicate post from the list_of_non_duplicate_posts into the list_of_all_posts
                    for post in list_of_non_duplicate_posts:

                        # add each post to the list_of_all_posts
                        list_of_all_posts.append(post)




                    #print("Added " + str(len(list_of_non_duplicate_posts)) + " posts from a shared thread to the old thread.posts list")
                    #print("Deleted " + str(len(list_of_duplicate_posts)) + " duplicate posts from the new thread")

                    # sets the Thread.posts list to the correct list
                    old_thread.set_posts(list_of_all_posts)
                    new_thread.set_posts(list_of_non_duplicate_posts)

                    #print(str(len(new_thread.posts)) + " posts in the new thread")
                    #print(str(len(old_thread.posts)) + " posts in the old thread")
                    

                

        # if the new thread was not found at all in the list of old threads, then add the index of the 
        # new thread to a list to be added to the list of old threads later on
        if (found_new_thread_in_old_list == False):
            
            # notes down which new_threads are the not in the old_list of Thread objects
            indexes_of_new_threads_not_found_in_old_threads.append(new_thread_index)

            # adds the number of posts in the non_duplicate_new_thread to a counter
            non_duplicate_new_thread_post_size += len(new_thread.posts)

        # increments the index variable
        new_thread_index += 1
    


    
      
    print("\n" + str(non_duplicate_new_thread_post_size) + " posts in the new threads that weren't in the list of old threads. (The first time the program runs, the list of old threads will be empty.)")



    # Holds the threads that were in the previous_thread_list, but not the new_thread_list. Since these threads have been pushed off
    # the front ten pages of /pol, this program will not encounter them again. Thus, I will send these Threads to the csv file because
    # this is the last time the program will encounter them. 

    # I need to make sure that the Threads in the previous_thread_list are not trimmed. All of the new posts are added to. Otherwise, 
    # the Thread will be trimmed every iteration of the program (since it is removing duplicates in my previous approach that 
    # sent the posts to the csv file every run until the Thread was no longer seen on the html scraping, it might be the case that 
    # the Posts objects in each Thread are cut down every run.) I need to do the opposite of this. I need to have EVERY Post in that
    # Thread saved and added so that when the Thread is no longer on the front pages of /pol, it will send the entire list of Posts to
    # the csv file.  
    threads_to_add_to_the_csv = []


    print("\nRemoved  " + str(len(indexes_of_old_threads_not_in_new_threads)) + " threads from the old thread list that were not in the new thread list.")

    print("\nThese threads are being outputted to the csv file shortly...")

    # sorts the list of indexes_of_old_threads_that_are_not_in_the_list_of_new_threads into reverse order
    indexes_of_old_threads_not_in_new_threads = sorted(indexes_of_old_threads_not_in_new_threads, reverse=True)

    # removes the old threads that are not in the list of new threads using the indexes of those old_threads
    for index in indexes_of_old_threads_not_in_new_threads:

        # add the Thread that's being removed to a list of threads to be outputted to the csv file.
        threads_to_add_to_the_csv.append(previous_thread_list[index])

        # remove the old thread at the specified index from the previous_thread_list
        previous_thread_list.pop(index)

        #print("Removed a thread from the old thread list.")


    print("\nAdded " + str(len(indexes_of_new_threads_not_found_in_old_threads)) + " threads from the new thread list to the old thread list.")

    # adds the new threads that are not in the list of old threads using the indexes of those new_threads
    for index in indexes_of_new_threads_not_found_in_old_threads:

        # adds the new_thread at the specified index to the list of old threads
        previous_thread_list.append(new_list[index])

        #print("Added a thread from the new thread list to the old thread list.")

    # prints the number of Threads in the previous_thread_list
    print("\n There are now " + str(len(previous_thread_list)) + " Threads in the previous_thread_list.")






    """
    # prints how many posts are in the previous_thread_list

    size = 0
    for thread in previous_thread_list:

        for post in thread.posts:

            size += 1

    print ("\nAfter removing duplicates it has " + str(size) + " posts.\n")
    """


    #print(str(len(previous_thread_list)) + " threads in old thread list.")
    #print(str(len(new_list)) + " threads in new thread list.")






    
    """
    
    # creating an empty list for the posts that aren't duplicates to be added to the csv file (dataset)
    list_without_duplicates = []
    
    # loops through the Thread objects in the new list
    for new_thread in new_list:

        # adds the String posts from the new_thread.posts list to list_without_duplicates
        list_without_duplicates.append(new_thread)
    """




    """
    # prints the number of new/unique posts that are from duplicate threads

    size = 0
    for thread in list_without_duplicates:

        for post in thread.posts:

            size += 1
    new_posts_from_duplicate_threads = size - non_duplicate_new_thread_post_size
    print("\nThere are " + str(new_posts_from_duplicate_threads) + " new non-duplicate posts from duplicate threads.")
    """


    # returns the list of Thread objects without 
    return threads_to_add_to_the_csv




# transforms the non_duplicate_list into an array
def list_to_NumPy_array(non_duplicate_list):

    # creating an empty NumPy array for the dataset
    arr = np.empty((1, 4), object)


    # looping through each thread in the THREADS list 
    for thread in non_duplicate_list:

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

    
    """
    # There are always 20 threads displayed on the homepage of 4Chan/pol
    #print(len(THREADS))
    """
    
    # prints the number of posts in each thread
    #for i in range(0, len(non_duplicate_list)):
        #print(len(non_duplicate_list[i].posts))
    
    # prints the shape of the NumPy array
    #print(arr.shape)


    # returns the list that's been converted into an array
    return arr




# writes the correct NumPy array of data to the dataset file
def write_to_dataset (array):

    # opening the dataset file
    writer_file = open(r"C:\Users\Jackson\Documents\Coding\4Chan-Web-Scraper\Pol_Forum_Dataset.csv", 'a', encoding='utf-8')

    # creating the writer for the csv file 
    writer = csv.writer(writer_file)

    # loops through every non-duplicate post in the list
    for post in array:

        # writes each post to the csv file
        writer.writerow(post)

    # closes the file
    writer_file.close()



    # takes the length of the list_without_duplicates list and saves it in the num_addd_posts variable
    num_added_posts = int(array.size / 4)
    
    # gets the datetime and converts it to a String
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    # prints the number of posts added to the database file
    print("Added " + str(num_added_posts) + " posts to csv file at time: " + current_time + ".\n\n\n\n")




# runs the main function if this is the file being run
if __name__=="__main__":
    
    # runs the main program once at the beginnning:   
    print("Starting Program: \n\n")

    # sets a list to hold Thread objects of previously added Threads and their lists of posts
    previous_thread_additions_to_csv_file = []

    # runs the web-scraping once
    data_collection_and_processing()

    """
    # prints the number of posts in the previous_thread_additions_to_csv_file

    size = 0
    for thread in previous_thread_additions_to_csv_file:

        for post in thread.posts:

            size += 1

    print ("\nThe comparator for the past iteration has " + str(size) + " posts.\n")
    """

    # runs the main program once every minute
    schedule.every().minute.do(data_collection_and_processing) 
    
    # loops and runs the scheduled job indefinitely every 1 seconds after 1 minute
    while True:  
        schedule.run_pending()
        time.sleep(1)


