from geopy.geocoders import Nominatim
from geopy.distance import distance
from math import ceil
def calculate_distance(location1, location2):
    geolocator=Nominatim(user_agent='distance_calculator')
    location1=geolocator.geocode(location1)
    location2=geolocator.geocode(location2)
    return (distance((location1.latitude,location1.longitude),(location2.latitude,location2.longitude)).meters)/1000
    
    
print(calculate_distance("delhi","shillong"))