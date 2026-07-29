import pandas as pd

def process_lap_data(df: pd.DataFrame ) -> pd.DataFrame:
    """
    Process the lap data DataFrame by performing necessary cleaning and transformations.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing lap data.

    Returns:
    pd.DataFrame: The processed DataFrame with cleaned and transformed data.
    """
    if df.empty:
        return df

    df = df[df['lap_duration'].notna()] 
    df = df.sort_values(['driver_number', 'lap_number'])
    
    return df

def process_stints(df: pd.DataFrame) -> pd.DataFrame:

    if df.empty:
        return df

    df = df.sort_values(['driver_number', 'stint_number'])
    df['compound'] = df["compound"].fillna("Unknown")
    df["lap_count"] = df["lap_end"] - df["lap_start"] + 1

    return df

def process_pit_stops(df: pd.DataFrame) -> pd.DataFrame:

    if df.empty:
        return df

    df = df[df["pit_duration"].notna()]
    df = df.sort_values(['driver_number', 'lap_number'])

    return df

def build_driver_color_map(driver_df: pd.DataFrame) -> dict:
    if driver_df.empty:
        return {}

    driver_df['team_colour'] = driver_df['team_colour'].apply(lambda x: f"#{x}" if not str(x).startswith('#') else x)

    driver_df["driver_number"] = driver_df["driver_number"].astype(str)

    color_map = {
        str(row["name_acronym"]): row['team_colour'] for _, row in driver_df.iterrows()
        for _, row in driver_df.iterrows()
        if pd.notna(row['team_colour'])
    }

    return color_map