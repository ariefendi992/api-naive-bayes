import requests


def getukt(x):
    url = 'http://127.0.0.1:5000/api/v1/beasiswa-ukt'
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0OTM3ODcyMCwianRpIjoiODNjNWEwZTAtY2I3Yi00OWU1LWJkNTQtNGNiNjRmYzQ3NjA1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6NywibmltIjoiMTgwMjQwMTQwNzciLCJuYW1hIjoiSXNoYWsgTWFyYXNhYmVzc3kifSwibmJmIjoxNjQ5Mzc4NzIwLCJleHAiOjE2NDk5ODM1MjB9.loc1P90-sw-zhVqL5lI_VUwySQb_vtsHwQOgNlMP-X4'
    }
    req = requests.get(url + f'?page={x}', headers=headers)
    res = req
    return res.json()


data = getukt(2)


def getPages():
    url = 'http://127.0.0.1:5000/api/v1/beasiswa-ukt'
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0OTM3ODcyMCwianRpIjoiODNjNWEwZTAtY2I3Yi00OWU1LWJkNTQtNGNiNjRmYzQ3NjA1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6NywibmltIjoiMTgwMjQwMTQwNzciLCJuYW1hIjoiSXNoYWsgTWFyYXNhYmVzc3kifSwibmJmIjoxNjQ5Mzc4NzIwLCJleHAiOjE2NDk5ODM1MjB9.loc1P90-sw-zhVqL5lI_VUwySQb_vtsHwQOgNlMP-X4'
    }
    req = requests.get(url, headers=headers)

    return req.json()


dataPage = getPages().get('meta').get('pages')
print(dataPage)

for data in range(0, dataPage):
    print('%d: helo' % data)
