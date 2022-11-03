# import basic libs
import pandas as pd
import numpy as np

# imports the libraries needed to work with csv files
import csv
import os

# imports datetime to store time data in objects
from datetime import datetime

# imports tensorflow libraries
import tensorflow as tf
from tensorflow import keras

# imports libraries to clean data
import nltk
from nltk.corpus import stopwords
import re
import string 


# import library to split train and test
from sklearn.model_selection import train_test_split

# imports library to Vectorize words in a String
from sklearn.feature_extraction.text import CountVectorizer




# to run this program, type this into the anaconda prompt:
# python C:\Users\jacks\OneDrive\Desktop\Coding\4Chan-Web-Scraper\analytics.py
# python C:\Users\Jackson\Documents\Coding\4Chan-Web-Scraper\analytics.py





# the main program
def main():

    # creates the dataframe from the csv file
    dataframe = pd.read_csv(r"C:\Users\Jackson\Documents\Coding\4Chan-Web-Scraper\Pol_Forum_Dataset.csv", header= None)

    # adds the correct label names to the dataframe object
    # "Thread Title","Country of Origin","Date and Time","Post Text"
    dataframe = dataframe.rename(columns={0: "Thread Title", 1: "Country of Origin", 2: "Date and Time", 3: "Post Text"})


    
    # removes null rows
    dataframe.dropna()

    # iterates through the string data in the dataframe and formats them
    for row in range(0, int(dataframe.size / 4)):
        
        # formats text for the Thread Title column
        original_post = dataframe.at[row, "Thread Title"]
        
        # replaces the original unformatted String with the formatted String
        if (original_post != ""):
            dataframe.at[row, "Thread Title"] = format_text(original_post)


        # formats text for the Post Text column
        original_post = dataframe.at[row, "Post Text"]

        # replaces the original unformatted String with the formatted String
        dataframe.at[row, "Post Text"] = format_text(original_post)


    print("Clean Data Obtained.")


    # output the dataframe
    print(dataframe)







    print(dataframe["Post Text"][100])




    print("\n\n\n\n")






    from sklearn.feature_extraction.text import CountVectorizer

    # only includes words that appear in less than 80% of the document and 
    # appear in at least 2 documents
    count_vect = CountVectorizer(max_df=0.8, min_df=2, stop_words='english')
    
    #
    doc_term_matrix = count_vect.fit_transform(dataframe["Post Text"].values.astype('U'))


    print(doc_term_matrix[100:110])


    print(doc_term_matrix)





    from sklearn.decomposition import LatentDirichletAllocation

    LDA = LatentDirichletAllocation(n_components=5, random_state=42)
    LDA.fit(doc_term_matrix)



    import random

    for i in range(10):
        random_id = random.randint(0,len(count_vect.get_feature_names()))
        print(count_vect.get_feature_names()[random_id])



    first_topic = LDA.components_[0]












# formats a String to remove unclean data
def format_text(unformatted_post):

    # if the an empty float, then turn it into a String
    if (type(unformatted_post) == float):
        unformatted_post = str(unformatted_post)

    # else the type is a String, then clean the String
    else:
        # make the post all lower case
        unformatted_post = unformatted_post.lower()

        # removing unicode characters    
        unformatted_post = unformatted_post.encode('ascii', 'ignore').decode()

        # removing stop words
        stop_words = stopwords.words("english")
        unformatted_post = ' '.join([word for word in unformatted_post.split(' ') if word not in stop_words])           # where x is a string
        
        # remove mentions
        unformatted_post = re.sub("@\S+", " ", unformatted_post)

        # remove Hashtags
        unformatted_post = re.sub("#\S+", " ", unformatted_post)

        # removes links/URLs
        unformatted_post = re.sub("https*\S+", " ", unformatted_post)

        # removes punctuations
        unformatted_post = re.sub('[%s]' % re.escape(string.punctuation), ' ', unformatted_post)
        
        # removes apostrophes like Jimmy's
        unformatted_post = re.sub("\'\w+", '', unformatted_post)

        # remove numbers
        #unformatted_post = re.sub(r'\w*\d+\w*', '', unformatted_post)

        # remove the extra spaces
        unformatted_post = re.sub('\s{2,}', " ", unformatted_post)


    return unformatted_post











# runs the main function if this is the file being run
if __name__=="__main__":
    
    # runs the main program once at the beginnning:   
    print("Starting Data Analytics: \n\n") 


    # runs the main program
    main()








 






































"""
# ranking posts based on ------- racism, anti-semitism, homophobia, sexism

labels = ["Racism", "Anti-Semitism", "Homophobia", "Sexism"]


print(tf.version.VERSION)
print(len(tf.config.list_physical_devices('GPU')) > 0)
"""











# splitting data into labels and features 
#y = data.temp
#X = data.drop('temp', axis=1)  

# split the dataset into training and test
#X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2)





# writing individual words from each
#for word in dataframe["Post Text"]:

    # write each unique word to vocab.csv





# creating a vocabulary containing all the words each user ever posted on 4Chan/pol with the database

