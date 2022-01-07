import requests

def getLatLng_Geocode(dataList):
    address = str(dataList[2][1])+"+"+dataList[2][0]+",+"+dataList[3]+",+"+dataList[4]+",+"+dataList[5]
    requestURL = 'https://maps.googleapis.com/maps/api/geocode/json?address='+address

    response = requests.get(requestURL)
    print(response)
    resp_json_payload = response.json()

    latitude = resp_json_payload['results'][0]['geometry']['location']['lat']
    longitude = resp_json_payload['results'][0]['geometry']['location']['lng']
    coord = [latitude,longitude]
    return coord


