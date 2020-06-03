import data_analysis
from data_processing import process_data
import data_viz
from utils import assert_equals

def  test_data_processing(data_file):
    """
    tests data_processing on 4 lines from the data
    prints the dataframe to be checked manually
    and uses assert_equals to test the values of the
    columns used in our analysis is correct 
    """
    data = process_data(data_file)
    print(data)
    assert_equals(.0092997, data['Eccentricity'].loc[0])
    assert_equals(.0005588, data['Eccentricity'].loc[1])
    assert_equals('62039A', data['InternationalDesignator'].loc[0])
    assert_equals('62047A', data['InternationalDesignator'].loc[1])
    assert_equals(14.837090930, data['MeanMotion'].loc[0])
    assert_equals(14.88449574, data['MeanMotion'].loc[1])
    assert_equals(98.4577, data['OrbitInclination'].loc[0])
    assert_equals(58.3055, data['OrbitInclination'].loc[1])
    


def main():
    test_data_processing('test_process_data.txt')    

if __name__ == '__main__':
    main()