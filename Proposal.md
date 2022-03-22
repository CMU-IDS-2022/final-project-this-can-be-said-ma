# Final Project Proposal

**GitHub Repo URL**: https://github.com/CMU-IDS-2022/final-project-this-can-be-said-ma

**Group members**

Wenxing Deng, Jiuzhi Yu, Siyu Zhou, Huiyi Zhang


**Problem Description**

Stress is defined as a reaction to mental or emotional pressure [1]. It is probably one of the commonly experienced feelings, but it might be hard to share. Stress can be caused by a variety of sources includes uncertain future, discrimination, etc., and the coronavirus pandemic has risen as a substantial source of stress [2]. People from different age and/or socioeconomic groups may experience very different sources and symptoms of stress. In this project, we hope to bring a narrative of stress that enhances people’s understanding of it. The goal of the project is to have an in-depth understanding of the following questions: 

- What are the sources and impact of stress for people from different age groups and socioeconomic backgrounds? 
- What are the factors that correlate with stress level and how are they related?  
   - Delving into sleep quality: Stress is sometimes related to how well people sleep. What is the correlation between people’s sleep quality and stress levels? Can we detect stress levels from sleep quality?
- How is stress level reflected on people’s expression on social media? We will provide a stress level detection service that takes in users’ text inputs. 
When the stress level turns to be overwhelming, what are tips for people from different age groups? 

We will first start with introductory visualizations that give users an overview of how people from different groups face different sources and symptoms of stress. Users will be able to interactively zoom in to the groups of interest and explore survey results of stress among different age, gender, racial, geographical, and/or socioeconomic groups. 

To understand the impact of stress, we plan to pick 1-3 factors and explore their correlation with stress level. For example, this kaggle dataset [3] illustrates people’s attitude towards music and the perceived stress level. In addition, Covid19 pandemic has caused high stress levels for many groups, among them students who experienced educational stress [4]. 

To further understand how stress level is related to and affected by those factors, we plan to delve deeper into the sleeping factor as an example. Given the dataset [5], we first plan to visualize the correlation between stress and the quality of sleep, in terms of snoring rate, heart rate, body temperature, and sleeping hours. Second, based on the correlation and also sleeping data gathered by apple watch [6], which is a good representative of people’s sleeping patterns, we hope to figure out the deciding factors for improving sleep quality. Third, we plan to make some suggestions on how to change these sleeping patterns to improve the sleep quality, so as to reduce the overall stress level. 

​​After the user has fully understood the reasons for the formation of stress and the impact of stress on people, we plan to design an interactive function to detect the user's current stress situation. Users can know their stress level through our program, and at the same time, the function will personalize the user with customized stress relief suggestions. Our program will ask the user to input a sentence. After the system receives the text, it will use the machine learning model to analyze the text input by the user, and give the system a stress analysis of the sentence. We plan to use natural language processing (NLP) and machine learning methods to build stress classification models. This was inspired by the published paper called Dreaddit: A Reddit Dataset for Stress Analysis in Social Media [7]. We plan to use the Twitter and Reddit Sentimental analysis Dataset [8] to train the model. We believe this function will allow our program to interact with users in an interesting way and give them a clearer picture of their stress situations and personalized care advice. It makes our program not only educational, but also allows users to know their stress situation and guide them through ways to reduce the negative effects of stress.

For people of different ages, we will provide corresponding tips for reducing stress. Although we can provide general tips like exercising and eating healthy food for ages, we plan to provide more detailed and specific tips. For example, we will recommend kids and teens who age from 6 to 17 exercise at least 60 minutes a day. But for older people, we will suggest they take 40-minute walks three days per week as their physical conditions may not allow them to exercise much. And for the diet suggestions, we will recommend kids and teens eat an abundance of vegetables, fish, nuts and eggs. While we will ask the young adults to reduce their alcohol, caffeine, sugar intake. And for older people, we will suggest they avoid sugar as overconsumption of sugar has a direct correlation to obesity, diabetes and even death.


**Dataset & References**

[1] https://www.nhs.uk/mental-health/feelings-symptoms-behaviours/feelings-and-symptoms/stress/#:~:text=Causes%20of%20stress,such%20as%20adrenaline%20and%20cortisol.

[2] https://www.apa.org/news/press/releases/stress/2020/report-october

[3] https://www.kaggle.com/datasets/tineeeeey/perceived-stress-level-and-attitude-towards-music

[4] https://www.kaggle.com/datasets/bsoyka3/educational-stress-due-to-the-coronavirus-pandemic

[5] https://www.kaggle.com/datasets/laavanya/human-stress-detection-in-and-through-sleep?select=SaYoPillow.csv

[6] https://www.kaggle.com/datasets/danagerous/sleep-data

[7] https://arxiv.org/abs/1911.00133

[8] https://www.kaggle.com/datasets/cosmos98/twitter-and-reddit-sentimental-analysis-dataset
