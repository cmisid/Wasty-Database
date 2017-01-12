import json
import requests
from urllib.request import urlopen
from xml.dom import minidom


def request_http(url, rep=False):
    ''' Envoyez une requête et décoder les octets reçus. '''
    if rep is False:
        with urlopen(url) as response:
            return response.read().decode('utf-8')
    # Possibilité de réessayer si la requête n'a pas fonctionné
    else:
        response = None
        while response is None:
            try:
                with urlopen(url) as response:
                    return response.read().decode('utf-8')
            except:
                response = None
        

def geocoder(address):
    '''
    Geocoder une adresse en (latitude, longitude) grâce à
    l'API de Nominatim.
    '''
    base = 'http://nominatim.openstreetmap.org/search?' \
           'format=json&polygon_geojson=1&q='
    url = base + str(address[0]) + str(address[1]) + str(address[2]) + str(address[3])
    response = request_http(url)
    try:
        address = json.loads(response)[0]
        latitude = float(address['lat'])
        longitude = float(address['lon'])
        return (latitude, longitude)
    except:
        return (0,0)
        
#         
# def geocoder_inverse(adresse):
# 	sensor = 'true'
# 	base = "http://maps.googleapis.com/maps/api/geocode/json?"
# 	params = "latlng={lat},{lon}&sensor={sen}".format(lat=adresse[0],lon=adresse[1],sen=sensor)
# 	url = "{base}{params}".format(base=base, params=params)
# 	response = requests.get(url)
# 	return response.json()['results'][0]['formatted_address']
	
def geocoder_reverse(address):
	'''
    Geocoder en inversant une adresse en (latitude, longitude) grâce à
    l'API de Nominatim.
    '''
	base = 'http://nominatim.openstreetmap.org/reverse?' \
           '?format=xml&lat='
	url = base + str(address[0]) + '&lon=' + str(address[1])
	response = request_http(url)
	try:
		xmldoc = minidom.parseString(response)
		obs_values1 = xmldoc.getElementsByTagName('house_number')
		house_number = obs_values1[0].firstChild.nodeValue
		obs_values2 = xmldoc.getElementsByTagName('road')
		road = obs_values2[0].firstChild.nodeValue
		obs_values3 = xmldoc.getElementsByTagName('postcode')
		postcode = obs_values3[0].firstChild.nodeValue
		obs_values4 = xmldoc.getElementsByTagName('city')
		city = obs_values4[0].firstChild.nodeValue
		return (house_number,road,postcode,city)
	except:
		return 'ERROR'
		
		
#print(geocoder_reverse([43.5542267,1.4666994]))
#print(geocoder(("6"," chemin des Sauges"," 31400"," Toulouse")))



