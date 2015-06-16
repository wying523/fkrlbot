"""
  FKRBot -- calculates the Flesch-Kincaid Reading Level
            for each submission in a subreddit
  Licensed under MIT License
"""

import praw
import pdb
import re
import os
import string
from config_bot import *


def count_syllables(word):
  vowels = ["a", "e", "i", "o", "u", "y"]
  num_vowels = 0
  last_char_was_vowel = False

  for c in word:
    found_vowel = False
    for v in vowels:
      if v == c && last_char_was_vowel:
        found_vowel = True
        last_char_was_vowel = True
        break
      elif v == c && !last_char_was_vowel
        num_vowels = num_vowels + 1
        found_vowel = True
        last_char_was_vowel = True
        break
    if not found_vowel:
      last_char_was_vowel = False

  if len(word) > 2 && ("es" in word[-2:])
    num_vowels = num_vowels - 1;
  elif len(word) > 1 && ("e" in word[-1])
    num_vowels = num_vowels - 1;
  return num_vowels

def title_score(num_words, num_sentences, num_syllables):
  return 206.835 - 1.015(num_words/num_sentences) - 84.6(num_syllables/num_words)


u_a = "Flesch-Kincaid Reading Level v0.0.1 by /u/__0xDEADBEEF)"
r = praw.Reddit(user_agent = u_a)


# see config_skel.py for username and password formatting
r.login(REDDIT_USERNAME, REDDIT_PASSWORD)


# stores each post replied to's unique ID in a file
# 


already_done = []

subreddit = r.get_subreddit("news")
num_posts = 10
for submission in subreddit.get_hot(limit = num_posts):
  """
    TODO: 
    (1) count the number of words
    (2) count the number of sentences
    (3) calculate the Flesch-Kincaid score
    (4) output a sentence describing the readibility of 
        the title
    (5) submit the comment to all the new posts in a 
        subreddit
  """
  title_string = submission.title
  title_arr = title_string.split()

  num_words = len(title_string.split())

  # does not account for interrobangs
  num_sentences = (title_string.count('.') + title_string.count('!') 
                    + title_string.count('?'))
  # if the title does not have any punctuation, then consider it as 1 sentence         
  if num_sentences < 1:
    num_sentences = 1

  total_syllables = 0

  for i in title_string.split():
    i = i.translate(None, "?.!/;:-")
    i = i.lower()
    total_syllables = total_syllables + count_syllables(i)

  score = title_score(num_words, num_sentences, num_syllables)




