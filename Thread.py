import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

#
import Post



class Thread:
    
    # the posts=[] is there because python doesn't support multiple constructors
    # thus, by default posts is an empty list when it is the constructor is called
    # without posts given as an argument
    def __init__(self, title, string_id, posts=[]):
        self.title = title
        self.id = string_id
        self.posts = posts

    # creates a way to set the posts 
    def set_posts(self, new_posts):
        self.posts = new_posts
    
