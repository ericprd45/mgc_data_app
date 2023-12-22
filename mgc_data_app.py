import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import pickle
import re
import time
import os
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
#from plotly.subplots import make_subplots
import matplotlib.dates as mdates
import plotly.express as px


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

    data = pd.read_csv("C:/Users/eric_/Projects/mgc_data_app/data/api_transaction.csv")

    frequence = st.selectbox(
     "Sélectionner la fréquence d'analyse",
     ('Jour', 'Semaine', 'Mois', 'Année'))

    frequence_mapper = {'Jour':'d','Semaine':'w','Mois':'M','Année':'a'}
    data.lastTransitionedAt = pd.to_datetime(data.lastTransitionedAt)
    data['istransaction'] = data.lastTransition.apply(lambda x : map_transaction(x))
    freq_transac = data.groupby(pd.Grouper(key='lastTransitionedAt',freq=frequence_mapper[frequence])).sum()['istransaction']
    freq_transac = pd.DataFrame(freq_transac).reset_index()
    #st.dataframe(freq_transac)

    fig = px.bar(freq_transac, x=freq_transac.lastTransitionedAt, y='istransaction')
    fig.update_layout(title=f"Nombre de transaction par {frequence}", autosize=True,
                  #width=800, height=400,
                  margin=dict(l=40, r=40, b=40, t=40))
    st.plotly_chart(fig)