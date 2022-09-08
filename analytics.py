import pandas as pd
import numpy as np



# imports the libraries needed to work with csv files
import csv
import os



# imports datetime to store time data in objects
from datetime import datetime











# to run this program, type this into the anaconda prompt:
# python C:\Users\jacks\OneDrive\Desktop\Coding\4Chan-Web-Scraper\analytics.py

print("doing data analytics")

# creates the dataframe from the csv file
dataframe = pd.read_csv(r"C:\Users\jacks\OneDrive\Desktop\Coding\4Chan-Web-Scraper\Pol_Forum_Dataset.csv", header= None)

# adds the correct label names to the dataframe object
formatted_df = dataframe.rename(columns={0: "Thread Title", 1: "Country of Origin", 2: "Date and Time", 3: "Post Text"})



# data cleaning 
# checking that every data type is what it should be



# ranking posts based on ------- racism, anti-semitism, homophobia, sexism




# output the dataframe
print(formatted_df)



# "Thread Title","Country of Origin","Date and Time","Post Text"

# Name,Team,Number,Position,Age,Height,Weight,College,Salary

#dataframe = pd.read_csv(r"C:\Users\jacks\OneDrive\Desktop\Coding\4Chan-Web-Scraper\nba.csv", header=None)
