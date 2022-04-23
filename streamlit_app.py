from attr import attr
from numpy import character
import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

################################################
##########      Global attributes     ##########
################################################

stress_sleep_attrs = ["snoring rate", "respiration rate", "body temperature",
                      "limb movement", "body oxygen", "eye movement", "sleeping hours", "heart rate"]


################################################
##########      Helper functions      ##########
################################################

@st.cache  # add caching so we load the data only once
def load_data():
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
    sleep_data["Start"] = pd.to_datetime(
        sleep_data["Start"], format='%H:%M:%S').dt.tz_localize("US/Eastern")
    sleep_data["End"] = pd.to_datetime(
        sleep_data["End"], format='%H:%M:%S').dt.tz_localize("US/Eastern")
    return sleep_stress, sleep_data


def plot(title, df, xlabel, ylabel, column, index):
    # plt.clf()
    dfs = []
    for i in range(len(index)):
        dfs.append(df[df[column] == index[i]])
    P, D, S, A, N = [0] * len(index), [0] * len(index), [0] * \
        len(index), [0] * len(index), [0] * len(index)
    disorder = ['Panic attack', 'depression', 'stress', 'anxiety']
    for i in range(len(index)):
        P[i] = len(dfs[i][dfs[i]["mental_disorder"] == disorder[0]])
        D[i] = len(dfs[i][dfs[i]["mental_disorder"] == disorder[1]])
        S[i] = len(dfs[i][dfs[i]["mental_disorder"] == disorder[2]])
        A[i] = len(dfs[i][dfs[i]["mental_disorder"] == disorder[3]])
        # N[i] = len(df[df[column] == index[i]]["mental_disorder"] == disorder[i])
    for i in range(len(index)):
        N[i] = len(df[df[column] == index[i]]) - P[i] - D[i] - S[i] - A[i]
    plotdata = pd.DataFrame({
        "Panic attack": P,
        "Depression": D,
        "Stress": S,
        "Anxiety": A,
        "N/A": N
    },
        index=index
    )
    c = alt.Chart(plotdata).mark_bar().encode()
    st.altair_chart(c)


def gen_stress_sleep_chart(attrs):
    chart_list = []
    for attr in attrs:
        chart_list.append(
            alt.Chart(stress).mark_bar().encode(
                alt.X(attr, scale=alt.Scale(
                    zero=False), bin=alt.Bin()),
                alt.Y("count()"),
                alt.Color("stress level")
            ).properties(
                width=280,
                height=210
            )
        )
    return chart_list

@st.cache
def binaryEncodeResponse(response):
    result = []
    if "Yes" in response:
        result.append(1)
    if "No" in response:
        result.append(0)
    return result

@st.cache
def get_sleep_membership(sleep, score_range=None, coffee=None, tea=None, ate_late=None, worked_out=None):
    labels = pd.Series([1] * len(sleep), index=sleep.index)
    if score_range:
        labels &= (sleep['Sleep quality'] >= score_range[0]) & (
            sleep['Sleep quality'] <= score_range[1])
    if coffee:
        coffee = binaryEncodeResponse(coffee)
        labels &= (sleep['Drank coffee'].isin(coffee))
    if tea:
        tea = binaryEncodeResponse(tea)
        labels &= (sleep['Drank tea'].isin(tea))
    if ate_late:
        ate_late = binaryEncodeResponse(ate_late)
        labels &= (sleep['Ate late'].isin(ate_late))
    if worked_out:
        worked_out = binaryEncodeResponse(worked_out)
        labels &= (sleep['Worked out'].isin(worked_out))
    return labels

################################################
##########      Main starts here      ##########
################################################


st.title("Stress Analysis: Narrative of stress to enhance people's understanding")

st.sidebar.title(
    "Stress Data Analysis: To have an in-depth understanding of the following questions")
st.sidebar.markdown(
    "This application is a Streamlit dashboard to enhances people's understanding of stress")

st.sidebar.header("Page navigation")
selectplot = st.sidebar.selectbox("Select the question you want to view", [
                                  "Introduction", "Stress & age/backgrounds", "Factors correlate with stress level", "Stress & social media"], key="0")
# Page 0
if selectplot == "Introduction":
    st.markdown(
        "Do we need an intro page to show the overall structure of our application?\n" +
        "## Purpose of this application\n" + 
        "In this application, we will show a general overview of stress, including the sources of stress, the factors that will" +
        "influence people's stress level, and the relationship of stress and social media.\n" +
        "## Overall structure\n" +
        "There are in total four pages in this application. (Need more words here?)\n" +
        "1. Overall introduction\n" +
        "2. Stress & age/backgrounds\n" +
        "3. Factors correlate with stress level\n" +
        "4. Factors correlate with stress level\n" + 
        "### Please proceed to page 2 to start your exploration!"
    )

