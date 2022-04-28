import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import bentoml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from gensim.models import Word2Vec
import sys
sys.path.append('script/')
from bentoml.artifact import PickleArtifact
from bentoml.handlers import DataframeHandler
from data_preprocess import Posts
from word_embedding_vectorizer import WordEmbeddingVectorizer
from gensim.models import Word2Vec
import nltk
import time

################################################
##########      Global attributes     ##########
################################################
saved_path = "./bentoml/repository/WordEmbeddingModel/20220424153645_7494D6"
stress_sleep_attrs = ["snoring rate", "respiration rate", "body temperature",
                      "limb movement", "body oxygen", "eye movement", "sleeping hours", "heart rate"]


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
    sleep_data["Start"] = pd.to_datetime(
        sleep_data["Start"], format='%H:%M:%S').dt.tz_localize("US/Eastern")
    sleep_data["End"] = pd.to_datetime(
        sleep_data["End"], format='%H:%M:%S').dt.tz_localize("US/Eastern")
    return sleep_stress, sleep_data


def plot(title, df, xlabel, ylabel, column, index):
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
                test_df = test_df.append(
                    {column: index[i], xlabel: disorder[j], ylabel: P[i]}, ignore_index=True)
            elif j == 1:
                test_df = test_df.append(
                    {column: index[i], xlabel: disorder[j], ylabel: D[i]}, ignore_index=True)
            elif j == 2:
                test_df = test_df.append(
                    {column: index[i], xlabel: disorder[j], ylabel: S[i]}, ignore_index=True)
            elif j == 3:
                test_df = test_df.append(
                    {column: index[i], xlabel: disorder[j], ylabel: A[i]}, ignore_index=True)
            elif j == 4:
                test_df = test_df.append(
                    {column: index[i], xlabel: disorder[j], ylabel: N[i]}, ignore_index=True)

    c = alt.Chart(test_df).mark_bar().encode(x=xlabel, y=ylabel, column=alt.Column(
        column, sort=index), color=alt.Column(column, sort=index), tooltip=[ylabel]).properties(title=title)
    st.altair_chart(c)


def plot_pie(df, disorder):
    index = ["Panic attack", "depression", "anxiety", 'stress']
    dfs = []
    for i in range(len(index)):
        dfs.append(df[df["mental_disorder"] == index[i]])
    dfs.append(df[(df["mental_disorder"] != index[0]) & (df["mental_disorder"] != index[1]) & (
        df["mental_disorder"] != index[2]) & (df["mental_disorder"] != index[3])])
    P, D, S, A, N = [0] * 2, [0] * 2, [0] * 2, [0] * 2, [0] * 2
    therapy = ['no', 'yes']
    for i in range(2):
        P[i] = len(dfs[0][dfs[0]["therapy"] == therapy[i]])
        D[i] = len(dfs[1][dfs[1]["therapy"] == therapy[i]])
        S[i] = len(dfs[2][dfs[2]["therapy"] == therapy[i]])
        A[i] = len(dfs[3][dfs[3]["therapy"] == therapy[i]])
        N[i] = len(dfs[4][dfs[4]["therapy"] == therapy[i]])
    if disorder == "Panic attack":
        source = pd.DataFrame({"category": ['no', 'yes'], "value": P})
        title = "Percentage of people seeking therapy who have panic attack"
    elif disorder == "Depression":
        source = pd.DataFrame({"category": ['no', 'yes'], "value": D})
        title = "Percentage of people seeking therapy who have depression"
    elif disorder == "Anxiety":
        source = pd.DataFrame({"category": ['no', 'yes'], "value": A})
        title = "Percentage of people seeking therapy who have anxiety"
    elif disorder == "Stress":
        source = pd.DataFrame({"category": ['no', 'yes'], "value": S})
        title = "Percentage of people seeking therapy who have stress"
    elif disorder == "No mental disorder":
        source = pd.DataFrame({"category": ['no', 'yes'], "value": N})
        title = "Percentage of people seeking therapy who don't have any mental disorders"
    c = alt.Chart(source).mark_arc().encode(
        theta=alt.Theta(field="value", type="quantitative"),
        color=alt.Color(field="category", scale=alt.Scale(scheme='set2')), tooltip=["value"]).properties(title=title)
    st.altair_chart(c, use_container_width=True)

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


# st.markdown(
#     """
#     <style>
#         .stProgress > div > div > div > div {
#             background-image: linear-gradient(to right, green, 35%, #81D181);
#         }
#     </style>""",
#     unsafe_allow_html=True,
# )


@bentoml.artifacts([PickleArtifact('word_vectorizer'),
                    PickleArtifact('word_embedding_rf')]) 

