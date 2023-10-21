import pandas as pd

def word_count(s):
    return len(str(s).split())

def load_and_process_data(file_path):
    df = pd.read_excel(file_path)
  
    columns_to_rename = {
        'Почему вы хотите стать ведущим на imo? Как это поможет вам лично и в вашей карьере?': 'RUQ1',
        'Предложите идею для уникального аудиошоу на imo. Что сделает его интересным?': 'RUQ2',
        'Как вы собираетесь совмещать обязанности ведущего на imo с другими делами? ': 'RUQ3',
        '...',
    }
    df.rename(columns=columns_to_rename, inplace=True)
    
    # Filtering rows based on word count
    selected_columns = list(columns_to_rename.values())
    filtered_rows = df[selected_columns].applymap(word_count).any(axis=1)
    filtered_df = df[filtered_rows]

    # Dropping and renaming columns
    drop_cols = ["问卷id", "答题开始时间", "时长(分钟)"]
    rename_cols = {
        'UZQ7': 'TGQ7',
        'UZQ8': 'TGQ8',
        'UZQ9': 'TGQ9',
        'TGQ4': 'UZQ4',
        'TGQ5': 'UZQ5',
        'TGQ6': 'UZQ6'
    }
    filtered_df = filtered_df.drop(columns=drop_cols).rename(columns=rename_cols)

    # Replacing values and swapping values, because the form as different order in questions, TJ and UZ
    replacements = {
        "🇷🇺 На Русском": {1: "RU"},
        "🇹🇯 Ба Тоҷики": {1: "TG"},
        "🇺🇿 Узбек тилида": {1: "UZ"},
        'TG': 'UZ',
        'UZ': 'TG'
    }
    filtered_df.replace(replacements, inplace=True)
    
    # Reordering columns, not working 100% yet
    column_order = [
        'uid',
        '🇷🇺 На Русском',
        '🇹🇯 Ба Тоҷики',
        '🇺🇿 Узбек тилида',
        'RUQ1', 'RUQ2', 'RUQ3',
        'UZQ4', 'UZQ5', 'UZQ6',
        'TGQ7', 'TGQ8', 'TGQ9',
    ]
    filtered_df = filtered_df[column_order]
    
    # Converting UID column to string, avoid Excel dynamic change
    filtered_df['uid'] = filtered_df['uid'].astype(str)
    
    return filtered_df

# Load, process, and save the data
file_path = "to_your_file.xlsx"
output_path = "to_your_file.xlsx"
filtered_df = load_and_process_data(file_path)
filtered_df.to_excel(output_path, index=False)

