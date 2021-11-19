import filedatastorage
import logging

from fileobjects import DisplayInfo
from fileobjects import UploadedFile


def save_file(filename, content):
    uploaded_file = UploadedFile(filename, content)
    filedatastorage.save_uploaded_file(uploaded_file)


def get_uploaded_file_display(filename, token):
    di = DisplayInfo('Dog or Taco?')
    di.p['name'] = filename
    di.p['token'] = token

    if filename:
        uploaded_file_content = filedatastorage.get_uploaded_file_content(filename)
        if uploaded_file_content:
            di.p['content'] = uploaded_file_content
        else:
            di.add_error('No file was found for filename "%s"' % (filename))
    else:
        di.add_error('No filename provided.')

    return di
