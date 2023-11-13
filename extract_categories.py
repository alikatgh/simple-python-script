import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_excel("way_to_your_xlsx")

column_mapping = {
    '🇹🇲Turkmen dilinde': 'tk',
    '🇷🇺На Русском': 'ru',
    '🇹🇯Ба Тоҷики': 'tj',
    '🇺🇿Узбек тилида': 'uz'
}
df.rename(columns=column_mapping, inplace=True)

langs_df = df[['tk', 'ru', 'tj', 'uz']].copy()
langs_df.loc[langs_df['tk'] == 1, 'tk'] = 'tk'
langs_df.loc[langs_df['ru'] == 1, 'ru'] = 'ru'
langs_df.loc[langs_df['tj'] == 1, 'tj'] = 'tj'
langs_df.loc[langs_df['uz'] == 1, 'uz'] = 'uz'

# Create the 'lang' column
langs_df['lang'] = langs_df[['tk', 'ru', 'tj', 'uz']].apply(
    lambda row: next((x for x in row if isinstance(x, str)), None), axis=1)

# Insert the 'lang' column next to 'uid' in the original DataFrame
df.insert(df.columns.get_loc('uid') + 1, 'lang', langs_df['lang'])

# Drop the original language columns
df.drop(['tk', 'ru', 'tj', 'uz'], axis=1, inplace=True)

# Categories and their corresponding columns in different languages
categories = {
    "Game": ["Игра", "Уйин", "Oyun"],
    "Friend-Making": ["Знакомства", "Танишув", "Tanyshlyk"],
    "Competition": ["Соревнование", "Беллашув", "Yaryshmak"],
    "Talk Show": ["Ток-шоу", "Ток Шоу", "Ток-Шоу"],
    "Talent Show": ["Шоу талантов", "Намоиши истеъдод", "Истеъдодлар Намойиши", "Sho zehinler", "Show"],
    "Radio": ["Радио", "Радио", "Радио", "Radio"],
    "Couple Wedding": ["Пара свадьба", "Тӯйи ҷуфт", "Туй маросими", "Toy dawarasy"],
    "Channel Awards Ceremony": ["Церемония награждения канала", "Маросими ҷоизасупории канал", "Канални Тақдирлаш Маросими", "Kanal acylysh dabarasy"]
}

# Merging categories
df_merged = pd.DataFrame()
for category, cols in categories.items():
    df_merged[category] = df[cols].replace('-', 0).astype(int).sum(axis=1)

# Identifying the chosen category
chosen_categories = df_merged.idxmax(axis=1)
# Replace '0' with None for no chosen category
chosen_categories = chosen_categories.replace({'0': None})

# Adding chosen categories to the main dataframe
df['Chosen Category'] = chosen_categories

# Final dataset
final_df = df[['uid', 'lang', 'Chosen Category']]

# Displaying the final dataset
print(final_df.head(50))

# Splitting the 'Chosen Category' into individual categories and counting each category
category_counts = final_df['Chosen Category'].str.split(
    ', ', expand=True).stack().value_counts()

# Create the plot
plt.figure(figsize=(10, 6))
sns.barplot(x=category_counts.index, y=category_counts.values, color='skyblue')
plt.title('Frequency of Chosen Categories')
plt.xlabel('Category')
plt.ylabel('Frequency')

plt.xticks(rotation=45)
plt.show()

# Counting the frequency of each language
language_counts = final_df['lang'].value_counts()

# another plot
plt.figure(figsize=(8, 5))
sns.barplot(x=language_counts.index,
            y=language_counts.values, color='lightgreen')
plt.title('Frequency of Languages')
plt.xlabel('Language')
plt.ylabel('Count')
plt.show()

# Avoid SettingWithCopyWarning
final_df = final_df.copy()

# Excel messing up uids
final_df['uid'] = final_df['uid'].astype(str)

# save the results
filename = "way_to_your_xlsx"
final_df.to_excel(filename, index=False)

