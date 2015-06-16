"""
  FKRLBot -- calculates the Flesch-Kincaid Reading Level
            for each submission in a subreddit
  Licensed under MIT License
"""

import praw
import pdb
import re
import os
import string
import time
from config_bot import *

# quick n' dirty syllable counter from:
# http://www.howmanysyllables.com/howtocountsyllables.html
# syllabes for more complex words may be off by one 
def count_syllables(word):
  vowels = ["a", "e", "i", "o", "u", "y"]
  num_vowels = 0
  prev_is_vowel = False

  for c in word:
    found_vowel = False

    for v in vowels:
      if v == c and prev_is_vowel:
        found_vowel = True
        prev_is_vowel = True
        break
      elif v == c and not prev_is_vowel:
        num_vowels = num_vowels + 1
        found_vowel = True
        prev_is_vowel = True
        break
    if not found_vowel:
      prev_is_vowel = False

  if len(word) > 2 and ("es" in word[-2:]):
    num_vowels = num_vowels - 1;
  elif len(word) > 1 and ("e" in word[-1]):
    num_vowels = num_vowels - 1;

  return num_vowels


def title_score(nword, nsent, nsyl):
  return 206.835 - 1.015 * (nword / nsent) - 84.6 * (nsyl / nword)


def main():
  u_a = "Flesch-Kincaid Reading Level v0.0.1 by /u/__0xDEADBEEF)"
  r = praw.Reddit(user_agent = u_a)

  # see config_skel.py for username and password formatting
  r.login(REDDIT_USERNAME, REDDIT_PASSWORD, )

  # stores each post replied to's unique ID in a file
  already_done = []

  # currently works with only one subreddit
  subreddit = r.get_subreddit(REDDIT_SUB)
  num_posts = 10

  while True: 

    time.sleep(2)
    for submission in subreddit.get_hot(limit = num_posts):
      """
        TODO: 
        (4) output a sentence describing the readibility of 
            the title
        (5) submit the comment to all the new posts in a 
            subreddit
      """
      if not submission.id in already_done:
        # don't comment on a submission that we've already dealt with 
        already_done.insert(0, submission.id)

        title_string = submission.title
        title_words = title_string.split()

        num_words = len(title_words)

        # does not account for interrobangs b/c of their infrequency
        num_sentences = (title_string.count('.') + title_string.count('!') 
                          + title_string.count('?'))

        # if the title does not have any punctuation, 
        # then consider it as 1 sentence         
        if num_sentences < 1:
          num_sentences = 1

        total_syllables = 0

        for i in title_words:
          # regex to strip most common punctuation or special characters
          i = re.sub("[\.\t\,\:;\(\)\.\-\--]", "", i, 0, 0)
          i = i.lower()
          total_syllables = total_syllables + count_syllables(i)

        score = title_score(num_words, num_sentences, total_syllables)

        resp_corpus = ["an average 11 year old", 
                "an average 13-to-15 year old", 
                "an average college graduate"]

        submstr = ""

        if score >= 80:
          submstr = resp_corpus[0]
        elif score >= 60 and score <= 70:
          submstr = resp_corpus[1]
        elif score < 50:
          submstr = resp_corpus[2]

        comment = "The Flesch-Kincaid score for this submission is {0}. This score indicates the readibility of your title. Based on your score, the title of your sumbission can be understood easily by {1}.\n\n---\nFKRLBot v0.0.1 | [PM Feedback](http://www.reddit.com/message/compose/?to=__0xDEADBEEF)".format(score, submstr)

        submission.add_comment(comment)


if __name__ == "__main__":
  main()
