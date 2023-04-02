import pandas as pd
import numpy as np
from sklearn import base
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline,FeatureUnion
from sklearn.neighbors import NearestNeighbors
import re


#Check if Ingredient list contains allergen item

def containsAllergen(df,allergen):
    return df[ df['Ingredient'].str.contains(allergen.strip(), na=False,case=False)==False]



#Feature engineering
class DictEncoder(base.BaseEstimator, base.TransformerMixin):
    
    def __init__(self, col):
        self.col = col
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        
        def to_dict(l):
            try:
                return {x.strip(): 1 for x in l}
            except TypeError:
                return {}        
        return X[self.col].apply(to_dict)


def recommender(df,product, allergen):
    df_1=df.copy()
    df_1['Ig_list']=df.apply(lambda x:x['Ingredient'].split(','),axis=1)
    ig_pipe = Pipeline([('encoder', DictEncoder('Ig_list')),
                     ('vectorizer', DictVectorizer())#,('svd', TruncatedSVD(n_components=300))
                   ])
    #dt_pipe=Pipeline([("encoder",DictEncoder('Dt_list')),('vectorizer',DictVectorizer())])
    #union=FeatureUnion([('Ingredient',ig_pipe),('Detail',dt_pipe)])
    features = ig_pipe.fit_transform(df_1)
    nn = NearestNeighbors(n_neighbors=20).fit(features)
    index=df_1.index[df_1['Name']==product][0]
    dists, indices = nn.kneighbors(features[index])
    
    prod_nbr=df_1.iloc[indices[0]]    
    prod_nbr=prod_nbr[prod_nbr['Main_Category']==df_1['Main_Category'][index]]
    
   
    return containsAllergen(prod_nbr,allergen).head(5)
