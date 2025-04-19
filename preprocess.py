import pandas as pd

def process(df, df2):
    # Filter data for the Summer Olympics only
    #df = df[df['Season'] == 'Summer']
    df = df[df['Season'] == 'Summer']


    # Merge the main dataset with the regions dataset on the 'NOC' column
    df = df.merge(df2, on='NOC', how='left')

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # One-hot encoding for medal columns (Gold, Silver, Bronze)
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    #print("Columns in df:", df.columns.tolist())
    #print(df.head())


    return df
