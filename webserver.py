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
 
@_App.route('/OnBoth', methods=['GET'])
def onBoth():
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
 
@_App.route('/OnA', methods=['GET'])
def onA():
   pixels_out = []
   for ii in range(_LedCount):
       red = 256
       green = 0
       blue = 0
       pixels_out.append((red, green, blue))
   _Client.put_pixels(pixels_out, channel=0)
   return 'okay'
 
@_App.route('/OnB', methods=['GET'])
def onB():
   pixels_out = []
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