import pandas as pd
from collections import OrderedDict


def get_raw_dataframe():
    # Read NBA_Player_Stats.csv into a dataframe
    df = pd.read_csv("data/NBA_Player_Stats.csv")

    # Drop the "Rk" and "Tm" column
    df.drop(columns=["Rk", "Tm"], inplace=True)
    # Drop any rows where the "G" column is less than 45
    df = df[df["G"] >= 45]
    # Sort the dataframe by Player Column
    df.sort_values(by=["Player", "Year"], inplace=True)
    # Drop any players who only show up in one row
    df = df.groupby("Player").filter(lambda x: len(x) > 1)
    df = df.reset_index(drop=True)
    # Convert the "Year" column to the lower year, i.e. 1997-1998 becomes 1997
    df["Year"] = df["Year"].apply(lambda x: int(x.split("-")[0]))
    return df


def get_input_output(df):
    df_grouped = df.groupby("Player")
    # Use ordered dictionary over dataframe append to improve performance
    od_inputs = OrderedDict()
    od_outputs = OrderedDict()
    index = 0
    for _, data in df_grouped:
        for i in range(1, data.shape[0]):
            if data.iloc[i - 1]["Year"] + 1 == data.iloc[i]["Year"]:
                od_inputs[index] = data.iloc[i - 1]
                od_outputs[index] = data.iloc[i]
                index += 1
    inputs = pd.DataFrame.from_dict(od_inputs, orient="index")
    outputs = pd.DataFrame.from_dict(od_outputs, orient="index")
    return (inputs, outputs)


def generate_data():
    df = get_raw_dataframe()
    X, Y = get_input_output(df)
    X.to_csv("data/X.csv", index=False)
    Y.to_csv("data/Y.csv", index=False)
