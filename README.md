# COSE-player
A tool for player [the Airline Game](https://private.lud.io/) automatically.  

Exhaustive search is possible, but it costs to much time. Strategy is still needed.

PS: If you like this program, plz give me a star ⭐

## Requirement
Pycharm 2023.2.1.0  
python 3.11.4  
selenium 3.141.0  
pandas 2.1.1  

## Example
1. modify or add the data for each year in /data/yearX.csv
2. run main.py
```
coseplayer = Coseplayer()
# run until the end year, use the last data in yearX.csv
coseplayer.run(end_year=2)
# repeat the year, use all data in year[repeat].csv
coseplayer.repeat(repeat_year=1)
```
3. results are added in the end in result_yearX.csv, so the previous results can be saved 

   ![image](https://github.com/yuyan-z/COSE-player/assets/64955334/9dc046f7-a9a9-4c49-b27b-c6af989ede25)

