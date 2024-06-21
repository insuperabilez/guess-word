import numpy as np
from scipy.spatial.distance import euclidean
from scipy.spatial.distance import cosine
from navec import Navec
import random

def load_navec(path):
    navec = Navec.load(path)
    return navec

def load_words(path):
    with open(path,'r',encoding='utf-8') as f:
        words = f.read().splitlines()
    return words

def cos_dist(navec, word1, word2):
  vector1 = navec[word1]
  vector2 = navec[word2]
  return cosine(vector1, vector2)

def euc_dist(navec, word1, word2):
  vector1 = navec[word1]
  vector2 = navec[word2]
  return euclidean(vector1, vector2)

def generate_distances(keyword, words, navec):
  wordlist={}
  for word in words:
    wordlist[word]=cos_dist(navec,keyword,word)
  wordlist = [k for k, v in sorted(wordlist.items(), key=lambda item: item[1])]
  return wordlist

def sample_word(words):
  return random.choice(words)

def get_distances(keyword,words,navec):
  distances = generate_distances(keyword,words,navec)
  return distances

def check_number(word,distances):
  try:
    index = distances.index(word)
  except ValueError:
    index = -1
  return index
