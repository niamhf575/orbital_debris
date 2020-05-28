import pandas as pd 
from data_processing import process_data
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

def get_launch_year(n):
    """
    returns launch year as an int from international designator
    """
    year = int(n[0:2])
    if year>= 57:
        year = year + 1900
    else:
        year = year + 2000
    return year


def line_plot(data):
    """
    line plot for count by year from dataframe
    """
    data = data['InternationalDesignator']
    data = data.dropna()
    data = data.apply(get_launch_year)
    data = data.groupby(data).count()
    data.plot(kind = 'line')
    plt.title("Orbital Debris Count Over Time")
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.savefig('count_over_years.png')


def bar_plot(data):
    """
    bar plot for count by year from dataframe
    """
    data = data['InternationalDesignator']
    data = data.dropna()
    data = data.apply(get_launch_year)
    data = data.groupby(data).count()
    data.plot(kind = 'bar', figsize=(17,10))
    plt.title("Orbital Debris Count Over Time")
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.savefig('count_over_years_bar.png')


def main():
    data = process_data('test.txt')
    line_plot(data)
    bar_plot(data)


if __name__ == '__main__':
    main()