@bentoml.env(pip_dependencies=["pandas", "numpy", "gensim", "scikit-learn", "nltk"])

class WordEmbeddingModel(bentoml.BentoService):
        
    @bentoml.api(DataframeHandler, typ='series')
    def preprocess(self, series):
        preprocess_series = Posts(series).preprocess()
        input_matrix = self.artifacts.word_vectorizer.fit(preprocess_series).transform(preprocess_series)
        return input_matrix
    
    @bentoml.api(DataframeHandler, typ='series')
    def predict(self, series):
        input_matrix = self.preprocess(series)
        pred_labels = self.artifacts.word_embedding_rf.predict(input_matrix)
        pred_proba = self.artifacts.word_embedding_rf.predict_proba(input_matrix)
        confidence_score = [prob[1] for prob in pred_proba]
        output = pd.DataFrame({'text': series, 'confidence_score': confidence_score, 'labels': pred_labels})
        output['labels'] = output['labels'].map({1: 'stress', 0: 'non-stress'})
        
        return output

@st.cache
def load_covidistress_data():
    path = 'data/COVIDiSTRESS_May_30_cleaned_final.csv'
    df = pd.read_csv(path, encoding = "ISO-8859-1")
    columns = ['answered_all', 'Dem_age', 'Dem_gender', 'Dem_edu', 'Dem_edu_mom', 'Dem_employment', 'Country',
               'Dem_maritalstatus', 'Dem_dependents', 'Dem_riskgroup', 'PSS10_avg', 'SPS_avg', 'SLON3_avg']
    df_s = df[columns]
    df_s = df_s.dropna()
    return df_s

def plot_covid_corr_stress_slon(df, option_c1):
    if option_c1 == "Gender": var = 'Dem_gender'
    if option_c1 == "Education level": var = 'Dem_edu'
    if option_c1 == "Mother\' education level": var = 'Dem_edu_mom'
    if option_c1 == "Employment status": var = 'Dem_employment'
    if option_c1 == "Marital status": var = 'Dem_maritalstatus'
    if option_c1 == "Risk group": var = 'Dem_riskgroup'
    area_selection = alt.selection_interval(empty="all")
    corr1 = alt.Chart(df).mark_circle(size=10).encode(
        y=alt.Y("PSS10_avg", title='Perceived stress', scale=alt.Scale(domainMin=0.5, domainMax=5.5)),
        x=alt.X("SLON3_avg", title="Scale of loneliness", scale=alt.Scale(domainMin=0.5, domainMax=5.5)),
        tooltip=["Dem_age", "Dem_gender", "Dem_employment", "Dem_maritalstatus"],
        color=alt.condition(
            area_selection, var, alt.value("lightgrey"))
    ).add_selection(
        area_selection
    ).properties(
        width=500,
        height=400,
        title="Correlation between stress and self-identified scale of loneliness"
    )#.interactive()
    hist1 = alt.Chart(df).transform_filter(
        area_selection
    ).transform_joinaggregate(
    total='count(*)'
    ).transform_calculate(
        pct='1 / datum.total'
    ).mark_bar().encode(
        x=alt.X('sum(pct):Q', title='Percentage of data'),
        y=alt.Y(var, title=option_c1),
        color=var,
        tooltip="count()"
    ).properties(
        width=500
    )
    st.write(corr1 & hist1)

def plot_covid_corr_stress_sps(df, option_c3):
    if option_c3 == "Gender": var = 'Dem_gender'
    if option_c3 == "Education level": var = 'Dem_edu'
    if option_c3 == "Mother\' education level": var = 'Dem_edu_mom'
    if option_c3 == "Employment status": var = 'Dem_employment'
    if option_c3 == "Marital status": var = 'Dem_maritalstatus'
    if option_c3 == "Risk group": var = 'Dem_riskgroup'
    area_selection = alt.selection_interval(empty="all")
    corr1 = alt.Chart(df).mark_circle(size=10).encode(
        y=alt.Y("PSS10_avg", title='Perceived stress', scale=alt.Scale(domainMin=0.5, domainMax=5.5)),
        x=alt.X("SPS_avg", title="Social provision scale", scale=alt.Scale(domainMin=0.5, domainMax=6.5)),
        tooltip=["Dem_age", "Dem_gender", "Dem_employment", "Dem_maritalstatus"],
        color=alt.condition(
            area_selection, var, alt.value("lightgrey"))
    ).add_selection(
        area_selection
    ).properties(
        width=500,
        height=400,
        title="Correlation between stress and social provision scale"
    )  # .interactive()
    hist1 = alt.Chart(df).transform_filter(
        area_selection
    ).transform_joinaggregate(
        total='count(*)'
    ).transform_calculate(
        pct='1 / datum.total'
    ).mark_bar().encode(
        x=alt.X('sum(pct):Q', title='Percentage of data'),
        y=alt.Y(var, title=option_c1),
        color=var,
        tooltip="count()"
    ).properties(
        width=500
    )
    st.write(corr1 & hist1)