# Page 1
if selectplot == "Stress & age/backgrounds":
    st.markdown("Stress is defined as a reaction to mental or emotional pressure. It is probably \
   one of the commonly experienced feelings, but it might be hard to share. Stress can be caused by a \
   variety of sources includes uncertain future, discrimination, etc., and the coronavirus pandemic \
   has risen as a substantial source of stress. People from different age and/or socioeconomic \
   groups may experience very different sources and symptoms of stress. In this project, we hope to bring \
   a narrative of stress that enhances people's understanding of it.")

    st.subheader(
        'Q1: What are the sources and impact of stress for people from different backgrounds?')
    st.markdown("We will use the Kaggle dataset *Mental Health Checker* collected from a mental health survey for general analysis. \
   The survey consists of 36 questions and has 207 interviewees. Here are the 36 questions of the survey.")
    image = Image.open('img/1.png')
    st.image(image)

    st.markdown("First, let's explore whether stress level has specific relationships with gender, \
   age, marital status, income level, loan, time spent in social media a day or sleep disorder. ")
    'sleep_disorder'
    mental_df = load_data()
    factor = st.selectbox("Please select the factors you are interested in and analyze the bar charts.", [
                          "gender", "age", "marital", "income", "loan", "social media", "sleep disorder"])
    if factor == "gender":
        plot("Mental disorder distribution among different genders", mental_df,
             "Mental disorder type", "Number of interviewees", 'gender', ['female', 'male'])
    elif factor == "age":
        plot("Mental disorder distribution among different age groups", mental_df, "Mental disorder type",
             "Number of interviewees", 'age', ['13-19', '20-26', '27-33', '34-44', '45 or more'])
    elif factor == "marital":
        plot("Mental disorder distribution among different  marital status groups", mental_df,
             "Mental disorder type", "Number of interviewees", 'marital', ['single', 'marital', 'divorced', 'separated'])
    elif factor == "income":
        plot("Mental disorder distribution among different income level groups", mental_df,
             "Mental disorder type", "Number of interviewees", 'income', ['<10', '<20', '<30', '30+', '50+'])
    elif factor == "loan":
        plot("Relationship between mental disorder and loan", mental_df,
             "Mental disorder type", "Number of interviewees", 'loan', ['yes', 'no'])
    elif factor == "social media":
        plot("Mental disorder distribution with time spent on social media per day", mental_df, "Mental disorder type",
             "Number of interviewees", 'social_media', ['<1 hour', '<2 hours', '<3 hours', '3+ hours'])
    elif factor == "sleep disorder":
        plot("Relationship between mental disorder and sleep disorder", mental_df,
             "Mental disorder type", "Number of interviewees", 'sleep_disorder', ['yes', 'no'])

