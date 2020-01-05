import pandas as pd
import math
import numpy as np


def calc_similarity(metro_df=None,
                    df_dist_min_max=None,
                    metro_area=None,
                    fruit_per_day=None,
                    voting_likelihood=None,
                    education=None,
                    insured=None,
                    park_access=None
                    ):
    metro_data = metro_df.loc[metro_df.metro_normed == metro_area, :]
    ## fruit
    # fruit_n_per_day varies between 0.5 and 2
    assert (fruit_per_day >= 0.5) and (fruit_per_day <= 2)
    food_first_pc_new = (11 / 1.5) * (fruit_per_day - 0.5) - 5

    ## voting liklihood
    assert (voting_likelihood >= 0) and (voting_likelihood <= 1)

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

    ## insured
    assert (insured == 1) or (insured == 0)
    uninsured = 1 - insured

    ## park_access
    assert (park_access == 1) or (park_access == 0)

    dist = math.sqrt((food_first_pc_new - metro_data['food_first_pc']) ** 2 +
                     (voting_likelihood - metro_data['voters_ratio']) ** 2 +
                     (education_rank - metro_data['education_weight']) ** 2 +
                     (uninsured - metro_data['uninsured_ratio']) ** 2 +
                     (park_access - metro_data['park_access_ratio']) ** 2)

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
df = pd.read_csv('data/data_all_determinants_with_normed_metro.csv')
df.sort_values('metro_normed', inplace=True)

df_dist_min_max = pd.read_csv('back_end_dev/df_dist_min_max.csv')

##
list_similarity = []
for m in list(df.metro_normed):
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
                        sim = calc_similarity(metro_df=df.copy(),
                                              df_dist_min_max=df_dist_min_max,
                                              metro_area=m,
                                              fruit_per_day=fruit_per_day,
                                              voting_likelihood=voting_likelihood,
                                              education=education,
                                              insured=insured,
                                              park_access=park_access
                                              )
                        print(sim)
                        list_similarity.append(sim)

pd.DataFrame({'sim': list_similarity})['sim'].hist()
