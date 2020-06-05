import data_analysis
import calculations as calcs
from data_processing import process_data
# import data_viz
from utils import assert_equals
import pandas as pd


def test_data_processing(data_file):
    """
    tests data_processing on 4 lines from the data
    prints the dataframe to be checked manually
    and uses assert_equals to test the values of the
    columns used in our analysis is correct
    """
    data = process_data(data_file)

    assert_equals(.0092997, data['Eccentricity'].loc[0])
    assert_equals(.0005588, data['Eccentricity'].loc[1])
    assert_equals('62039A', data['InternationalDesignator'].loc[0])
    assert_equals('62047A', data['InternationalDesignator'].loc[1])
    assert_equals(14.837090930, data['MeanMotion'].loc[0])
    assert_equals(14.88449574, data['MeanMotion'].loc[1])
    assert_equals(98.4577, data['OrbitInclination'].loc[0])
    assert_equals(58.3055, data['OrbitInclination'].loc[1])


def test_launch_years_column(df):
    '''
    tests the get_launch_year_column
    function from data_analysis.py
    (this tests get_launch_year function
    at the same time since they rely on
    each other)
    '''
    df = data_analysis.get_launch_years_column(df)
    assert_equals(1962, df['LaunchYear'].loc[0])
    assert_equals(1962, df['LaunchYear'].loc[1])


def test_get_launch_year_tally():
    '''
    tests get_launch_year_tally from data_analysis.py
    '''
    data = {'InternationalDesignator': ['02', '02', '01', '03', '67',
                                        '67', '91']}
    headers = ['InternationalDesignator']
    data = pd.DataFrame(data, columns=headers)
    data = data_analysis.get_launch_year_tally(data)
    assert_equals([2, 3, 4, 6, 7], list(data['Total']))
    assert_equals([2, 1, 1, 2, 1], list(data['Count']))


def test_calcs(data_file):
    """
    tests calculations for semimajor axis and probability for a
    satellite with non-zero probability.
    """
    data = process_data(data_file)
    calc_df = calcs.probability_calc(data)
    relevant = calc_df[calc_df['SatelliteCatalogNumber'] == 614]

    assert_equals(7072.035, relevant['SemiMajorAxis'])
    assert_equals(0.000000302, relevant['Probability'])


''''def test_get_orbit_tally():

    data = {'InternationalDesignator':['02','02', '01', '03', '67', '67', '91'], 'LEO': [True,True,False,True,False,True,False]}
    headers = ['InternationalDesignator', 'LEO']

    data = pd.DataFrame(data, columns = headers)
    #data = data_analysis.get_orbit_tally(data, 'LEO')
    print(data)
    #assert_equals([2,1,1], list(data['LEO']))''''


def main():
    test_data_processing('test_process_data.txt')
    test_calcs('test.txt')
    test_df = process_data('test_process_data.txt')
    test_data_processing('test_process_data.txt')
    test_launch_years_column(test_df)
    test_get_launch_year_tally()
    test_get_orbit_tally()
    print('Success!!!!!')


if __name__ == '__main__':
    main()
