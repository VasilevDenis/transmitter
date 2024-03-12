import time
import yd
import vk
import requests
import json


class Transmitter:
    def __init__(self, window):
        self.window = window

    def send_from_vk_to_yandex_disk(self, owner_id: str, photo_count: str, album_id='profile') -> None:
        vk_shell = vk.VK(self.window)
        yd_shell = yd.YaUploader(self.window)
        self.window.show_message('Connecting to VK')
        photo_dict = vk_shell.photos_get(owner_id, album_id)
        i = int(photo_count)
        for_json_list = []
        current_time = time.strftime(format('%H_%M_a%S'))
        folder_name_for_yd = f'Photo_{current_time}'
        yd_shell.create_folder(folder_name_for_yd)
        for name in photo_dict.keys():
            if i != 0:
                url = photo_dict[name]['url']
                size = photo_dict[name]['size']
                r = requests.get(url)
                if r.status_code == 200:
                    path_on_ya_disk = f'{folder_name_for_yd}/{name}.jpg'
                    yd_shell.upload_file_to_disk(path_on_ya_disk, r.content)
                    for_json_dict = {'file_name': path_on_ya_disk, 'size': size}
                    for_json_list.append(for_json_dict)
                    i -= 1
            else:
                break
        self.window.show_message('Transmission completed!')
        with open('log.json', 'w') as f:
            json.dump(fp=f, obj=for_json_list)
        self.window.lock = False



