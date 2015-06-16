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


def fkrl(nword, nsent, nsyl):
  return 206.835 - 1.015 * (nword / nsent) - 84.6 * (nsyl / nword)

def fkgl(nword, nsent, nsyl):
  return 0.39 * (nword / nsent) + 11.8 * (nsyl / nword) - 15.59


def main():
  u_a = "Flesch-Kincaid Reading Level v0.0.4 by /u/__0xDEADBEEF)"
  r = praw.Reddit(user_agent = u_a)

  # see config_skel.py for username and password formatting
  r.login(REDDIT_USERNAME, REDDIT_PASSWORD)

  # stores each post replied to's unique ID in a file
  already_done = []

  # currently works with only one subreddit
  subreddit = r.get_subreddit(REDDIT_SUB)
  num_posts = 10

  num_comments = 0;
  while True: 
    for submission in subreddit.get_new(limit = num_posts):
      # wait 2 seconds between each submission
      time.sleep(2)
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

        reading_lvl = fkrl(num_words, num_sentences, total_syllables)
        grade_lvl = fkgl(num_words, num_sentences, total_syllables)

        resp_corpus = ["easy to read", 
                      "readable, but its clarity could be improved with very minor tweaks",
                      "somewhat readable, but its clarity could be improved with some tweaks", 
                      "hard to read -- please rephrase your future titles for clarity"]  

        submstr = ""

        if reading_lvl >= 90:
          submstr = resp_corpus[0]
        if reading_lvl > 70 and reading_lvl < 90:
          submstr = resp_corpus[1]
        elif reading_lvl >= 60 and reading_lvl <= 70:
          submstr = resp_corpus[2]
        elif reading_lvl < 50:
          submstr = resp_corpus[3]

        score_str = "Your post has a Flesch-Kincaid score of {}. This score indicates the readability of your title. ".format(reading_lvl)
        recmd_str = "Based on this score, this submission's title is {}. ".format(submstr)
        grade_lvl_str = "An average student in grade {} or higher shouldn't have an issue reading your title.".format(int(grade_lvl + 0.5))
        cmt_ftr = "\n\n---\nFKRLBot v0.0.4 | [Want to leave feedback? Shoot me a PM!](http://www.reddit.com/message/compose/?to=__0xDEADBEEF) | [Source](https://github.com/achiwhane/fkrlbot)"

        comment = score_str + recmd_str + grade_lvl_str + cmt_ftr

        submission.add_comment(comment)
        time.sleep(2)
        num_comments = num_comments + 1
        print "Submissions commented on so far: {}".format(num_comments)

if __name__ == "__main__":
  main()
