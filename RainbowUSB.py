import usb.core
import usb.util
from ClrMsg import ClrMsg
from struct import *

class Rainbow:

    ep = None
    ON1 = "\x80\x00\x00\x00"
    ON2 = "\xC0\x00\x00\x00"

    def __init__(self):
        # find our device
        dev = usb.core.find(idVendor=0x2341, idProduct=0x8036)

        # was it found?
        if dev is None:
            raise ValueError('Device not found')

        reattach = False
        if dev.is_kernel_driver_active(2):
                dev.detach_kernel_driver(2)
                print "kernel driver detached"
        else:
            print "Kernel Already Detached"

        # set the active configuration. With no arguments, the first
        # configuration will be the active one
        dev.set_configuration()

        # get an endpoint instance
        cfg = dev.get_active_configuration()
        intf = cfg[(1,0)]

        ep = usb.util.find_descriptor(
            intf,
            # match the first OUT endpoint
            custom_match=lambda e:
            usb.util.endpoint_direction(e.bEndpointAddress) ==
            usb.util.ENDPOINT_OUT)

        if ep is None:
            print "Endpoint Not Found"

    def TestUSBs(self):
        for x in range(0, 48):
            msg = ClrMsg(1,x,127,0 ,0)
            ep.write(msg.payload)

        for x in range(0, 32):
            msg = ClrMsg(2,x,0,127,0)
            ep.write(msg.payload)

        ep.write(ON1)
        ep.write(ON2)




