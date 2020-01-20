# weather-challenge
 Weather information from Dark Sky API

INSTRUCTION TO USE:

1. Install libriries: pip install -r requirements.txt

2. Register in https://darksky.net/dev and put your "Secret Key" here:
API_KEY = 'ab7ddfe913d5af4489a00847a7461ecb'

3. Put True - If you want to get the current weather information for 5 cities and save them into the “weather” table:
   Put False - If you want to only see weather information (max, min, avg temp) for specified city_id and export weather information into CSV that:
   get_info_from_API = False # True, False

4. Specify a city (1-NewYork, 2-London, 3-Moscow, 4-Tashkent, 5-Sydney) as parameter:
   city_id_parameter = 1

5. "fname" parameter that is exported into a csv file to the path specified as a parameter:
   fname = 'fname.csv'
