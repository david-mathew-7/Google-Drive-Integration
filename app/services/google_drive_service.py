from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaIoBaseUpload
import io
from app.utils.credentials_helper import get_credentials_from_dict


def list_files(credentials_dict):
    """
    List files from the user's Google Drive.
    """
    credentials = get_credentials_from_dict(credentials_dict)
    service = build('drive', 'v3', credentials=credentials)

    results = service.files().list(pageSize=10,
                                   fields="nextPageToken, files(id, name, mimeType, modifiedTime)").execute()
    return results.get('files', [])


def upload_file(credentials_dict, file_content, file_name, folder_id=None):
    credentials = get_credentials_from_dict(credentials_dict)
    service = build('drive', 'v3', credentials=credentials)

    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaIoBaseUpload(io.BytesIO(file_content), mimetype='application/octet-stream')

    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    return file


def download_file(credentials_dict, file_id, destination_path):
    """
    Download a file from the user's Google Drive.
    """
    credentials = get_credentials_from_dict(credentials_dict)

    service = build('drive', 'v3', credentials=credentials)

    request = service.files().get_media(fileId=file_id)
    with open(destination_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
    return destination_path


def delete_file(credentials_dict, file_id):
    """
    Delete a file from the user's Google Drive.
    """

    credentials = get_credentials_from_dict(credentials_dict)

    service = build('drive', 'v3', credentials=credentials)

    service.files().delete(fileId=file_id).execute()


def get_file_metadata(credentials_dict, file_id):
    """
    Get metadata of a file from Google Drive.
    """
    credentials = get_credentials_from_dict(credentials_dict)
    service = build('drive', 'v3', credentials=credentials)
    metadata = service.files().get(fileId=file_id, fields="id, name, mimeType").execute()
    return metadata
