# Usual libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from matplotlib import rcParams
import seaborn as sns

# Other libraries
import requests
from urllib.request import urlopen
import json
#from jsonpath_rw import jsonpath
#from jsonpath_rw_ext import parse
#import jsonpath_rw_ext as jp
#import streamlit as st
#from binance.client import Client
#import feedparser

# from workspace
#from utils.constants import *


####################################################### FORMATTING #######################################################################

def map_transaction(x):
    if x in ['transition/complete','transition/review-2-by-customer',
             'transition/review-1-by-provider','transition/review-2-by-provider',
             'transition/review-1-by-customer','transition/expire-review-period',
             'transition/expire-provider-review-period','transition/expire-customer-review-period',
             'transition/accept'
            ]:
        return 1
    else : 
        return 0
    