
class Cities:
    """Cities class - city name, latitude, longitude"""

    def __init__(self, city_id, name, lat, lon):
        self.city_id = city_id
        self.name = name
        self.lat = lat
        self.lon = lon


class Weather_info:
    """Make weather info from API for comparing with table"""

    def get_weather_info_tuple(self):
        return tuple(list([self.currently.summary,
              self.currently.wind_speed,
              self.currently.temperature,
              self.currently.uv_index,
              self.currently.visibility]))
