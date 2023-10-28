import pandas as pd
import numpy as np

# Load the Excel file
df = pd.read_excel("your.xlsx")

df.drop(['问卷id', '答题开始时间', '时长(分钟)'], axis=1, inplace=True)

# check column positions
for index, column_name in enumerate(df.columns):
    print(index, column_name)

new_names = ['Q1', 'Q2', 'Q3']

# rename columns
positions = list(range(5, 17))

new_names_cycle = list(itertools.islice(itertools.cycle(new_names), len(positions)))
col_mapping = {df.columns[i]: new_names_cycle[j] for j, i in enumerate(positions)}
df.rename(columns=col_mapping, inplace=True)

# rename telephone column
tel_position = 17 
tel_new_name = "tel"

# Create a mapping from the old column name to the new name using the position
col_mapping = {df.columns[tel_position]: tel_new_name}

# Rename the column
df.rename(columns=col_mapping, inplace=True)

# Rename columns
column_mapping = {
    '🇹🇲Turkmen dilinde': 'tk',
    '🇷🇺На Русском': 'ru',
    '🇹🇯Ба Тоҷики': 'tj',
    '🇺🇿Узбек тилида ': 'uz'
}
df.rename(columns=column_mapping, inplace=True)
# print(df.columns)

# Isolate the language columns and work on a copy
langs_df = df[['tk', 'ru', 'tj', 'uz']].copy()

# Replace 1s with Language Codes using .loc
langs_df.loc[langs_df['tk'] == 1, 'tk'] = 'tk'
langs_df.loc[langs_df['ru'] == 1, 'ru'] = 'ru'
langs_df.loc[langs_df['tj'] == 1, 'tj'] = 'tj'
langs_df.loc[langs_df['uz'] == 1, 'uz'] = 'uz'

# Create the 'lang' column
langs_df['lang'] = langs_df[['tk', 'ru', 'tj', 'uz']].apply(lambda row: next((x for x in row if isinstance(x, str)), None), axis=1)

# Insert the 'lang' column next to 'uid' in the original DataFrame
df.insert(df.columns.get_loc('uid') + 1, 'lang', langs_df['lang'])

# Drop the original language columns from the main DataFrame
df.drop(['tk', 'ru', 'tj', 'uz'], axis=1, inplace=True)

# For each unique question, merge its columns
for question in ['Q1', 'Q2', 'Q3']:
    # Create a new column with merged values
    df[question + '_merged'] = df[[question + suffix for suffix in ['', '.1', '.2', '.3'] if question + suffix in df.columns]].apply(lambda row: next((x for x in row if x != '-'), '-'), axis=1)
    
    # Drop the original columns
    for suffix in ['', '.1', '.2', '.3']:
        col_name = question + suffix
        if col_name in df.columns:
            df.drop(col_name, axis=1, inplace=True)

# Merged columns to original names
df.rename(columns={'Q1_merged': 'Q1', 'Q2_merged': 'Q2', 'Q3_merged': 'Q3'}, inplace=True)

# Count strings
def word_count(s):
    return len(str(s).split())

# Identify the columns to check
columns_to_check = ['Q1', 'Q2', 'Q3']

# Filter the dataframe
df = df[df[columns_to_check].applymap(word_count).max(axis=1) >= 8]

# Avoid Excel messing up uids
df['uid'] = df['uid'].astype(str)

filename = "your-updated.xlsx"
df.to_excel(filename, index=False)
