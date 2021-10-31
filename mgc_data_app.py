import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import pickle
import re
import time
import os.path
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
#from plotly.subplots import make_subplots
import matplotlib.dates as mdates


# from Project Workspace
from utils.utils import *
#fromtabs import fundamental_analysis


#######################  Page and sidebar config  #######################

st.set_page_config(page_title='MGC Data Dashboard', page_icon=None, layout='wide', initial_sidebar_state='auto')

st.sidebar.title('MGC dashboard')

navigation = st.sidebar.radio("Navigation",('Home','Transactions','Propriétaires','Locatrices','Listings'))

st.sidebar.markdown('---')



#######################  Tabs  #######################


####################### Tab 1 : Transactions #######################


if navigation=='Transactions':

    data = pd.read_csv("./data/api_transaction.csv")
    st.dataframe(data)

    data.lastTransitionedAt = pd.to_datetime(data.lastTransitionedAt)
    data['istransaction'] = data.lastTransition.apply(lambda x : map_transaction(x))
    transac_by_date = data.groupby(pd.Grouper(key='lastTransitionedAt',freq='m')).sum()['istransaction']
    transac_by_date = pd.DataFrame(transac_by_date).reset_index()

    fig, ax = plt.subplots(constrained_layout=True)
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    #formatter = mdates.AutoDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    ax.bar(transac_by_date.lastTransitionedAt,transac_by_date.istransaction, width = 10)
    ax.set_title('Transaction Per Month')
    st.pyplot(fig)
