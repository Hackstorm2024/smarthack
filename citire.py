import pandas as pd

def citire_date():

    raf_df = pd.read_csv('refineries.csv', delimiter=';')
    conn_df = pd.read_csv('connections.csv', delimiter=';')
    customers_df = pd.read_csv('customers.csv', delimiter=';')
    demands_df = pd.read_csv('demands.csv', delimiter=';')
    tanks_df = pd.read_csv('tanks.csv', delimiter=';')
    teams_df = pd.read_csv('teams.csv', delimiter=';')
    
    return raf_df, conn_df, customers_df, demands_df, tanks_df, teams_df
