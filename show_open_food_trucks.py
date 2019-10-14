# Make sure to install requirements before running this program:
# > pip3 install -r requirements.txt

import requests
from datetime import datetime
import sys
import calendar


class FoodTruck:
    def __init__(self, json_data):
        self.day = json_data["dayofweekstr"]
        self.starthour = int(json_data["start24"][:2])
        self.startminute = int(json_data["start24"][3:])
        self.endhour = int(json_data["end24"][:2])
        self.endminute = int(json_data["end24"][3:])
        self.name = json_data["applicant"]
        self.address = json_data["location"]

    def open(self, now):
        """ Returns a boolean if a foodtruck is open now. 
        Here, now is a datetime object provided as input.
        """
        today = calendar.day_name[now.today().weekday()]
        time = now.now()

        if self.day == today:
            if time.hour > self.starthour and time.hour < self.endhour:
                return True
            elif time.hour == self.starthour and time.minute > self.startminute:
                return True
            elif time.hour == self.endhour and time.minute < self.endminute:
                return True
        return False

    
class JsonResponse:
    """ Uses URL provided to make object of json response."""
    def __init__(self, url):    
        self.url = url

    def get_data(self):
        """ Sends request to url and returns a json response"""
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                json_response = response.json()
                return json_response
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

class AllFoodTrucks:
    """ Array object with FoodTruck elements"""
    def __init__(self, json_data):
        """ Returns array of FoodTruck objects using json response """
        self.all_foodtrucks = [FoodTruck(food_truck) for food_truck in json_data]

    def open_now(self):
        """ Returns an array of food trucks objects that are open 
            at the time when user runs this program. 
            NOTE: Array does not change if time increases while the
            program is running. 
        """
        open_foodtrucks = []
        now = datetime
        today = calendar.day_name[now.today().weekday()]
        for food_truck in self.all_foodtrucks:
            if food_truck.open(now):
                open_foodtrucks.append(food_truck)
        return open_foodtrucks


def get_input():
    """ Asks for input from user and returns appropriate response """
    while True:
        user_response = input(
            "Please enter n for the remaining list of food trucks or q to exit: "
        )
        if user_response == "n":
            return "next"
        elif user_response == "q":
            print("Goodbye!")
            break
        else:
            print("Incorrect response. Please try again.")

def print_output(sliced_filtered_data):
    """ Sorts the Foodtruck objects provided by name and prints out the 
    respective name and location of Foodtruck. """

    ordered_open_food_trucks = sorted(
        sliced_filtered_data, key=lambda food_truck: food_truck.name
    )
    num_results = len(ordered_open_food_trucks)
    print(f"\nShowing {num_results} results...")
    print("Name, Location")
    for food_truck in ordered_open_food_trucks:
        print(f"{food_truck.name}, {food_truck.address}")

def process_output(open_foodtrucks, num_outputs):
    """ Based on user's input, calls print_output with  
    filtered_data sliced on specific num_outputs."""
    if not open_foodtrucks:
        print("No food trucks found open.")

    while  open_foodtrucks:
        if len(open_foodtrucks) >= num_outputs:
            print_output(open_foodtrucks[:num_outputs])
            user_input = get_input()
            if user_input == "next":
                open_foodtrucks = open_foodtrucks[num_outputs:]
        else:
            print_output(open_foodtrucks)
            open_foodtrucks = None
            print("\n\nThat's all we have. Now go eat something tasty!")



def main():
    URL = "http://data.sfgov.org/resource/bbb8-hzi6.json"
    json_response = JsonResponse(URL).get_data()
    all_foodtrucks = AllFoodTrucks(json_response)
    open_foodtrucks = all_foodtrucks.open_now()
    process_output(open_foodtrucks,10)

if __name__ == "__main__":
    main()
