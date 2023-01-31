

import os

import pandas as pd
from sympy import Q


# imports HashTable class
from HashTable import HashTable





















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






















#      Thread#,   Num1/Num2/Num3/Num4/Num5,

# The thread# could come from a hashmap or 
# It could just be an index like a the latest one is the last_thread_num + 1


"""
# 
def get_last_thread_number ():

    # opening the dataset file
    reader_file = open(r"", 'r', encoding='utf-8')

    # creating the reader for the csv file 
    reader = csv.reader(reader_file)


    # sets the default value of post to None if there were no rows of data in the csv file
    post = None

    # loops through every post in the csv file
    for post in reader:

        # passes through each post
        pass

    # closes the file
    reader_file.close()

    #
    print(post)

    #
    post_attributes = post.split(',')

    print(int(post_attributes[0]))

    # returns the last 
    return int(post_attributes[0])














# tells users that it is running again
print("\nScanning /pol for new posts...")


# the url we are using to draw text data
url = "https://boards.4chan.org/pol/"


# gets the soup of the page
soup = get_soup_from_page(url)

# gets the data into a list of Thread Objects
list_of_threads = scrape_to_list(soup)

# check for duplicate threads in the NumPy array and the dataset
non_duplicate_list = remove_duplicates(list_of_threads, previous_thread_additions_to_csv_file)


size = 0

for thread in previous_thread_additions_to_csv_file:

    for post in thread.posts:

        size += 1

print ("\nThe comparator for the past iteration has been updated to include a total of " + str(size) + " posts.\n")

# transforms the non_duplicate_list into an array
array = list_to_NumPy_array(non_duplicate_list)

# add NumPy array to the dataset file
write_to_dataset(array)
    
    
    
    
    




print("Added " + str(len(indexes_to_add_new_posts_to_old_list)) + " posts from a shared thread to the old thread.posts list")

#
try:

    # loops through the specified indexes of the new_list of posts in this new_thread and 
    # appends each new addition to the old_thread.posts list 
    for index in indexes_to_add_new_posts_to_old_list:

        # adds the posts from the new_list of posts at the specified indexes
        old_thread.posts.append(new_thread.posts[index])

        #print("Added a post from a shared thread to the old thread.posts list")

# 
except:
    print("A   TypeError: 'NoneType' object is not iterable    exception occurred")







print("Deleted " + str(len(indexes_to_delete_new_posts)) + " duplicate posts from the new thread")
#print(indexes_to_delete_new_posts)

#
try:

    # reverses the order
    indexes_to_delete_new_posts.reverse()
    
    # loops through the specified indexes of the new_list of posts in this new_thread backwards 
    # and deletes each duplicate
    for index in indexes_to_delete_new_posts:

        # deletes the posts at the specified indexes
        new_thread.posts.pop(index)

        print("Removed a duplicate post from a shared thread.")

# 
except:
    print("A   TypeError: 'NoneType' object is not iterable    exception occurred")
















Search through the csv file for posts that are in the 20 threads on the homepage of pol

For each post in the csv file that is in one of the 20 threads 
	Compare it with the posts in the numpy array to see if there are any duplicates. 
	If there are duplicates:
		Remove the duplicates from the NumPy array

After searching through all the posts (rows) of the csv file, add the remaining NumPy 
array rows to the end of the csv file. 




I could make some mathematical function that keeps track of what I add to the csv file
and only sorts through a certain number of posts (rows) at the bottom of the file. 

Could keep track of:

- number of posts added to the csv file   (would grow as the program keeps running)
- number of duplicates removed
- how many threads are being used repeatedly from run of the program. 



Also figure out how to remove the moderator pinned messages from showing up in
the csv file (dataset)






List of Errors:

Max Retries Exceeded With Url Error - Resolved: Attempted, but Unknown
https://linuxpip.org/fix-max-retries-exceeded-with-url-error-python/#Unstable_internet_connection_server_overload





    


 

# remove everything in the original csv file.
file = r"url.com"

if(os.path.exists(file) and os.path.isfile(file)):
    os.remove(file)
    #print("File deleted")
else:
    #print("File not found")



"""