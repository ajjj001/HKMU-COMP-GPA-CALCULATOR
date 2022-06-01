import pandas as pd
import argparse

points = {
    'A' : 4,
    'A-': 3.7,
    'B+': 3.3,
    'B' : 3, 
    'B-': 2.7,
    'C+': 2.3,
    'C' : 2,
}

honours = {
    'First Class' : 3.5,
    'Second Class (Upper Division)' : 3.0,
    'Second Class (Lower Division)' : 2.5,
    'Third Class' : 2.0,
}

A = [
    'S312F',
    'S313F',
    'S320F',
    'S321F',
    'S350F',
    'S351F',
]

def find(target, df):
    index = 0 
    for i in range(len(df)):
        target -= df.iloc[i]['Unit']
        if target <= 0:
            index = i
            break
    df = df.iloc[:index+1]
    return df

parser = argparse.ArgumentParser()                                               

parser.add_argument("--file", "-f", type=str, required=True)
args = parser.parse_args()

df = pd.read_csv(args.file)

df = df[['Subject','Unit','Grade']]

# FILL or DROP subjects missing grades
# df.fillna('B', inplace=True)
df.dropna(inplace=True) 

df['points'] = df['Grade'].map(points)
df['scaled'] = df['points'] * df['Unit']
df['is_higher'] = df['Subject'].str.contains('S3') | df['Subject'].str.contains('S4')
df['is_middle'] = df['Subject'].str.contains('S2')

df_A = df[df['Subject'].isin(A)].sort_values(by='points', ascending=False)

target = 20
df_A = find(target, df_A)

df_A2 = df[(df['is_higher'] == True) & (df['Subject'].isin(df_A['Subject']) == False)].sort_values(by='points', ascending=False)

target = 20
df_A2 = find(target, df_A2)

df_A = pd.concat([df_A, df_A2])

df['is_higher'] = df['Subject'].str.contains('S3') | df['Subject'].str.contains('S4')

df_B = df[((df['is_higher'] == True) | (df['is_middle'] == True)) &  (df['Subject'].isin(df_A['Subject']) == False)].sort_values(by='points', ascending=False)

target = 40
df_B = find(target, df_B)

df_A['scaled'] = df_A['scaled'] * 2

ggpa = (df_A['scaled'].sum() + df_B['scaled'].sum()) / 120
cgpa = df['scaled'].sum() / df['Unit'].sum()
print(f'Your CGPA is {cgpa}')
print(f'Your GGPA is {ggpa}')

for key, value in honours.items():
    if ggpa >= value:
        print(f'Your Honours Classification is {key}')
        break