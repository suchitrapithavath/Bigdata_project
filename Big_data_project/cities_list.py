import requests
import json
my_city = []
with open('city.txt') as json_file:  # txt filw which has all the cities name accross the world
    data = json.load(json_file)# converting it to json file
    for p in data['cities']:# getting city attribute
        my_city.append(p['city'])# append the city name in my_city name

print(len(my_city))


for i in my_city:
    url = 'https://www.numbeo.com/api/indices?api_key=ycpmuzwqm08144&query='+i
    r = requests.get(url, allow_redirects=True)# requesting to numbeo.com to get the indices of the city
    open('data.txt', 'ab').write(r.content)
    open('data.txt', 'a').write(",")#writing it to file
print("done")
