from flask import Flask, request
import opc

_App = Flask(__name__)
_IPPort = '127.0.0.1:7890'
_Client = opc.Client(_IPPort)
_LedCount = 60
_ChannelCount = 2

pixels_state = [[(0,0,0) for x in range(_LedCount)] for y in range(_ChannelCount)]

@_App.route('/Rainbow', methods=['POST'])
def handle_rainbow():
    try:
        data = request.get_json(force=True)
        pixels = data["pixels"]
        for p in pixels:
            pixels_state[int(p.get("channel"))][int(p.get("pos"))] = (p["red"], p["green"], p["blue"])

        for c in range(_ChannelCount):            
            if(_Client.put_pixels(pixels_state[c], channel=c)):
                return '\tsuccess\n'
        return '\tfail\n'
    except Exception:
        return '\tInvalidInput\n'

@_App.route('/On', methods=['GET'])
def on():
    pixels_out = []
    for c in range(_ChannelCount):
        for ii in range(_LedCount):
            red = 256
            green = 256
            blue = 256
            pixels_out.append((red, green, blue))
        _Client.put_pixels(pixels_out, channel=c)
    return 'okay'

@_App.route('/OnA', methods=['GET'])
def onA():
    pixels_out = []
    for ii in range(_LedCount):
        red = 256
        green = 0
        blue = 0
        pixels_out.append((red, green, blue))
    _Client.put_pixels(pixels_out, channel=0)
    for ii in range(_LedCount):
        red = 0
        green = 256
        blue = 0
        pixels_out.append((red, green, blue))
    _Client.put_pixels(pixels_out, channel=1)
    return 'okay'

@_App.route('/Off', methods=['GET'])
def off():
    pixels_out = []
    for c in range(_ChannelCount):
        for ii in range(_LedCount):
            red = 0
            green = 0
            blue = 0
            pixels_out.append((red, green, blue))
        _Client.put_pixels(pixels_out, channel=c)
    return 'okay'

# Connect to FC Server and start webserver
if __name__ == '__main__':
    _App.run(host='0.0.0.0', debug=True)
    if _Client.can_connect():
        print('    connected to FCServer: %s' % _IPPort)
    else:
        # can't connect, but keep running in case the server appears later
        print('    WARNING: could not connect to %s' % _IPPort)
    print('')

