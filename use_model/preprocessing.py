from fancyimpute import KNN
import numpy as np
import pandas as pd


def claster_fillna(df, name_feature):
    index_feature = df.columns.tolist().index(name_feature)    
    impute_feature = KNN(k=2, verbose=0).fit_transform(df)[:, index_feature]
    return impute_feature

# категориальные признаки
cols_cat =['Pclass', 'Sex', 'SibSp', 'family_size', 'Embarked', 'Parch',
           'Ticket', 'Cabin', 'Cabin_count_psng', 'Words_in_name', 'last_name',  'first_Name'] #Ticket_duplicate
# текстовый признак
cols_txt = ['Name']

# 22.86 Растояние от палубы, на которой находились спасательные шлюпки, до нижнего жилого этажа
# 7 - количество жилых этажей
l = 22.86/7
# словарь для перевода кабины в шкалу расстояния от верхней палубы 
distance_to_deck = {'A':l , 'B':2*l , 'C':3*l , 'D':4*l , 'F':5*l , 'E':6*l , 'G':7*l }

def clear_df(df):
    # создание признака, показывающий расстояние до верхней палубы
    df['Cabin_distance'] = df['Cabin'].apply(lambda x: distance_to_deck.get(str(x)[0], np.nan))
    # признак - состоит ли билет только из цифр
    df['Ticket_onlynum'] = df['Ticket'].apply(lambda x: int(x.isdigit()))
    # количество пассажиров в кабине
    df['Cabin_count_psng'] = df['Cabin'].astype(str).map(lambda x: len(x.split(' ')))
    # Кодирование категориальных признаков
    #df['Embarked'] = df['Embarked'].apply(lambda x: {'S':0, 'C':1, 'Q':2}.get(x, -1))
    df['Sex'] = df['Sex'].apply(lambda x: {'male':0, 'female':1}.get(x, -1))
    # добавляем признак "логарифм цены"
    #df['Fare_log'] = np.log(df['Fare'] + 1)
    # признак показывает, сколько вообще родственников у пассажира 
    df['family_size'] = df['SibSp'] + df['Parch']
    # асстояние от палубы с шлюпками до палубы пассажира
    df['Cabin_distance'] = claster_fillna(df.drop(columns=['Name', 'Ticket', 'Cabin', 'Embarked', 'PassengerId']), 'Cabin_distance')
    
    
    NUMERIC = ['Fare', 'Age']

    df[NUMERIC] = df[NUMERIC].fillna(-1)
    df[NUMERIC] = df[NUMERIC].astype(float)
    
    # Названия с очень низким количеством ячеек будут объединены до уровня "редкие"
    rare_titles = ['Dona', 'Lady', 'the Countess','Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer']
    df['Name'].replace(rare_titles, "Rare title", inplace=True)
    # "Mlle","Ms", "Mme" переводим в шкалу "Miss", "Mrs"
    df['Name'].replace(["Mlle","Ms", "Mme"], ["Miss", "Miss", "Mrs"], inplace=True)
    
    df['Words_in_name'] = df['Name'].str.findall('[A-Za-z]+').apply(len)
    
    # берем только имя
    df['first_Name'] = df['Name'].apply(lambda x: x.split(',')[0].strip())
    df['first_Name'] = df['first_Name'].str.lower()
    
    df['last_name'] = df['Name'].apply(lambda x: x.split(' ')[-1].strip())
    bad_chars = ('"', '(', ')', '-',)
    for bad_char in bad_chars:
        df['last_name'] = df['last_name'].str.replace( bad_char, '')
        
    df['last_name'] = df['last_name'].str.lower()
    
    df[cols_cat] = df[cols_cat].fillna('')
    df[cols_txt] = df[cols_txt].fillna('')
    df[cols_cat] = df[cols_cat].astype(str)
    df[cols_txt] = df[cols_txt].astype(str)
    
    # Удаление признаков
    df = df.drop(columns=['PassengerId'])

    df[NUMERIC] = (df[NUMERIC] - df[NUMERIC].mean())/df[NUMERIC].std()
    
    return df
