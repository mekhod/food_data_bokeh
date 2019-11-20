import pandas as pd
import numpy as np
import seaborn as sns;

sns.set()

df = pd.read_csv("data/Food/wrangled_food_data.csv")

names = [str(n).split(',')[0].strip() for n in df.MMSANAME]

df['city'] = names

df = df.loc[df.city != 'nan', :].copy()

df.drop('Unnamed: 0', axis=1, inplace=True)

list_selected_features = ['city', 'FTJUDA2_', 'FRUTDA2_', 'GRENDA1_', 'FRNCHDA_', 'POTADA1_',
                          'VEGEDA2_', '_FRUTSU1', '_VEGESU1', '_FRTLT1A', '_VEGLT1A',
                          '_FRT16A', '_VEG23A']

df = df.loc[:, list_selected_features].reindex()

df.set_index('city', inplace=True)

## Exploration
dict_col_unique_counts = {}

for c in df.columns:
    print('')
    print(c)
    print(len(df[c].unique()))
    dict_col_unique_counts[c] = len(df[c].unique())

## Filling NAs
df = df.astype(str)

for col in df.columns:
    df[col] = df[col].str.strip()

np.where(df.applymap(lambda x: x == ''))

for col in df.columns:
    df[col] = df[col].replace("", "-1.0")
    df[col] = df[col].replace("nan", "-1.0")

np.where(df.applymap(lambda x: x == ''))

df.head()

df = df.fillna("-1.0")

df = df.astype(float)

df.head()

## Transformation
list_data_transformed = []


def transform_chunk(chunk):
    dict_temp_transformed_data = {}
    dict_temp_transformed_data['city'] = np.unique(chunk.index)[0]
    for col in chunk.columns:
        print(col)
        if dict_col_unique_counts[col] < 30:
            print(col)
            for cat in list(np.unique(chunk[[col]])):
                dict_temp_transformed_data[col + '_' + str(cat)] = sum((chunk[[col]].values == cat).squeeze()) / len(
                    chunk)
        else:
            dict_temp_transformed_data[col + '_mean'] = np.mean(chunk.loc[:, col].values)
            print(np.mean(chunk.loc[:, col].values))

    list_data_transformed.append(dict_temp_transformed_data)
    return


sth = df.groupby('city').apply(lambda chunk: transform_chunk(chunk))

df_transformed = pd.DataFrame(list_data_transformed)

set(df_transformed.columns) - set(['FTJUDA2__mean', 'FRUTDA2__mean', 'GRENDA1__mean', 'FRNCHDA__mean',
                                   'POTADA1__mean', 'VEGEDA2__mean', '_FRUTSU1_mean', '_VEGESU1_mean',
                                   '_FRTLT1A_1.0', '_FRTLT1A_2.0', '_FRTLT1A_9.0', '_VEGLT1A_1.0',
                                   '_VEGLT1A_2.0', '_VEGLT1A_9.0', '_FRT16A_1.0', '_VEG23A_0.0',
                                   '_VEG23A_1.0', '_FRT16A_0.0'])

## Fill Na of df_transformed
df_transformed = df_transformed.fillna(df_transformed.median())

df_transformed = df_transformed.set_index('city')

## Save data
df_transformed.to_csv('data/Food/df_transformed.csv')
