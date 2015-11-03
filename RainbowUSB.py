import usb.core
import usb.util
from ClrMsg import ClrMsg


class Rainbow:
    endpoint = None
    ON1 = "\x80\x00\x00\x00"
    ON2 = "\xC0\x00\x00\x00"

    def __init__(self):
        # find our device
        dev = usb.core.find(idVendor=0x2341, idProduct=0x8036)

        # was it found?
        if dev is None:
            raise ValueError('Device not found')

        if dev.is_kernel_driver_active(2):
            dev.detach_kernel_driver(2)
            print "Dettached Kernel"
        else:
            print "Kernel Already Dettached"

        # set the active configuration. With no arguments, the first
        # configuration will be the active one
        dev.set_configuration()

        # get an endpoint instance
        cfg = dev.get_active_configuration()

        interface = cfg[(1, 0)]

        self.endpoint = usb.util.find_descriptor(
            interface,
            # match the first OUT endpoint
            custom_match=lambda e:
            usb.util.endpoint_direction(e.bEndpointAddress) ==
            usb.util.ENDPOINT_OUT)

        if self.endpoint is None:
            print "Endpoint Not Found"

    def TestUSBs(self):
        for x in range(0, 48):
            msg = ClrMsg(1, x, 127, 0, 0)
            self.endpoint.write(msg.payload)

        for x in range(0, 32):
            msg = ClrMsg(2, x, 0, 127, 0)
            self.endpoint.write(msg.payload)

        self.endpoint.write(self.ON1)
        self.endpoint.write(self.ON2)

    def setColor(self, strip, pos, red, green, blue):
        if self.endpoint is None:
            return "No usb connected"

        print "Strip %1 Pos %2 Red %3 Green %4 Blue %5".format(strip, pos, red, green, blue)
        msg = ClrMsg(strip, pos, red, green, blue)
        return self.endpoint.write(msg.payload)

