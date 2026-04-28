from gpiozero import PWMOutputDevice, DigitalOutputDevice, AngularServo
import sys
import termios
import tty
import time

# Define GPIO pins (BCM mode)
PWM_PIN = 17  # PWM input for motor speed control
DIR_PIN = 18  # Direction input for motor (HIGH for forward, LOW for reverse)
SERVO_PIN = 22  # PWM output for servo control

# Set up devices
pwm = PWMOutputDevice(PWM_PIN, frequency=1000)  # 1kHz frequency
dir_pin = DigitalOutputDevice(DIR_PIN)
servo = AngularServo(SERVO_PIN, min_angle=-45, max_angle=45, min_pulse_width=0.0005, max_pulse_width=0.0025)

def move_forward():
    dir_pin.on()  # Set direction HIGH
    pwm.value = 1.0  # Full speed (100% duty cycle)

def move_reverse():
    dir_pin.off()  # Set direction LOW
    pwm.value = 1.0  # Full speed (100% duty cycle)

def stop_motor():
    pwm.value = 0.0  # Stop motor by setting PWM to 0


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


def sweep_servo():
    angle = 0
    servo.angle = angle
    print("Use up/down arrow keys to change servo angle. Press q to quit.")
    print(f"Servo angle: {angle}°")
    while True:
        key = get_key()
        if key == 'A':  # Up arrow
            if angle >= 45:
                print("LIMIT REACHED")
            else:
                angle += 1
                servo.angle = angle
                print(f"Servo angle: {angle}°")
        elif key == 'B':  # Down arrow
            if angle <= -45:
                print("LIMIT REACHED")
            else:
                angle -= 1
                servo.angle = angle
                print(f"Servo angle: {angle}°")
        elif key in ('q', 'Q'):
            break

try:
    # Move forward for 3 seconds
    #move_forward()
    #time.sleep(3)
    
    # Stop for 2 seconds
    #stop_motor()
    #time.sleep(2)
    
    # Move reverse for 3 seconds
    #move_reverse()
    #time.sleep(3)
    
    # Stop
    stop_motor()
    
    # Sweep servo 10° one way and 10° the other
    sweep_servo()

finally:
    # Clean up devices
    pwm.close()
    dir_pin.close()
    servo.close()

