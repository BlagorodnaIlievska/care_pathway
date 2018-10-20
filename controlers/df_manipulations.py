import pandas as pd


def calculate_df(df, calulation, column_name, column1, column2=None, column3=None, column4=None):

    "calculation can be: count, sum, median, min, max, first and last occurrence of a column value"
    if column4 is not None:
        new_df = df.groupby([column1, column2, column3, column4], as_index=False).calulation()
    else:
        if column3 is not None:
            new_df = df.groupby([column1, column2, column3], as_index=False).calulation()
        else:
            if column2 is not None:
                new_df = df.groupby([column1, column2], as_index=False).calulation()
            else:
                new_df = df.groupby(column1, as_index=False).calulation()

    new_df = pd.DataFrame(new_df)
    new_df = new_df.reset_index()
    new_df = new_df.rename(columns={0: column_name})
    return new_df


def shift_df(df, shift_column, column1, column2=None, column3=None):

    if column3 is not None:
        new_df = df.groupby([column1, column2, column3])[shift_column].shift(-1)
    else:
        if column2 is not None:
            new_df = df.groupby([column1, column2])[shift_column].shift(-1)
        else:
            new_df = df.groupby([column1])[shift_column].shift(-1)

    new_df = pd.DataFrame(new_df)
    new_df = new_df.reset_index()
    new_df = new_df.rename(columns={shift_column: 'Shifted'})

    return new_df


def remove_consecutive_rows_same_value(df, id):

    members = df[id].unique()
    all_members = []
    all_members_df = pd.DataFrame()
    for member in members:
        temporary_df = df[df[id] == member]
        date_time = ['Procedure_start']
        temporary_df = set_data_types(df=temporary_df, columns=date_time, sortby='Procedure_start')
        temporary_df = temporary_df.sort_values(['Procedure_start', 'Category'])
        temporary_df['Repetitions'] = temporary_df.Category\
            .groupby((df.Category != df.Category.shift()).cumsum()).transform('size')
        temporary_df = temporary_df[temporary_df['Category'].shift(-1) != temporary_df['Category']]
        all_members.append(temporary_df)

    all_members_df = pd.concat(all_members)
    return all_members_df


def set_data_types(df, columns, sortby):

    for column in columns:
        df[column] = pd.to_datetime(df[column], dayfirst=True, errors='coerce')

    df = df.sort_values([sortby])
    return df


def add_new_columns(df, column):

    df['Last_4'] = df[column].astype(str).str[-4:]
    df['Last_6'] = df[column].astype(str).str[-6:]
    df['Last_5'] = df[column].astype(str).str[-5:]
    df['First_6_of_last_9'] = df[column].astype(str).str[-9:]
    df['First_6_of_last_9'] = df['First_6_of_last_9'].astype(str).str[:6]

    return df
