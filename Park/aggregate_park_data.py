import pandas as pd
from tools.compute_areas_overlap import find_area_mapper

path_park_data_by_county = "data/Parks/park_access_by_county/data_171554.csv"
df_park_data = pd.read_csv(path_park_data_by_county)
df_park_data.columns

# ## append all fips
# def append_fips(x):
#     return
#
#
# df_park_data['FIPS'] = df_park_data.apply(lambda x: int(str(x['stateFIPS']) + str(x['countyFIPS'])), axis=1)

# df_park_data.countyFIPS

##################
# path_map_FIPS_to_urban = "data/Parks/park_access_by_county/ansi_metro1_cbsa_july_2015.xls"
# df_map_FIPS_to_urban = pd.read_excel(path_map_FIPS_to_urban)
# df_map_FIPS_to_urban.columns
# set(df_map_FIPS_to_urban['FIPS County Code'])
# set(df_map_FIPS_to_urban['FIPS State Code'])


# ## append all FIPS
# def append_fips(x):
#     try:
#         fips = str(str(int(x['FIPS State Code'])) + str(int(x['FIPS County Code'])))
#         print(fips)
#     except:
#         fips = None
#     return fips
#
#
# df_map_FIPS_to_urban['FIPS'] = df_map_FIPS_to_urban.apply(lambda x: append_fips(x), axis=1)
# df_map_FIPS_to_urban['FIPS'] = df_map_FIPS_to_urban['FIPS'].astype(str, errors='ignore')
# # df_map_FIPS_to_urban['FIPS'] = [int(i) for i in df_map_FIPS_to_urban['FIPS']]
# ##
# df_park_data.countyFIPS = df_park_data.countyFIPS.astype(str)
# set(df_park_data.countyFIPS) & set(df_map_FIPS_to_urban['FIPS'])


#####################################################################################################
path_map_county_to_urban = "data/Parks/park_access_by_county/ua_county_rel_10.txt"
df_map_county_to_urban = pd.read_csv(path_map_county_to_urban, sep=",", encoding='latin-1')
df_map_county_to_urban.columns

all_counties = [c.replace('County', '').strip() for c in df_map_county_to_urban.CNAME]
len(all_counties)
len(set(all_counties))
len(set(df_map_county_to_urban.CNAME))
len(set(df_park_data.County))

# Hi Paul. I have been trying to use ua_county_rel_10.txt to map county to urban, but one county
# belongs to more than one urban area in a state and a county name can be used in more than one state, which
# means we cannot map a county (just by name) to a specific urban area.
# Please let me know if you have any recommendations. I am not too sure, but I think we can use countyFIPS for mapping.

print(len(set(df_park_data.County) - set(all_counties)))
print(set(df_park_data.County) - set(all_counties))

mapper_all = find_area_mapper(list_area_1=list(set(df_park_data.County) - set(all_counties)),
                              list_area_2=list(all_counties),
                              stop_words=["city", "new", "county", "falls", "st."])

mapper_2 = {i: i for i in all_counties}

mapper_all.update(mapper_2)

## to map counties using mapper_all
df_park_data.County = [c.strip() for c in df_park_data.County]
df_park_data.County = df_park_data.County.map(mapper_all)
set(df_park_data.County) - set(mapper_all.keys())

## to add statistical metropoletan using df_map_county_to_urban
df_map_county_to_urban.columns
df_map_county_to_urban.CNAME
set(df_map_county_to_urban.UANAME)

mapper_county_to_metro = dict(zip(df_map_county_to_urban.CNAME, df_map_county_to_urban.UANAME))






#################################################################################




df_map_county_to_urban.loc[:, 'county_stripped'] = all_counties


## to remove 'Not in a 2010 urban area' from the map df
# bool_1 = df_map_county_to_urban['UANAME'] != 'Not in a 2010 urban area'
#
# print(df_map_county_to_urban.shape)
# df_map_county_to_urban = df_map_county_to_urban.loc[bool_1, :]
# print(df_map_county_to_urban.shape)

## to check the metros for each county
def print_if_more_than_one_metro_for_one_county_exists(x=None):
    # print(x)
    # print(x['UANAME'])
    print(list(x['CNAME'])[0])
    if len(set(x['UANAME'])) != 1:
        print(set(x['UANAME']))
    # else:
    #     print('sdfsdf')
    return None


sth = df_map_county_to_urban.groupby(['CNAME', 'STATE'], group_keys=False). \
    apply(lambda x: print_if_more_than_one_metro_for_one_county_exists(x=x))

## create a county_to_urban mapper for the existing counties in both df_map_county_to_urban and df_park_data


path_map_urban_to_metro = "data/Parks/park_access_by_county/ua_cbsa_rel_10.txt"
df_map_urban_to_metro = pd.read_csv(path_map_urban_to_metro, sep=",", encoding='latin-1')









