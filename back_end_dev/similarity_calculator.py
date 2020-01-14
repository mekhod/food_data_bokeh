import pandas as pd
import math
import numpy as np
import pickle
import json


def calc_similarity(metro_df=None,
                    df_dist_min_max=None,
                    metro_area=None,
                    fruit_per_day=None,
                    voting_likelihood=None,
                    education=None,
                    insured=None,
                    park_access=None,
                    scaler=None):
    dict_individual_data = {}
    dict_individual_data['metro_normed'] = metro_area

    ## fruit
    # fruit_n_per_day varies between 0.5 and 2
    assert (fruit_per_day >= 0.5) and (fruit_per_day <= 2)
    food_first_pc_new = (11 / 1.5) * (fruit_per_day - 0.5) - 5

    dict_individual_data['food_first_pc'] = food_first_pc_new

    ## voting liklihood
    assert (voting_likelihood >= 0) and (voting_likelihood <= 1)

    dict_individual_data['voters_ratio'] = voting_likelihood

    ## education weight
    mapper_education = {'LESS THAN 1ST GRADE': 0,
                        '1ST, 2ND, 3RD OR 4TH GRADE': 1,
                        '5TH OR 6TH GRADE': 2,
                        '7TH OR 8TH GRADE': 3,
                        '9TH GRADE': 4,
                        '10TH GRADE': 5,
                        '11TH GRADE': 6,
                        '12TH GRADE NO DIPLOMA': 7,
                        'HIGH SCHOOL GRAD-DIPLOMA OR EQUIV (GED)': 8,
                        'SOME COLLEGE BUT NO DEGREE': 9,
                        'ASSOCIATE DEGREE-OCCUPATIONAL/VOCATIONAL': 10,
                        'ASSOCIATEDEGREE-ACADEMICPROGRAM': 11,
                        "BACHELOR'S DEGREE (EX: BA, AB, BS)": 12,
                        "MASTER'S DEGREE (EX:MA,MS,MEng,MEd, MSW)": 13,
                        "PROFESSIONAL SCHOOL DEG (EX:MD, DDS, DVM)": 14,
                        "DOCTORATE DEGREE (EX: PhD, EdD)": 14}

    assert education in list(mapper_education.keys())

    education_rank = mapper_education[education]

    dict_individual_data['education_weight'] = education_rank

    ## insured
    assert (insured == 1) or (insured == 0)
    uninsured = 1 - insured

    dict_individual_data['uninsured_ratio'] = uninsured

    ## park_access
    assert (park_access == 1) or (park_access == 0)

    dict_individual_data['park_access_ratio'] = park_access

    # print(dict_individual_data)

    ## df
    df_individual_data = pd.DataFrame(dict_individual_data, index=[0])
    df_individual_data = df_individual_data.loc[:,
                         ['voters_ratio',
                          'education_weight',
                          'food_first_pc',
                          'uninsured_ratio',
                          'park_access_ratio']]

    ## standardize individual data
    individual_data_standardized = scaler.transform(df_individual_data)
    individual_data_standardized = pd.DataFrame(individual_data_standardized)
    mapper_col = {i: j for i, j in enumerate(df_individual_data.columns)}
    individual_data_standardized = individual_data_standardized.rename(mapper_col, axis=1)

    food_first_pc_new = individual_data_standardized['food_first_pc']
    voting_likelihood = individual_data_standardized['voters_ratio']
    education_rank = individual_data_standardized['education_weight']
    uninsured = individual_data_standardized['uninsured_ratio']
    park_access = individual_data_standardized['park_access_ratio']

    ##
    metro_data = metro_df.loc[metro_df.metro_normed == metro_area, :]
    dist = math.sqrt((food_first_pc_new - metro_data['food_first_pc'].values.squeeze()) ** 2 +
                     (voting_likelihood - metro_data['voters_ratio'].values.squeeze()) ** 2 +
                     (education_rank - metro_data['education_weight'].values.squeeze()) ** 2 +
                     (uninsured - metro_data['uninsured_ratio'].values.squeeze()) ** 2 +
                     (park_access - metro_data['park_access_ratio'].values.squeeze()) ** 2)

    ##
    metro_dist_min_max = df_dist_min_max.loc[df_dist_min_max.metro == metro_area, :]
    metro_dist_min = metro_dist_min_max['distance_least'].values.squeeze()
    metro_dist_max = metro_dist_min_max['distance_most'].values.squeeze()

    similarity = (dist - metro_dist_max) * (100 / (metro_dist_min - metro_dist_max))

    if similarity < 0:
        similarity = 0

    if similarity > 100:
        similarity = 100

    return similarity


## trial
with open('back_end_dev/dict_data_scaler.pkl', 'rb') as handle:
    dict_data_scaler = pickle.load(handle)

df = dict_data_scaler['df_standardized'].copy()
df['state_code'] = df.metro_normed.apply(lambda x: x.split(',')[1].strip().split(' ')[0])
df['metro_name'] = df.metro_normed.apply(lambda x: x.split(',')[0].strip())
scaler = dict_data_scaler['scaler']
df_dist_min_max = dict_data_scaler['df_dist_min_max']


##
# list_similarity = []
dict_all_metro_sim = {}

for voting_likelihood in np.linspace(0, 1, 11):
    for fruit_per_day in np.linspace(0.5, 2.0, 4):
        for education in ['LESS THAN 1ST GRADE',
                          '1ST, 2ND, 3RD OR 4TH GRADE',
                          '5TH OR 6TH GRADE',
                          '7TH OR 8TH GRADE',
                          '9TH GRADE',
                          '10TH GRADE',
                          '11TH GRADE',
                          '12TH GRADE NO DIPLOMA',
                          'HIGH SCHOOL GRAD-DIPLOMA OR EQUIV (GED)',
                          'SOME COLLEGE BUT NO DEGREE',
                          'ASSOCIATE DEGREE-OCCUPATIONAL/VOCATIONAL',
                          'ASSOCIATEDEGREE-ACADEMICPROGRAM',
                          "BACHELOR'S DEGREE (EX: BA, AB, BS)",
                          "MASTER'S DEGREE (EX:MA,MS,MEng,MEd, MSW)",
                          'PROFESSIONAL SCHOOL DEG (EX:MD, DDS, DVM)',
                          'DOCTORATE DEGREE (EX: PhD, EdD)']:
            for park_access in [0, 1]:
                for insured in [0, 1]:
                    dict_similarity = {}
                    for m in list(df.metro_normed):
                        sim = calc_similarity(metro_df=df.copy(),
                                              df_dist_min_max=df_dist_min_max,
                                              metro_area=m,
                                              fruit_per_day=fruit_per_day,
                                              voting_likelihood=voting_likelihood,
                                              education=education,
                                              insured=insured,
                                              park_access=park_access,
                                              scaler=scaler
                                              )
                        dict_similarity[m] = sim
                        # print(sim)
                        # list_similarity.append(sim)
                    closest = [m for m in list(dict_similarity.keys())
                               if dict_similarity[m] == np.max(list(dict_similarity.values()))]
                    if len(closest) > 1:
                        print(closest)
                    dict_temp = {'similarities': dict_similarity,
                                 'closest': closest}
                    dict_all_metro_sim[str((insured,
                                            park_access,
                                            voting_likelihood,
                                            fruit_per_day,
                                            education))] = dict_temp

json_all_metro_similarity = json.dumps(dict_all_metro_sim)

with open('back_end_dev/json_all_metro_similarity.json', 'w', encoding='utf-8') as f:
    json.dump(json_all_metro_similarity, f, ensure_ascii=False)
