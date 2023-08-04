# A longitudinal study on the temporal validity of software samples

This is the complete dataset used in the study "A longitudinal study on the temporal validity of software samples".

## Data collected
In "datasets" folder is the data used in the study. 
+ dunn-test-results: contains .CSV files with the results of the Dunn test for each variable.
+ snapshots: has the population of quality repositories in each wave (from 2017-07-01 until 2023-06-01.
+ updates-monthly-data: comprise the projects that registered activity or updates every month.
+ varga-test-results: contains .CSV files with the results of the Vargha Delaney test for each variable.

## Plot graphics
To plot the results and graphics in the article there is a Jupyter Notebook "LongStudyGraphNotebook.ipynb".
It is initially configured to use the data in "datasets" folder.

## Replication Kit
For replication purposes, a new dataset can be generated running. To do so, the virtual environment must be configured using requirements.txt file and then just run "main.py" script. 
The script comprise 3 specific stages:
+ Project retrieval: at first the project are retrieved from Github's API.
+ Xia script: with the list of projects, [Xia's script](https://github.com/arennax/Health_Indicator_Prediction) is used to extract monthly repository information. Xia's project is imported in "Health_Indicator_Prediction" folder.
+ Generate datasets for the study: finally, the data for the study is generated using the output of Xia's script


