from google.cloud import datastore
from fileobjects import UploadedFile

_FILE_ENTITY = 'File'


def save_uploaded_file(uploaded_file_object):
    """Save the uploaded file information to the datastore."""
    client = _get_client()
    key = client.key(_FILE_ENTITY, uploaded_file_object.filename)
    entity = datastore.Entity(key, exclude_from_indexes=['content'])
    entity['content'] = uploaded_file_object.content
    client.put(entity)


def get_uploaded_file_content(filename):
    """Retrieve the uploaded file information from the datastore."""
    client = _get_client()
    key = client.key(_FILE_ENTITY, filename)
    entity = client.get(key)
    if entity:
        return entity['content']
    return None


def _get_client():
    """Build a datastore client."""

    return datastore.Client()

