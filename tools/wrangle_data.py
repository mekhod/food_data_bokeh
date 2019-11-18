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
    interview_type = work[56:58]  # 1 is interview and what we need here
    voting_type = work[1000:1002]  # voter type cannot be -1 because it means the person is not in
    # the universe(is not qualified for voting)
    registered_type = work[1002:1004]
    age_range = work[160:162]  # anything other than 1, as 1 is child
    year_of_interview = work[17:21]
    state_code = work[92:94]
    metropolitan_code = work[95:100]  # 00000 means it is not identified
    county_code = work[100:103]  # 000 means it is not identified

    dict_individual_community = {'interview_type': interview_type,
                                 'voting_type': voting_type,
                                 'registered_type': registered_type,
                                 'age_range': age_range,
                                 'year_of_interview': year_of_interview,
                                 'state_code': state_code,
                                 'metropolitan_code': metropolitan_code,
                                 'county_code': county_code}

    return dict_individual_community