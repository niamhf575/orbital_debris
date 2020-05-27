"""
Performs Various Calculations from pulled data in data_processing 
"""

import data_processing as dp 
import math
import pandas as pd 


def semimajor_calc(df):
    """
    Calculates semimajor axis (km) given mean motion in dataset
    """
    
    mean_motion = df['MeanMotion']

    M = 5.972 * (10 ** 24) 
    G = 6.673 * ( 10 ** -11)
    df['OrbitalPeriod'] = 1 / mean_motion * 3600 * 24
    period = df['OrbitalPeriod']
    df['SemiMajorAxis'] = ((G  * M * period **2)/(4 * math.pi ** 2)) ** (1/3) / 1000

    return df


def main():
    df = dp.process_data('test.txt')
    
    df = semimajor_calc(df)

    df.to_csv('semimajor.csv')

if __name__ == "__main__":
    main()
