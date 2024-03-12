import requests
import time
import json


class VK:
    def __init__(self, window: object) -> None:
        self.window = window
        self.params = self._get_settings()
        self.base_url = 'https://api.vk.com/method/'

    def photos_get(self, owner_id: str, album_id: str) -> dict:
        method = 'photos.get'
        params = {'owner_id': owner_id,
                  'album_id': album_id,
                  'extended': '1',
                  'photo_sizes': '0'}
        response = self._get(method, params)
        items = response['response']['items']
        photo_items = {}
        for item in items:
            likes_count = item['likes']['count']
            if likes_count in photo_items.keys():
                likes_count = likes_count + str(time.time_ns())
            max_size_photo = self._get_max_size_photo(item)
            photo_items[likes_count] = {'url': max_size_photo['url'], 'size': max_size_photo['type']}
        photo_items_count = len(photo_items.keys())
        self.window.show_message(f'Found photos: {photo_items_count}')
        self.window.photo_items_count = photo_items_count
        return photo_items

    @staticmethod
    def _get_max_size_photo(item: dict) -> str:
        types = 'wzurqpoxms'
        for sym in types:
            for size_item in item['sizes']:
                if sym == size_item['type']:
                    return size_item

    def _get(self, method, params: dict = None) -> object:
        if params is not None:
            params.update(self.params)
        else:
            params = self.params
        url = self.base_url + method
        request_obj = requests.get(url=url, params=params)
        time.sleep(0.3)
        return request_obj.json()

    def _get_settings(self) -> object:
        with open('vk_settings.json') as file:
            return json.load(file)