def plot_covid_stress(df, option_c2):
    if option_c2 == "Gender": var = 'Dem_gender'
    if option_c2 == "Education level": var = 'Dem_edu'
    if option_c2 == "Mother\' education level": var = 'Dem_edu_mom'
    if option_c2 == "Employment status": var = 'Dem_employment'
    if option_c2 == "Marital status": var = 'Dem_maritalstatus'
    if option_c2 == "Risk group": var = 'Dem_riskgroup'
    df_new = df[['PSS10_avg', var]].groupby(var).mean().reset_index()

    selec = alt.selection_single(fields=[var], empty='all')
    bar1 = alt.Chart(df_new).mark_bar().encode(
        x=alt.X('PSS10_avg', title="Perceived stress"),
        y=var,
        color=alt.condition(selec, var, alt.value('lightgrey')),
        tooltip=['PSS10_avg']
    ).properties(
        title='Average perceived stress level for different ' + option_c2
    ).add_selection(
        selec
    )
    try:
        df_slice = df[df[var]==selec]
    except:
        df_slice = df.copy()
    hist1 = alt.Chart(df_slice).transform_filter(
        selec
    ).mark_area(
        opacity=0.5,
        interpolate='step'
    ).encode(
        alt.X('PSS10_avg:Q', bin=alt.Bin(maxbins=100, step=0.5), title="Perceived stress"),
        alt.Y('count()', stack=None),
        tooltip=['count()']
    ).interactive()
    st.write(bar1 & hist1)


@st.cache
def load_educational_stress_data():
    df_edu= pd.read_csv(
        "data/covid_school_stress_responses.csv"
    )
    df_edu['Change in classwork stress'] = df_edu['Now-ClassworkStress'] - df_edu['Before-ClassworkStress']
    df_edu['Change in homework stress'] = df_edu['Now-HomeworkStress'] - df_edu['Before-HomeworkStress']
    df_edu['Change in homework hours'] = df_edu['Now-HomeworkHours'] - df_edu['Before-HomeworkHours']
    return df_edu

def plot_edu_dist_overview(option_g1, option_g2, option_g3, option_e1, option_e2, option_e3):
    df_edu = load_educational_stress_data()
    if not option_g1:
        df_edu = df_edu[df_edu['Gender'] != 'Female']
    if not option_g2:
        df_edu = df_edu[df_edu['Gender'] != 'Male']
    if not option_g3:
        df_edu = df_edu[df_edu['Gender'] != 'Other']
    if not option_e1:
        df_edu = df_edu[df_edu['Before-Environment'] != 'Physical']
    if not option_e2:
        df_edu = df_edu[df_edu['Before-Environment'] != 'Virtual']
    if not option_e3:
        df_edu = df_edu[df_edu['Before-Environment'] != 'Hybrid']
    df_classwork_melted = df_edu[['Before-ClassworkStress', 'Now-ClassworkStress']].melt(var_name='Stage',
                                                                                         value_name='Classwork Stress')
    df_homework_melted = df_edu[['Before-HomeworkStress', 'Now-HomeworkStress']].melt(var_name='Stage',
                                                                                         value_name='Homework Stress')
    edu_chart1 = alt.Chart(df_classwork_melted).mark_area(
        opacity=0.5,
        interpolate='step'
    ).encode(
        alt.X('Classwork Stress:Q', bin=alt.Bin(maxbins=100, step=0.5)),
        alt.Y('count()', stack=None),
        alt.Color('Stage:N')
    ).properties(
        title='Change in Experienced Classwork Stress'
    )
    edu_chart2 = alt.Chart(df_homework_melted).mark_area(
        opacity=0.5,
        interpolate='step'
    ).encode(
        alt.X('Homework Stress:Q', bin=alt.Bin(maxbins=100, step=0.5)),
        alt.Y('count()', stack=None),
        alt.Color('Stage:N')
    ).properties(
        title='Changes in Experienced Homework Stress'
    )
    st.altair_chart(edu_chart1, use_container_width=True)
    st.altair_chart(edu_chart2, use_container_width=True)
    # cur_chart = alt.vconcat(edu_chart1, edu_chart2)
    # st.write(cur_chart)

