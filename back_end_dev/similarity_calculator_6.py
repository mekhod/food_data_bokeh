import pandas as pd
import numpy as np
import pickle
import json

##################################################
df_corrected_cities_states = pd.read_csv('data/corrected_cities_states_Kelsey.csv')

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands': 'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Palau': 'PW',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

df_corrected_cities_states = df_corrected_cities_states.rename(columns={'State': 'state',
                                                                        'City': 'metro_name'})
df_corrected_cities_states['state_code'] = df_corrected_cities_states.state.map(us_state_abbrev)

mapper_metro_to_metro_name = dict(zip(df_corrected_cities_states.metro_normed,
                                      df_corrected_cities_states.metro_name))

mapper_metro_to_state = dict(zip(df_corrected_cities_states.metro_normed,
                                 df_corrected_cities_states.state))

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands': 'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Palau': 'PW',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

##
with open('back_end_dev/dict_data_scaler.pkl', 'rb') as handle:
    dict_data_scaler = pickle.load(handle)

##
df = df_corrected_cities_states.copy()
df = dict_data_scaler['df_standardized'].copy()

df['metro_name'] = df.metro_normed.map(mapper_metro_to_metro_name)
df['state'] = df.metro_normed.map(mapper_metro_to_state)
df['state_code'] = df.state.map(us_state_abbrev)

##
scaler = dict_data_scaler['scaler']
df_dist_min_max = dict_data_scaler['df_dist_min_max']

## new structure of json file
df_states_divided = df.copy()

df_states_divided.sort_values(by=['state', 'metro_name'], inplace=True)

df_states_divided.loc[:, ['state', 'metro_name']]

##


# to create nested dictionary
dict_final_all_state = {}
for state_code in list(df_states_divided['state_code'].unique()):
    df_temp_one_state_code = None
    df_temp_one_state_code = \
        df_states_divided[df_states_divided['state_code'] == state_code].copy()

    df_temp_one_state_code.sort_values(by=['state', 'metro_name'], inplace=True)

    ##
    dict_temp_all_metros_in_one_state = {}
    for _, row in df_temp_one_state_code.iterrows():
        dict_temp_metro = dict()
        # print(row['metro_normed'])

        # Scores
        dict_metro_scores = {}
        dict_metro_scores['HealthcareCoverage'] = round(1 - float(row['uninsured_ratio']), 2)
        dict_metro_scores['ParkAccessibility'] = round(row['park_access_ratio'], 2)
        dict_metro_scores['AccessToHealthyFood'] = round(row['food_first_pc'], 2)
        dict_metro_scores['EducationLevel'] = round(row['education_weight'], 2)
        dict_metro_scores['CivicEngagement'] = round(row['voters_ratio'], 2)

        # Responses
        dict_temp_responses = {}

        ##
        map_vote = {0: 'No', 1: 'YES'}
        dict_temp_vote = {}
        for voting_likelihood in [0, 1]:
            dict_temp_vote[map_vote[voting_likelihood]] = \
                abs(round(voting_likelihood - row['voters_ratio'], 2))

        ##
        dict_temp_responses['Vote'] = dict_temp_vote

        ##
        dict_temp_fruit = {}
        for fruit_per_day in np.linspace(0.5, 2.0, 4):
            food_first_pc = (11 / 1.5) * (fruit_per_day - 0.5) - 5
            food_first_pc_std = scaler.transform([[0, 0, food_first_pc, 0, 0]])[0][2]
            if food_first_pc_std < 0:
                food_first_pc_std = 0
            if food_first_pc_std > 1:
                food_first_pc_std = 1
            dict_temp_fruit[fruit_per_day] = \
                abs(round(food_first_pc_std - row['food_first_pc'], 2))

        dict_temp_responses['Fruit'] = dict_temp_fruit

        ##
        dict_temp_education = {}
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
            education_rank = mapper_education[education]

            ## education_weight varies between 8.056 and 10.49
            education_rank_std = scaler.transform([[0, education_rank, 0, 0, 0]])[0][1]

            dict_temp_education[education] = \
                abs(round(education_rank_std - row['education_weight'], 2))

        ##
        dict_temp_responses['Education'] = dict_temp_education

        ##
        map_park_access = {0: 'No', 1: 'YES'}
        dict_temp_park_access = {}
        for park_access in [0, 1]:
            dict_temp_park_access[map_park_access[park_access]] = \
                abs(round(park_access - row['park_access_ratio'], 2))

        ##
        dict_temp_responses['Parks'] = dict_temp_park_access

        ##
        map_insured = {0: 'No', 1: 'YES'}
        dict_temp_insured = {}
        for insured in [0, 1]:
            uninsured = 1 - insured
            dict_temp_insured[map_insured[insured]] = \
                abs(round(uninsured - row['uninsured_ratio'], 2))

        ##
        dict_temp_responses['Insured'] = dict_temp_insured

        ##
        min_distance = round(df_dist_min_max.loc[df_dist_min_max.metro == row['metro_normed'],
                                                 'distance_least'].values[0], 2)
        max_distance = round(df_dist_min_max.loc[df_dist_min_max.metro == row['metro_normed'],
                                                 'distance_most'].values[0], 2)
        dict_temp_metro['Min_Max'] = str([min_distance, max_distance])
        dict_temp_metro['Responses'] = dict_temp_responses
        dict_temp_metro['Scores'] = dict_metro_scores

        ##
        dict_temp_all_metros_in_one_state[row['metro_name']] = dict_temp_metro

    ##
    dict_final_all_state[state_code] = dict_temp_all_metros_in_one_state
#####################################################################

list_all_states = []
for s in list(dict_final_all_state.keys()):
    dict_one_state = {}
    dict_one_state["Name"] = dict_state_code_mapper[s]
    dict_one_state["Code"] = s
    list_all_cities_in_one_state = []
    for c in list(dict_final_all_state[s].keys()):
        dict_one_city = {}
        Name = c
        Scores = dict_final_all_state[s][c]['Scores']
        Responses = dict_final_all_state[s][c]['Responses']
        Min_Max = dict_final_all_state[s][c]['Min_Max']
        dict_one_city["Name"] = Name.split("-")[0].strip().split("/")[-1].strip()
        print(dict_one_city["Name"])
        dict_one_city["Code"] = str.lower(s.strip() + dict_one_city["Name"].replace(" ", ""))
        dict_one_city["Scores"] = Scores
        dict_one_city["Responses"] = Responses
        dict_one_city["min_max"] = Min_Max
        list_all_cities_in_one_state.append(dict_one_city)
    dict_one_state["Cities"] = list_all_cities_in_one_state
    list_all_states.append(dict_one_state)

dict_final = {}
dict_final["States"] = list_all_states
list_final = [dict_final]

######################################################################
with open('back_end_dev/json_6.json', 'w', encoding='utf-8') as f:
    json.dump(list_final, f, ensure_ascii=False)
