import fastf1
import pandas as pd

def get_driver_data(driver):
    session = fastf1.get_session(2024, 'Silverstone', 'R')
    session.load()
    driver_data = session.laps.pick_driver(driver)
    driver_df = pd.DataFrame(driver_data)
    return driver_df
    
def get_start_positions(year: int, race: str):
    session = fastf1.get_session(year, race, 'Q')
    session.load()

    drivers = pd.unique(session.laps['Driver']).tolist()

    encoded_drivers = {}

    for pos, driver in enumerate(drivers):
        encoded_drivers[driver] = pos + 1
    return encoded_drivers

def timedelta_to_seconds(dataframe: pd.DataFrame, col : str, new_col: str):
    dataframe[new_col] = dataframe[col].astype("int64") * 1e-9
    dataframe.drop(columns=col, inplace=True)  
    return dataframe

def adjust_laptimes(dataframe: pd.DataFrame):
    dataframe["Laptime"] = dataframe["LapTime"].astype("int64") * 1e-9  # Converts LapTime to seconds
    dataframe["Position(s)"] = dataframe["Position"].astype("int64")  # Converts Position to integer
    dataframe.drop(columns=["LapTime", "Position"], inplace=True)  # Drops LapTime and Position columns
    dataframe.rename(columns={"Position(s)": "Position"}, inplace=True)  # Renames Position(s) to Position
    return dataframe

def get_common(dataframe: pd.DataFrame):
    new_df = dataframe[["LapNumber", "TrackStatus"]]  # Selects only LapNumber and TrackStatus
    return new_df

def get_pitstop(dataframe):
    # Replace NaT or NaN with 0 for both columns
    dataframe["PitInTime"] = dataframe["PitInTime"].fillna(pd.Timedelta(0))
    dataframe["PitOutTime"] = dataframe["PitOutTime"].fillna(pd.Timedelta(0))
    
    # Convert Timedelta to seconds using total_seconds()
    dataframe["PitInTime"] = dataframe["PitInTime"].apply(lambda x: x.total_seconds() if isinstance(x, pd.Timedelta) else x)
    dataframe["PitOutTime"] = dataframe["PitOutTime"].apply(lambda x: x.total_seconds() if isinstance(x, pd.Timedelta) else x)
    
    # Create the PitstopTime column as the difference between PitOutTime and PitInTime
    dataframe["PitstopTime"] = dataframe["PitOutTime"] - dataframe["PitInTime"]
    
    return dataframe

def remove_extras(dataframe):
    new_df = dataframe[["Driver", "Laptime", "PitstopTime", "Position", "Compound"]]  # Drops unnecessary columns
    return new_df
