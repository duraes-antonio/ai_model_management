import io
import os.path
from typing import Generic, TypeVar, Optional

import google.oauth2 as goauth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from models.entity import Entity
from models.services.model_storage_service import ModelStorageService

T = TypeVar('T')


class GoogleDriveTokenManager:
    __scope__ = ['https://www.googleapis.com/auth/drive']
    __credentials_file_name__ = 'google_credentials.json'

    def load_credentials(self) -> Credentials:
        token_file_name = 'token.json'
        recovered_credentials = None

        if os.path.exists(token_file_name):
            recovered_credentials = Credentials.from_authorized_user_file(token_file_name)

        if not recovered_credentials:
            return self.__authenticate_with_file__(token_file_name)

        if recovered_credentials.valid and not recovered_credentials.expired:
            return recovered_credentials

        if recovered_credentials.expired and recovered_credentials.refresh_token:
            recovered_credentials.refresh(Request())
            return self.__save_credentials__(token_file_name, recovered_credentials)

        return self.__authenticate_with_file__(token_file_name)

    def __authenticate_with_file__(self, token_file_name: str) -> Credentials:
        flow = InstalledAppFlow.from_client_secrets_file(
            self.__credentials_file_name__, self.__scope__
        )
        credentials: goauth.credentials.Credentials = flow.run_local_server(port=0)
        return self.__save_credentials__(token_file_name, credentials)

    def __save_credentials__(self, filename: str, credentials: Credentials) -> Credentials:
        with open(filename, 'w') as token_file:
            token_file.write(credentials.to_json())

        return credentials


class GoogleDriveModelStorageService(ModelStorageService, Generic[T]):
    directory = 'models'

    def __init__(self):
        self.__credentials__ = GoogleDriveTokenManager().load_credentials()
        self.__service__ = build('drive', 'v3', credentials=self.__credentials__)

    def __create_folder__(self, name: str):
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        files = self.__service__.files()
        file = files.create(body=file_metadata, fields='id').execute()
        return file.download('id')

    def __get_metadata_by_id__(self, file_id: str) -> Optional[Entity]:
        files = self.__service__.files().get(fileId=file_id).execute()

        if not files:
            return None

        return Entity(files['name'], files['id'])

    def __search_folder__(self, name: str) -> str:
        files = self.__service__.files()
        folders_dict = files.list(
            q=f"name = '{name}' and mimeType='application/vnd.google-apps.folder'",
            fields="files(id, name)"
        ).execute()
        folders = folders_dict['files']
        return folders[0]['id'] if folders else None

    def __upload_file__(self, file_path: str, folder_id: str) -> str:
        file_metadata = {
            'name': 'photo.md',
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path, resumable=True)
        file = self.__service__.files().create(
            body=file_metadata, media_body=media, fields='id'
        ).execute()
        return file.download('id')

    def __download_file__(self, new_name: str, file_id: str):
        request = self.__service__.files().get_media(fileId=file_id)
        file_io = io.FileIO(new_name, mode='wb')
        downloader = MediaIoBaseDownload(file_io, request)
        done = False

        while not done:
            _, done = downloader.next_chunk()

    def save(self, model_file_path: str) -> None:
        folder_id = self.__search_folder__(self.directory)

        if not folder_id:
            folder_id = self.__create_folder__(self.directory)

        self.__upload_file__(model_file_path, folder_id)

    def download_last(self) -> Optional[Entity]:
        folder_id = self.__search_folder__(self.directory)

        if not folder_id:
            return None

        files_service = self.__service__.files()
        files_dict = files_service.list(
            q=f"'{folder_id}' in parents",
            orderBy="modifiedTime desc",
            fields="files(id, name)"
        ).execute()

        files = files_dict['files']

        if not files:
            return None

        self.__download_file__(files[0]['name'], files[0]['id'])

    def download(self, file_id: str) -> Optional[Entity]:
        file_metadata = self.__get_metadata_by_id__(file_id)
        self.__download_file__(file_metadata.name, file_metadata.id)
        return file_metadata
