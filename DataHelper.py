import numpy as np
from bs4 import BeautifulSoup as soup
import requests
from langdetect import detect
import spacy
import re
import requests

class DataHelper:
    """
    this function loads the website using requests 
    please note the following most of website will refuse the connection as its automated 
    Input:
    --------
    String:url 
     the url of the website
    Output:
    -----------
    String : website
    the html of the loaded website
    """ 

    def load_website(self,url):
        website = requests.get(url)
        
        return website
    """
    this function cleans the data after being loaded in spacy it removes:-
        stop words, puncitation, spaces, brackets, quotation marks, ascii symbols and currency symbols
    Input:
    --------
    Spacy.doc: doc
        the doc of the data after being loaded into spacy
    Returns:
    List<String>:words
        the remaning words after removing the stop words, symbols, spcaes ... etc"""
    def clean_words(self, doc):
        words = []
        for token in doc:
            if not token.is_stop and not token.is_punct and not token.is_space\
            and not token.is_bracket and not token.is_quote and token.is_ascii and not token.is_currency:
                words.append(token.text)
        return words

    """
    this function removes the html from the loaded website and the sequnces of whitesspaces and new
    lines 
    input
    -----------
    String: text
        the loaded website html 
    Returns:
    String: clean_text
    """
    def clean_data(self,text):
        ##remove the html tags from the data
       
        cleantext = soup(text, "html").text
        #remove the sequnces of whitespaces or new lines 
        r = re.compile(r"^\s+", re.MULTILINE)
        clean_text = r.sub("", cleantext) # "a\nb\nc"
        
        return clean_text
    """
    this function detects the language of the website
    Input
    --------
    String:text
    
    Returns:
    String
        the detected language of the webiste
    """
    def detect_lang(self,text):
        
        return  detect(text)