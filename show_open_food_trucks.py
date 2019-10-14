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

class FoodTrucksCollection:
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

class UserSession:
    """ """
    def __init__(self, open_foodtrucks, num_outputs):
        self.open_foodtrucks = open_foodtrucks
        self.num_outputs = num_outputs

    def get_input(self):
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
    
    def process_output(self):
        """ Based on user's input, calls print_output with  
        filtered_data sliced on specific num_outputs."""
        if not self.open_foodtrucks:
            print("No food trucks found open.")
         
        while self.open_foodtrucks:
            print(f"\nShowing {self.num_outputs} results...")
            print("Name, Location")
            sliced_open_foodtrucks = self.open_foodtrucks[:self.num_outputs]
            sorted_foodtrucks = sorted(sliced_open_foodtrucks, key=lambda food_truck: food_truck.name)
            print(f"\nShowing results...")
            print("Name, Location")
            for food_truck in sorted_foodtrucks:
                print(f"{food_truck.name}, {food_truck.address}")
            user_input = self.get_input()
            if user_input == "next":
                self.open_foodtrucks = self.open_foodtrucks[self.num_outputs:]
                continue
            else:
                break


def main():
    URL = "http://data.sfgov.org/resource/bbb8-hzi6.json"
    json_response = JsonResponse(URL).get_data()
    all_foodtrucks = FoodTrucksCollection(json_response)
    open_foodtrucks = all_foodtrucks.open_now()
    begin_session = UserSession(open_foodtrucks, 10).process_output()

if __name__ == "__main__":
    main()
