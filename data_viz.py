"""
Data visualizations
to support analysis
"""
import pandas as pd
from data_processing import process_data
import matplotlib.pyplot as plt
import seaborn as sns
from data_analysis import get_launch_year, get_launch_year_tally

sns.set()

def line_plot(data):
    """
    line plot for count by launch year from dataframe
    """
    data = data['InternationalDesignator']
    data = data.dropna()
    data = data.apply(get_launch_year)
    data = data.groupby(data).count()
    data.plot(kind='line')
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
    data.plot(kind='bar', figsize=(17, 10))
    plt.title("Orbital Debris Count Increase Per Year")
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.savefig('count_over_years_bar.png')


def total_line_and_scatter_plot(data):
    '''
    creates line and bar plots for the 
    total count of objects per year
    '''
    data = get_launch_year_tally(data)
    data.plot(kind='line', x='Year', y='Total')
    plt.title("Orbital Debris Total Count Over Time")
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.savefig('total_count_over_years.png')
    data.plot(kind='scatter', x=0, y=1)
    plt.title("Orbital Debris Total Count Over Time")
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.savefig('total_count_over_years_scatter.png', figsize=(17, 10))


def total_bar_stacked(data):
    '''
    creates a stacked bar chart that shows 
    the total count of objects per year 
    highlighting the increase each year in
    a different color
    '''
    data = get_launch_year_tally(data)
    data['PrevSum'] = data['Total'] - data['Count']
    fig, ax = plt.subplots(1, figsize=(17, 10))
    data.plot(y='Total', x='Year', kind='bar', color="blue", ax=ax)
    data.plot(y='PrevSum', x='Year', kind='bar', color="lightgreen", ax=ax)
    plt.title("Orbital Debris Total Count Over Time")
    plt.xlabel('Year')
    plt.ylabel('Count')
    fig.savefig('stacked_bar.png')


def main():
    data = process_data('test.txt')
    line_plot(data)
    bar_plot(data)
    total_line_and_scatter_plot(data)
    total_bar_stacked(data)


if __name__ == '__main__':
    main()
