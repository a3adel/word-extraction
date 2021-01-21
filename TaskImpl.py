from sent2vec.vectorizer import Vectorizer
from scipy import spatial
from DataHelper import DataHelper
import spacy
import numpy as np
import json


class TaskImpl:
    """
    this function is the entry point of the task and it takes the url and keywords as input and returns the 
    most important words as output by measuring the distance between the scentences 
    
    Input:
    --------------
    String:url
        the url of the website
    List<String>: keywords
        the keywords to get the closest words to from the website
        
    Returns:
    ---------------
    List<String>:important_words
    
    """
    def run(self, url,keywords):
        helper = DataHelper()
        website = helper.load_website(url)
        clean_body = helper.clean_data(website.text)
        lang = helper.detect_lang(clean_body)
        nlp = self.get_spacy_model(lang)
        doc = nlp(clean_body)
        words = list(set(helper.clean_words(doc)))
        for i in range(len(keywords)):
            words.insert(i,keywords[i])
        words_vectors = self.get_scent_vectors(words)
        nearest_words_indecies = self.get_nearest_words_indecies(keywords_length=len(keywords),vectors = words_vectors)
        nearest_words = []
        for index in nearest_words_indecies:
            nearest_words.append(words[index])
        return nearest_words
    """
    This function takes the website langugae key and returns the spacy model that supports the language
    Input
    ----------
    String: lang
        the language key
    Returns:
    Spacy:nlp 
        the model that supports the language
    Exception:
        If the language is not supported
    """
    def get_spacy_model(self,lang):
        try:
            print(lang)
            spacy_model = {"en":"en_core_web_sm","de":"de_core_news_sm","fr":"fr_core_news_sm"}
            nlp = spacy.load(spacy_model[lang])
            return nlp
        except:
            raise Exception(lang," is not supported, please install it") 
    """
    This function returns the vectors of the words using Bert model
    Input:
    List<String>:words
        the words to get the vector to
    Returns:
    List<Vectors>:vectors_bert
        the list of vectors of the word embeddings 
    
    """        
    def get_scent_vectors(self,words):
        vectorizer = Vectorizer()
        vectorizer.bert(words)
        vectors_bert = vectorizer.vectors
       
        return vectors_bert
    
    def get_nearest_words_indecies(self,keywords_length,vectors,number_of_nearest_words = 10):
        total_distances = []
        
        for keyword_index in range(keywords_length):
            distances = []
            for i in range(len(vectors)):
                distance = spatial.distance.cosine(vectors[keyword_index], vectors[i])
                distances.append(distance)
            total_distances.append(distances)

        final_distances_indecies = []    
        for distances in total_distances:
            ind = np.argsort(distances)
            ind = ind[0:number_of_nearest_words]
            
            for index in ind:
                if index not in final_distances_indecies:
                    final_distances_indecies.append(index)
        result = np.sort(final_distances_indecies)          
        return final_distances_indecies