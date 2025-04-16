from machine import ADC, Pin, Timer

class Joystick:
    def __init__(self, xAxis: int, yAxis: int, buttonPin: int, mode: str = 'polling'):
        # Initialize ADC pins for joystick axes
        self.x_adc = ADC(Pin(xAxis))
        self.y_adc = ADC(Pin(yAxis))

        # Configure the ADC width and attenuation
        self.x_adc.atten(ADC.ATTN_11DB)  # Full range: 0-3.3V
        self.y_adc.atten(ADC.ATTN_11DB)  # Full range: 0-3.3V

        # Initialize button pin
        self.button = Pin(buttonPin, Pin.IN, Pin.PULL_UP)

        # Initialize variables to store joystick state
        self.x_value = 2048
        self.y_value = 2048
        self.mode = mode
        self.timer = None

        if mode == 'interrupt':
            # Set up a timer interrupt to periodically read joystick data
            self.timer = Timer(-1)
            self.timer.init(period=100, mode=Timer.PERIODIC, callback=self.read_callback)

    def read_callback(self, timer):
        # Timer callback function to read joystick values
        self.x_value = self.x_adc.read()
        self.y_value = self.y_adc.read()

    def read(self):
        if self.mode == 'polling':
            # Read the analog values from the joystick in polling mode
            self.x_value = self.x_adc.read()
            self.y_value = self.y_adc.read()

        # Determine the joystick state
        threshold = 200
        center = 2048
        
        if abs(self.x_value - center) < threshold and abs(self.y_value - center) < threshold:
            return 'M'  # Middle
        elif self.x_value < (center - threshold):
            return 'L'  # Left
        elif self.x_value > (center + threshold):
            return 'R'  # Right
        elif self.y_value < (center - threshold):
            return 'U'  # Up
        elif self.y_value > (center + threshold):
            return 'D'  # Down

    def is_button_pressed(self):
        # Return True if button is pressed (active low)
        return not self.button.value()
