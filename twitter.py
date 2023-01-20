
import streamlit as st
import plotly.express as px
st.sidebar.header('Twitter Sentiment Visualizer')
from transformers import pipeline
senti_pipeline = pipeline('sentiment-analysis')
st.markdown(
    f'''
        <style>
            .sidebar .sidebar-content {{
                width: 375px;
            }}
        </style>
    ''',
    unsafe_allow_html=True
)
uploaded_file = st.sidebar.file_uploader("Choose a file")
st. markdown("<h1 style='text-align: center; color: #3E3C3C;'>Twitter Sentiment Visualizer</h1>", unsafe_allow_html=True)
if uploaded_file is not None:
    import pandas as pd
    df = pd.read_csv(uploaded_file)
    df = df. iloc[:, [5,7,10,12]]
    sentiment = []
    polarity = []
    for i in df['text']:
        sentiment.append(senti_pipeline(i)[0]['label'])
        polarity.append(senti_pipeline(i)[0]['score'])
    df['sentiment'] = sentiment
    df['polarity'] = polarity
    st.dataframe(df)
    positive = 0
    negitive = 0
    neutral = 0
    for i in range(df.shape[0]):
        if df.loc[i, 'sentiment'] =='POSITIVE' and df.loc[i, 'polarity'] >0.96:
            positive+=1
        elif df.loc[i]['sentiment'] == 'NEGATIVE' and df.loc[i, 'polarity'] >0.96:
            negitive += 1
        else:
            df.at[i, 'sentiment'] = 'NEUTRAL'
            neutral += 1
    sentiment = ['positive', 'negitive', 'nuetral']
    arr = [positive, negitive, neutral]
    data = {'sentiment': sentiment,
            'val':  arr}
    # Create DataFrame
    st.markdown("<h3 style='text-align: center; color: black;'>Sentiment Analysis</h3>",
                                unsafe_allow_html=True)
    df1 = pd.DataFrame(data)
    fig = px.pie(df1, values='val', names='sentiment')
    fig
    x = df['airline'].value_counts().head()
    df2 = round((df['airline'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns = {'index': 'Airline', 'user': 'percentage'})
    count_p = []
    for i in df2['Airline']:
        df3 = df[df['airline'] == i]
        df3 = df3[df3['sentiment'] == 'POSITIVE']
        count_p.append(len(df3))
    df2['Positive'] = count_p
    count_n = []
    for i in df2['Airline']:
        df3 = df[df['airline'] == i]
        df3 = df3[df3['sentiment'] == 'NEGATIVE']
        count_n.append(len(df3))
    df2['Negitive'] = count_n
    count_nu = []
    for i in df2['Airline']:
        df3 = df[df['airline'] == i]
        df3 = df3[df3['sentiment'] == 'NEUTRAL']
        count_nu.append(len(df3))
    df2['Neutral'] = count_nu
    import plotly.graph_objects as go
    st.markdown("<h3 style='text-align: center; color: black;'>Positive Comments</h3>",
                                unsafe_allow_html=True)
    word = df2['Airline']
    number = df2['Positive']
    fig = px.bar(df2, y=number, x=word, color=word)
    fig
    st.markdown("<h3 style='text-align: center; color: black;'>Neutral Comments</h3>",
                                unsafe_allow_html=True)
    word = df2['Airline']
    number = df2['Neutral']
    fig = px.bar(df2, y=number, x=word, color=word)
    fig
    st.markdown("<h3 style='text-align: center; color: black;'>Negitive Comments</h3>",
                                unsafe_allow_html=True)
    word = df2['Airline']
    number = df2['Negitive']
    fig = px.bar(df2, y=number, x=word, color=word)
    fig
    x = df['name'].value_counts().head()
    new_df = round((df['name'].value_counts()/df.shape[0])*100, 2).reset_index().head(10).rename(columns = {'index': 'names', 'name': 'percentage'})
    names = new_df['names']
    percentage = new_df['percentage']
    fig = px.bar(new_df, x=names, y=percentage, color=names)
    fig
