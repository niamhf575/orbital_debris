"""
put 2-line element data from a txt file into a pandas data frame
should remove excess whitespace from words
"""
import pandas as pd 
import numpy as np
# from data_viz import total_bar_stacked, total_line_and_bar_plot


def process_data(file_name):
    """
    file_name is a txt file,
    csv file created is processed.csv
    returns a pandas dataframe
    """
    with open(file_name) as f:
        lines = f.readlines()

    with open('processed.csv', "w") as f:
        titles = "SatelliteCatalogNumber,ElsetClassification,InternationalDesignator,ElementSetEpoch(UTC),1stDerivativeMeanMotion,2ndDerivativeMeanMotion,b*DragTerm,ElementSetType,ElementNumber,Checksum,OrbitInclination,RightAscension,Eccentricity,ArgumentofPerigee,MeanAnomaly,MeanMotion,RevolutionNumberatEpoch,Checksum(2)"
        print(titles, file=f)
        word_line = ""
        for line in lines:
            words = []
            line_number = int(line[0])
            if line_number == 1:
                    #words.apppend(line[0])
                    words.append(line[2:7])
                    words.append(line[7])
                    words.append(line[9:17])
                    words.append(line[18:32])
                    words.append(line[33:43])
                    words.append(line[44:52])
                    words.append(line[53:61])
                    words.append(line[62])
                    words.append(line[64:68])
                    words.append(line[68])
                    word_line = word_line + words[0].strip()
                    words = words[1:]
            else:
                words.append(line[8:16])
                words.append(line[17:25])
                words.append(line[26:33])
                words.append(line[34:42])
                words.append(line[43:51])
                words.append(line[52:63])
                words.append(line[63:68])
                words.append(line[68])
            #words = words[2:] 
            for word in words:
                word_line = word_line + ","+ word.strip()
            if line_number == 2:
                print(word_line, file=f)
                word_line = ""
    df = pd.read_csv('processed.csv')
    return df


def get_year(epoch):
    year = int(epoch//1000)
    if year>= 57:
        year = year + 1900
    else:
        year = year + 2000
    return year


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


def main():
    df = process_data('test.txt')
    

if __name__ == '__main__':
    main()
