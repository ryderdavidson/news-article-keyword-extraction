#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Use newsapi and spacy to generate keywords related to recent articles on COVID.
Graphically show these keyword results in a wordcloud using pyplot and WordCloud.

Author: Ryder Davidson
Class: CS-4650-01
Module: HW#5
"""

import string
import spacy
import pandas as pd
import matplotlib.pyplot as plt
from newsapi import NewsApiClient
from datetime import date, timedelta
from collections import Counter
from wordcloud import WordCloud


def get_keywords_eng(text):
    """Tokenize text, remove stop words and punctuation, and return keywords."""
    result = []
    for token in nlp_eng(text):
        if token.text in nlp_eng.Defaults.stop_words or token.text in string.punctuation:
            continue
        else:
            result.append(token.text)
    return result


def get_top_five(text):
    """Take a list of keywords and return the top five most common keywords."""
    return [x[0] for x in Counter(text).most_common(5)]


pd.set_option('display.max_rows', None, 'display.max_columns', None)
nlp_eng = spacy.load('en_core_web_sm')
newsapi = NewsApiClient(api_key='9db55cc40c4146e5b74d822e29303402')
start_date = date.today() - timedelta(days=30)

# These API call parameters are restricted by "developer level" subscription to newsapi.
# More substantial results can be obtained by acquiring a paid licence for this API.
query_params = {
    "q": "coronavirus",
    "language": "en",
    "from_param": start_date,
    "to": date.today(),
    "sort_by": "relevancy",
    "page": 5
}

raw_data = newsapi.get_everything(**query_params)
clean_data = []

for i in raw_data['articles']:
    clean_data.append({'title': i['title'], 'desc': i['description'], 'content': i['content']})

df = pd.DataFrame(clean_data)
df = df.dropna()
df['keyword'] = df['title'].apply(get_keywords_eng).apply(get_top_five)


# Generate a wordcloud using the 'keyword' column of the dataframe above.
results = str(df['keyword'])
wordcloud = WordCloud(max_font_size=50, max_words=100, background_color='white').generate(results)
plt.figure()
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