# Page 2
elif selectplot == "Factors correlate with stress level":
    st.markdown(
        "In this page, we will explore several factors that can influence people's stress level.\n" +
        "1. COVID-19's Impact on Educational Stress\n" + 
        "2. Impact of Sleep on Stress"
    )
    
    # Stress vs sleep
    st.subheader("2. Impact of Sleep on Stress")
    st.markdown("In this section, we will first delve into the relationship between sleep and stress,\
      and then focus on how to improve sleep quality inorder to reduce stress.")
    stress, sleep = load_sleep_data()

    # Stress data
    st.markdown(
        "#### 2.1 How sleep influences stress levels\n" +
        "Let's explore several attributes of sleep to discover the" +
        "relationship between sleep and stress.\n\n" +
        "The stress level has a range from 0 to 4. The higher the stress level, the higher the stress people experience."
    )
    attrs = st.multiselect("Choose the attributes:", stress_sleep_attrs, default=[
                           "sleeping hours", "snoring rate"])

    chart_list = gen_stress_sleep_chart(attrs)

    concated_chart = None

    for i in range(0, len(attrs), 2):
        cur_chart = None
        if i + 1 >= len(attrs):
            cur_chart = chart_list[i]
        else:
            cur_chart = alt.hconcat(chart_list[i], chart_list[i + 1])
        if concated_chart is None:
            concated_chart = cur_chart
        else:
            concated_chart = alt.vconcat(concated_chart, cur_chart)

    st.write(concated_chart)
    st.markdown(
        "#### Summary:\n" +
        "From the charts above, we can clearly see that the stress level is strongly correlated " +
        "to the quality of sleep. With a longer sleeping hour, or a lower snoring rate, people tend " +
        "to experience a lower stress level.\n\n" +
        "Then the question we are interested in is:\n\n ***How can we improve sleep quality to reduce stress?***"
    )

    # Sleep data
    st.markdown(
        "#### 2.2 How to improve sleep quality\n" +
        "Now let's see how to improve sleep quality in order to reduce stress.\n" +
        "In this section, we would like to see the relationship between sleep quality with some " +
        "attributes, including sleep start and end time, time in bed, heart rate, and daily lifestyle.\n"
    )

    st.markdown("##### Step 1: Please select the sleep quality interval you are\
        interested in")
    score_range = st.select_slider("", range(101), value=(0, 100))
    st.markdown(
        "##### Step 2: Four different lifestyle attributes are provided. Choose the lifestyle that best describes yourself!\n"
    )
    sleep_cols = st.columns(2)
    with sleep_cols[0]:
        coffee_attr = st.multiselect("Drank coffee?", ["Yes", "No"], default=["Yes", "No"])
        tea_attr = st.multiselect("Drink tea?", ["Yes", "No"], default=["Yes", "No"])
    with sleep_cols[1]:
        ate_late_attr = st.multiselect("Eat late?", ["Yes", "No"], default=["Yes", "No"])
        worked_out_attr = st.multiselect("Work out?", ["Yes", "No"], default=["Yes", "No"])

    sleep_score_range = sleep[get_sleep_membership(sleep, score_range, coffee_attr, tea_attr, ate_late_attr, worked_out_attr)]

    sleep_selection = alt.selection(type="interval")

    st.markdown(
        "##### Step 3: Now let's see the sleeping quality distribution.\n\n" +
        "You can select some data points in \"Time in bed\" to see other sleep attributes of these people!"
    )

    time_in_bed = alt.Chart(sleep_score_range).mark_circle(size=10).add_selection(sleep_selection).encode(
        alt.X("Time in bed"),
        alt.Y("Sleep quality", scale=alt.Scale(zero=False)),
        tooltip=["Time in bed", "Sleep quality"],
        color=alt.condition(sleep_selection, alt.value(
            "steelblue"), alt.value("gray"))
    ).properties(
        width=400,
        height=300
    )

    start_time = alt.Chart(sleep_score_range).mark_circle(size=10).encode(
        alt.X("hours(Start):T"),
        alt.Y("Sleep quality", scale=alt.Scale(zero=False)),
        tooltip=["hours(Start):T", "Sleep quality"],
        color=alt.condition(sleep_selection, alt.value(
            "orange"), alt.value("gray"))
    ).properties(
        width=240,
        height=180
    )

    end_time = alt.Chart(sleep_score_range).mark_circle(size=10).encode(
        alt.X("hours(End):T"),
        alt.Y("Sleep quality", scale=alt.Scale(zero=False)),
        tooltip=["hours(End):T", "Sleep quality"],
        color=alt.condition(sleep_selection, alt.value(
            "orange"), alt.value("gray"))
    ).properties(
        width=240,
        height=180
    )

    heart_rate = alt.Chart(sleep_score_range).mark_circle(size=10).encode(
        alt.X("Heart rate"),
        alt.Y("Sleep quality", scale=alt.Scale(zero=False)),
        tooltip=["Heart rate", "Sleep quality"],
        color=alt.condition(sleep_selection, alt.value(
            "orange"), alt.value("gray"))
    ).properties(
        width=240,
        height=180
    )

    step = alt.Chart(sleep_score_range).mark_circle(size=10).encode(
        alt.X("Activity (steps)"),
        alt.Y("Sleep quality", scale=alt.Scale(zero=False)),
        tooltip=["Activity (steps)", "Sleep quality"],
        color=alt.condition(sleep_selection, alt.value(
            "orange"), alt.value("gray"))
    ).properties(
        width=240,
        height=180
    )

    # coffee = alt.Chart(sleep_score_range).mark_bar(size=10).encode(
    #     alt.X("Drank coffee:Q"),
    #     alt.Y("count()"),
    #     tooltip=["count()"]
    # ).transform_filter(sleep_selection).properties(
    #     width=240,
    #     height=180
    # )

    st.write(time_in_bed & (start_time | end_time) & (heart_rate | step))

    st.markdown(
        "#### Summary:\n" +
        "By exploring the dataset, we can see several points to improve sleep quality:\n" +
        "1. Sleep early. Do not try to go to sleep after 12 am.\n" +
        "2. Keep sleeping hours around 6-9. Do not sleep too much or too less.\n" +
        "3. Try to exercise more. People who tend to exercise more will get a much better sleep quality\n"
    )

    st.markdown(
        "Then we are ready to proceed to the last page!"
    )

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
