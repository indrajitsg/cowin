# Check Vaccine Availability on Cowin Website
In this repo we have a Python script to identify available slots on cowin.gov.in website for COVID 19 vaccination. The script checks every 15 seconds (can be modified in the parameters) for availability. Note that the script currently checks for availabilty of first dose only. If the user wants to change it to second dose, it can be done with minimal changes to the script. The user needs to specify the **state name**, **pincode** and **age** in the yaml.config file. Parameter **district** can be ignored as it is not used by the **main** function. To run the program, specify the date and the number of days ahead to search. If the program finds any availability, it will play an alarm. The mp3 file added in this repo is from https://soundbible.com/1937-Tornado-Siren-II.html which is under Attribution 3.0 license. It can be replaced by any desired mp3 the user wants - after making the necessary changes in the **main** function inside cowin_check.py.

### Packages to be Installed
- cowin_api
- yaml
- playsound

### Instructions
1. In your Python environment ensure the packages mentioned above are installed.
2. Open config.yaml in any editor like Notepad and specify the parameters.
3. From command line, to check for availability for two consecutive days run the python script cowin_api as follows
```
python cowin_check.py -d 25-05-2021 -n 1
```

