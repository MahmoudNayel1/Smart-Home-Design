import csv
import math

import pandas as pd

class VirtualHouse:
    def __init__(self, outdoor_temp, outdoor_humidity , indoor_temp, indoor_humidity):
        self.indoor_temp = indoor_temp # Initial indoor temperature
        self.indoor_humidity = indoor_humidity  # Initial indoor humidity
        self.outdoor_temp = outdoor_temp
        self.outdoor_humidity = outdoor_humidity
        self.mechanical_ventilation = False  # Mechanical ventilation status
        self.storage_heaters_count = 0  # Number of times storage heaters used today
        self.indoor_temp_history = []  # List to store indoor temperature history
        self.indoor_humidity_history = []  # List to store indoor humidity history
        self.time=[]

    def update_environment(self):
        # Update indoor temperature and humidity based on outdoor conditions and management options
        if self.mechanical_ventilation:
            # If mechanical ventilation is on, indoor conditions become equal to outdoor conditions
            self.indoor_temp = self.outdoor_temp
            self.indoor_humidity = self.outdoor_humidity
        else:
            # Otherwise, indoor conditions gradually return to outdoor conditions
            self.indoor_temp += (self.outdoor_temp - self.indoor_temp) / 15
            self.indoor_humidity += (self.outdoor_humidity - self.indoor_humidity) / 15

    def apply_storage_heaters(self):
        # Apply storage heaters to increase indoor temperature
        if self.storage_heaters_count < 2:
            self.indoor_temp += 0.5
            self.storage_heaters_count += 1

    def toggle_mechanical_ventilation(self):
        # Toggle mechanical ventilation
        self.mechanical_ventilation = not self.mechanical_ventilation




# Example usage:
def main():
    # Read data from the CSV file
    data = pd.read_csv("windows_open.csv")
    indoor_temperature = data["Indoor_temperature_room"]
    indoor_humidity = data["humidity"]
    outdoor_temperature = data["outside temp"]
    outdoor_humidity = data["Outdoor_relative_humidity_Sensor"]



    # Instantiate virtual house with initial outdoor conditions
    virtual_house = VirtualHouse(outdoor_temperature[0], outdoor_humidity[0] , indoor_temperature[0] , indoor_humidity[0] )

    # Simulate time passage using data from the CSV
    for i in range(len(data)):
        # Extract indoor temperature, outdoor temperature, indoor humidity, and outdoor humidity from the current row
        indoor_temp = indoor_temperature[i]
        outdoor_temp = outdoor_temperature [i]
        indoor_humid = indoor_humidity[i]
        outdoor_humid = outdoor_humidity [i]

        # Update indoor temperature and humidity in the virtual house
        virtual_house.indoor_temp = indoor_temp
        virtual_house.indoor_humidity = indoor_humid
        virtual_house.outdoor_temp = outdoor_temp
        virtual_house.outdoor_humidity = outdoor_humid
        virtual_house.indoor_temp_history.append(indoor_temp)
        virtual_house.indoor_humidity_history.append(indoor_humid)
        hours = math.floor((i*15)/60)
        min = (i*15)%60
        time = f"{hours} : {min}"
        virtual_house.time.append(time)

    # Output results to CSV
    with open('indoor_environment_history.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Time' , 'Indoor Temperature', 'Indoor Humidity'])
        for tim , temp, humidity in zip(virtual_house.time , virtual_house.indoor_temp_history, virtual_house.indoor_humidity_history):
            writer.writerow([tim , temp, humidity])

if __name__ == "__main__":
    main()