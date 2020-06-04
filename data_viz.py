"""
Data visualizations
to support analysis
"""
import numpy as np
import pandas as pd
from data_processing import process_data
import matplotlib.pyplot as plt
import seaborn as sns
from astropy import units as u
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from poliastro.plotting import StaticOrbitPlotter

from data_analysis import get_launch_year, get_launch_year_tally, get_orbit_tally, get_launch_years_column
from calculations import get_orbit_columns

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


def orbit_plot():
    """This function plots the boundaries of Low Earth Orbit (LEO), Medium Earth
    Orbit (MEO), Geosyncronous Orbit (GEO) and High Earth Orbit.
    """

    # LEO boundary
    LEO_orb = Orbit.circular(Earth, alt=2000 * u.km)
    # MEO boundary
    MEO_orb = Orbit.circular(Earth, alt=35786 * u.km)

    fig, ax = plt.subplots(figsize=(17, 10))
    op = StaticOrbitPlotter(ax)
    op.plot(LEO_orb, label='LEO/MEO Boundary')
    op.plot(MEO_orb, label='MEO/GEO Boundary')
    ax.set_title('Geocentric Orbit Boundaries')
    plt.savefig('orbit_fig.png')


def compare_years_by_orbit(data):
    data = get_launch_years_column(data)
    data = get_orbit_columns(data)
    data_LEO = get_orbit_tally(data, 'LEO', False)
    data_MEO = get_orbit_tally(data, 'MEO', False)
    data_GEO = get_orbit_tally(data,'GEO', False)
    data_HEO = get_orbit_tally(data, 'HighEarthOrbit', False)
    
    fig, [ax1, ax2, ax3, ax4] = plt.subplots(4 , figsize=(17, 17)) 
    
    data_LEO.plot(kind='bar', y='LEO', x='LaunchYear', ax = ax1)
    
    data_MEO.plot(kind='bar', y='MEO', x='LaunchYear', ax = ax2)
    
    data_GEO.plot(kind='bar', y='GEO', x='LaunchYear', ax = ax3)
    
    data_HEO.plot(kind='bar', y='HighEarthOrbit', x='LaunchYear', ax = ax4)

    df = data_LEO.merge(data_MEO, left_on='LaunchYear', right_on='LaunchYear', how='outer')
    df = df.merge(data_GEO, left_on='LaunchYear', right_on='LaunchYear', how='outer')
    df = df.merge(data_HEO, left_on='LaunchYear', right_on='LaunchYear', how='outer')
    
    fig.savefig('barcomp.png')
    df = df.fillna(0)

    fig, [ax1, ax2, ax3, ax4] = plt.subplots(4 , figsize=(17, 17)) 
    df.plot(kind='bar', y='LEO', x='LaunchYear', ax = ax1)
    df.plot(kind='bar', y='MEO', x='LaunchYear', ax = ax2)
    df.plot(kind='bar', y='GEO', x='LaunchYear', ax = ax3)
    df.plot(kind='bar', y='HighEarthOrbit', x='LaunchYear', ax = ax4)
    fig.savefig('barcomp2.png')

    fig, ax = plt.subplots(1)
    total = len(data)
    leo = len(data[data['LEO']])
    meo = len(data[data['MEO']])
    geo = len(data[data['GEO']])
    heo = len(data[data['HighEarthOrbit']])
    y = np.arange(4)
    x = [leo,meo,geo,heo]
    plt.bar(y, x)
    fig.savefig('a.png')


def compare_by_alt(data):
    data = get_launch_years_column(data)
    data = get_orbit_columns(data)
    data.plot(kind='scatter', x='LaunchYear', y='Apoapsis')
    plt.title("something")
    plt.xlabel('Year')
    plt.ylabel('Altitude')
    plt.savefig('scatter.png')
    fig, ax = plt.subplots(1)
    data = data['Apoapsis'].apply(lambda x: int(x))
    data = data // 1000
    data = data.groupby(data).count()
    data.plot(kind='bar',  figsize=(17, 10), ax=ax)
    plt.title("something")
    plt.xlabel('Altitude grouped by megameters')
    plt.ylabel('Count')
    plt.savefig('scatter2.png')
    


def main():
    data = process_data('test.txt')
    '''line_plot(data)
    bar_plot(data)
    total_line_and_scatter_plot(data)
    total_bar_stacked(data)
    # orbit_plot()'''
    #compare_years_by_orbit(data)
    compare_by_alt(data)


if __name__ == '__main__':
    main()
