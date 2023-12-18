"""
Class to watch the file and retrieve the recent updates in the file
"""
import os


class FileWatcher:
    def __init__(self, file_path):
        self.file_path = file_path
        self.last_read_index = None
        self.last_read_at = None
        self.file_cursor = None

    def get_logs(self, lines_to_read=None):
        # create a cursor
        if self.file_cursor is None:
            self.file_cursor = open(self.file_path, "r")

        if self.last_read_index is None:
            self.file_cursor.seek(0, 2)
            self.last_read_index = self.file_cursor.tell()

        current_index = self.last_read_index
        read_last_10 = False

        # find last 10 lines if reading for first time
        while lines_to_read != 0 and current_index != -1:
            read_last_10 = True
            self.file_cursor.seek(current_index)
            char = self.file_cursor.read(1)
            if char == '\n':
                lines_to_read -= 1
            current_index -= 1

        current_index += 1
        if not read_last_10 and current_index == 1:  # if the file was empty and now we're watching
            current_index -= 1

        # read the data
        self.file_cursor.seek(current_index)
        lines = self.file_cursor.read()

        # move to EOF
        self.file_cursor.seek(0, 2)
        self.last_read_index = self.file_cursor.tell()
        self.last_read_at = os.path.getmtime(self.file_path)

        return lines.strip().splitlines()

    def watch(self):
        if os.path.getmtime(self.file_path) > self.last_read_at:
            return self.get_logs(0)
        return []
