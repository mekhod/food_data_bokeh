import pandas as pd
import math
import numpy as np
import pickle
from scipy import stats
import json

# df = pd.read_csv('data/data_all_determinants_with_normed_metro.csv')
# df.sort_values('metro_normed', inplace=True)

with open('back_end_dev/dict_data_scaler.pkl', 'rb') as handle:
    dict_data_scaler = pickle.load(handle)

df = dict_data_scaler['df_standardized'].copy()
df['insured_ratio'] = 1 - df['uninsured_ratio']

dict_metro = {}
for m in list(df.metro_normed):
    dict_temp = {}
    metro_data = df.loc[df.metro_normed == m, :].copy()
    dict_temp['food_first_pc'] = stats.percentileofscore(df['food_first_pc'],
                                                         metro_data['food_first_pc'].values[0])
    dict_temp['voters_ratio'] = stats.percentileofscore(df['voters_ratio'],
                                                        metro_data['voters_ratio'].values[0])
    dict_temp['education_weight'] = stats.percentileofscore(df['education_weight'],
                                                            metro_data['education_weight'].values[0])
    dict_temp['insured_ratio'] = stats.percentileofscore(df['insured_ratio'],
                                                         metro_data['insured_ratio'].values[0])
    dict_temp['park_access_ratio'] = stats.percentileofscore(df['park_access_ratio'],
                                                             metro_data['park_access_ratio'].values[0])
    dict_metro[m] = dict_temp

json_metro_percentile_rank = json.dumps(dict_metro)

with open('back_end_dev/json_metro_percentile_rank.json', 'w', encoding='utf-8') as f:
    json.dump(json_metro_percentile_rank, f, ensure_ascii=False)
