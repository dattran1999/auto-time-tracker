import platform
import datetime
import time
import subprocess
import re
import matplotlib.pyplot as plt

def convert_to_json(dictionary):
    return {'events': [value for key, value in dictionary.items()]}

def plot_data(json):
    # Data to plot
    labels = [event['app'] for event in json['events']]
    sizes = [event['time'].total_seconds() for event in json['events']]
    # Plot
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.axis('equal')
    plt.show()

# remove http:// and route 
def process_url(url):
    url = re.sub('^https?://', '', url)
    url = re.sub('/.*\n', '', url)
    return url

def main():
    print("Press Ctrl+C to kill the program")
    # if macOS
    if platform.system() == 'Darwin':
        from AppKit import NSWorkspace
    else:
        print("Not supported for this OS yet...")
        exit(1)
    last_active_window = "Starting program"
    last_url = ""
    # dict maps from app name to dict of event, which is {app, time}
    history = {}
    start = datetime.datetime.now()
    while True:
        try:
            time.sleep(1)
            # credits to https://stackoverflow.com/questions/10266281/obtain-active-window-using-python
            active_window_name = (NSWorkspace.sharedWorkspace()
                                    .activeApplication()['NSApplicationName'])
            # track url we are on
            if active_window_name == "Google Chrome":
                # specific solution to macOS
                cmd = ['osascript', '-e', 'tell application "Google Chrome" to get URL of active tab of window 0']
                url = subprocess.run(cmd, stdout=subprocess.PIPE).stdout
                url = process_url(url.decode('utf-8'))
                if url != last_url:
                    if last_url == "":
                        last_url = url
                    end = datetime.datetime.now()
                    event = {"website": last_url, "time": end-start}
                    # try to add to history
                    try:
                        history[last_url]['time'] += event['time']
                    # if not in the history yet
                    except KeyError:
                        history[last_url] = event
                    print(event['website'], str(event['time']))
                    last_url = url
                    start = datetime.datetime.now()
                        
            elif last_active_window != active_window_name:
                end = datetime.datetime.now()
                event = {"app": last_active_window, "time": end-start}
                # try to add to history
                try:
                    history[last_active_window]['time'] += event['time']
                # if not in the history yet
                except KeyError:
                    history[last_active_window] = event
                print(event['app'], str(event['time']))
                last_active_window = active_window_name
                start = datetime.datetime.now()
        except KeyboardInterrupt:
            # finish logging the last app
            end = datetime.datetime.now()
            event = {"app": last_active_window, "time": end-start}
            try:
                history[active_window_name]['time'] += event['time']
            except KeyError:
                history[active_window_name] = event
            print(event['app'], str(event['time']))

            # remove the time it takes to start the program
            del history["Starting program"]
            history_json = convert_to_json(history)
            print(history_json)
            # plot_data(history_json)
            exit(0)

if __name__ == "__main__":
    main()