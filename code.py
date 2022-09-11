import board
import digitalio
import analogio
import usb_hid

from hid_gamepad import Gamepad
from stickDeadzone import StickDeadzone
from stick import Stick

gp = Gamepad(usb_hid.devices)
stickDeadzone = StickDeadzone()
stick = Stick()
deadzone = 0

# Create some buttons. The physical buttons are connected
# to ground on one side and these and these pins on the other.
#buttonPins = (board.GP22)

# Map the buttons to button numbers on the Gamepad.
# gamepad_buttons[i] will send that button number when buttons[i]
# is pushed.
gamepadButtons = [1]
button = digitalio.DigitalInOut(board.GP22)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

#buttons = [digitalio.DigitalInOut(pin) for pin in buttonPins]
#for button in buttons:
#    button.direction = digitalio.Direction.INPUT
#    button.pull = digitalio.Pull.UP

# Connect an analog two-axis joystick to A4 and A5.
ax = analogio.AnalogIn(board.A0)
ay = analogio.AnalogIn(board.A1)

stickDeadzone.initDeadzone(ax, ay)
deadzone = stickDeadzone.getDeadzone()
stick.setDeadzone(stickDeadzone)

#print("Deadzone: " + str(deadzone))
#print("Upper Bound: " + str(stickDeadzone.getUpperBoundary()))
#print("Lower Bound: " + str(stickDeadzone.getLowerBoundary()))

while True:
    # Buttons are grounded when pressed (.value = False).
    #for i, button in enumerate(buttons):
    gamepadButtonNum = gamepadButtons[0]

    if button.value:
        gp.release_buttons(gamepadButtonNum)
        #print(" release", gamepadButtonNum, end="")
    else:
        gp.press_buttons(gamepadButtonNum)
        #print(" press", gamepadButtonNum, end="")

    stickValues = stick.doStickCalculations(ax, ay, True)
    #print(stickValues)
    gp.move_joysticks(x=stickValues[0], y=stickValues[1])
