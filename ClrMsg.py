from struct import *


class ClrMsg:
    payload = ''

    def __init__(self, strip, pos, red, green, blue):
        # Sanitize bad inputs
        red = self.clamp(red, 0, 127)
        green = self.clamp(green, 0, 127)
        blue = self.clamp(blue, 0, 127)

        if strip == 1:
            pos = self.clamp(pos, 0, 47)
        if strip == 2:
            pos = self.clamp(pos, 0, 31)

        # For strip 2, we add 64 to represent the bit in that position
        byte0 = 0
        if strip == 2:
            byte0 += 64
        else:
            byte0 += 0
        byte0 += pos
        self.payload = pack('BBBB', byte0, red, green, blue)

    def clamp(self, value, low, high):
        if value > high:
            value = high
        if value < low:
            value = low
        return value
