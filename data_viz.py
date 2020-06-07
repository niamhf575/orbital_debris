"""
Data visualizations
to support analysis
"""
import numpy as np
from data_processing import process_data
import matplotlib.pyplot as plt
import seaborn as sns
from astropy import units as u
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from poliastro.plotting import StaticOrbitPlotter

from data_analysis import get_launch_year, get_launch_year_tally
from data_analysis import get_orbit_tally, get_launch_years_column
from calculations import get_orbit_columns


def bar_plot_LEO(data):
    """
    takes a dataframe from process_data and creates a
    bar plot for count by launch year from dataframe
    (for LEO)
    """
    data = get_orbit_columns(data)
    data = data[data['LEO']]
    data = data['InternationalDesignator']
    data = data.dropna()
    data = data.apply(get_launch_year)
    data = data.groupby(data).count()
    data.plot(kind='bar', figsize=(17, 10), color='#0f4c81')
    plt.title("Orbital Debris Count Increase Per Year (LEO)")
    plt.xlabel('Launch Year')
    plt.ylabel('Count')
    plt.savefig('visualizations/count_by_launch_year.png')


def total_line_and_scatter_plot_LEO(data):
    '''
    takes a dataframe from process_data
    creates line and bar plots for the 
    total count of objects present per year
    (for LEO)
    '''
    data = get_orbit_columns(data)
    data = data[data['LEO']]
    data = get_launch_year_tally(data)
    data.plot(kind='line', x='Year', y='Total', color='#0f4c81')
    plt.title("Orbital Debris Total Count Over Time (LEO)")
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.savefig('visualizations/total_count_over_years_line.png')
    data.plot(kind='scatter', x='Year', y='Total', color='#0f4c81')
    plt.title("Orbital Debris Total Count Over Time (LEO)")
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.savefig('visualizations/total_count_over_years_scatter.png', figsize=(17, 10))


def total_bar_stacked_LEO(data):
    '''
    from a dataframe of orbital data
    creates a stacked bar chart that shows 
    the total count of objects per year 
    highlighting the increase each year in
    a different color
    (for LEO)
    '''
    data = get_orbit_columns(data)
    data = data[data['LEO']]
    data = get_launch_year_tally(data)
    data['PrevSum'] = data['Total'] - data['Count']
    fig, ax = plt.subplots(1, figsize=(17, 10))
    data.plot(y='Total', x='Year', kind='bar', color="#ed6663", ax=ax)
    data.plot(y='PrevSum', x='Year', kind='bar', color="#0f4c81", ax=ax)
    plt.title("Orbital Debris Total Count Over Time (LEO)")
    plt.xlabel('Year')
    plt.ylabel('Count')
    fig.savefig('visualizations/stacked_bar_count.png')


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
    plt.savefig('visualizations/orbit_fig.png')


def compare_years_by_orbit(data):
    """
    takes a dataframe of orbital debris data and adds columns 
    with information about orbits. Creates three visualizations:
    1. A set of four bar graphs showing objects per year by orbit
    2. A bar graph showing total count per orbit
    3. A stacked bar showing objects per year colored by orbit
    """
    # processing
    data = get_launch_years_column(data)
    data = get_orbit_columns(data)
    data = data[['LaunchYear', 'LEO', 'MEO', 'GEO', 'HighEarthOrbit']]
    data = data.dropna()
    data_LEO = get_orbit_tally(data, 'LEO', False)
    data_MEO = get_orbit_tally(data, 'MEO', False)
    data_GEO = get_orbit_tally(data, 'GEO', False)
    data_HEO = get_orbit_tally(data, 'HighEarthOrbit', False)
    df = data_LEO.merge(data_MEO, left_on='LaunchYear', right_on='LaunchYear', how='outer')
    df = df.merge(data_GEO, left_on='LaunchYear', right_on='LaunchYear', how='outer')
    df = df.merge(data_HEO, left_on='LaunchYear', right_on='LaunchYear', how='outer')
    df = df.fillna(0)
    # first plot
    fig, [ax1, ax2, ax3, ax4] = plt.subplots(4 , figsize=(17, 30), subplot_kw={'ylim': (0,16000)}) 
    df.plot(kind='bar', y='LEO', x='LaunchYear', ax = ax1, color="#0f4c81")
    df.plot(kind='bar', y='MEO', x='LaunchYear', ax = ax2, color="#0f4c81")
    df.plot(kind='bar', y='GEO', x='LaunchYear', ax = ax3, color="#0f4c81")
    df.plot(kind='bar', y='HighEarthOrbit', x='LaunchYear', ax = ax4, color="#0f4c81")
    ax1.set_title('LEO')
    ax2.set_title('MEO')
    ax3.set_title('GEO')
    ax4.set_title('High Earth Orbit')
    plt.setp([ax1, ax2, ax3, ax4], xlabel='Year')
    plt.setp([ax1, ax2, ax3, ax4], ylabel='Count')
    fig.savefig('visualizations/orbit_years_comp.png')
    # second plot
    fig, ax = plt.subplots(1)
    total = len(data)
    leo = len(data[data['LEO']])
    meo = len(data[data['MEO']])
    geo = len(data[data['GEO']])
    heo = len(data[data['HighEarthOrbit']])
    y = np.arange(4)
    x = [leo, meo, geo, heo]
    plt.bar(y, x)
    fig.savefig('visualizations/orbit_bar.png')
    # third plot
    fig, ax = plt.subplots(1, figsize=(17, 10))
    df['HighEarthOrbit'] = df['LEO'] + df['MEO'] + df['GEO'] + df['HighEarthOrbit']
    df['GEO'] = df['LEO'] + df['MEO'] + df['GEO']
    df['MEO'] =df['LEO'] + df['MEO']
    df.plot(y='HighEarthOrbit', x='LaunchYear', kind='bar', color="#ffa372", ax=ax)
    df.plot(y='GEO', x='LaunchYear', kind='bar', color="#ed6663", ax=ax)
    df.plot(y='MEO', x='LaunchYear', kind='bar', color="#3282b8", ax=ax)
    df.plot(y='LEO', x='LaunchYear', kind='bar', color="#0f4c81", ax=ax)
    plt.title("Orbital Debris Total Count Over Time, by Orbit")
    plt.xlabel('Year')
    plt.ylabel('Count')
    fig.savefig('visualizations/stacked_bar_orbits.png')


def compare_by_alt(data):
    """
    takes a dataframe of orbital debris data and adds columns 
    with information about orbits. Creates a scatter plot of
    altitude vs launch year
    """
    data = get_launch_years_column(data)
    data = get_orbit_columns(data)
    data.plot(kind='scatter', x='LaunchYear', y='Apoapsis', figsize=(7, 5), color="#0f4c81")
    plt.title("Altitude vs Year Launched")
    plt.xlabel('Launch Year')
    plt.ylabel('Altitude (km)')
    plt.savefig('visualizations/alt_vs_launch_year.png')
    


def main():
    data = process_data('test.txt')
    bar_plot_LEO(data)
    total_line_and_scatter_plot_LEO(data)
    total_bar_stacked_LEO(data)
    orbit_plot()
    compare_years_by_orbit(data)
    compare_by_alt(data)


if __name__ == '__main__':
    main()
