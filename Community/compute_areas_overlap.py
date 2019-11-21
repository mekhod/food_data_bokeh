from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np


df_food_transformed = pd.read_csv('data/Food/df_transformed.csv')
areas_food = list(df_food_transformed.city)

df_voters_ratio = pd.read_csv('data/Community_Context/data_voters_ratio.csv')
areas_voters = list(df_voters_ratio.metropolitan)

areas_all = areas_food + areas_voters

vect = TfidfVectorizer(stop_words=["city", "new", "county", "falls"], analyzer='word')

tfidf = vect.fit_transform(areas_all)

pairwise_similarity = tfidf * tfidf.T

array_pairwise_similarity = pairwise_similarity.toarray()

mapper_area = {}
for i, area_food in enumerate(areas_food):
    array_similarity = array_pairwise_similarity[i]
    array_similarity_right_tail = array_similarity[len(areas_food):]
    max_array_similarity_right_tail = np.max(array_similarity_right_tail)

    if max_array_similarity_right_tail != 0:
        # array_argsort = np.flip(np.argsort(array_similarity_right_tail))
        # for ind in array_argsort:
        #     similarity = array_similarity_right_tail[ind]
        #     count = 0
        #     if similarity != 0:
        arg_max_array_similarity_right_tail = np.argmax(array_similarity_right_tail)
        area_voter = areas_voters[arg_max_array_similarity_right_tail]
                # area_voter = areas_voters[ind]
        mapper_area[area_food] = area_voter
                # count += 1
            # else:
            #     break
    else:
        mapper_area[area_food] = None

