from flask import Flask, request
import json
import RainbowUSB

#Set up dependencies
app = Flask(__name__)
rainbow = RainbowUSB.Rainbow()


@app.route('/Rainbow', methods=['POST'])
def handle_rainbow():
    data = request.get_json(force=True)
    strip = int(data.get("strip"))
    pos = int(data.get("position"))
    red = int(data.get("red"))
    green = int(data.get("green"))
    blue = int(data.get("blue"))
    return rainbow.setColor(strip, pos, red, green, blue)

@app.route('/Test', methods=['POST'])
def test_usb():
    return rainbow.TestUSBs()


# Connect USB and start webserver
if __name__ == '__main__':
    app.run(debug=True)
