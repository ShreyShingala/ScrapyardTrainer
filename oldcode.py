import time
import board
import digitalio

# Set up GPIO pin 16
print(dir(board))
pin = digitalio.DigitalInOut(board.GP16)
pin.direction = digitalio.Direction.OUTPUT
'''
while True:
    try:
        with open("kill_signal.txt", "r+") as f:
            data = f.read().strip()
            if data == "1":
                print("Signal received! Activating servo.")
                pin.value = True
                time.sleep(1)
                pin.value = False
                f.seek(0)
                f.write("0")
                f.truncate()
                time.sleep(4)
    except FileNotFoundError:
        pass  # File not yet created
    time.sleep(1)
'''