"""
This file contains our main data analysis,
including polynomial fit functions for
count and probability
"""
import numpy as np
import pandas as pd
from data_processing import process_data
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from calculations import probability_calc, get_orbit_columns


def get_launch_year(n):
    """
    returns launch year as an int from international designator
    leaves NaN values as NaN
    """
    if n is np.NaN:
        return n
    year = int(n[0:2])
    if year >= 57:
        year = year + 1900
    else:
        year = year + 2000
    return year


def get_launch_years_column(data):
    '''
    adds a launch year column to the dataframe
    column 'LaunchYear'
    (returns a new dataframe)
    NaN in InternationalDesignator remains NaN
    in LaunchYear
    '''
    data = data.copy()
    data['LaunchYear'] = data['InternationalDesignator'].apply(get_launch_year)
    return data


def get_launch_year_tally(data):
    '''
    input is a dataframe
    returns a dataframe with columns
    'Years', 'Count' (# of objects launched that year),
    'Total' (sum of counts up to that year)
    '''
    data = data['InternationalDesignator']
    data = data.dropna()
    data = data.apply(get_launch_year)
    data = data.groupby(data).count()
    data = dict(data)
    data = sorted(
        [(key, data[key]) for key in data.keys()], key=lambda t: t[0]
        )
    data[0] = (data[0][0], data[0][1], data[0][1])
    for i in range(1, len(data)):
        data[i] = (data[i][0], data[i][1] + data[i-1][1], data[i][1])
    headers = ['Year', 'Total', 'Count']
    return pd.DataFrame(data, columns=headers)


def polynomial_fit_count(data):
    """
    from a dataframe, makes a polynomial
    best fit model of the count of objects
    per year. Creates a plot of the model
    overtop a scatter plot of the data points.
    Prints some information about the model,
    includung the R-squared value. Creates a
    plot of the residuals.
    """
    # get the data in the right format
    data = get_launch_year_tally(data)
    x = np.array(list(data['Year']))
    y = np.array(list(data['Total']))
    # create the model
    count_func = np.poly1d(np.polyfit(x, y, 2))
    # plot the scatter plot & line of best fit
    fig, ax = plt.subplots(1)
    plt.scatter(x, y)
    line = np.linspace(1958, 2020, 18000)
    plt.scatter(x, y)
    plt.plot(line, count_func(line))
    fig.savefig('poly_fit_count.png')
    # print some information about the model
    print('Polynomial fit for number of objects:')
    print('Eq: ')
    print(count_func)
    print('R-squared: ', r2_score(y, count_func(x)))
    # plot the residuals
    fig, ax = plt.subplots(1)
    res = y - count_func(x)
    d = {'x': x, 'res': res}
    df = pd.DataFrame(d)
    df.plot(kind='scatter', x='x', y='res', ax=ax)
    fig.savefig('count_residuals.png')


def get_probability_tally(data):
    '''
    input is a dataframe
    returns a dataframe with columns
    'LaunchYear', 'Probabilty' (total probability
    of impact for that year),
    '''
    data = probability_calc(data)
    data = get_launch_years_column(data)
    data = data[['LaunchYear', 'Probability']]
    data = data.groupby(['LaunchYear'], as_index=False).sum()
    for i in range(1, len(data)):
        data.loc[i, 'Probability'] += data.loc[i-1, 'Probability']
    return data


def polynomial_fit_probability(data):
    """
    from a dataframe, makes a polynomial
    best fit model of the probability of impact
    per year. Creates a plot of the model
    overtop a scatter plot of the data points.
    Prints some information about the model,
    includung the R-squared value. Creates a
    plot of the residuals.
    """
    # get the data in the right format
    data = get_probability_tally(data)
    x = np.array(list(data['LaunchYear']))
    y = np.array(list(data['Probability']))
    # create the model
    prob_func = np.poly1d(np.polyfit(x, y, 2))
    # plot the scatter plot & line of best fit
    # plt.scatter(x, y)
    fig, ax = plt.subplots(1)
    plt.scatter(x, y, color='lightblue')
    line = np.linspace(1963, 2020, 6)
    plt.plot(line, prob_func(line))
    fig.savefig('poly_fit_probability.png')
    # print some information about the model
    print()
    print('Polynomial fit for probability:')
    print('Eq: ')
    print(prob_func)
    print('R-squared: ', r2_score(y, prob_func(x)))
    # plot the residuals
    fig, ax = plt.subplots(1)
    res = y - prob_func(x)
    d = {'x': x, 'res': res}
    df = pd.DataFrame(d)
    df.plot(kind='scatter', x='x', y='res', ax=ax)
    fig.savefig('probability_residuals.png')
    # something


def get_orbit_tally(data, orbit, pre = True):
    """
    set pre = False if you already added orbit columns to data
    tallys up the count of objects per year in orbit 
    returns a dataframe w/ columns orbit (containing counts)
    and 'LaunchYear', orbit may be LEO, MEO, GEO or HighEarthOrbit
    """
    if pre:
        data = get_launch_years_column(data)
        data = get_orbit_columns(data)
    data = data[data[orbit]]
    data = data[['LaunchYear', orbit]]
    data = data.groupby(['LaunchYear'], as_index=False).count()
    for i in range(1, len(data)):
        data.loc[i, orbit] += data.loc[i-1, orbit]
    return data

def main():
    df = process_data('test.txt')
    #polynomial_fit_count(df)
    #polynomial_fit_probability(df)
    get_orbit_tally(df, 'GEO')


if __name__ == '__main__':
    main()
