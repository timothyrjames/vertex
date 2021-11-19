import base64
import fileapp
import flask
import logging
import urllib

from fileobjects import DisplayInfo
from fileobjects import UploadedFile


app = flask.Flask(__name__)


_BUCKET_NAME = 'cs1520-image-uploads'


@app.route('/')
def root():
    di = DisplayInfo('Taco or Dog?')
    return show_page('index.html', di)


@app.route('/upload', methods=['POST'])
def upload():
    di = DisplayInfo('Taco or Dog?')

    token = None
    if 'token' in flask.request.form:
        token = flask.request.form['token']
    if not token:
        token = 'ya29.a0ARrdaM9HKaOui9OGvty9bKoBGmd3TcOdg96vPEIgVH0kcJW6BtmuNfy4xV0OZvgHvWq_afNrwSQ8cZw0zCpuNOfrE-n7vXsVgV3burryPtCrkHIrEyzyIPwwY9GeXwLBnYQrCRNuw6tBA96S5YxRlME4A-kJPrfukcyfePwHZqRakH66ibRs5QTDuuTnaI8xSQUar0xB5eGYsEicaABWiKJXPT08lDBRD6gfzuleiSrwMQJEbaobG7XF082nWe-p4KXvcEY'

    uploaded_file = flask.request.files.get('file')

    if not uploaded_file:
        di.add_error('No file uploaded.')

    filename = flask.request.form.get('filename')

    if not filename:
        di.add_error('No file name provided.')

    encoded_content = base64.encodebytes(uploaded_file.read()).decode('utf-8')

    if len(encoded_content) > 500000:
        di.add_error('Uploaded image is too large.')

    if di.errors:
        return show_page('index.html', di)

    fileapp.save_file(filename, encoded_content)

    return flask.redirect('/showfile?token=' + urllib.parse.quote_plus(token) + '&name=' + urllib.parse.quote_plus(filename))


@app.route('/showfile')
def showfile():
    filename = flask.request.args['name']
    token = flask.request.args['token']
    di = fileapp.get_uploaded_file_display(filename, token)
    return show_page('showfile.html', di)
    

def show_page(filename, displayinfo):
    return flask.render_template(filename, display=displayinfo)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
