import datetime
import time
import re
import sys

class Timer:
    def __init__(self):
        self._active_window = self.find_active_window()
        self._last_window = self._active_window
        self._window_start_time = datetime.datetime.now()
        self._window_end_time = None
        self._current_url = ''
        self._last_url = ''

    def find_active_window(self):
        pass
    
    def find_current_url(self):
        pass


    def start_timer(self):
        """ 'main' function of this class """
        while True:
            try:
                time.sleep(1)
                # update current active window
                self._active_window = self.find_active_window()
                if self._last_window != self._active_window:
                    # if previous window was chrome, finish tracking the website access time
                    if self._last_window == 'Google Chrome':
                        self.time_internet_activity()
                    self.time_window()
                if self._active_window == 'Google Chrome':
                    self.time_internet_activity()
            except KeyboardInterrupt:
                self.stop_timer()
                sys.exit(0)

    def time_window(self):
        """ find end time of current window then reset timer """
        self._window_end_time = datetime.datetime.now()
        self.log_activity()
        self._last_window = self._active_window
        # restart time
        self.restart_timer()


    def time_internet_activity(self):
        """ find end time of current url then reset timer """
        self._current_url = self.find_current_url()
        # active window is not chrome anymore, finish tracking last website
        if self._active_window != 'Google Chrome':
            self._current_url = ''

        if self._last_url == '':
            self._last_url = self._current_url

        if self._last_url != self._current_url:
            self._window_end_time = datetime.datetime.now()
            self.log_internet_activity()
            self._last_url = self._current_url
            # restart time
            self.restart_timer()

    def log_activity(self):
        # TODO: maybe add to database?
        print(self._last_window)
        print(self._window_start_time)
        print(self._window_end_time)

    def log_internet_activity(self):
        print(self._last_window + ": " + self._last_url)
        print(self._window_start_time)
        print(self._window_end_time)

    # helper functions --------------------------------
    def process_url(self, url):
        url = re.sub('^https?://', '', url)
        url = re.sub('/.*\n', '', url)
        return url

    def restart_timer(self):
        self._window_start_time = datetime.datetime.now()
        self._window_end_time = None
    # ------------------------------------------------
    def stop_timer(self):
        if self._active_window == 'Google Chrome':
            self.time_internet_activity()
        else:
            self.time_window()
