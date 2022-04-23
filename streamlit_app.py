import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

################################################
##########      Helper functions      ##########
################################################

@st.cache  # add caching so we load the data only once
def load_mental_data():
    mental_df = pd.read_csv(
        "data/Mental Health Checker.csv", encoding="ISO-8859-1")
    mental_df = mental_df[['gender', 'age', 'marital', 'income', 'loan',
                           'social_media', 'sleep_disorder', 'mental_disorder', 'therapy']]
    mental_df.mental_disorder.fillna("None", inplace=True)
    return mental_df


@st.cache
def load_sleep_data():
    sleep_stress = pd.read_csv("data/sleep_stress.csv")
    sleep_data = pd.read_csv("data/sleep_data_cleaned.csv")
    return sleep_stress, sleep_data


def plot(df, xlabel, ylabel, column, index):
    # plt.clf()
    dfs = []
    for i in range(len(index)):
        dfs.append(df[df[column] == index[i]])
    P, D, S, A, N = [0] * len(index), [0] * len(index), [0] * \
        len(index), [0] * len(index), [0] * len(index)
    disorder = ['Panic attack', 'depression', 'stress', 'anxiety', "None"]
    for i in range(len(index)):
        P[i] = len(dfs[i][dfs[i]["mental_disorder"] == disorder[0]])
        D[i] = len(dfs[i][dfs[i]["mental_disorder"] == disorder[1]])
        S[i] = len(dfs[i][dfs[i]["mental_disorder"] == disorder[2]])
        A[i] = len(dfs[i][dfs[i]["mental_disorder"] == disorder[3]])
        # N[i] = len(df[df[column] == index[i]]["mental_disorder"] == disorder[i])
    for i in range(len(index)):
        N[i] = len(df[df[column] == index[i]]) - P[i] - D[i] - S[i] - A[i]

    test_df = pd.DataFrame(columns=[column, xlabel, ylabel])

    for i in range(len(index)):
      for j in range(5):
         if j == 0:
            test_df = test_df.append({column: index[i], xlabel: disorder[j], ylabel: P[i]}, ignore_index=True)
         elif j == 1:
            test_df = test_df.append({column: index[i], xlabel: disorder[j], ylabel: D[i]}, ignore_index=True)
         elif j == 2:
            test_df = test_df.append({column: index[i], xlabel: disorder[j], ylabel: S[i]}, ignore_index=True)
         elif j == 3:
            test_df = test_df.append({column: index[i], xlabel: disorder[j], ylabel: A[i]}, ignore_index=True)
         elif j == 4:
            test_df = test_df.append({column: index[i], xlabel: disorder[j], ylabel: N[i]}, ignore_index=True)

    c = alt.Chart(test_df).mark_bar().encode(x=xlabel,y=ylabel,column=column, color=column, tooltip=[ylabel])
    st.altair_chart(c)

################################################
##########      Main starts here      ##########
################################################

st.title("Stress Analysis: Narrative of stress that enhances people’s understanding of it")

st.sidebar.title(
    "Stress Data Analysis: To have an in-depth understanding of the following questions")
st.sidebar.markdown(
    "This application is a Streamlit dashboard to enhances people’s understanding of stress")

st.sidebar.header("待填入")
selectplot = st.sidebar.selectbox("待填入Select the question you want to view", [
                                  "Stress & age/backgrounds", "Factors correlate with stress level", "Stress & social media"], key="0")

