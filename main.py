from Timer import Timer
import platform

def main():
    timer = Timer()
    if platform.system() == 'Darwin':
        from TimerMacOS import TimerMacOS
        timer = TimerMacOS()
        print("macos???")
    else:
        print("Not supported for this OS yet...")
        exit(1)
    timer.start_timer()

if __name__ == "__main__":
    main()