from flask import Flask, request
import RainbowUSB
import random

#Set up dependencies
app = Flask(__name__)
rainbow = RainbowUSB.Rainbow()


@app.route('/Rainbow', methods=['POST'])
def handle_rainbow():
    data = request.get_json(force=True)
    strip = int(data.get("strip"))
    pixels = data.get("pixels")
    for pixel in pixels:
        pixel_strip = int(data.get("strip") or strip)
        pos = int(pixel.get("position") or -1)
        red = int(pixel.get("red") or 127)
        green = int(pixel.get("green") or 0)
        blue = int(pixel.get("blue") or 0)
        if pos == -1:
            for i in range(0, 48):
                success = rainbow.setColor(pixel_strip, i, red, green, blue)
        else:
            success = rainbow.setColor(pixel_strip, pos, red, green, blue)
    rainbow.updateStrip(strip)
    if success == 1:
        return "yay"
    else:
        return "nah"

@app.route('/Test', methods=['POST'])
def test_usb():
    return rainbow.TestUSBs()


# Connect USB and start webserver
if __name__ == '__main__':
    app.run(debug=True)
