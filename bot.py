import praw
import pdb
import re
import os
from config_bot import *

"""
  FKRBot -- calculates the Flesch-Kincaid Reading Level
            for submission titles in all subreddits
  Licensed under GPLv3
"""

if not os.pathisfile("config_bot.py"):
  print """ Please create a config file containing the 
            username and password for your bot. 

            Please see config_skel.py """
  exit(1)


u_a = "Flesch-Kincaid Reading Level v0.0.1 by /u/__0xDEADBEEF)"
r = praw.Reddit(user_agent = u_a)

subreddit = r.get_subreddit("pythonforengineers")


r.login()

