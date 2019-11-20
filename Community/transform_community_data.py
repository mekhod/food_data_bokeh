import pandas as pd

df_community = pd.read_csv("data/Community_Context/nov18pub.dat", header=None)

# trial = df_community[0].values[0].replace("
# ", "")
interview_type = df_community[0].values[0][57:58] # 1 is interview and what we need here
voting_type = df_community[0].values[0][1001:1002] # voter type cannot be -1 because it means the person is not qualified for voting
age_range = df_community[0].values[0][161:162] # anything other than 1, as 1 is child
year_of_interview = df_community[0].values[0][18:21]
state_code = df_community[0].values[100][92:94]
metropolitan_code = df_community[0].values[100][95:100] # 00000 means it is not identified
county_code = df_community[0].values[10][100:103] # 000 means it is not identified

# len(df_community.values.squeeze())
df_community.values.squeeze()[0]