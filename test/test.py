import pandas as pd
import pytest
import sys
from os import path
rel_path = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(rel_path)

from src.featurise import build_feature_interval

inp_dict = {
    'ScheduledDay': ['2016-04-29T18:38:08Z','2016-04-29T16:08:27Z','2016-04-29T16:19:04Z'],
    'AppointmentDay': ['2016-04-29T00:00:00Z','2016-04-29T00:00:00Z','2016-04-29T00:00:00Z']
}

input_df = pd.DataFrame(inp_dict)

def test_build_feature_interval_happy():
    """
    Happy test to check if the columns are generated correct
    """
    exp_dict = {
        'ScheduledDay': ['2016-04-29', '2016-04-29', '2016-04-29'],
        'AppointmentDay': ['2016-04-29', '2016-04-29', '2016-04-29'],
        'interval' : [0,0,0]
    }
    exp_df = pd.DataFrame(exp_dict)
    exp_df['ScheduledDay'] = pd.to_datetime(exp_df['ScheduledDay'])
    exp_df['ScheduledDay'] = exp_df['ScheduledDay'].dt.date

    exp_df['AppointmentDay'] = pd.to_datetime(exp_df['AppointmentDay'])
    exp_df['AppointmentDay'] = exp_df['AppointmentDay'].dt.date

    input_df['ScheduledDay'] = pd.to_datetime(input_df['ScheduledDay'])
    input_df['ScheduledDay'] = input_df['ScheduledDay'].dt.date

    input_df['AppointmentDay'] = pd.to_datetime(input_df['AppointmentDay'])
    input_df['AppointmentDay'] = input_df['AppointmentDay'].dt.date

    true = build_feature_interval(input_df)
    true['interval'] = true['interval'].astype('int64')
    assert isinstance(true, pd.DataFrame)
    assert exp_df.equals(true)

def test_build_feature_interval_unhappy():
    """
    Unhappy test , keeping the appointment day before booking date
    """
    wrong_dict = {
    'ScheduledDay': ['2016-04-29T18:38:08Z','2016-04-29T16:08:27Z','2016-04-29T16:19:04Z'],
    'AppointmentDay': ['2016-04-27T00:00:00Z','2016-04-29T00:00:00Z','2016-04-29T00:00:00Z']
    }
    wrong_df = pd.DataFrame(wrong_dict)
    wrong_df['ScheduledDay'] = pd.to_datetime(wrong_df['ScheduledDay'])
    wrong_df['ScheduledDay'] = wrong_df['ScheduledDay'].dt.date

    wrong_df['AppointmentDay'] = pd.to_datetime(wrong_df['AppointmentDay'])
    wrong_df['AppointmentDay'] = wrong_df['AppointmentDay'].dt.date
    wrong_df = build_feature_interval(wrong_df)
    assert not (isinstance(wrong_df, pd.DataFrame))





