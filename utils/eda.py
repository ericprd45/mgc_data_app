from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from ipywidgets import FloatSlider
import pandas as pd

class DataFrameExplorer:
    def __init__(self,dataframe):
        self.dataframe = dataframe
        
    def col_proportion(self,col,max_occurences = 15):
        temp = (pd.DataFrame(
                self.dataframe[col].value_counts())
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
    
    def interactive_col_proportion(self):
        interact_manual(self.col_proportion,col=list(self.dataframe.columns),max_occurences=widgets.IntSlider(min=5, max=30, step=1, value=10))
    
    def interactive_parallel_categ_duo(self):
        pertinent_cols = self.get_pertinent_categ_columns()
        interact_manual(self.two_dim_parallel_categ_v2,col_1 = pertinent_cols, col_2 =pertinent_cols)
    
    def two_dim_parallel_categ_v2(self,col_1, col_2):
        # Create dimensions
        dim_1 = go.parcats.Dimension(values=self.dataframe[col_1],categoryorder='category ascending')
        dim_2 = go.parcats.Dimension(values=self.dataframe[col_2],categoryorder='category ascending')

        #wk_data['color'] = wk_data['precipType'].map({'no precip': 1, 'rain': 2, 'sleet': 3,'snow':4})

        # Create parcats trace
        #color = active_simo.data_envelope;

        fig = go.Figure(data = [go.Parcats(dimensions=[dim_1, dim_2],
            line={ 'colorscale': 'blues'},
            hoveron='color', hoverinfo='count+probability',
            labelfont={'size': 18, 'family': 'Times'},
            tickfont={'size': 16, 'family': 'Times'},
            arrangement='freeform')])

        fig.show()
        
    def get_pertinent_categ_columns(self) :
        pertinent = list()
        for column in self.dataframe.columns:
            if self.dataframe[column].dtypes == 'object':
                n_unique_values = self.dataframe[column].astype(str).nunique() 
                atomicity = n_unique_values / self.dataframe.shape[0]
                if n_unique_values > 1 and atomicity <= 0.9 :  
                    pertinent += [column]
        if len(pertinent) == 0 :
            print ('No pertinent category column for analysis (only ids, or unique-value columns)')
        return pertinent
    
    def get_numeric_columns(self) :
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        num_cols = list(self.dataframe.select_dtypes(include=numerics).columns)
        return num_cols