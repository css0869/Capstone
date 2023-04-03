import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
import re
from streamlit_extras.badges import badge
from streamlit_extras.app_logo import add_logo
from PIL import Image
from streamlit_extras.colored_header import colored_header
from streamlit_extras.customize_running import center_running

import Recommendation as rec

@st.cache_data
def get_data():
    df=pd.read_csv('Clean_data')
    return df

def get_list(df,name):
    idx=df.index[df['Name']==name][0]
    s=df['Ig_list'][idx]
    s=s.replace("'","").replace("[","").replace("]","")  
    l=[x.strip() for x in s.split(",")]
    return l


def show_product(result_df):
    result_df=pd.DataFrame(result_df,columns=['Brand','Name','Rating','Price','Category','Ingredient','Link']).reset_index(drop=True)

    for i in range(0,len(result_df)):
        #colored_header( label=result_df['Name'][i],description="",color_name="violet-70")
        #st.subheader(result_df['Name'][i].tostring():blue[colors] )
                     #](https://streamlit.io/docs/))
        
        st.markdown("***")
        st.subheader(result_df['Name'][i])
        st.write('Brand: ', result_df['Brand'][i])
        st.write('Price: ',result_df['Price'][i])
        st.write('Rating: ',result_df['Rating'][i]," out of 5 stars")
        st.write('Ingredient: ',result_df['Ingredient'][i])
        #url=result_df['Link'][i]
        #st.write("Check out this [link](%s)" % url)
        st.text("")
    return


       
def load_page():
    st.set_page_config(page_title="Safe Beauty Product Recommendation App")
    page_bg_img = '''
<style>
.stApp {
background-image: url("https://i.pinimg.com/564x/02/7b/db/027bdb4084cf31c9eb6d33940c3d14b5.jpg");
background-size: cover;
}
</style>
'''
    st.markdown(page_bg_img, unsafe_allow_html=True)
    add_logo("http://placekitten.com/120/120")
    #add_logo("Image/bottle_cloud.png", height=300)
    st.header("Find Safe-For-You Beauty Products")
    #st.title("Find Safe-For-You Beauty Products")
    st.sidebar.image('Image/bottle_cloud.png',  use_column_width=True)
    st.sidebar.markdown("## Once-loved Beuty Product")
    return
    
def app():       
    
    df=get_data()
    brand = st.sidebar.selectbox('Brand',sorted(df['Brand'].unique()))     
    prod = st.sidebar.selectbox('Product Name',sorted(df[df['Brand']==brand]['Name'])) 
    st.sidebar.subheader("But I don't like...")
    #st.sidebar.write("Which ingredient are you sensitive/allergic to?")
    igs=get_list(df,prod)
    allergen=st.sidebar.selectbox("Which ingredient are you sensitive/allergic to?", options=igs )
    #allergen = st.sidebar.radio("Ingredient List",get_ig_list(df,name) )
    
    btn=st.sidebar.button("Search for Skin Safe Substitutes")
    st.sidebar.info("Please consult with dermatologists or medical professionals to ensure you have an accurate list of potential allergens.", icon="ℹ️") 
            
    # Create a text element and let the reader know the data is loading.
    if btn:
        data_load_state = st.text('Looking for your new favourites.🏃‍♂️')
        center_running()
        result=rec.recommender(df,prod,allergen)
        st.markdown("You don't like {} . We got you....".format(allergen))
        st.markdown("These products are similar to **{}** **{}**, but do not contain **{}** as you noted.".format(brand,prod,allergen)) 
        show_product(result)
        # Notify the reader that the data was successfully loaded.
        data_load_state.text('Looking for your new favourites...Found it!')
        
        st.info("Disclaimer: this recommendation is based on the ingredient label on the product. It does not represent a guarantee that products have been tested to confirm the absence of any particular allergen or irritant. Please consult with your dermatologists.")
    
    return

    
if __name__ == "__main__": 
    
    load_page()
    tab1,tab2 = st.tabs(["Recommendation", "About"])
    with tab1:
        app()
    with tab2: 
        st.header("About")
        st.write("""
        
        People with sensitive skin or weak immune systems may develop a reaction to certain substances in cosmetic products. The best way to avoid contact allergies is to know what you are sensitive to and stop using that ingredient. Some companies label their products as ‘’for sensitive skin’, ‘hypoallergenic’ or ‘skin-friendly’. However, per the U.S. Food and Drug Administration (FDA), there is no federal standard on regulating the use of these terms (from FDA government website). 
 
And contact allergies can take years to surface, when once-loved beauty products need to be replaced with *safe* substitutes, with similar benefits or functions, for example skin tightening, customers will have to read labels line by line. This project builds a skincare recommendation system that incorporates allergy/irritation considerations. Can be a valuable resource for people having allergies and sensitivities to certain substances in beauty and skincare products. 
""")
        st.info("Read more about how the model works and see the code on my [Github](https://github.com/css0869/Safe-for-you-Beauty-Product-Recommendation).", icon="ℹ️")
        
        #badge(type="github", name="css0869/Safe-for-you-Beauty-Product-Recommendation")