# Page 1
if selectplot == "Stress & age/backgrounds":
    st.markdown("Stress is defined as a reaction to mental or emotional pressure. It is probably \
   one of the commonly experienced feelings, but it might be hard to share. Stress can be caused by a \
   variety of sources includes uncertain future, discrimination, etc., and the coronavirus pandemic \
   has risen as a substantial source of stress. People from different age and/or socioeconomic \
   groups may experience very different sources and symptoms of stress. In this project, we hope to bring \
   a narrative of stress that enhances people’s understanding of it.")

    st.subheader(
        'Q1: What are the sources and impact of stress for people from different backgrounds?')
    st.markdown("We will use the Kaggle dataset *Mental Health Checker* collected from a mental health survey for general analysis. \
   The survey consists of 36 questions and has 207 interviewees. Here are the 36 questions of the survey.")
    image = Image.open('img/1.png')
    st.image(image)


    st.markdown("First, let's explore whether stress level has specific relationships with gender, \
   age, marital status, income level, loan, time spent in social media a day or sleep disorder. ")
    'sleep_disorder'
    mental_df = load_mental_data()


    factor = st.selectbox("Please select the factors you are interested in and analyze the bar charts.", [
                          "gender", "age", "marital", "income", "loan", "social media", "sleep disorder"])
    if factor == "gender":
        plot(mental_df, "Mental disorder type", "Number of interviewees", 'gender', ['female', 'male'])
    elif factor == "age":
        plot(mental_df, "Mental disorder type","Number of interviewees", 'age', ['13-19', '20-26', '27-33', '34-44', '45 or more'])
    elif factor == "marital":
        plot(mental_df, "Mental disorder type", "Number of interviewees", 'marital', ['single', 'marital', 'divorced', 'separated'])
    elif factor == "income":
        plot(mental_df, "Mental disorder type", "Number of interviewees", 'income', ['<10', '<20', '<30', '30+', '50+'])
    elif factor == "loan":
        plot(mental_df, "Mental disorder type", "Number of interviewees", 'loan', ['yes', 'no'])
    elif factor == "social media":
        plot(mental_df, "Mental disorder type","Number of interviewees", 'social_media', ['<1 hour', '<2 hours', '<3 hours', '3+ hours'])
    elif factor == "sleep disorder":
        plot(mental_df, "Mental disorder type", "Number of interviewees", 'sleep_disorder', ['yes', 'no'])

# Page 2
elif selectplot == "Factors correlate with stress level":

    # Stress vs sleep
    st.subheader("Sleep")
    st.markdown("In this section, we will first delve into the relationship between sleep and stress,\
      and then focus on how to improve sleep quality inorder to reduce stress.")
    stress, sleep = load_sleep_data()


# Page 3
elif selectplot == "Stress & social media":
    st.subheader(
        'Interactive function to detect the user\'s current stress situation')
    image = Image.open('img/18.png')
    st.image(image, caption='Dataset: 3.5K total segments taken from 3K posts using Amazon Mechanical Turk')
    image = Image.open('img/19.png')
    st.image(image, caption='We have a total of 2,838 train data points and includes ten total subreddits')
    select = st.selectbox("Show word cloud plot", [
                          "Non_stress_post_words", "Stress_post_words"], key="1")
    if select == "Non_stress_post_words":
        image = Image.open('img/20.png')
        st.image(image, caption='Non_stress_post_words')
    else:
        image = Image.open('img/21.png')
        st.image(image, caption='Stress_post_words')

    st.sidebar.markdown(
        "##### Dataset: Dreaddit: A Reddit Dataset for Stress Analysis in Social Media")

    # @st.cache(persist = True, allow_output_mutation=True)
    # def load_data():
    #    data = pd.read_csv(DATA_URL)
    #    return data
    # data = load_data()
    st.subheader(
        'Would you like to know your stress level? Please enter some sentences')
    title = st.text_area(label='', value='Please enter some sentences here...')

    if title != 'Please enter some sentences here...':
        st.write('Your input is: [', title, ']')
        path = './data/'
        # path = '/content/Insight_Stress_Analysis/data/'
        train = pd.read_csv(path + 'dreaddit-train.csv', encoding="ISO-8859-1")
        test = pd.read_csv(path + 'dreaddit-test.csv', encoding="ISO-8859-1")
        DATA_COLUMN = 'text'
        LABEL_COLUMN = 'label'
        # label_list is the list of labels, i.e. True, False or 0, 1 or 'dog', 'cat'
        label_list = [0, 1]


st.markdown(
    "This project was created by Wenxing Deng, Jiuzhi Yu, Siyu Zhou and Huiyi Zhang for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")
