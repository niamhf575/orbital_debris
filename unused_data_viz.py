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


    fig, ax = plt.subplots(1)
    total = len(data)
    leo = len(data[data['LEO']])
    meo = len(data[data['MEO']])
    geo = len(data[data['GEO']])
    heo = len(data[data['HighEarthOrbit']])
    y = np.arange(4)
    x = [leo,meo,geo,heo]
    plt.bar(y, x)
    fig.savefig('orbit_bar.png')

    fig, ax = plt.subplots(1)
    data = data['Apoapsis'].apply(lambda x: int(x))
    data = data // 1000
    data = data.groupby(data).count()
    data.plot(kind='bar',  figsize=(17, 10), ax=ax)
    plt.title("something")
    plt.xlabel('Altitude grouped by megameters')
    plt.ylabel('Count')
    plt.savefig('scatter2.png')

    data['LaunchYear'] = data['LaunchYear'].apply(lambda x: int(x))