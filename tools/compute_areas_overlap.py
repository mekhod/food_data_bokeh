from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np

def find_area_mapper(list_area_1=None, list_area_2=None,
                     stop_words=["city", "new", "county", "falls", "st."]):
    areas_all = list_area_1 + list_area_2
    vect = TfidfVectorizer(stop_words=stop_words, analyzer='word')
    tfidf = vect.fit_transform(areas_all)

    pairwise_similarity = tfidf * tfidf.T

    array_pairwise_similarity = pairwise_similarity.toarray()

    mapper_area = {}
    for i, area_1 in enumerate(list_area_1):
        array_similarity = array_pairwise_similarity[i]
        array_similarity_right_tail = array_similarity[len(list_area_1):]
        max_array_similarity_right_tail = np.max(array_similarity_right_tail)

        if max_array_similarity_right_tail != 0:

            arg_max_array_similarity_right_tail = np.argmax(array_similarity_right_tail)
            area_voter = list_area_2[arg_max_array_similarity_right_tail]
            mapper_area[area_1] = area_voter
        else:
            mapper_area[area_1] = None
    return mapper_area

