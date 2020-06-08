# orbital_debris

To recreate our results:

1. Data processing & what to pass into our functions

Use the process_data from data_processing to convert the text file (data.txt)
to a pandas dataframe

All functions below can be passed the resulting dataframe and do
any more processing required themselves.

2. Polynomial fit models

These are in the data_analysis.py files. The functions are polynomial_fit_count
and polynomial_fit_probability. These print the equations and R-squared values
and create plots of the model and and the residuals.

3. Data visualizations

These are in data_viz.py 

4. Installing Poliastro

In Anaconda command terminal:

conda install poliastro --channel conda-forge

and ignore

gzip was not found on your system! You should solve this issue for astroquery.eso to be at its best!
On POSIX system: make sure gzip is installed and in your path!On Windows: same for 7-zip (http://www.7-zip.org)!

when running the program, it doesn't affect anything we're using the library for.



