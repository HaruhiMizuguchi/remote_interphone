from machine import Pin, PWM
import time
import config


class Servo:
    def __init__(self):
        self._pwm = PWM(Pin(config.SERVO_GPIO_PIN))
        self._pwm.freq(config.SERVO_FREQ_HZ)
        self._min_us = config.SERVO_MIN_US
        self._max_us = config.SERVO_MAX_US
        self.set_angle(config.ANGLE_REST)

    def set_angle(self, angle):
        """0〜180° の角度をパルス幅に変換して出力する。"""
        angle = max(0, min(180, angle))
        pulse_us = self._min_us + (self._max_us - self._min_us) * angle / 180
        # duty_u16: 0〜65535 の範囲に変換
        duty = int(pulse_us / (1_000_000 / config.SERVO_FREQ_HZ) * 65535)
        self._pwm.duty_u16(duty)

    def press_button(self):
        """開錠ボタンを押して戻す一連の動作。"""
        self.set_angle(config.ANGLE_PRESS)
        time.sleep_ms(config.PRESS_DURATION_MS)
        self.set_angle(config.ANGLE_REST)

    def deinit(self):
        self._pwm.deinit()
