import pandas as pd


def split_fields_per_layout(work=None):
    row = work[0]
    data = work[1]
    layout = work[2]
    print(row)
    x = data.loc[row, :]
    s = str(x[0])
    if len(s) == 435:
        dict_fields = {v_name: s[int(layout.loc[layout['Variable Name'] == v_name, 'Starting Column'].values[0]) - 1
                                 :int(layout.loc[layout['Variable Name'] == v_name, 'Starting Column'].values[0]) - 1
                                  + int(layout.loc[layout['Variable Name'] == v_name, 'Field Length'].values[0])]
                       for v_name in list(layout['Variable Name'])}
        return dict_fields
    return {}


def parse_community_data(work=None):
    ## mappers
    # mapper_age_range = {'1': 'child', '2': 'adult', '3': 'adult_armed_forces'}
    #
    # mapper_interview_type = {'1': 'interview',
    #                          '2': 'type_A_noninterview',
    #                          '3': 'type_B_noninterview',
    #                          '4': 'type_C_noninterview'}
    #
    # mapper_state_code = {'29': 'MO', '56': 'WY', '28': 'MS', '55': 'WI', '27': 'MN', '54': 'WV', '26': 'MI',
    #                      '53': 'WA', '25': 'MA', '51': 'VA', '24': 'MD', '50': 'VT', '23': 'ME', '49': 'UT',
    #                      '22': 'LA', '48': 'TX', '21': 'KY', '47': 'TN', '20': 'KS', '46': 'SD', '19': 'IA',
    #                      '45': 'SC', '18': 'IN', '44': 'RI', '17': 'IL', '42': 'PA', '16': 'ID', '41': 'OR',
    #                      '15': 'HI', '40': 'OK', '13': 'GA', '39': 'OH', '12': 'FL', '38': 'ND', '11': 'DC',
    #                      '37': 'NC', '10': 'DE', '36': 'NY', '09': 'CT', '35': 'NM', '08': 'CO', '34': 'NJ',
    #                      '06': 'CA', '33': 'NH', '05': 'AR', '32': 'NV', '04': 'AZ', '31': 'NE', '02': 'AK',
    #                      '30': 'MT', '01': 'AL'}

    ##
    year_of_interview = work[17:21]
    interview_type = work[56:58]  # 1 is interview and what we need here
    state_code = work[92:94]
    metropolitan_code = work[95:100]  # 00000 means it is not identified
    county_code = work[100:103]  # 000 means it is not identified
    age_range = work[160:162]  # anything other than 1, as 1 is child
    voting_type = work[1000:1002].strip()  # voter type cannot be -1 because it means the person is not in
    # the universe(is not qualified for voting)
    registered_type = work[1002:1004].strip()

    dict_individual_community = {'interview_type': interview_type,
                                 'voting_type': voting_type,
                                 'registered_type': registered_type,
                                 'age_range': age_range,
                                 'year_of_interview': year_of_interview,
                                 'state_code': state_code,
                                 'metropolitan_code': metropolitan_code,
                                 'county_code': county_code}

    return dict_individual_community
