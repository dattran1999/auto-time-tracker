from Timer import Timer
import subprocess
from AppKit import NSWorkspace

class TimerMacOS(Timer):
    def __init__(self):
        super().__init__()
        
    
    def find_active_window(self):
        return (NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName'])

    def find_current_url(self):
        cmd = ['osascript', '-e', 'tell application "Google Chrome" to get URL of active tab of window 0']
        url = subprocess.run(cmd, stdout=subprocess.PIPE).stdout
        url = self.process_url(url.decode('utf-8'))
        return url
