import json 
import torch
from datetime import datetime
from collections import defaultdict
import pandas as pd 
import numpy as np

from autocorrect import Speller
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModelWithLMHead

## ElasticSearch Connector
es = Elasticsearch(hosts="http://localhost:9200")
index = 'song-corpus'

def query_search(q, n=0):
    try:
        if n == 0:
            resp = es.search(index=index, query=q)
        else:
            resp = es.search(index=index, query=q, size=n)
        resp = resp['hits']['hits']
        # print('hits >> ', resp)
    except Exception as e:
        print(f"{'>'*10} ES Search Error {'<'*10} \n {e} \n ")
        resp = []
    
    return resp 

def get_all_data(hits):
    all_annotation = []
    all_data = {"Singer": [], "Musician": [], "Writer": [], "Topic": [], "Song": []}

    for h in hits:
        h = h['_source']
        all_annotation.extend(h['Annotation'])
        try:
            all_data['Singer'].append(h['Singer'])
        except:
            pass 

        try:
            all_data['Musician'].append(h['Music'])
        except:
            pass 

        try:
            all_data['Writer'].append(h['Lyrics'])
        except:
            pass 

        try:
            all_data['Topic'].append(h['topic'])
        except:
            pass 
        
        try:
            all_data['Song'].append(h['title'])
        except:
            pass 

        all_data['Metaphor'] = [i['Metaphore'] for i in all_annotation]
        all_data['Object_Sinhala'] = [i['Object-sinhala'] for i in all_annotation]
        all_data['Object_English'] = [i['Object-english'] for i in all_annotation]
        all_data['Subject_Sinhala'] = [i['Subject-sinhala'] for i in all_annotation]
        all_data['Subject_English'] = [i['Subject-english'] for i in all_annotation]

    return all_data, all_annotation


# ==========================================================================
# ===================== Auxiliary Functions ================================

def spellingCorrector(text):
    spell = Speller(lang='en')
    correction = spell(text)
    return correction

def textSimilarity(texts):
    model = SentenceTransformer('bert-base-nli-mean-tokens')
    sentence_embeddings = model.encode(texts)
    sims = cosine_similarity(
        [sentence_embeddings[0]],
        sentence_embeddings[1:]
    )[0]

    return sims

def textSummarization(text):
    tokenizer = AutoTokenizer.from_pretrained('t5-base')
    model = AutoModelWithLMHead.from_pretrained('t5-base', return_dict=True)

    inputs = tokenizer.encode("summarize: " + text, return_tensors='pt', max_length=512, truncation=True)
    summary_ids = model.generate(inputs, max_length=15, min_length=5, length_penalty=5., num_beams=2)
    summary = tokenizer.decode(summary_ids[0])
    return summary 


def get_frequency(arr, normalized=False):
    if type(arr) == list:
        arr = np.array(arr)
    t, c = np.unique(arr, return_counts=True)
    
    if normalized:
        c = c/c.sum()
    return t, c.tolist()



    