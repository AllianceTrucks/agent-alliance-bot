import pandas as pd

def load_auth_data(path):
    df = pd.read_excel(path)
    return df

def is_authorized(df, contract, password):
    result = df[(df['Номер договора'] == contract) & (df['Пароль'] == password)]
    return not result.empty