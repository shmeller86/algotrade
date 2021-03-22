from datetime import datetime, timedelta
import logging
import traceback


class Patterns:
    obj = None
    dodge_signal_y = []
    dodge_signal_x = []

    def __init__(self, obj):
        self.obj = obj

    def dodge(self):
        i = 0
        round_digit = 3
        while i <= len(self.obj) - 1:
            # if the opened candle is equal to the closed candle
            if round(float(self.obj[i][1]), round_digit) == round(float(self.obj[i][4]), round_digit):
                # that the character for Dodge pattern
                current_candle = i
                previous_candle = i - 1 if i > 0 else 0
                next_candle = i + 1 if i < len(self.obj) else len(self.obj)
                previous_candle_trend = 0
                next_candle_trend = 0

                if previous_candle > 0:
                    previous_candle_trend = 1 if self.obj[previous_candle][1] > self.obj[previous_candle][4] else -1
                if next_candle > 0:
                    next_candle_trend = 1 if self.obj[next_candle][1] > self.obj[next_candle][4] else -1

                # if the dodge pattern in top
                if (previous_candle_trend > 0) and (next_candle_trend < 0):
                    self.dodge_signal_x.append(datetime.fromtimestamp(int(str(self.obj[current_candle][0])[:-3])))
                    self.dodge_signal_y.append(round(float(self.obj[current_candle][3]), 1))

                # if the dodge pattern in top
                if (previous_candle_trend < 0) and (next_candle_trend > 0):
                    self.dodge_signal_x.append(datetime.fromtimestamp(int(str(self.obj[current_candle][0])[:-3])))
                    self.dodge_signal_y.append(round(float(self.obj[current_candle][4]), 1))

            # print(round(float(obj[i][1]),round_digit) )
            i = i + 1
