import smbus2
import sys
import termios
import tty
import time

# PCA9685 I2C configuration
PCA9685_ADDRESS = 0x40  # Default PCA9685 I2C address (can be 0x40-0x7F with address pins)
I2C_BUS = 1  # I2C bus number on Raspberry Pi 5

SERVO_CHANNEL = 0  # PCA9685 channel 0 for servo (0-15)
SERVO_FREQUENCY = 50  # Common servo frequency in Hz
MIN_PULSE_WIDTH = 0.0005  # 500 microseconds
MAX_PULSE_WIDTH = 0.0025  # 2500 microseconds

# PCA9685 register addresses
MODE1 = 0x00
PRESCALE = 0xFE
LED0_ON_L = 0x06
LED0_ON_H = 0x07
LED0_OFF_L = 0x08
LED0_OFF_H = 0x09

# Calculate min/max pulse values for 50Hz frequency
# At 50Hz, each cycle is 20ms. With 4096 steps, each step is ~4.88us
PULSE_MIN = int(MIN_PULSE_WIDTH * 1000000 / (1000000 / SERVO_FREQUENCY) * 4096)
PULSE_MAX = int(MAX_PULSE_WIDTH * 1000000 / (1000000 / SERVO_FREQUENCY) * 4096)

# Initialize I2C bus
bus = smbus2.SMBus(I2C_BUS)
servo_angle = 0


def init_pca9685():
    """Initialize PCA9685 PWM driver."""
    # Set MODE1 to sleep and configure
    bus.write_byte_data(PCA9685_ADDRESS, MODE1, 0x10)
    time.sleep(0.01)
    
    # Set prescale for 50Hz frequency
    # prescale = round(25MHz / (4096 * 50Hz)) - 1 = 121
    prescale = 121
    bus.write_byte_data(PCA9685_ADDRESS, PRESCALE, prescale)
    
    # Wake up the device
    bus.write_byte_data(PCA9685_ADDRESS, MODE1, 0x00)
    time.sleep(0.01)


def set_pwm(channel, on_value, off_value):
    """Set PWM values for a specific channel."""
    on_l = on_value & 0xFF
    on_h = (on_value >> 8) & 0xFF
    off_l = off_value & 0xFF
    off_h = (off_value >> 8) & 0xFF
    
    bus.write_byte_data(PCA9685_ADDRESS, LED0_ON_L + channel * 4, on_l)
    bus.write_byte_data(PCA9685_ADDRESS, LED0_ON_H + channel * 4, on_h)
    bus.write_byte_data(PCA9685_ADDRESS, LED0_OFF_L + channel * 4, off_l)
    bus.write_byte_data(PCA9685_ADDRESS, LED0_OFF_H + channel * 4, off_h)


def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch1 = sys.stdin.read(1)
        if ch1 == '\x1b':
            ch2 = sys.stdin.read(1)
            if ch2 == '[':
                ch3 = sys.stdin.read(1)
                return ch3
        return ch1
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def angle_to_pulse(angle):
    """Convert servo angle to PCA9685 pulse value."""
    angle = max(-45, min(45, angle))
    # Linear interpolation between min and max pulse
    pulse = PULSE_MIN + (angle + 45) / 90 * (PULSE_MAX - PULSE_MIN)
    return int(pulse)


def set_servo_angle(target_angle, step_delay=0.02):
    global servo_angle
    target_angle = max(-45, min(45, target_angle))
    if servo_angle == target_angle:
        return target_angle

    step = 1 if target_angle > servo_angle else -1
    for angle in range(int(servo_angle), int(target_angle) + step, step):
        pulse = angle_to_pulse(angle)
        set_pwm(SERVO_CHANNEL, 0, pulse)
        servo_angle = angle
        time.sleep(step_delay)

    return target_angle


def sweep_servo():
    angle = 0
    angle = set_servo_angle(angle)
    print("Use up/down arrow keys to change servo angle. Press q to quit.")
    print(f"Servo angle: {angle}°")
    while True:
        key = get_key()
        if key == 'A':  # Up arrow
            if angle >= 45:
                print("LIMIT REACHED")
            else:
                angle += 1
                angle = set_servo_angle(angle)
                print(f"Servo angle: {angle}°")
        elif key == 'B':  # Down arrow
            if angle <= -45:
                print("LIMIT REACHED")
            else:
                angle -= 1
                angle = set_servo_angle(angle)
                print(f"Servo angle: {angle}°")
        elif key in ('q', 'Q'):
            break

try:
    # Initialize PCA9685
    init_pca9685()
    
    # Set servo to center position
    center_pulse = (PULSE_MIN + PULSE_MAX) // 2
    set_pwm(SERVO_CHANNEL, 0, center_pulse)
    
    # Sweep servo
    sweep_servo()

finally:
    # Clean up I2C bus
    bus.close()

