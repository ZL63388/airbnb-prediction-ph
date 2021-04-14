import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def load_css(file_name:str)->None:
    """
    Function to load and render a local stylesheet
    """
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")
         
df = pd.read_csv("schools_combined.csv")

my_page = st.sidebar.radio('Contents', ['Introduction','Methodology', 'Data Information',  'Topic Modeling', 'Regression Model','Conclusion & Recommendation'])
if my_page == 'Introduction':
    col1, mid, col2 = st.beta_columns([1,3,20])
    with col1:
        st.image('reddit_logo.png', width=100)
    with col2:
        st.title("A Subreddit Analysis on Jokes")
    st.image('status.png')
    st.header("Introduction")
    st.markdown("The purpose of this research is to provide an analysis on subreddits related to jokes by implementing a **topic modelling** algorithm to derive the joke topics and by applying a **regression algorithm** to identify which jokes will have high engagements.")
    st.write("\n\n")
    st.header("But why Humor?")
    st.markdown("The use of humor as an advertising technique has been recurrent among brands. Brands become impactful and memorable for the audience. Just by looking at the Philippine market, we have **Angkas** which posted last March 4 on **Facebook**. This post garnered a total of Facebook engagements of **32k likes, 1.7k comments, and 8.7k shares**.")
    st.write("\n")
    st.image('fb.png',caption="Angkas Facebook Post")
    st.write("\n")
    st.markdown("We even had **RC Cola Philippines** which tweeted its advertising video last November 26 on **Twitter**. This tweet garnered a total of Twitter Engagements of **20.6k likes, 1.5 retweets, and 8.6 Quote retweets**. In fact, this commercial was also featured in **The Ellen Show**, a widely known international tv show.")
    st.write("\n\n")
    st.video('https://www.youtube.com/watch?v=9zrExsQpQhU&t=3s')
    st.write("\n\n")
    st.header("So what are we trying to say here?")
    st.markdown("**Humor** is **global**. By using subreddits with millions of users around the globe, we can help individual or corporate brands identify which jokes can have high engagements. These jokes can then be used by these brands to have impactful advertising campaigns.")
    st.write("\n\n")
    st.header("The team's objectives:")
    st.markdown("1.    Analyze the joke subreddits by using Topic Modelling")
    st.markdown("2.    Identify which jokes will have high engagements through a Regression model")  

elif my_page == 'Methodology':
    col1, mid, col2 = st.beta_columns([1,8,20])
    with col1:
        st.image('reddit_logo.png', width=100)
    with col2:
        st.title("Methodology")
    st.image('status.png')
    st.markdown("**Insert Methodology**")

elif my_page == 'Data Information':
    col1, mid, col2 = st.beta_columns([1,8,20])
    with col1:
        st.image('reddit_logo.png', width=100)
    with col2:
        st.title("Data Information")
    st.image('status.png')
    st.write("\n\n")
    st.subheader("**Title**: The title of the submission.")
    st.subheader("**Self text**: The submissions’ selftext - an empty string if a link post.")
    st.subheader("**Upvote**: The number of upvotes for the submission.")
    st.subheader("**Downvote**: The number of downvotes for the submission.")
    st.subheader("**Upvote ratio**: The percentage of upvotes from  all votes on the submission.")
    st.subheader("**Number of comments**: The number of comments on the submission.")
    st.subheader("**NSFW**: Whether or not the submission has been marked as NSFW.")
   

elif my_page == 'Topic Modeling':
    col1, mid, col2 = st.beta_columns([1,8,20])
    with col1:
        st.image('reddit_logo.png', width=100)
    with col2:
        st.title("Topic Modeling")
    st.image('status.png')
 
    
elif my_page == 'Regression Model':
    col1, mid, col2 = st.beta_columns([1,8,20])
    with col1:
        st.image('reddit_logo.png', width=100)
    with col2:
        st.title("Regression Model")
    st.image('status.png')

    
elif my_page == 'Conclusion & Recommendation':
    col1, mid, col2 = st.beta_columns([1,2,20])
    with col1:
        st.image('reddit_logo.png', width=100)
    with col2:
        st.title("Conclusion & Recommendation")
    st.image('status.png')
    st.write("\n\n")
    st.header("Conclusion")
    st.markdown("The use of humor as an advertising technique has been recurrent among brands. Brands become impactful and memorable for the audience. Just by looking at the Philippine market, we have **Angkas** which posted last March 4 on **Facebook**. This post garnered a total of Facebook engagements of **32k likes, 1.7k comments, and 8.7k shares**.")
    st.write("\n\n")
    st.header("Recommendation")
    st.markdown("The use of humor as an advertising technique has been recurrent among brands. Brands become impactful and memorable for the audience. Just by looking at the Philippine market, we have **Angkas** which posted last March 4 on **Facebook**. This post garnered a total of Facebook engagements of **32k likes, 1.7k comments, and 8.7k shares**.")
    st.write("\n")