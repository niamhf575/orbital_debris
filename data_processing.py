"""
put 2-line element data from a txt file into a pandas data frame
should remove excess whitespace from words
"""
import pandas as pd
import numpy as np


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
                # this has to be done because lots of the values in the text
                # file are not separated by spaces, or anything consistent
                # other than position
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
                words.append('0.'+line[26:33])
                words.append(line[34:42])
                words.append(line[43:51])
                words.append(line[52:63])
                words.append(line[63:68])
                words.append(line[68])
            # words = words[2:]
            for word in words:
                word_line = word_line + "," + word.strip()
            if line_number == 2:
                print(word_line, file=f)
                word_line = ""

    df = pd.read_csv('processed.csv')

    # df = eccentricity_fix(df)

    return df


def main():
    df = process_data('test.txt')


if __name__ == '__main__':
    main()
