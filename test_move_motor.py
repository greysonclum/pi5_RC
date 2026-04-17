import RPi.GPIO as GPIO
import time

# Define GPIO pins (BCM mode)
PWM_PIN = 17  # PWM input for speed control
DIR_PIN = 18  # Direction input (HIGH for forward, LOW for reverse)

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)

# Create PWM object for speed control
pwm = GPIO.PWM(PWM_PIN, 1000)  # 1kHz frequency
pwm.start(0)  # Start with 0% duty cycle (motor stopped)

def move_forward():
    GPIO.output(DIR_PIN, GPIO.HIGH)
    pwm.ChangeDutyCycle(100)  # Full speed forward

def move_reverse():
    GPIO.output(DIR_PIN, GPIO.LOW)
    pwm.ChangeDutyCycle(100)  # Full speed reverse

def stop_motor():
    pwm.ChangeDutyCycle(0)  # Stop motor by setting PWM to 0

try:
    # Move forward for 3 seconds
    move_forward()
    time.sleep(3)
    
    # Stop for 2 seconds
    stop_motor()
    time.sleep(2)
    
    # Move reverse for 3 seconds
    move_reverse()
    time.sleep(3)
    
    # Stop
    stop_motor()

finally:
    # Clean up GPIO
    pwm.stop()
    GPIO.cleanup()
