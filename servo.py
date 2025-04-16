from machine import Pin, PWM

class Servo:
    def __init__(self, pin: int, min=1000, max=9000):
        # Initialize the servo PWM
        self.pwm = PWM(Pin(pin, Pin.OUT))
        self.pwm.freq(50)  # Set frequency to 50Hz for servo control
        self.min = min  # Minimum duty cycle value
        self.max = max  # Maximum duty cycle value
        self.current_angle = 90  # Default to center position
        self.goto(90)  # Move to the default position at startup

    def goto(self, angle):
        dc = (((angle - 0) * (self.max - self.min)) // 180) + self.min
        self.pwm.duty_u16(dc)  # Set the duty cycle
        self.current_angle = angle  # Store the current angle

    def left(self, step=1):
        # Incrementally move the servo to the left by the specified step
        new_angle = max(0, self.current_angle - step)  # Ensure angle is within bounds
        self.goto(new_angle)

    def right(self, step=1):
        # Incrementally move the servo to the right by the specified step
        new_angle = min(180, self.current_angle + step)  # Ensure angle is within bounds
        self.goto(new_angle)
