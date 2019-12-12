import pandas as pd
import numpy as np
from bokeh.models import FactorRange
from bokeh.layouts import column
from bokeh.palettes import Spectral6, Spectral4
from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models.widgets import CheckboxGroup
from sklearn.preprocessing import MinMaxScaler

df = pd.DataFrame([])

def get_df_selected(df, cities):
    df_selected = df.loc[list(set(list(df.index)) & set(cities)), :].copy()
    df_selected.sort_index(inplace=True)
    return df_selected


def create_x_and_counts(df=None, cities=None,
                        list_of_determinants=['voters_ratio',
                                              'education_weight',
                                              'uninsured_ratio',
                                              'park_access_ratio',
                                              'food_first_pc']):
    df_selected = get_df_selected(df=df, cities=cities)

    ##################################################
    df_selected = df_selected.loc[:, list_of_determinants].copy()

    ##################################################
    x = [(str(determinant), str(city))
         for city in list(np.unique(list(df_selected.index)))
         for determinant in list(df_selected.columns)]

    cnts = [df_selected.loc[df_selected.index == city, determinant].values[0]
            for city in list(np.unique(list(df_selected.index)))
            for determinant in list(df_selected.columns)]
    return x, cnts


def update_plot(attrname, old, new):
    global df
    cities_0 = [city_selection.labels[i] for i in city_selection.active]
    cities_all = [i.strip() for i in list(df.index.unique())]
    cities = [i.strip() for i in cities_0 if i.strip() in cities_all]

    # dtrmts = [determinants_selection.labels[i] for i in determinants_selection.active]
    dtrmts = ['voters_ratio', 'education_weight',
              'uninsured_ratio', 'park_access_ratio', 'food_first_pc']

    should_scale = len(min_max_selection.active) != 0

    # should_scale = True

    if should_scale:
        df_temp = pd.DataFrame(scaler.transform(df))
        mapper_col = {i: j for i, j in enumerate(df.columns)}
        df_temp.index = df.index
        df_temp = df_temp.rename(mapper_col, axis=1)

    else:
        df_temp = df.copy()

    x_new, counts_new = create_x_and_counts(df=df_temp,
                                            cities=cities,
                                            list_of_determinants=dtrmts)

    palette = Spectral4 + Spectral6
    palette += palette

    clrs = []
    for i in range(len(cities)):
        factor = int(len(x_new) / len(cities))
        clrs.extend([palette[i]] * factor)

    source_new = ColumnDataSource(data=dict(x=x_new,
                                            counts=counts_new,
                                            colors=palette[0: len(cities)] * int(len(counts_new) / len(cities)),
                                            cities=cities * int(len(counts_new) / len(cities))))
    source.data = source_new.data
    p.vbar(x=source.data['x'], top=source.data['counts'], width=0.9,
           line_color="black",
           fill_color=clrs)

    p.x_range.factors = source.data['x']
    p.xgrid.grid_line_color = None


cities = ['']

df = pd.read_csv('data/data_all_determinants_with_normed_metro.csv')
df.sort_values('metro_normed', inplace=True)

# names = [str(n).split(',')[0].strip() for n in df.MMSANAME]
#
# df['city'] = names
#
# df = df.loc[df.city != 'nan', :].copy()

#########################
checkbox_cities_labels = list(df.metro_normed.unique())
city_selection = CheckboxGroup(labels=checkbox_cities_labels,
                               active=[])

#########################
min_max_selection = CheckboxGroup(labels=['min_max'],
                                  active=[])

#########################
# columns_to_select = [c for c in df.columns] # if c.startswith('_')]
columns_to_select = ['metro_normed', 'voters_ratio', 'education_weight',
                     'uninsured_ratio', 'park_access_ratio', 'food_first_pc']
# columns_to_select = ['city'] + columns_to_select
# df = df.loc[:, columns_to_select]

# cols = list(df.columns)
# cols.remove('city')

cols = ['voters_ratio', 'education_weight',
        'uninsured_ratio', 'park_access_ratio', 'food_first_pc']

for c in cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

# df = df.fillna(value=-1.0)

#########################
df.rename({'metro_normed': 'city'}, axis=1, inplace=True)
df.set_index('city', inplace=True)

####################### min max
scaler = MinMaxScaler()
scaler.fit(df)
# df_temp = pd.DataFrame(scaler.transform(df))
# mapper_col = {i:j for i, j in enumerate(df.columns)}
# df_temp.index = df.index
# df = df_temp.rename(mapper_col, axis=1)

#########################
# checkbox_determinants_labels = list(cols)
# determinants_selection = CheckboxGroup(labels=list(np.sort(checkbox_determinants_labels)),
#                                        active=['education_weight'])

#########################
x, counts = create_x_and_counts(df=df, cities=cities)

source = ColumnDataSource(data=dict(x=x, counts=counts, colors=()))  # ,colors=(sum(zip(Spectral6, Spectral6), ())

p = figure(x_range=FactorRange(*source.data['x']), plot_width=1400, plot_height=850, title="Determinants Comparison",
           toolbar_location=None, tools="")

p.xaxis.major_label_orientation = "vertical"

city_selection.on_change('active', update_plot)
# determinants_selection.on_change('active', update_plot)
min_max_selection.on_change('active', update_plot)

checkbox_cities_column = column(city_selection)
# checkbox_determinants_column = column(determinants_selection)
min_max_selection_column = column(min_max_selection)

bokeh_doc = curdoc()
bokeh_doc.add_root(row(checkbox_cities_column, p, min_max_selection_column, width=1500))

# bokeh serve --show All_Determinants/plot_bar_chart_all_determinants.py
# python -m notebook

