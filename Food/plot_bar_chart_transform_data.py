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


def create_x_and_counts(df=None, cities=None,
                        list_of_determinants=['FTJUDA2__mean', 'FRUTDA2__mean']):
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
    cities_0 = [city_selection.labels[i] for i in city_selection.active]
    cities_all = [i.strip() for i in list(df.index.unique())]
    cities = [i.strip() for i in cities_0 if i.strip() in cities_all]

    dtrmts = [determinants_selection.labels[i] for i in determinants_selection.active]

    x_new, counts_new = create_x_and_counts(df=df, cities=cities, list_of_determinants=dtrmts)

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

df = pd.read_csv('data/Food/df_transformed.csv')

# names = [str(n).split(',')[0].strip() for n in df.MMSANAME]
#
# df['city'] = names
#
# df = df.loc[df.city != 'nan', :].copy()

#########################
checkbox_cities_labels = list(df.city.unique())
city_selection = CheckboxGroup(labels=checkbox_cities_labels,
                               active=[])

#########################
columns_to_select = [c for c in df.columns] # if c.startswith('_')]
# columns_to_select = ['city'] + columns_to_select
# df = df.loc[:, columns_to_select]

cols = list(df.columns)
cols.remove('city')

for c in cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

df = df.fillna(value=-1.0)

#########################
df.set_index('city', inplace=True)

#########################
checkbox_determinants_labels = list(cols)
determinants_selection = CheckboxGroup(labels=list(np.sort(checkbox_determinants_labels)),
                                       active=[10, 11])

#########################
x, counts = create_x_and_counts(df=df, cities=cities)

source = ColumnDataSource(data=dict(x=x, counts=counts, colors=()))  # ,colors=(sum(zip(Spectral6, Spectral6), ())

p = figure(x_range=FactorRange(*source.data['x']), plot_width=1400, plot_height=850, title="Determinants Comparison",
           toolbar_location=None, tools="")

p.xaxis.major_label_orientation = "vertical"

city_selection.on_change('active', update_plot)
determinants_selection.on_change('active', update_plot)

checkbox_cities_column = column(city_selection)
checkbox_determinants_column = column(determinants_selection)

bokeh_doc = curdoc()
bokeh_doc.add_root(row(checkbox_cities_column, p, checkbox_determinants_column, width=1500))

# bokeh serve --show plot_bar_chart_transform_data.py
# python -m notebook
