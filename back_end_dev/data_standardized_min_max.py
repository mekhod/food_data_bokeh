from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import pickle

df = pd.read_csv('data/data_all_determinants_with_normed_metro.csv')
df.sort_values('metro_normed', inplace=True)
df.set_index('metro_normed', inplace=True)

scaler = MinMaxScaler()
scaler.fit(df)

array_standardized = scaler.transform(df)
df_temp = pd.DataFrame(array_standardized)
mapper_col = {i:j for i, j in enumerate(df.columns)}
df_temp.index = df.index
df_standardized = df_temp.rename(mapper_col, axis=1)
df_standardized.reset_index(drop=False, inplace=True)

with open('back_end_dev/dict_data_scaler.pkl', 'wb') as handle:
    pickle.dump({'df_standardized': df_standardized,
                 'scaler': scaler}, handle, protocol=pickle.HIGHEST_PROTOCOL)

