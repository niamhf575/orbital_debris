import numpy as np
import pandas as pd
from data_processing import process_data
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score


def get_launch_year(n):
    """
    returns launch year as an int from international designator
    """
    if n is np.NaN:
        return n
    year = int(n[0:2])
    if year>= 57:
        year = year + 1900
    else:
        year = year + 2000
    return year

def get_launch_years_column(data):
    '''
    adds a launch year column to the dataframe
    (returns a new dataframe)
    NaN remains NaN
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
    data  = dict(data)
    data = sorted([(key, data[key]) for key in data.keys()], key = lambda t: t[0])
    data[0] = (data[0][0], data[0][1], data[0][1])
    for i in range(1, len(data)):
        data[i]= (data[i][0], data[i][1] + data[i-1][1], data[i][1])
    headers = ['Year', 'Total', 'Count']
    return pd.DataFrame(data, columns = headers)

def polynomial_fit_count(data):
    # get the data in the right format
    data = get_launch_year_tally(data)
    x = np.array(list(data['Year']))
    y = np.array(list(data['Total']))
    # create the model
    count_func = np.poly1d(np.polyfit(x, y, 2))
    # plot the scatter plot & line of best fit
    plt.scatter(x, y)
    line = np.linspace(1958, 2020, 18000)
    plt.scatter(x, y)
    plt.plot(line, count_func(line))
    plt.savefig('poly_reg.png')
    # print some information about the model
    print('Polynomial fit for number of objects:')
    print('Eq: ')
    print(count_func)
    print('R-squared: ',r2_score(y, count_func(x)))
    # plot the residuals
    res = y - count_func(x)
    d = {'x':x, 'res':res}
    df = pd.DataFrame(d)
    df.plot(kind = 'scatter', x='x', y='res')
    plt.savefig('poly_res.png')


# def probablity_calc 

# def polynomial_fit_probability():

def main():
    df = process_data('test.txt')
    polynomial_fit_count(df)
    

if __name__ == '__main__':
    main()
