import streamlit as st
import pandas as pd
import altair as alt
# import plotly.express as px
import numpy as np
from PIL import Image

st.title("Stress Analysis: Narrative of stress that enhances people’s understanding of it")

st.sidebar.title("待填入Stress Data Analysis: To have an in-depth understanding of the following questions")
st.sidebar.markdown("待填入This application is a Streamlit dashboard to enhances people’s understanding of stress")

st.sidebar.header("待填入")
selectplot = st.sidebar.selectbox("待填入Select the question you want to view", ["Stress & age/backgrounds", "Factors correlate with stress level", "Stress & social media"] ,key = "0")

if selectplot == "Stress & social media":
   st.subheader('Interactive function to detect the user\'s current stress situation')
   image = Image.open('img/18.png')
   st.image(image, caption='Dataset: 3.5K total segments taken from 3K posts using Amazon Mechanical Turk')
   image = Image.open('img/19.png')
   st.image(image, caption='We have a total of 2,838 train data points and includes ten total subreddits')
   select = st.selectbox("Show word cloud plot", ["Non_stress_post_words", "Stress_post_words"],key = "1")
   if select == "Non_stress_post_words":
      image = Image.open('img/20.png')
      st.image(image, caption='Non_stress_post_words')
   else:
      image = Image.open('img/21.png')
      st.image(image, caption='Stress_post_words')



   st.sidebar.markdown("##### Dataset: Dreaddit: A Reddit Dataset for Stress Analysis in Social Media")

   # @st.cache(persist = True, allow_output_mutation=True)
   # def load_data():
   #    data = pd.read_csv(DATA_URL)
   #    return data
   # data = load_data()
   st.subheader('Would you like to know your stress level? Please enter some sentences')
   title = st.text_area(label = '',value='Please enter some sentences here...')

   if title !='Please enter some sentences here...':
      st.write('Your input is: [', title,']')
      path = '/data/' 
      # path = '/content/Insight_Stress_Analysis/data/'
      train = pd.read_csv(path + 'dreaddit-train.csv', encoding = "ISO-8859-1")
      test = pd.read_csv(path + 'dreaddit-test.csv', encoding = "ISO-8859-1")
      DATA_COLUMN = 'text'
      LABEL_COLUMN = 'label'
      # label_list is the list of labels, i.e. True, False or 0, 1 or 'dog', 'cat'
      label_list = [0, 1]

   

elif selectplot == "Stress & age/backgrounds":
   st.subheader('...')
   




st.markdown("This project was created by Wenxing Deng, Jiuzhi Yu, Siyu Zhou and Huiyi Zhang for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")
