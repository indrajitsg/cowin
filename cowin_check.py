import sys, getopt
import datetime
import time
import numpy
from cowin_api import CoWinAPI
import playsound
import signal
import yaml

#------------------------------------------
# Helper functions
#------------------------------------------

# Read config parameters file
def get_config_param():
    """Read config file for params"""
    with open('config.yaml') as con:
        config = yaml.safe_load(con)
    return config


# Search State ID
def find_state_id(api):
    """Find state id given a state name"""
    config = get_config_param()

    all_states = api.get_states()['states']
    for state in all_states:
        if state['state_name'] == config['state']:
            return state['state_id']

# find_state_id(api=cowin)


# Check valid district
def check_valid_district(api):
    """Find whether a district name is valid and returns id"""
    config = get_config_param()
    state_id = find_state_id(api=api)
    districts = api.get_districts(state_id=state_id)['districts']
    found = False
    found_id = 0
    for district in districts:
        if district['district_name'] == config['district']:
            found = True
            found_id = district['district_id']
    return found, found_id

# check_valid_district(api=cowin)


# Get centers available by district name
def check_avail_district(api, check_date):
    """Get centers available by district name"""
    config = get_config_param()
    dist_found, dist_id = check_valid_district(api=api,
                                               state_name=config['state'],
                                               district_name=config['district'])
    if dist_found is False:
        print("Incorrect state name or district name")
        return None
    else:
        available_centers = api.get_availability_by_district(str(dist_id),
                                                             check_date,
                                                             config['age'])
        return available_centers

# check_avail_district(api=cowin, check_date="25-05-2021")


# Get centers available by pincode
def check_avail_pincode(api, check_date):
    """Get center availability by pincode"""
    config = get_config_param()
    try:
        available_centers_by_pin = api.get_availability_by_pincode(config['pincode'],
                                                                   check_date,
                                                                   config['age'])
    except:
        available_centers_by_pin = {'centers': []}
    return available_centers_by_pin

# check_avail_pincode(api=cowin, check_date="25-05-2021")


# Perform a search for specific days
def search(api, start, days_to_check):
    """Search a set a of days for availability"""
    config = get_config_param()
    start_dt = datetime.datetime.strptime(start, "%d-%m-%Y")
    print("-----------------------------------------")
    for day in range(0, days_to_check+1):
        time_delta = datetime.timedelta(day)
        new_dt = start_dt + time_delta
        new_date = new_dt.strftime("%d-%m-%Y")

        print("Checking for:", new_date)
        response = check_avail_pincode(api=api,
                                       check_date=new_date)

        if len(response['centers']) > 0:
            num_centers = len(response['centers'])
            for j in range(num_centers):
                center_name = response['centers'][j]['name']
                center_available_capacity = response['centers'][j]['sessions'][0]['available_capacity_dose1']
                if center_available_capacity > 0:
                    print(f"Center found at {center_name} with available capacity {center_available_capacity}")
                    return True
    return False

#------------------------------------------
# Main function
#------------------------------------------
# Handle exits safely
def signal_handler(signal, frame):
    global exit_now
    print("Exiting program")
    exit_now = True

def main(argv):
    """Start a search from specified date for the next n days"""
    start_date = ""
    days = 0
    signal.signal(signal.SIGINT, signal_handler)
    global exit_now
    exit_now = False

    # Check parameters
    try:
        opts, args = getopt.getopt(argv, "d:n:", ["date=", "numdays="])
    except getopt.GetoptError:
        print("Use the following format:")
        print("python cowin_check.py -d 17-05-2021 -n 3")
        sys.exit()
    
    for opt, arg in opts:
        if opt in ("-d", "--date"):
            start_date = arg
        if opt in ("-n", "--numdays"):
            days = int(arg)
    
    # Initial display message
    print("You have specified: ")
    print("Starting date:", start_date)
    print("Number of days to check:", days+1)

    # Start the check
    cowin = CoWinAPI()
    config = get_config_param()
    delay = config['interval']
    starttime = time.time()
    response = False
    while response is False:
        response = search(api=cowin, start=start_date, days_to_check=days)
        # Wait for 15 seconds
        if not response:
            time.sleep(delay - ((time.time() - starttime) % delay))
        if exit_now:
            break
    if response is True:
        print("-------------------")
        print("Book immediately!!!")
        print("-------------------")
        playsound.playsound("audio/Tornado_Siren_II-Delilah-747233690.mp3")
    return None

if __name__ == "__main__":
    main(sys.argv[1:])
