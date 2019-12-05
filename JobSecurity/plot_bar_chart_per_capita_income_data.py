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


def get_df_selected(df, cities):
    df_selected = df.loc[list(set(list(df.index)) & set(cities)), :].copy()
    df_selected.sort_index(inplace=True)
    return df_selected


def create_x_and_counts(df=None, cities=None):
    df_selected = get_df_selected(df=df, cities=cities)

    ##################################################
    x = [str(city) for city in list(np.unique(list(df_selected.index)))]

    cnts = [df_selected.loc[df_selected.index == city, 'per_capita_income'].values[0]
            for city in list(np.unique(list(df_selected.index)))]
    return x, cnts


def update_plot(attrname, old, new):
    cities_0 = [city_selection.labels[i] for i in city_selection.active]
    cities_all = [i.strip() for i in list(df.index.unique())]
    cities = [i.strip() for i in cities_0 if i.strip() in cities_all]
    print(cities)

    # dtrmts = [determinants_selection.labels[i] for i in determinants_selection.active]

    x_new, counts_new = create_x_and_counts(df=df, cities=cities)

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


#########################
df = pd.read_csv('data/Job_Security/per_capita_income.csv')
df['city'] = df['GeoName']
df['per_capita_income'] = df['2017']

#########################
cities = []
cities.append(df.loc[df.per_capita_income == np.max(df.per_capita_income), 'city'].values[0])
cities.append(df.loc[df.per_capita_income == np.median(df.per_capita_income), 'city'].values[0])
cities.append(df.loc[df.per_capita_income == np.min(df.per_capita_income), 'city'].values[0])

#########################
index_cities = [list(df.city).index(i) for i in cities]
checkbox_cities_labels = list(df.city.unique())
city_selection = CheckboxGroup(labels=checkbox_cities_labels,
                               active=index_cities)

#########################
columns_to_select = ['per_capita_income']

for c in columns_to_select:
    df[c] = pd.to_numeric(df[c], errors='coerce')

#########################
df.set_index('city', inplace=True)
df = df.loc[:, ['per_capita_income']]

#########################
x, counts = create_x_and_counts(df=df, cities=cities)

source = ColumnDataSource(data=dict(x=x, counts=counts, colors=()))  #

p = figure(x_range=FactorRange(*source.data['x']),
           plot_width=400, plot_height=800,
           title="per_capita_income comparison",
           toolbar_location=None, tools="")

####################################
palette = Spectral4 + Spectral6
palette += palette
clrs = []
for i in range(len(cities)):
    factor = 1
    clrs.extend([palette[i]] * factor)

source_new = ColumnDataSource(data=dict(x=x,
                                        counts=counts,
                                        colors=palette[0: len(cities)] * int(len(counts) / len(cities)),
                                        cities=cities * int(len(counts) / len(cities))))
source.data = source_new.data
p.vbar(x=source.data['x'], top=source.data['counts'], width=0.9,
       line_color="black",
       fill_color=clrs)

p.x_range.factors = source.data['x']
p.xgrid.grid_line_color = None

########################################
p.xaxis.major_label_orientation = "vertical"

city_selection.on_change('active', update_plot)

checkbox_cities_column = column(city_selection)

bokeh_doc = curdoc()
bokeh_doc.add_root(row(checkbox_cities_column, p, width=1500))

# bokeh serve --show JobSecurity/plot_bar_chart_per_capita_income_data.py
# python -m notebook
