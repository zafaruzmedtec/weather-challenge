import sqlite3
from helper import Cities, Weather_info
from darksky.api import DarkSky, DarkSkyAsync
from darksky.types import languages, units, weather
import time
import csv

""" Register in https://darksky.net/dev and put your "Secret Key" here """
API_KEY = 'ab7ddfe913d5af4489a00847a7461ecb'

""" Put True - If you want to get the current weather information for 5 cities 
    and save them into the “weather” table
    Put False - If you want to only see weather information (max, min, avg temp) 
    for specified city_id and export weather information into CSV that """
get_info_from_API = False # True, False

""" Specify a city (1-NewYork, 2-London, 3-Moscow, 4-Tashkent, 5-Sydney) as parameter """
city_id_parameter = 1

""" "fname" parameter that is exported into a csv file to the path specified as a parameter"""
fname = 'fname.csv'

# Synchronous way with API
darksky = DarkSky(API_KEY)
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Creates cities table
c.execute("""CREATE TABLE IF NOT EXISTS cities (
            city_id INTEGER PRIMARY KEY,
            name TEXT,
            lat REAL,
            lon REAL
            )""")

# Creates weather table
c.execute("""CREATE TABLE IF NOT EXISTS weather (
            city_id INTEGER,
            time TEXT,
            summary TEXT,
            windSpeed REAL,
            temperature REAL,
            uvIndex INTEGER,
            visibility REAL,
            FOREIGN KEY (city_id) REFERENCES cities (city_id) 
            )""")

def insert_city(city):
    """Inserts city information into the cities table"""
    with conn:
        c.execute("INSERT OR IGNORE INTO cities VALUES (:city_id, :name, :lat, :lon)",
                  {'city_id': city.city_id,
                   'name': city.name,
                   'lat': city.lat,
                   'lon': city.lon})

def insert_weather(weather, city_id):
    """Inserts weather information into the weather table"""
    with conn:
        c.execute("INSERT INTO weather VALUES (:city_id, :time, :summary, :windSpeed, :temperature, :uvIndex, :visibility)",
                  {'city_id': city_id,
                   'time': weather.currently.time,
                   'summary': weather.currently.summary,
                   'windSpeed': weather.currently.wind_speed,
                   'temperature': weather.currently.temperature,
                   'uvIndex': weather.currently.uv_index,
                   'visibility': weather.currently.visibility})

# Latitude and Longitude informations of 5 cities were received using https://www.latlong.net/
NewYork_city = Cities(1, 'New York', 40.712776, -74.005974)
London_city = Cities(2, 'London', 51.507351, -0.127758)
Moscow_city = Cities(3, 'Moscow', 55.755825, 37.617298)
Tashkent_city = Cities(4, 'Tashkent', 41.299496, 69.240074)
Sydney_city = Cities(5, 'Sydney', -33.868820, 151.209290)

# Inserts all cities into the "cities" table
cities = [NewYork_city, London_city, Moscow_city, Tashkent_city, Sydney_city]
for i in range(len(cities)):
    insert_city(cities[i])

# Saves weather information into weather table for a specified cities, if data differs >=1 min
starttime = time.time()
while get_info_from_API:
    for i in range(len(cities)):
        city_weather = darksky.get_forecast(cities[i].lat, cities[i].lon, extend=False, lang=languages.ENGLISH,
                                            units=units.AUTO, exclude=[], timezone=None)
        #city_weather_copy = copy.deepcopy(city_weather)
        c.execute("""SELECT * FROM weather WHERE city_id=:city_id ORDER BY time DESC LIMIT 1""", {'city_id': i + 1})

        selected_data = c.fetchall()
        current_weather = Weather_info.get_weather_info_tuple(city_weather)
        if selected_data == []:
            insert_weather(city_weather, i + 1)
            print("Current weather information of {} was saved first time into weather table ...".format(city_weather.timezone))
        elif selected_data[0][2:] != current_weather:
            insert_weather(city_weather, i + 1)
            print("Current weather information of {} was saved into weather table ...".format(city_weather.timezone))
        else:
            print('Current weather information of {} was not saved ...'.format(city_weather.timezone))
    print('=> 1 minut ...')
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))


# Show weather information table (min, max, average temperature) for the last 10 mins
c.execute("""SELECT min(temperature) FROM weather WHERE city_id=:city_id AND time >= time(datetime('now', '-10 minutes'))""", {'city_id': city_id_parameter})
min_temperature = c.fetchall()
c.execute("""SELECT max(temperature) FROM weather WHERE city_id=:city_id AND time >= time(datetime('now', '-10 minutes'))""", {'city_id': city_id_parameter})
max_temperature = c.fetchall()
c.execute("""SELECT avg(temperature) FROM weather WHERE city_id=:city_id AND time >= time(datetime('now', '-10 minutes'))""", {'city_id': city_id_parameter})
avg_temperature = c.fetchall()

print('Minimum temperature of {} city is {} for the last 10 minutes!'.format(cities[city_id_parameter].name, min_temperature[0][0]))
print('Maximum temperature of {} city is {} for the last 10 minutes!'.format(cities[city_id_parameter].name, max_temperature[0][0]))
print('Average temperature of {} city is {} for the last 10 minutes!'.format(cities[city_id_parameter].name, round(avg_temperature[0][0],2)))


# Export all data into CSV file
c.execute("SELECT * FROM weather")
export_data = c.fetchall()

with open(fname,'w', newline='') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['city_id','time', 'summary', 'windSpeed', 'temperature', 'uvIndex', 'visibility'])
    for row in export_data:
        csv_out.writerow(row)
print('All data exported into a fname.csv file ...')

conn.commit()
conn.close()