import time
import board
import digitalio
import usb_cdc

# Set up GPIO pin 16
# print(dir(board))
pin = digitalio.DigitalInOut(board.GP16)
pin.direction = digitalio.Direction.OUTPUT

serial = usb_cdc.console

#signal = 0
#prev = 0

while True:
    if serial.in_waiting > 0:
        data = serial.read(1)
        pin.value = True
        time.sleep(1)
        pin.value = False
        time.sleep(4)