# Usual libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from matplotlib import rcParams
import seaborn as sns

from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from ipywidgets import FloatSlider
import plotly.graph_objects as go
import plotly.express as px

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


transitions = ['customer | confirm-payment',
 'customer | enquire',
 'customer | request-payment',
 'customer | request-payment-after-enquiry',
 'customer | review-1-by-customer',
 'customer | review-2-by-customer',
 'operator | cancel',
 'operator | decline',
 'provider | accept',
 'provider | decline',
 'provider | request-payment',
 'provider | review-1-by-provider',
 'provider | review-2-by-provider',
 'system | complete',
 'system | confirm-payment',
 'system | expire']


####################################################### FORMATTING #######################################################################

def map_transaction(x):
    if x in ['transition/complete', 'transition/accept',
             'transition/review-2-by-customer','transition/review-2-by-provider',
             'transition/review-1-by-provider','transition/review-1-by-customer',
             'transition/expire-review-period','transition/expire-provider-review-period','transition/expire-customer-review-period',
            ]:
        return 1
    else : 
        return 0

def col_proportion(dataframe,col,max_occurences = 15):
    temp = (pd.DataFrame(
            dataframe[col].value_counts())
           )
    if isinstance(col,list):
        temp.rename(columns={0:'count'},inplace=True)
        if ('NA','NA') in temp.index:
            print(f"There are {'{:.1%}'.format(temp.loc[('NA','NA'),'count']/temp['count'].sum())} missing values")
            temp.drop(index=('NA','NA'),inplace=True)
        temp['proportion'] = temp['count']/temp['count'].sum()
        temp = temp.head(max_occurences)
        temp = temp.style.format({'proportion': "{:.1%}"}).bar(subset='count',width = 80,vmin=0)
    else:
        if 'NA' in temp.index:
            print(f"There are {'{:.1%}'.format(temp.loc['NA',col]/temp[col].sum())} missing values")
            temp.drop(index='NA',inplace=True)
        temp ['proportion'] = temp[col]/temp[col].sum()
        temp = temp.head(max_occurences)
        temp = temp.style.format({'proportion': "{:.1%}"}).bar(subset=col,width = 80,vmin=0)
    return temp
    
def get_histo_transition(transition):
    ''' transition as a dictionnary, get by and transition informations'''
    if isinstance(transition,dict):
        return transition['~:by'].replace('~:','') +' | ' + transition['~:transition'].replace('transition/','')
    else :
        return None

def get_histo_transition_date(transition):
    ''' transition as a dictionnary, get date information'''
    if isinstance(transition,dict):
        return transition['~:createdAt'].replace('~t','')[:10]
    else :
        return None

def get_histo_transition_hour(transition):
    ''' transition as a dictionnary, get date information'''
    if isinstance(transition,dict):
        return transition['~:createdAt'].replace('~t','')[11:19]
    else :
        return None

def get_transition_histo_details(data,key,freq,transition):
    by_freq = (pd.DataFrame(
                data.groupby(pd.Grouper(key = key,freq = freq))
                .sum()
                [transition]
                )
                .reset_index()
                .melt(id_vars=[key])
                .rename(columns={'variable':'transition'})
                )
    return by_freq

    def plot_transition_histo_details(key,freq,transition):
        data = data_expl_dummies
        by_freq = get_transition_histo_details(data,key,freq,transition)
        fig = px.bar(by_freq, x=key, y = 'value')
        fig.show()

    def interactive_plot_transition_histo_details(data,key):       
        interact_manual(plot_transition_histo_details, key = key, freq = ['d','w','m','y'] , transition = transitions)

def value_counts_of_X_by_Y(dataframe,X,Y):
    '''
    Returns value counts of column X by values of Y
    '''
    temp = (pd.DataFrame(
            pd.crosstab(dataframe[Y],dataframe[X])
        .ne(0)
        .sum(1)
        .sort_values(ascending = False))
           )
    temp = temp.rename(columns={0:'count'})
    temp ['proportion'] = temp['count']/dataframe[X].nunique()
    temp = temp.style.format({'proportion': "{:.1%}"}).bar(subset='count',width = 80,vmin=0)
    return temp
