from joystick import Joystick
from servo import Servo
import time
from machine import Pin

print("Starting")

# Default gain value
gain = 1

# Initialize four servos for two cameras
servo_pan1 = Servo(pin=18)   # Pan servo for camera 1
servo_tilt1 = Servo(pin=19)  # Tilt servo for camera 1
servo_pan2 = Servo(pin=4)    # Pan servo for camera 2
servo_tilt2 = Servo(pin=5)   # Tilt servo for camera 2

print("Servo setup completed")

# Initialize the joystick in interrupt mode
joystick = Joystick(xAxis=34, yAxis=35, buttonPin=32, mode='interrupt')  # GPIO 34, 35 for axes; GPIO 32 for button

print("Joystick setup completed")

# Initialize slide switch as a digital input
slide_switch = Pin(33, Pin.IN)

# Initialize LEDs as digital outputs
led1 = Pin(25, Pin.OUT)
led2 = Pin(26, Pin.OUT)

print("Switch and LEDs setup completed")


def request_gain():
    global gain
    while True:
        try:
            gain_input = input("Enter gain value (1-10): ")
            gain = int(gain_input)
            if 1 <= gain <= 10:
                print(f"Gain set to: {gain}")
                break
            else:
                print("Invalid input. Gain must be between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 10.")

def move_servo(joystick_state, pan, tilt):
    if joystick_state == 'L':
        pan.left()
    elif joystick_state == 'R':
        pan.right()
    elif joystick_state == 'U':
        tilt.left()
    elif joystick_state == 'D':
        tilt.right()

while True:
    # Read joystick state
    joystick_state = joystick.read()
    
    # Check joystick button
    button_pressed = joystick.is_button_pressed()

    # If button is pressed, ask for gain value from the user
    if button_pressed:
        print("Joystick button pressed")
        request_gain()

    # Read the slide switch state
    switch_state = slide_switch.value()

    if switch_state == 1:
        # Camera 1 selected: control servos for Camera 1
        move_servo(joystick_state, servo_pan1, servo_tilt1)
        # Turn on LED1, turn off LED2
        led1.value(1)
        led2.value(0)
    else:
        # Camera 2 selected: control servos for Camera 2
        move_servo(joystick_state, servo_pan2, servo_tilt2)
        # Turn on LED2, turn off LED1
        led1.value(0)
        led2.value(1)

    # Use the gain value to control the speed of the servo movement
    time.sleep(0.1 / gain)  # Higher gain results in a shorter delay (faster movement)
