import streamlit as st
import pandas as pd
import altair as alt
# import plotly.express as px
import numpy as np
st.title("Stress Analysis: Narrative of stress that enhances people’s understanding of it")

st.sidebar.title("待填入Stress Data Analysis: To have an in-depth understanding of the following questions")
st.sidebar.markdown("待填入This application is a Streamlit dashboard to enhances people’s understanding of stress")

st.sidebar.header("待填入")
selectplot = st.sidebar.selectbox("待填入Select the question you want to view", ["Stress & age/backgrounds", "Factors correlate with stress level", "Stress & social media"] ,key = "0")

if selectplot == "Stress & social media":
   st.subheader('Interactive function to detect the user\'s current stress situation')
   st.sidebar.markdown("##### Dataset: Dreaddit: A Reddit Dataset for Stress Analysis in Social Media")
   select1 = st.sidebar.selectbox("Show ", ["", "2012","2013", "2014","2015"],key = "1")
   DATA_URL = select1+"group_diff.csv"

   @st.cache(persist = True, allow_output_mutation=True)
   def load_data():
      data = pd.read_csv(DATA_URL)
      return data
   data = load_data()

   # st.sidebar.subheader('Breakdown categories by machine learning groups')
   st.sidebar.markdown('##### Breakdown categories by Groups(K-means)')
   st.markdown('##### Breakdown categories by Groups(K-means)')
   choice = st.sidebar.multiselect('Pick categories', ("FOODS","HOBBIES","HOUSEHOLD"), default =(["FOODS","HOBBIES","HOUSEHOLD"]), key =0)
   if len(choice)>0:
      choice_data = data[data.cat_id.isin(choice)]
      print(choice_data)
      # fig_choice = px.histogram(choice_data, x='cat_id', y='group', histfunc='count', color='group')
      base1 = alt.Chart(choice_data).mark_bar(size=50).encode(
         x=alt.X("cat_id", title="cat_id"),
         y=alt.Y("sum(group):Q", title="people count"),
         color='cat_id:N',
         # color=alt.condition(cat_brush, alt.value("darkblue"), alt.value("lightgrey")),
         tooltip=['sum(group):Q']
      ).properties(
         width=510,
         height=550
      )
      st.write(base1)
   
   # weekday
   if st.sidebar.checkbox("Weekday & Groups(K-means)", True):
      st.markdown('##### Weekday & Groups(K-means)')
      DATA_URL1 = select1+"group_diff2.csv"
      @st.cache(persist = True)
      def load_data_weekday():
         df = pd.read_csv(DATA_URL1, usecols=['weekday', 'group', 'quantity', 'price'])
         df['group'] = df['group'].astype('str')
         df['weekday'] = df['weekday'].astype('str')
         df['quantity'] = df['quantity'].astype('int')
         df['price'] = df['price'].apply(lambda x:round(x,1))
         df['revenue'] = df['quantity'] * df['price']
         return df

      df = load_data_weekday()
      cat_brush = alt.selection_multi(fields=['group'])

      base1 = alt.Chart(df).mark_bar(size=25).encode(
         x=alt.X("sum(revenue):Q", title="Total revenue"),
         y=alt.Y("group", title="Item category(ML)"),
         color='group:N',
         # color=alt.condition(cat_brush, alt.value("darkblue"), alt.value("lightgrey")),
         tooltip=['sum(revenue):Q']
      ).add_selection(
         cat_brush
      ).properties(
         width=510,
         height=350
      )
      base2 = alt.Chart(df).mark_bar(size=30).encode(
         x=alt.X("weekday", sort=["Monday", 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
               title='Weekday'),
         y=alt.Y("sum(revenue):Q", title="Total revenue"),
         color='weekday:N',
         tooltip=['sum(revenue):Q']
      ).transform_filter(
         cat_brush
      ).properties(
         width=510,
         height=350
      )
      integrated = alt.vconcat(base1, base2)
      st.write(integrated)
   
   # month
   if st.sidebar.checkbox("Month & Groups(K-means)", True):
      st.markdown('##### Month & Groups(K-means)')
      DATA_URL2 = select1+"group_diff3.csv"
      @st.cache(persist = True)
      def load_data_weekday():
         df = pd.read_csv(DATA_URL2, usecols=['month', 'group', 'quantity', 'price'])
         df['group'] = df['group'].astype('str')
         df['month'] = df['month'].astype('str')
         df['month'].replace("1", "January",inplace=True)
         df['month'].replace("2", "February",inplace=True)
         df['month'].replace("3", "March",inplace=True)
         df['month'].replace("4", "April",inplace=True)
         df['month'].replace("5", "May",inplace=True)
         df['month'].replace("6", "June",inplace=True)
         df['month'].replace("7", "July",inplace=True)
         df['month'].replace("8", "August",inplace=True)
         df['month'].replace("9", "September",inplace=True)
         df['month'].replace("10", "October",inplace=True)
         df['month'].replace("11", "November",inplace=True)
         df['month'].replace("12", "December",inplace=True)
         df['quantity'] = df['quantity'].astype('int')
         df['price'] = df['price'].apply(lambda x:round(x,1))
         df['revenue'] = df['quantity'] * df['price']
         return df

      df = load_data_weekday()
      cat_brush = alt.selection_multi(fields=['group'])

      base1 = alt.Chart(df).mark_bar(size=25).encode(
         x=alt.X("sum(revenue):Q", title="Total revenue"),
         y=alt.Y("group", title="Item category(ML)"),
         color='group:N',
         # color=alt.condition(cat_brush, alt.value("darkblue"), alt.value("lightgrey")),
         tooltip=['sum(revenue):Q']
      ).add_selection(
         cat_brush
      ).properties(
         width=510,
         height=350
      )
      base2 = alt.Chart(df).mark_bar(size=30).encode(
         x=alt.X("month", sort=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October','November','December'],
               title='Month'),
         y=alt.Y("sum(revenue):Q", title="Total revenue"),
         color='month:N',
         tooltip=['sum(revenue):Q']
      ).transform_filter(
         cat_brush
      ).properties(
         width=510,
         height=350
      )
      integrated = alt.vconcat(base1, base2)
      st.write(integrated)

      # holiday
   if st.sidebar.checkbox("Holiday Type & Groups(K-means)", True):
      st.markdown('##### Holiday Type & Groups(K-means)')
      DATA_URL3 = select1+"group_diff4.csv"
      @st.cache(persist = True)
      def load_data_weekday():
         df = pd.read_csv(DATA_URL3, usecols=['event_type_1', 'group', 'quantity', 'price'])
         df['group'] = df['group'].astype('str')
         df['event_type_1'] = df['event_type_1'].astype('str')
         df['quantity'] = df['quantity'].astype('int')
         df['price'] = df['price'].apply(lambda x:round(x,1))
         df['revenue'] = df['quantity'] * df['price']
         return df

      df = load_data_weekday()
      cat_brush = alt.selection_multi(fields=['group'])

      base1 = alt.Chart(df).mark_bar(size=25).encode(
         x=alt.X("sum(revenue):Q", title="Total revenue"),
         y=alt.Y("group", title="Item category(ML)"),
         color='group:N',
         # color=alt.condition(cat_brush, alt.value("darkblue"), alt.value("lightgrey")),
         tooltip=['sum(revenue):Q']
      ).add_selection(
         cat_brush
      ).properties(
         width=510,
         height=350
      )
      base2 = alt.Chart(df).mark_bar(size=30).encode(
         x=alt.X("event_type_1", title='Holiday Type'),
         y=alt.Y("sum(revenue):Q", title="Total revenue"),
         color='event_type_1:N',
         tooltip=['sum(revenue):Q']
      ).transform_filter(
         cat_brush
      ).properties(
         width=510,
         height=350
      )
      integrated = alt.vconcat(base1, base2)
      st.write(integrated)


      @st.cache(persist = True)
      def load_data():
         data = pd.read_csv(DATA_URL3)
         return data
      data = load_data()
      type_count = data["event_type_1"].value_counts()

      type_count = pd.DataFrame({"hoilday type":type_count.index, "count type":type_count.values})
      # fig = px.bar(type_count, x = "hoilday type", y = "count type",text_auto=True, height = 500, color = "hoilday type" )
      # st.plotly_chart(fig)
      base2 = alt.Chart(type_count).mark_bar(size=50).encode(
         x=alt.X("hoilday type", title="hoilday type"),
         y=alt.Y("count type", title="count type"),
         color='hoilday type:N',
         tooltip=['count type:Q']
      ).properties(
         width=510,
         height=400
      )
      st.write(base2)


      # holiday name
   if st.sidebar.checkbox("Holiday Name & Groups(K-means)", True):
      st.markdown('##### Holiday Name & Groups(K-means)')
      DATA_URL4 = select1+"group_diff5.csv"
      @st.cache(persist = True)
      def load_data_weekday():
         df = pd.read_csv(DATA_URL4, usecols=['event_name_1', 'group', 'quantity', 'price'])
         df['group'] = df['group'].astype('str')
         df['event_name_1'] = df['event_name_1'].astype('str')
         df['quantity'] = df['quantity'].astype('int')
         df['price'] = df['price'].apply(lambda x:round(x,1))
         df['revenue'] = df['quantity'] * df['price']
         return df

      df = load_data_weekday()
      cat_brush = alt.selection_multi(fields=['group'])

      base1 = alt.Chart(df).mark_bar(size=25).encode(
         x=alt.X("sum(revenue):Q", title="Total revenue"),
         y=alt.Y("group", title="Item category(ML)"),
         color='group:N',
         # color=alt.condition(cat_brush, alt.value("darkblue"), alt.value("lightgrey")),
         tooltip=['sum(revenue):Q']
      ).add_selection(
         cat_brush
      ).properties(
         width=510,
         height=350
      )
      base2 = alt.Chart(df).mark_bar(size=10).encode(
         x=alt.X("event_name_1", title='Holiday Name'),
         y=alt.Y("sum(revenue):Q", title="Total revenue"),
         color='event_name_1:N',
         tooltip=['sum(revenue):Q']
      ).transform_filter(
         cat_brush
      ).properties(
         width=510,
         height=350
      )
      integrated = alt.vconcat(base1, base2)
      st.write(integrated)


      @st.cache(persist = True)
      def load_data():
         data = pd.read_csv(DATA_URL4)
         return data
      data = load_data()
      type_count = data["event_name_1"].value_counts()

      type_count = pd.DataFrame({"hoilday name":type_count.index, "count type":type_count.values})
      # fig = px.bar(type_count, x = "hoilday name", y = "count type",text_auto=True, height = 500, color = "hoilday name" )
      # st.plotly_chart(fig)
      base2 = alt.Chart(type_count).mark_bar(size=10).encode(
         x=alt.X("hoilday name", title="hoilday name"),
         y=alt.Y("count type", title="count type"),
         color='hoilday name:N',
         tooltip=['count type:Q']
      ).properties(
         width=700,
         height=400
      )
      st.write(base2)



elif selectplot == "The impact of weekdays on sales":
   st.subheader('Weekday & Weekend Sales Analysis by Item Category')
   select1 = st.sidebar.selectbox("year", ["2011", "2012","2013", "2014","2015"],key = "1")
   select2 = st.sidebar.selectbox("store", ['CA_1', 'CA_2', 'CA_3', 'CA_4', 'TX_1', 'TX_2', 'TX_3', 'WI_1',
       'WI_2', 'WI_3'], key="1")




st.markdown("This project was created by Wenxing Deng, Jiuzhi Yu, Siyu Zhou and Huiyi Zhang for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")
