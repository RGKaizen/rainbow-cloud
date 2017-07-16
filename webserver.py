from flask import Flask, request
import opc

_App = Flask(__name__)
_IPPort = '127.0.0.1:7890'
_Client = opc.Client(_IPPort, verbose=True)
if _Client.can_connect():
    print(' Connected to opc')
else:
    print(' Could not connect to opc')
_LedCount = 60
_ChannelCount = 2
_PixelState = [[(0,0,0) for x in range(_LedCount)] for y in range(_ChannelCount)]

@_App.route('/Rainbow', methods=['POST'])
def handle_rainbow():
   try:
       data = request.get_json(force=True)
       pixels = data["pixels"]
       for p in pixels:
           _PixelState[p["channel"]][p["pos"]] = (p["red"], p["green"], p["blue"])
 
       for c in range(_ChannelCount):            
           if(_Client.put_pixels(_PixelState[c], channel=c)):
               print('\tsuccess {}\n').format(c)
       return '\tfail\n'
   except Exception:
       return '\tInvalidInput\n'
 
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