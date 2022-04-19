#using spacy parser:
import spacy
#import benepar 
import numpy as np
#from spacy.language import Language
nlp = spacy.load('en_core_web_md')
# if spacy.__version__.startswith('2'):
#     nlp.add_pipe(benepar.BeneparComponent("benepar_en3_large"))
# else:
#     nlp.add_pipe("benepar", config={"model": "benepar_en3_large"})
    

def spacySplit(question):
    # splitting based on spacy tokenization ( instead of string.split() )
    #input:
        # question: an string that needs to be tokenized
    #output:
        # parsed:   list of Tokenized terms
    doc = nlp(question)
    parsed=[]
    for i in doc:
        parsed.append(i.text)
    return parsed