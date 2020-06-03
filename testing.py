import data_analysis
import calculations as calcs
from data_processing import process_data
# import data_viz
from utils import assert_equals

def  test_data_processing(data_file):
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
    

def test_calcs(data_file):

    data = process_data(data_file)
    calc_df = calcs.probability_calc(data)
    semimajor_df = calcs.semimajor_calc(data)
    relevant = calc_df[calc_df['SatelliteCatalogNumber'] == 614]

    print(relevant)

    assert_equals(7072.035, relevant['SemiMajorAxis'])
    assert_equals(0.000000302, relevant['Probability'])

def main():
    test_data_processing('test_process_data.txt')    
    test_calcs('test.txt')

if __name__ == '__main__':
    main()