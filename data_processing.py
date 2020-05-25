"""
put 2-line element data from a txt file into a pandas data frame
still need to remove excess whitespace from words :(
"""
import pandas as pd 

with open('test.txt') as f:
    lines = f.readlines()

with open("test.csv", "w") as f:
    titles = "Satellite Catalog Number, Elset Classification, Element Set Epoch (UTC), 1st Derivative Mean Motion, 2nd Derivative Mean Motion, b* Drag Term, Element Set Type, Element Number, Checksum, Orbit Inclination, Eccentricity, Argument of Perigee, Mean Anomaly, Mean Motion, Revolution Number at Epoch, Checksum(2)"
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
                word_line = word_line + words[0]
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
            word_line = word_line + ", "+ word
        if line_number == 2:
            print(word_line, file=f)
            word_line = ""
