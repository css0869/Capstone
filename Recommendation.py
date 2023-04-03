import pandas as pd

from sklearn import base

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors

import re


#Check if Ingredient list contains allergen item
def containsAllergen(df,allergen):
    return df[df['Ingredient'].apply(lambda x: allergen not in x)]


def recommender(df,product, allergen):
    safe_df= df.copy()
    
    bag_of_words_vectorizer=CountVectorizer(min_df=0,
                             ngram_range=(1,2), 
                             stop_words='english')
    counts=bag_of_words_vectorizer.fit_transform(safe_df['Ingredient'])
    nn = NearestNeighbors(n_neighbors=20).fit(counts) 
    index=safe_df[safe_df['Name']==product].index
    #safe_df.index[safe_df['Name']==product][0]
    dists, indices = nn.kneighbors(counts[index[0]])
    prod_nbr=safe_df.iloc[indices[0]]
    
    prod_nbr=prod_nbr[prod_nbr['Main_Category']==df['Main_Category'][index[0]]]
    return containsAllergen(prod_nbr,allergen).head(5)

