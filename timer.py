import platform
import datetime
import time
import matplotlib.pyplot as plt

def convert_to_json(dictionary):
    return [value for key, value in dictionary.items()]

def plot_data(json):
    # Data to plot
    labels = [event['app'] for event in json]
    sizes = [event['time'].total_seconds() for event in json]
    # Plot
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.axis('equal')
    plt.show()

def main():
    print("Press Ctrl+c to kill the program")
    # if macOS
    if platform.system() == 'Darwin':
        from AppKit import NSWorkspace

    last_active_window = "Starting program"
    # dict maps from app name to dict of event, which is {app, time}
    history = {}
    start = datetime.datetime.now()
    while True:
        try:
            # credits to https://stackoverflow.com/questions/10266281/obtain-active-window-using-python
            active_window_name = (NSWorkspace.sharedWorkspace()
                                    .activeApplication()['NSApplicationName'])
            if last_active_window != active_window_name:
                time.sleep(1)  
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

            # TODO: maybe print a summary or something
            # remove the time it takes to start the program
            del history["Starting program"]
            history_json = convert_to_json(history)
            print(history_json)
            plot_data(history_json)
            exit(0)

if __name__ == "__main__":
    main()