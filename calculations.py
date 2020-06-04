"""
Performs Various Calculations from pulled data in data_processing
"""

import data_processing as dp
import math
import pandas as pd
import numpy as np


def semimajor_calc(df):
    """
    Calculates semimajor axis (km) given mean motion in dataset
    """

    mean_motion = df['MeanMotion']

    M = 5.972 * (10 ** 24)
    G = 6.673 * (10 ** -11)
    df['OrbitalPeriod'] = 1 / mean_motion * 3600 * 24
    period = df['OrbitalPeriod']
    df['SemiMajorAxis'] = ((G * M * period ** 2)/(4 * math.pi ** 2)) ** (1/3) / 1000

    return df


def probability_calc(df):
    a0 = 408 + 6371
    df = semimajor_calc(df)

    a = df['SemiMajorAxis']
    e = df['Eccentricity']
    i = df['OrbitInclination'] * math.pi / 180

    df['U'] = (3 - a0 / a - 2 * ((a * (1 - e ** 2)) / a0) ** 0.5 * np.cos(i)) ** 0.5
    df['Ux'] = (2 - a0 / a - a*(1 - e ** 2) / a0) ** 0.5

    U = df['U']
    Ux = df['Ux']
    # print(U)
    # print(Ux)
    # print(a0/a)
    # print(a*(1-e**2)/a0)
    # print(a.min())
    df['Probability'] = U / (2 * math.pi ** 2 * a ** 1.5 * Ux * np.sin(i))
    # print(df['Probability'])
    # print(df.dropna())
    return df.dropna()


def get_altitude_columns(data):
    """
    returns a new dataframe
    with altitude columns 'Periapsis'
    and 'Apoapsis'
    """
    data = data.copy()
    data = semimajor_calc(data)
    radius_earth = 6378
    a = data['SemiMajorAxis']
    e = data['Eccentricity']
    r_p = a * (1 - e)
    r_a = (2 * a) - r_p
    z_p = r_p - radius_earth
    z_a = r_a - radius_earth
    data['Periapsis'] = z_p
    data['Apoapsis'] = z_a
    return data


def get_orbit_columns(data):
    """
    returns a new dataframe
    with altitude columns 'Periapsis'
    and 'Apoapsis' in addition to a column
    with True/False values for whether
    that object's orbit passes through 
    LEO, MEO, GEO, or high earth orbit
    each object may pass through mulitple orbits.
    """
    data = get_altitude_columns(data)
    data['LEO'] = (data['Periapsis'] <= 2000) | (data['Apoapsis'] <= 2000)
    data['MEO'] = ((data['Periapsis'] > 2000) & (data['Periapsis'] < 35786))|((data['Apoapsis'] > 2000) & (data['Apoapsis'] < 35786))
    touches_geo_at_zp_or_za = (data['Periapsis'] == 35786) | (data['Apoapsis'] == 35786)
    touches_geo_btwn_zpza = (data['Periapsis'] < 35786) & (data['Apoapsis'] > 35786)
    data['GEO'] = touches_geo_at_zp_or_za | touches_geo_btwn_zpza
    data['HighEarthOrbit'] = (data['Periapsis'] > 35786) | (data['Apoapsis'] > 35786)
    return data



def main():

    df = dp.process_data('test.txt')

    df = probability_calc(df)

    df.to_csv('probability.csv')

    print('Probability Finished!')


if __name__ == "__main__":
    main()
