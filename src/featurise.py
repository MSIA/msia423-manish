import pandas as pd

def build_feature_interval(no_show_df):
    """
    This function accepts a dataframe and builds the interval feature. This is the only feature built, the data from kaggle was already clean
    also, didn't need to encode the categorical feature since used tree based model
    Testing of this function has been designed to check if all this feature is built correctly
    Input : Pandas dataframe
    Output : Pandas dataframe
    """


    no_show_df['interval'] = no_show_df['AppointmentDay'] - no_show_df['ScheduledDay']
    no_show_df['interval'] = pd.to_numeric(no_show_df['interval'].dt.days, downcast='integer')
    if (no_show_df.interval < 0).any():
        return None
    return no_show_df