def plot_edu_age():
    df_edu = load_educational_stress_data()
    df_count = df_edu[[
        'Age', 'FamilyRelationships'
    ]].groupby('Age').count().reset_index().rename({"FamilyRelationships": "Count"}, axis=1)

    df_grouped = df_edu[[
        'Age', 'Change in classwork stress', 'Change in homework stress', 'Change in homework hours'
    ]].groupby('Age').mean().reset_index()
    df_grouped = df_grouped.merge(df_count, on="Age", how='left')

    df_melted = df_grouped[['Age', 'Count', 'Change in classwork stress', 'Change in homework stress', 'Change in homework hours']].melt(
        id_vars=['Age', 'Count'], value_vars=['Change in classwork stress', 'Change in homework stress', 'Change in homework hours'],
        var_name='Stress Type', value_name='Change in Stress Level')

    edu_chart1 = alt.Chart(df_melted).mark_bar().encode(
        column=alt.Column("Age"),
        x=alt.X('Stress Type', title="", axis=alt.Axis(labelAngle=60)),
        y='Change in Stress Level',
        color='Stress Type',
        tooltip='Count'
    ).properties(
        title='Change in Experienced Stress Level by Age',
        width=45,
        height=300
    )
    st.altair_chart(edu_chart1)


def plot_edu_gender():
    df_edu = load_educational_stress_data()
    df_count = df_edu[[
        'Gender', 'FamilyRelationships'
    ]].groupby('Gender').count().reset_index().rename({"FamilyRelationships": "Count"}, axis=1)

    df_grouped = df_edu[[
        'Gender', 'Change in classwork stress', 'Change in homework stress', 'Change in homework hours'
    ]].groupby('Gender').mean().reset_index()
    df_grouped = df_grouped.merge(df_count, on="Gender", how='left')
    df_melted = df_grouped[['Gender', 'Count', 'Change in classwork stress', 'Change in homework stress', 'Change in homework hours']].melt(
        id_vars=['Gender', 'Count'], value_vars=['Change in classwork stress', 'Change in homework stress', 'Change in homework hours'],
        var_name='Stress Type', value_name='Change in Stress Level')

    edu_chart1 = alt.Chart(df_melted).mark_bar().encode(
        row=alt.Row("Gender"),
        y=alt.Y('Stress Type', title=""),
        x='Change in Stress Level',
        color='Stress Type',
        tooltip='Count'
    ).properties(
        title='Change in Experienced Stress Level by Gender',
        width=300,
        height=100
    )
    st.altair_chart(edu_chart1)


def plot_edu_relationship_corr():
    df_edu = load_educational_stress_data()
    corrMatrix = df_edu[['Change in classwork stress', 'Change in homework stress', 'FamilyRelationships',
                         'FriendRelationships']].corr().reset_index().melt('index')
    corrMatrix.columns = ['var1', 'var2', 'correlation']
    square_brush = alt.selection_single(fields=['var1', 'var2'], clear=False,
                                  init={'var1': 'FriendRelationships', 'var2': 'FamilyRelationships'})
    base = alt.Chart(corrMatrix).transform_filter(
        alt.datum.var1 <= alt.datum.var2
    ).encode(
        x=alt.X('var1', title="Stress factor 1"),
        y=alt.Y('var2', title="Stress factor 2"),
    ).properties(
        width=alt.Step(55),
        height=alt.Step(55)
    )
    rects = base.mark_rect().encode(
        color='correlation'
    ).add_selection(square_brush)
    
    text = base.mark_text(
        size=15
    ).encode(
        text=alt.Text('correlation', format=".2f"),
        color=alt.condition(
            "datum.correlation > 0.5",
            alt.value('white'),
            alt.value('black')
        )
    )
    # st.write(rects + text)

    def generate_2d(var1, var2):
        H, xe, ye = np.histogram2d(df_edu[var1], df_edu[var2], density=True)
        H[H == 0] = np.nan
        xe = pd.Series(['{0:.4g}'.format(num) for num in xe])
        xe = pd.DataFrame({"a": xe.shift(), "b": xe}).dropna().agg(' - '.join, axis=1)
        ye = pd.Series(['{0:.4g}'.format(num) for num in ye])
        ye = pd.DataFrame({"a": ye.shift(), "b": ye}).dropna().agg(' - '.join, axis=1)

        res = pd.DataFrame(
            H, index=ye, columns=xe
        ).reset_index().melt(id_vars='index').rename(columns={'index': 'value2',
                                                              'value': 'count',
                                                              'variable': 'value'})
        res['raw_left_value'] = res['value'].str.split(' - ').map(lambda x: x[0]).astype(float)
        res['raw_left_value2'] = res['value2'].str.split(' - ').map(lambda x: x[0]).astype(float)
        res['var1'] = var1
        res['var2'] = var2
        return res.dropna()

    table_2d = pd.concat(
        [generate_2d(var1, var2) for var1 in corrMatrix['var1'] for var2 in corrMatrix['var2']])
    # st.write(table_2d)

    scat_plot = alt.Chart(table_2d).transform_filter(
        square_brush
    ).mark_rect().encode(
        alt.X('value:N', sort=alt.EncodingSortField(field='raw_left_value'), title='Selected factor 1'),
        alt.Y('value2:N', sort=alt.EncodingSortField(field='raw_left_value2', order='descending'), title='Selected factor 2'),
        alt.Color('count:Q', scale=alt.Scale(scheme='blues'))
    )
    concat = alt.hconcat((rects + text).properties(width=230, height=230),
                        scat_plot.properties(width=230, height=230),
                         title = 'Correlation between Changes in Stress Level and Changes in Familly & Friends Relationship').resolve_scale(color='independent')
    st.write(concat)



        

