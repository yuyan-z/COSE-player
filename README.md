# COSE-player
A tool for player the Airline Game automatically

## Requirement
Pycharm 2023.2.1.0
python 3.11.4  
selenium 3.141.0  
pandas 2.1.1  

## Example
1. modify the data for each year in /data/yearX.csv
2. run main.py
```
coseplayer = Coseplayer()
# run until the end year, use the last data in yearX.csv
coseplayer.run(end_year=2)
# repeat the year, use all data in year[repeat].csv
coseplayer.repeat(repeat_year=1) # repeat the year
```
3. results are generated in result_yearX.csv
