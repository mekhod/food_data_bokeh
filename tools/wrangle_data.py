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