################################################
##########      Main starts here      ##########
################################################

nltk.download("stopwords")
nltk.download("wordnet")
nltk.download('omw-1.4')

st.title("Stress Analysis: Narrative of stress to enhance people's understanding")

st.sidebar.title(
    "Stress Data Analysis: To have an in-depth understanding of the following questions")
st.sidebar.markdown(
    "This application is a Streamlit dashboard to enhances people's understanding of stress")

st.sidebar.header("Page navigation")
selectplot = st.sidebar.selectbox("Select the question you want to view", [
                                  "Introduction", "Stress sources", "Factors correlate with stress level", "Test your stress"], key="0")
# Page 0
if selectplot == "Introduction":
    st.markdown(
        "### Purpose of this application\n" +
        "Stress is defined as a reaction to mental or emotional pressure. It is probably one of the commonly experienced feelings, " + 
        "but it might be hard to share. In this application, we will show a general overview of stress, including the sources, " + 
        "the factors that will influence people's stress level, and the relationship of stress. Then you may use our application to determine your level of stress.\n"
    )
    st.image('img/meme.jpeg', caption='Meme on handling stress, source: https://rankedbyvotes.com/memes/memes-about-stress/')
    st.markdown(
        "### Overall structure\n" +
        "We will bring a narrative of stress that enhances people’s understanding of it through the following three sections. \n" +
        "- Stress sources \n" +
        "- Factors correlate with stress level\n" +
        "- Test your stress level\n" + 
        "### Please proceed to the next page to start your exploration!"
    )
    # st.markdown(
    #     "Do we need an intro page to show the overall structure of our application?\n" +
    #     "## Purpose of this application\n" + 
    #     "In this application, we will show a general overview of stress, including the sources of stress, the factors that will" +
    #     "influence people's stress level, and the relationship of stress and social media.\n" +
    #     "## Overall structure\n" +
    #     "There are in total four pages in this application. (Need more words here?)\n" +
    #     "1. Overall introduction\n" +
    #     "2. Stress & age/backgrounds\n" +
    #     "3. Factors correlate with stress level\n" +
    #     "4. Factors correlate with stress level\n" + 
    #     "### Please proceed to page 2 to start your exploration!"
    # )

# Page 1
if selectplot == "Stress sources":
    st.sidebar.markdown("##### Dataset: Mental Health Checker")
    st.markdown("Stress is defined as a reaction to mental or emotional pressure. It is probably \
   one of the commonly experienced feelings, but it might be hard to share. Stress can be caused by a \
   variety of sources includes uncertain future, discrimination, etc., and the coronavirus pandemic \
   has risen as a substantial source of stress. People from different age and/or socioeconomic \
   groups may experience very different sources and symptoms of stress. In this project, we hope to bring \
   a narrative of stress that enhances people's understanding of it.")

    st.subheader(
        'What are the sources and impact of stress for people from different backgrounds?')
    st.markdown("We will use the Kaggle dataset *Mental Health Checker* collected from a mental health survey for general analysis. \
   The survey consists of 36 questions and has 207 interviewees. Here are the 36 questions of the survey.")
    image = Image.open('img/1.png')
    st.image(image)

    st.markdown("First, let's explore whether stress level has specific relationships with gender, \
   age, marital status, income level, loan, time spent in social media per day and sleep disorder. ")

    mental_df = load_mental_data()

    factor = st.selectbox("Please select the factors you are interested in and analyze the bar charts.", [
        "gender", "age", "marital", "income", "loan", "social media", "sleep disorder"])
    if factor == "gender":
        plot("Mental disorder distribution among different genders", mental_df,
             "Mental disorder type", "Number of interviewees", 'gender', ['Female', 'Male'])
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

    st.markdown(
        "Next, let's visualize the percentage of people seeking therapy with different mental disorder levels.")
    disorder_factor = st.selectbox("Please select the mental disorder levels you want to explore further.", [
        "Panic attack", "Depression", "Anxiety", 'Stress', "No mental disorder"])
    plot_pie(mental_df, disorder_factor)
    st.markdown("We can figure out that many people seek therapy when they have panic attacks. \
    But only a small portion of people with depression, anxiety and stress go to therapy. We want to \
    encourage people with mental disorders to seek appropriate therapy when they are not feeling very well through our project.")


