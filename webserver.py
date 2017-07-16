from flask import Flask, request
import opc

_App = Flask(__name__)
_IPPort = '127.0.0.1:7890'
_Client = opc.Client(_IPPort, verbose=True)
_LedCount = 128
_PixelState = [(0,0,0) for x in range(_LedCount)]

@_App.route('/Rainbow', methods=['POST'])
def handle_rainbow():
   try:
       data = request.get_json(force=True)
       pixels = data["pixels"]
       for p in pixels:
           position = p["channel"] * 64 + p["pos"]
           _PixelState[position] = (p["red"], p["green"], p["blue"])
      
       if(_Client.put_pixels(_PixelState, channel=0)):
           print('\tsuccess {}\n').format(c)
       return '\tfail\n'
   except Exception:
       return '\tInvalidInput\n'
 
@_App.route('/Off', methods=['GET'])
def off():
   pixels_out = []
   for c in range(2):
       for ii in range(_LedCount):
           red = 0
           green = 0
           blue = 0
           pixels_out.append((red, green, blue))
       _Client.put_pixels(pixels_out, channel=c)
   return 'okay'

@_App.route('/On', methods=['GET'])
def on():
   pixels_out = []
   for c in range(2):
       for ii in range(_LedCount):
           red = 0
           green = 256
           blue = 0
           pixels_out.append((red, green, blue))
       _Client.put_pixels(pixels_out, channel=c)
   return 'okay'

if __name__ == "__main__":
    _App.run(host='0.0.0.0', port=5000, debug=True)