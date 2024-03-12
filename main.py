from tkinter import ttk
import tkinter as tk
import transmitter
import threading


class MainWindow:
    def __init__(self) -> None:
        self.lock = False
        self.copied = 0
        self.count_for_progress = 0
        self.photo_items_count = int()
        self.root = tk.Tk()
        self.root.title('Photo from VK to YD')
        self.row = 0

        self.id_label = ttk.Label(self.root, text='User ID:')
        self.id_label.grid(column=0, row=self._next_row(), columnspan=1, padx=10, pady=10)
        self.owner_id_var = tk.StringVar()
        self.entry_owner_id_var = ttk.Entry(self.root, textvariable=self.owner_id_var)
        self.entry_owner_id_var.grid(column=1, row=self.row, columnspan=1, padx=10, pady=10)

        self.photo_count_label = ttk.Label(self.root, text='Number of photos:')
        self.photo_count_label.grid(column=0, row=self._next_row(), columnspan=1, padx=10, pady=10)
        self.photo_count_var = tk.StringVar()
        self.photo_count_entry = ttk.Entry(self.root, textvariable=self.photo_count_var)
        self.photo_count_entry.grid(column=1, row=self.row, columnspan=1, padx=10, pady=10)

        self.album_label = ttk.Label(self.root, text='Album:')
        self.album_label.grid(column=0, row=self._next_row(), columnspan=1, padx=10, pady=10)
        self.album_var = tk.StringVar()
        self.album_radio_prof = ttk.Radiobutton(self.root, text='Profile', variable=self.album_var,
                                                value='profile')
        self.album_radio_prof.grid(column=1, row=self.row, columnspan=1, padx=10, pady=10, sticky='W')
        self.album_var.set('profile')
        self.album_radio_wall = ttk.Radiobutton(self.root, text='Wall', variable=self.album_var, value='wall')
        self.album_radio_wall.grid(column=1, row=self._next_row(), columnspan=1, padx=10, pady=10, sticky='W')
        self.album_radio_saved = ttk.Radiobutton(self.root,
                                                 text='Saved', variable=self.album_var, value='saved')
        self.album_radio_saved.grid(column=1, row=self._next_row(), columnspan=1, padx=10, pady=10, sticky='W')

        self.message_label = ttk.Label(self.root, text='Press start to copy')
        self.message_label.grid(column=0, row=self._next_row(), columnspan=2, padx=10, pady=10)

        # progressbar
        self.pb = ttk.Progressbar(
            self.root,
            orient='horizontal',
            mode='determinate',
            length=280
        )
        # place the progressbar
        self.pb.grid(column=0, row=self._next_row(), columnspan=2, padx=10, pady=20)

        # label
        self.value_label = ttk.Label(self.root, text=self.update_progress_label())
        self.value_label.grid(column=0, row=self._next_row(), columnspan=2)

        # start button
        self.start_button = ttk.Button(
            self.root,
            text='Start',
            command=self.start
        )
        self.start_button.grid(column=0, row=self._next_row(), columnspan=2, padx=10, pady=10)
        self.tr = transmitter.Transmitter(self)
        self.root.eval('tk::PlaceWindow . center')

    def _next_row(self) -> int:
        self.row += 1
        return self.row

    def update_progress_label(self) -> None:
        return f"Progress: {self.pb['value']}%"

    def start(self) -> None:
        if self.lock:
            self.show_message('Process is already executing!')
            return
        self.lock = True
        self.pb['value'] = 0
        self.value_label['text'] = self.update_progress_label()
        self.lock = True
        threading.Thread(target=self.tread).start()
        self.show_message('Error!')
        self.stop()

    def tread(self) -> None:
        owner_id = self.owner_id_var.get()
        if not owner_id.isdigit():
            self.show_message('Input ID!')
            return
        photo_count = self.photo_count_var.get()
        if photo_count == '':
            photo_count = '5'
        self.count_for_progress = int(photo_count)
        self.copied = 0
        if not photo_count.isdigit():
            self.show_message('Input count of photo!')
            return
        album = self.album_var.get()
        self.tr.send_from_vk_to_yandex_disk(owner_id, photo_count, album)


    def update_progress(self) -> None:
        self.copied += 1
        if self.copied == self.count_for_progress:
            self.pb['value'] = 100
            self.value_label['text'] = self.update_progress_label()
            return
        self.pb['value'] = int(100 / self.count_for_progress * self.copied)
        self.value_label['text'] = self.update_progress_label()

    def stop(self) -> None:
        self.pb.stop()
        self.count_for_progress = 0
        self.copied = 0
        self.value_label['text'] = self.update_progress_label()

    def show_message(self, message) -> None:
        self.message_label['text'] = message


if __name__ == '__main__':
    main_window = MainWindow()
    main_window.root.mainloop()