# Page 2
elif selectplot == "Factors correlate with stress level":

    st.sidebar.markdown(
        "##### Dataset:\n" + 
        "1. COVIDiSTRESS\n" + 
        "2. COVID-19's Impact on Educational Stress\n" +
        "3. Human Stress Detection in and through Sleep\n" +
        "4. Personal Sleep Data from Sleep Cycle iOS App\n"
    )
    st.markdown(
        "In this page, we will explore several factors that can influence people's stress level.\n" +
        "1. COVID-19's Impact on Stress\n" + 
        "2. Impact of Sleep on Stress"
    )

    st.subheader("1. Impact of COVID-19 on Stress")
    st.markdown("According to [American Psychological Association](https://www.apa.org/news/press/releases/stress/2020/report-october)\
            , stress can be caused by a variety \
            of sources includes uncertain future, discrimination, etc., and the coronavirus pandemic\
            has risen as a substantial source of stress. In this section, we will explore stress caused\
            by the COVID-19 pandemic. ")
    # dataset 1: educational stress
    st.markdown("#### 1.1 Educational Stress Experienced by Students")
    st.markdown("In this section, we will explore the relationship between the COVID-19 pandemic and \
            educational stress experienced by students. Students in the age of middle school, high school, \
            and college reported their stress level before and after the pandemic.")
    # visualization: distribution overview
    st.markdown(
        "##### 1.1.1 Overall change in educational stress level\n" +
        "Let's explore the overall distribution of change in stress level experienced by students from different groups."
    )
    # with st.form("my_form"):
    #     st.write("Inside the form")
    #     slider_val = st.slider("Form slider")
    #     checkbox_val = st.checkbox("Form checkbox")
    #
    #     # Every form must have a submit button.
    #     submitted = st.form_submit_button("Submit")
    #     if submitted:
    #         st.write("slider", slider_val, "checkbox", checkbox_val)
    with st.form("my_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('**Gender**')
            option_g1 = st.checkbox('Female', value=True)
            option_g2 = st.checkbox('Male', value=True)
            option_g3 = st.checkbox('Other', value=True)
        with col2:
            st.markdown('**Before pandemic education environment**')
            option_e1 = st.checkbox('Physical', value=True)
            option_e2 = st.checkbox('Virtual', value=True)
            option_e3 = st.checkbox('Hybrid', value=True)
        submitted = st.form_submit_button("Submit")
        if submitted:
            plot_edu_dist_overview(option_g1, option_g2, option_g3, option_e1, option_e2, option_e3)

    # # visualization: factor=age
    # st.markdown(
    #     "#### 1.1.2 Factors related to stress level\n" +
    #     "Does there exist systematic difference in change in experienced stress level across different age and gender groups?"
    # )
    # plot_edu_age()
    
    # # visualization: factor=gender
    # plot_edu_gender()

    # visualization: factor=family & friends relationship
    st.markdown(
        "##### 1.1.2 Correlation between changes in stress level and social relationships\n" +
        "A positive family or friends relationship suggests improved relationship after the pandemic. \n" +
        "Let's explore the correlation between them!\n *Click on the correlation blocks to see detailed heatmap.*\n"
    )
    plot_edu_relationship_corr()

    # dataset 2: COVID-19 stress
    st.markdown("#### 1.2 Global Survey on Psychological and Behavioral Consequences of the COVID-19 Outbreak")
    st.markdown("The COVIDiSTRESS dataset is a global survey that collects psychological and behavioural responses to \
                the  pandemic. In this section, we will delve into the relationship between stress and the pandemic.")
    df_covid = load_covidistress_data()
    # visualization: preceived stress (PSS10_avg)
    st.markdown("##### 1.2.1 Preceived stress")
    
    option_c2 = st.selectbox("Select the aspect to view distribution of perceived stress.",
                             ('Employment status', 'Education level', 'Mother\' education level', 'Gender',
                              'Marital status', 'Risk group')
                             )
    st.markdown("*Click on the bar of different categories to explore the difference in stress distribution*")
    plot_covid_stress(df_covid, option_c2)

    # visualization: availability of social provisions (SPS-10)
    st.markdown("##### 1.2.2 Correlation between perceived stress and self-reported scale loneliness")
    option_c1 = st.selectbox("Select the aspect for more details",
                             ('Employment status', 'Education level', 'Mother\' education level', 'Gender',
                              'Marital status', 'Risk group')
                             )
    st.markdown("*Select the area of interest to explore*")
    plot_covid_corr_stress_slon(df_covid, option_c1)

    # visualization: self-report scale of loneliness (SLON3_avg)
    st.markdown("##### 1.2.3 Correlation between perceived stress and availability of social provisions ")
    st.markdown("*Select the area of interest to explore*")
    option_c3 = st.selectbox("Select the aspect for more details ...",
                             ('Employment status', 'Education level', 'Mother\' education level', 'Gender',
                              'Marital status', 'Risk group')
                             )
    plot_covid_corr_stress_sps(df_covid, option_c3)



    
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
        "You can select some data points in \"Start (hours)\" to see other sleep attributes of these people!"
    )
    sleep_cols = st.columns(2)
    with sleep_cols[0]:
        st.metric("Mean sleep quality", round(sleep_score_range["Sleep quality"].mean(), 2))
    with sleep_cols[1]:
        st.metric("Sleep quality std", round(sleep_score_range["Sleep quality"].std(), 2))

    sleep_quality = alt.Chart(sleep_score_range).mark_bar().encode(
        alt.X("Sleep quality", scale=alt.Scale(zero=False), bin=True),
        alt.Y("count()"),
        tooltip=["count()"]
    ).properties(
        width=200,
        height=150
    )

    time_in_bed = alt.Chart(sleep_score_range).mark_circle(size=10).encode(
        alt.X("Time in bed"),
        alt.Y("Sleep quality", scale=alt.Scale(zero=False)),
        tooltip=["Time in bed", "Sleep quality"],
        color=alt.condition(sleep_selection, alt.value(
            "steelblue"), alt.value("gray"))
    ).properties(
        width=200,
        height=150
    )

    start_time = alt.Chart(sleep_score_range).mark_circle(size=10).add_selection(sleep_selection).encode(
        alt.X("hours(Start):T"),
        alt.Y("Sleep quality", scale=alt.Scale(zero=False)),
        tooltip=["hours(Start):T", "Sleep quality"],
        color=alt.condition(sleep_selection, alt.value(
            "orange"), alt.value("gray"))
    ).properties(
        width=200,
        height=150
    )

    end_time = alt.Chart(sleep_score_range).mark_circle(size=10).encode(
        alt.X("hours(End):T"),
        alt.Y("Sleep quality", scale=alt.Scale(zero=False)),
        tooltip=["hours(End):T", "Sleep quality"],
        color=alt.condition(sleep_selection, alt.value(
            "#aa33cc"), alt.value("gray"))
    ).properties(
        width=200,
        height=150
    )

    heart_rate = alt.Chart(sleep_score_range).mark_circle(size=10).encode(
        alt.X("Heart rate"),
        alt.Y("Sleep quality", scale=alt.Scale(zero=False)),
        tooltip=["Heart rate", "Sleep quality"],
        color=alt.condition(sleep_selection, alt.value(
            "#ff86c2"), alt.value("gray"))
    ).properties(
        width=200,
        height=150
    )

    step = alt.Chart(sleep_score_range).mark_circle(size=10).encode(
        alt.X("Activity (steps)"),
        alt.Y("Sleep quality", scale=alt.Scale(zero=False)),
        tooltip=["Activity (steps)", "Sleep quality"],
        color=alt.condition(sleep_selection, alt.value(
            "#50c878"), alt.value("gray"))
    ).properties(
        width=200,
        height=150
    )

    # coffee = alt.Chart(sleep_score_range).mark_bar(size=10).encode(
    #     alt.X("Drank coffee:Q"),
    #     alt.Y("count()"),
    #     tooltip=["count()"]
    # ).transform_filter(sleep_selection).properties(
    #     width=240,
    #     height=180
    # )

    st.write((sleep_quality | time_in_bed) & (start_time | end_time) & (heart_rate | step))

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
elif selectplot == "Test your stress":
    st.markdown("Did you know that what you say in your daily life or what you post on social media can tell you if you are stressed?")
    # st.subheader(
        # "Did you know that what you say in your daily life or what you post on social media can tell you if you are stressed?")
    # select = st.selectbox("To see which words are stressed and which aren't, keep going.", [
    #                       "show stress free post words", "show stress post words"], key="1")
    # if select == "show stress free post words":
    #     image = Image.open('img/20.png')
    #     st.image(image, caption='Non_stress_post_words')
    # else:
    #     image = Image.open('img/21.png')
    #     st.image(image, caption='Stress_post_words')

    st.sidebar.markdown(
        "##### Dataset: Dreaddit: A Reddit Dataset for Stress Analysis in Social Media")

    st.subheader(
        'How much stress are you under? Test it right now by typing in a sentence.')
    title = st.text_area(label='', value='Please enter some sentences here...')
    
    if title == "":
        st.markdown("###### Don't write a word? you must be too stressed to type.")

    elif title != 'Please enter some sentences here...':
        with st.spinner('Our model is detecting your stress level...'):
            # time.sleep()
            # st.write('Your input is: [', title, ']')
            stress = 0
            # Load exported bentoML model archive from path
            bento_model = bentoml.load(saved_path)
            # series = "We'd be saving so much money with this new house"
            series = pd.Series(title)
            output = bento_model.predict(series)
            time.sleep(3)
        if output["labels"].values == "stress":
            st.success('Our model detects that you are STRESSED from this sentence you input')
            st.image('img/stress.jpeg',width=300)
            ratio = output["confidence_score"].values[0]
            st.markdown("#### Your Stress Level is "+str(ratio))
            st.markdown("**Higher than 0.5: detected as stress**")
            st.markdown("Equal or lower than 0.5: detected as stress free")
            with st.expander("Expand to see how to lessen your stress"):
                select = st.radio(
                    "What's your age",
                    ( "6-17", "18-49", "50+"))
            # select = st.slider('How old are you?', min_value=6, max_value=100, value=20, step=1)
            # with st.expander("See tips for you"):
                if select=="6-17":
                    st.markdown("**Sleep well.** Sleep is essential for physical and emotional well-being. For children under 12 years old, they need 9 to 12 hours of sleep a night. Teens need 8 to 10 hours a night.")
                    st.markdown(
                        "**Exercise.** Physical activity is an essential stress reliever. At least 60 minutes a day of activity for children ages 6 to 17.")
                    st.markdown("**Talk it out.** Talking about stressful situations with a trusted adult can help kids and teens put things in perspective and find solutions. Parents can help them combat negative thinking, remind them of times they worked hard and improved.")
                    st.markdown("**Get outside.** Spending time in nature is an effective way to relieve stress and improve overall well-being. Researchers have found that people who live in areas with more green space have less depression, anxiety and stress.")
                    st.markdown(
                        "**Diet.** We recommend kids and teens eat an abundance of vegetables, fish, nuts and eggs.")
                elif select=="18-49":
                    st.markdown("**Spend less time on social media.** Spending time on social media sites can become stressful, not only because of what we might see on them, but also because the time you are spending on social media might be best spent enjoying visiting with friends, being outside enjoying the weather or reading a great book.")
                    st.markdown(
                        "**Manage your time.** When we prioritize and organize our tasks, we create a less stressful and more enjoyable life.")
                    st.markdown("**Having a balanced and healthy diet.** Making simple diet changes, such as reducing your alcohol, caffeine and sugar intake.")
                    st.markdown(
                        "**Share your feelings.** A conversation with a friend lets you know that you are not the only one having a bad day, caring for a sick child or working in a busy office. Stay in touch with friends and family. Let them provide love, support and guidance. Don’t try to cope alone.")
                elif select=="50+":
                    st.markdown("**Regular aerobic exercise.** Taking 40-minute walks three days per week will result in a 2% increase in the size of their hippocampus, the area of the brain involved in memory and learning. In contrast, without exercise, older adults can expect to see a decrease in the size of their hippocampus by about 1-2% each year.")
                    st.markdown("**Become active within your community and cultivate warm relationships.** You can choose to volunteer at a local organization, like a youth center, food bank, or animal shelter.")
                    st.markdown("**Diet.** Recommended diets include an abundance of vegetables, fish, meat, poultry, nuts, eggs and salads. Olders should avoid sugar, overconsumption of sugar has a direct correlation to obesity, diabetes, disease and even death.")
        else:
            st.success('We detected from your text that your stress level is NOT high') 
            # st.balloons()
            st.image('img/dogstress.jpg',width=400)
            ratio = output["confidence_score"].values[0]
            st.markdown("#### Your Stress Level is "+str(ratio))
            st.markdown("Higher than 0.5: DETECTED AS STRESSED")
            st.markdown("**Equal or Lower than 0.5: DETECTED AS STRESS FREE**") 
    else:
        st.markdown("")  
st.markdown(
    "This project was created by Wenxing Deng, Jiuzhi Yu, Siyu Zhou and Huiyi Zhang for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")
