import requests
import json

# USER INPUTS
#TODO Consider adding different fuel efficiency formats (MPG etc.)
def get_fuel_efficiency():
    """
    User inputs fuel efficiency of their vehicle.
    Validates user input of float. 
    """

    while True:
        try:
            fuel_efficiency = float(input('Enter fuel efficiency L/100km: '))
        except ValueError:
            print('Please enter a number.')
        else:
            break

    return fuel_efficiency          


def get_fuel_price():
    """
    User inputs fuel price per Litre in dollars.
    Validates user input of float.
    """

    while True:
        try:
            fuel_price = float(input('Enter fuel price $/L: '))
        except ValueError:
            print('Please enter dollar amount with decimal')
        else:
            break

    return fuel_price


# API Functions
def create_API_url(api_key):
    
    #Origin
    origin = str(input('Starting address: '))
    origin.replace(' ','+') # Format for URL
    
    #Destination
    destination = str(input('Destination: '))

    url = ("https://maps.googleapis.com/maps/api/directions/json?origin=" 
           + origin + "&destination=" + destination + "&key=" + api_key)

    
    return url 

def get_request(url):

    retries = 1

    for n in range(retries):
        try:
            response = requests.request("GET", url)
            response.raise_for_status()
        except Exception as error:
            print(f'{error}')
            print(f'Attempt {n} of {retries}')

    return response


def get_driving_distance(response):
    """
    Processes json response to get driving distance in meters.
    """

    response = response.text #Converts to string format
    data = json.loads(response) #Converts string to dict

    #print(data)
    #Access nested dictionary and lists
    #TODO Implement this with recursive function?? Nope?
    
    routes_dict = data['routes'][0]                 #Type: dictionary
    legs_list = routes_dict['legs']                 #Type: List
    legs_summary_list = legs_list[0]                    #Type: List
    distance_dict = legs_summary_list['distance']  #Type: dictionary
    distance_meters = distance_dict['value']   #Type: dictionary
    return distance_meters

def get_driving_time(response):
    """
    Processes json response to get driving distance in meters.
    """

    response = response.text #Converts to string format
    data = json.loads(response) #Converts string to dict

    #Access nested dictionary and lists
    routes_dict = data['routes'][0]                 #Type: dictionary
    legs_list = routes_dict['legs']                 #Type: List
    legs_summary_list = legs_list[0]                    #Type: List
    duration_dict = legs_summary_list['duration']  #Type: dictionary
    time_seconds = duration_dict['value']   #Type: dictionary
    time_mins = round(time_seconds / 60)
    return time_mins

def convert_meters_to_km(distance_in_meters):

    meters_per_km = 1000
    distance_km = distance_in_meters/meters_per_km
    return distance_km

def calculate_fuel_cost(fuel_efficiency, fuel_price, driving_distance):
    """
    Calculates the fuel cost for the driving distance.
    Inputs [units]:
    fuel_efficiency [L/100km]
    fuel_price [$/L]
    driving_distance [km]
    Outputs:
    cost [$]
    """

    conversion_factor_for_fuel_efficiency = 1/100
    cost = (fuel_efficiency * fuel_price * driving_distance 
            * conversion_factor_for_fuel_efficiency)
    cost_rounded = round(cost, 2)

    return cost_rounded

def main():
    
    with open('GoogleMapsAPI_Key.txt') as file:
        api_key = file.read()
        
    url = create_API_url(api_key)
    print(url)

    response = get_request(url)
    print(response.raise_for_status())

    driving_distance_meters = get_driving_distance(response)
    driving_distance_km = convert_meters_to_km(driving_distance_meters)
    
    driving_time = get_driving_time(response)

    fuel_efficiency = get_fuel_efficiency()
    
    fuel_price = get_fuel_price()
    
    cost = calculate_fuel_cost(fuel_efficiency, fuel_price, driving_distance_km)

    print(f'The cost of this {driving_distance_km}km one-way trip is:')
    print(f'${cost} and {driving_time} mins')

    print(f'The cost of this {driving_distance_km*2}km round-trip is:')
    print(f'${cost*2} and {driving_time*2} mins')


    
    

if __name__ == "__main__":
    main()

