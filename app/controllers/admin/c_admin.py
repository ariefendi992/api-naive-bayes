from flask import Blueprint, render_template, request
import requests

admin = Blueprint('admin', __name__, url_prefix='/admin',
                  template_folder='../../templates/admin/')


@admin.route('/', methods=['GET', 'POST'])
def adminDashboadr():
    return render_template('dashboard.html')


@admin.route('/kategori-fakultas', methods=['GET', 'POST'])
def kategoriF():
    url = 'https://api-beasiswa.herokuapp.com/api/v1/kampus/fakultas'
    r = requests.get(url).json()
    response = r.get('data')

    return render_template('fakultas.html', response=response)


@admin.route('/kategori-jurusan', methods=['GET', 'POST'])
def kategoriJ():
    url = 'https://api-beasiswa.herokuapp.com/api/v1/kampus/jurusan'
    req = requests.get(url).json()
    response = req.get('data')

    return render_template('jurusan.html', response=response)


@admin.route('/get-ukt', methods=['GET', 'POST'])
def getUkt():
    url = 'https://api-beasiswa.herokuapp.com/api/v1/beasiswa-ukt'
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0OTM3ODcyMCwianRpIjoiODNjNWEwZTAtY2I3Yi00OWU1LWJkNTQtNGNiNjRmYzQ3NjA1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6NywibmltIjoiMTgwMjQwMTQwNzciLCJuYW1hIjoiSXNoYWsgTWFyYXNhYmVzc3kifSwibmJmIjoxNjQ5Mzc4NzIwLCJleHAiOjE2NDk5ODM1MjB9.loc1P90-sw-zhVqL5lI_VUwySQb_vtsHwQOgNlMP-X4'
    }
    x = request.args.get('page')
    req = requests.get(url + f'?page={x}', headers=headers)

    if req.status_code == 200:
        response = req.json()
        return render_template('get-ukt.html', response=response)
    else:
        return req.json().get('msg')
