####################################################
# Name: Jackson Gregg
# Date: 1/25/2023
# Objective: The goal of this program is to run text analysis on the data in the 
# Pol_Forum_Dataset.csv file.  
####################################################


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

    # iterates through the rows of string data in the dataframe and formats them into the columns named above
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


    print("Clean Data Obtained.\n")


    # output the dataframe
    print(dataframe)




    # Now that I have prepared the dataframe correctly, I can 

    #
    from sklearn.feature_extraction.text import CountVectorizer

    # creates a vector that will hold the 
    # only includes words that appear in less than 90% of the document and 
    # appear in at least 2 documents
    count_vect = CountVectorizer(max_df=0.90, min_df=2, stop_words='english')
    
    # creates a document-term matrix where the rows are the seperate documents (in this case the text in posts) and
    # the columns are specific words. The values of this matrix are the number of times the word appears in the 
    # post text. 
    doc_term_matrix = count_vect.fit_transform(dataframe["Post Text"].values.astype('U'))


    #print(doc_term_matrix[0:10])
    # print(doc_term_matrix)





    # loops through the LDA topic modeling algorithm for different numbers of topics
    for i in range(3, 20):

        # groups the words based on the number of topics and the word vector
        topic_modeling(i, count_vect, doc_term_matrix)



    # Topics = 6


    







    



    










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


        # lemmatizer = WordNetLemmatizer()
        """
        

        Something this method fails to do is lemmatization (tenses are changed to present tense and everything is in first person)
        Also, words should be stemmed (reduced to the base/root form)
        """





    return unformatted_post




#
def topic_modeling(num_of_topics, count_vect, doc_term_matrix):

    # Latent Dirichlet Allocation is a 
    from sklearn.decomposition import LatentDirichletAllocation


    # n_components is the number of topics
    # random_state is a variable that controls the random assignment of words to topics during the first part of the algorithm
    LDA = LatentDirichletAllocation(n_components = num_of_topics, random_state = 42, max_iter=50)
    
    # 
    LDA.fit(doc_term_matrix)



    # collects the topics that the model outputed
    topics = LDA.components_[0:num_of_topics]

    #print(len(topics))

    
    # this iterator keeps track of which topic is being examined
    i = 1    

    # loops through every topic
    for topic in topics:

        print("\nTopic #" + str(i) + ":")

        top_10_words = topic.argsort() [-10:]

        # outputs the top 10 words that represent the topic
        for index in top_10_words:
            
            print(count_vect.get_feature_names_out()[index])

        i += 1






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

"""
# creating 2 lists 'ids' and 'marks'
    sentiment_scores = []
    topic_identities = []

    # Creating columns 'ID' and 'Uni_marks' 
    # using Dictionary and zip()
    dataframe["Sentiment Score"] = dict(zip(sentiment_scores, dataframe["Thread Title"]))
    dataframe["Topic Identity"] = dict(zip(topic_identities, dataframe["Thread Title"]))



# print(dataframe["Post Text"][100])




    print("\n\n\n\n")

"""



"""
Creates two new columns Sentiment Score and Topic Identity
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




"""
Loops through each row in the dataset and sets the values of the two new columns to
the values of the sentiment analysis and topic analysis generated from the Post Text
String
    
For topic analysis, the number of words that need to be included in the topic for 
it to count as a post underneath that topic should be a percentage of the number of 
(non-stopword and meaningful) words in the post.    
"""    





"""

from gensim import matutils, models
import scipy.sparse

term_doc_matrix = doc_term_matrix.transpose

term_doc_matrix.head()



sparse_counts = scipy.sparse.csr_matrix(term_doc_matrix)
corpus = matutils.Sparse2Corpus(sparse_counts)

"""