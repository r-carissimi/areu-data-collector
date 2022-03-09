# 🚑 AREU Data Collector
Little utility that downloads and stores real-time data available at [official website](https://www.areu.lombardia.it/web/home/missioni-aat-real-time) of AREU, the agency that coordinates the ambulances in Lombardy, Italy.



## Running

Just run the script with python. Move to the directory of the script and type

```
python3 areu-collector.py
```

Data will be available in the `data` folder as `.csv` files.

### Collecting data automatically

Under Linux, you can append a rule in your crontab file to run the script every 2 minutes or so. Please refer to the [crontab manual](https://linux.die.net/man/5/crontab), or read a tutorial.

Based on superficial pure experience data is updated every 3 minutes.



## TODO

- [ ] Let the user choose the data folder
- [ ] Give the option to save data in a single file
- [ ] Give the option to run the script forever
