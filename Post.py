import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np





class Post:
    def __init__(self, countryOfOrigin, time, text):
        self.country = countryOfOrigin
        self.time = time
        self.text = text
    
    
    
    
