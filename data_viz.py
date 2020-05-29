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
    line plot for count by launch year from dataframe
    """
    data = data['InternationalDesignator']
    data = data.dropna()
    data = data.apply(get_launch_year)
    data = data.groupby(data).count()
    data.plot(kind = 'line')
    plt.title("Orbital Debris Count Increase Per Year")
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.savefig('count_over_years.png')


def bar_plot(data):
    """
    bar plot for count by launch year from dataframe
    """
    data = data['InternationalDesignator']
    data = data.dropna()
    data = data.apply(get_launch_year)
    data = data.groupby(data).count()
    # print(data.sum())
    data.plot(kind = 'bar', figsize=(17,10))
    plt.title("Orbital Debris Count Increase Per Year")
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.savefig('count_over_years_bar.png')

def total_line_and_bar_plot(data):
    data = data['InternationalDesignator']
    data = data.dropna()
    data = data.apply(get_launch_year)
    data = data.groupby(data).count()
    data  = dict(data)
    data = sorted([(key, data[key]) for key in data.keys()], key = lambda t: t[0])
    for i in range(1, len(data)):
        data[i]= (data[i][0], data[i][1] + data[i-1][1])
    data = pd.DataFrame(data)
    data.plot(kind = 'line', x=0, y=1)
    plt.title("Orbital Debris Total Count Over Time")
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.savefig('total_count_over_years.png')
    data.plot(kind = 'bar', x=0, y=1)
    plt.title("Orbital Debris Total Count Over Time")
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.savefig('total_count_over_years_bar.png', figsize=(17,10))


def total_bar_stacked(data):
    data = data['InternationalDesignator']
    data = data.dropna()
    data = data.apply(get_launch_year)
    data = data.groupby(data).count()
    data  = dict(data)
    data = sorted([(key, data[key]) for key in data.keys()], key = lambda t: t[0])
    data[0] = (data[0][0], data[0][1], data[0][1])
    for i in range(1, len(data)):
        data[i]= (data[i][0], data[i][1] + data[i-1][1], data[i][1])
    headers = ['Year', 'Total', 'Increase']
    data = pd.DataFrame(data, columns = headers)
    data['PrevSum'] = data['Total'] - data['Increase']
    fig,ax = plt.subplots(1, figsize=(17,10))
    data.plot(y='Total', x='Year', kind='bar', color = "blue", ax=ax)
    data.plot(y='PrevSum', x='Year', kind='bar', color = "lightgreen", ax=ax)
    plt.title("Orbital Debris Total Count Over Time")
    plt.xlabel('Year')
    plt.ylabel('Count')
    fig.savefig('stacked_bar.png')

def main():
    data = process_data('test.txt')
    # line_plot(data)
    # bar_plot(data)
    # total_line_and_bar_plot(data) 
    total_bar_stacked(data)   


if __name__ == '__main__':
    main()
