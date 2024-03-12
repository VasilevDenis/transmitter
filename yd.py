import json
import requests


class YaUploader:
    def __init__(self, window: object) -> None:
        self.window = window
        self.access_token = self._get_access_token()
        self.url = 'https://cloud-api.yandex.net/'

    def create_folder(self, folder_name: str) -> None:
        request_url = f'{self.url}v1/disk/resources'
        headers = self._get_headers()
        params = {'path': folder_name}
        response = requests.put(url=request_url, headers=headers, params=params)
        response.raise_for_status()
        if response.status_code == 201:
            self.window.show_message(f'Folder {folder_name} created on Yandex.Disk')

    def upload_file_to_disk(self, disk_file_path: str, image: str) -> None:
        file_name = disk_file_path.split('/')[1]
        print(type(image))
        self.window.show_message(f'Uploading {file_name} to YD')
        href_response = self._get_upload_link(disk_file_path=disk_file_path)
        href = href_response.get('href', '')
        response = requests.put(url=href, data=image)
        response.raise_for_status()
        if response.status_code == 201:
            self.window.show_message(f'Photo {file_name} copied to disk.')
            self.window.update_progress()

    def _get_headers(self) -> dict:
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.access_token}'}

    def _get_upload_link(self, disk_file_path: str) -> object:
        upload_url = f'{self.url}v1/disk/resources/upload'
        headers = self._get_headers()
        params = {'path': disk_file_path, 'overwrite': 'true'}
        href_response = requests.get(upload_url, headers=headers, params=params)
        return href_response.json()
    
    def _get_access_token(self) -> str:
        with open('yandex_disk_settings.json') as file:
            return json.load(file)['access_token']

