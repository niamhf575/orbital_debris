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


def probability_calc(df):
    a0 = 300
    df = semimajor_calc(df)

    a = df['SemiMajorAxis']
    e = df['Eccentricity']
    i = df['OrbitInclination'] * math.pi / 180

    df['U'] = (3 - a0 / a - 2 * ((a * (1 - e ** 2))/ a0) ** 0.5 * math.cos(i)) ** 0.5
    df['Ux'] = (2 - a0 / a - a(1 - e ** 2)/ a0) ** 0.5

    U = df['U']
    Ux = df['Ux']
    df['Probablity'] = U / (2 * math.pi ** 2 * a ** 1.5 * Ux * math.sin(i))

    return df

def main():

    df = dp.process_data('test.txt')
    
    df = probability_calc(df)

    df.to_csv('probability.csv')

if __name__ == "__main__":
    main()
