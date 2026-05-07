"""USB Communication Handler for ProFlow 240"""

import logging
import usb.core
import usb.util
from typing import Optional

from device.protocol import ProFlowProtocol

logger = logging.getLogger(__name__)

# Device IDs
VENDOR_ID = 0x33C3
PRODUCT_ID = 0x7792

# Endpoints
EP_OUT = 0x02  # Write endpoint
EP_IN = 0x81   # Read endpoint
TIMEOUT = 5000  # 5 seconds


class USBHandler:
    """Handle USB communication with ProFlow 240"""
    
    def __init__(self):
        self.device = None
        self.ep_out = None
        self.ep_in = None
    
    def find_device(self) -> bool:
        """
        Find and connect to ProFlow 240 device
        
        Returns:
            bool: True if device found, False otherwise
        """
        try:
            self.device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
            
            if self.device is None:
                logger.warning("ProFlow 240 device not found")
                return False
            
            logger.info(f"Device found: {self.device.manufacturer} {self.device.product}")
            
            # Set configuration
            try:
                self.device.set_configuration()
            except usb.core.USBError as e:
                logger.warning(f"Could not set configuration: {e}")
            
            # Get endpoints
            cfg = self.device.get_active_configuration()
            intf = cfg[(0, 0)]
            
            self.ep_out = usb.util.find_descriptor(
                intf,
                custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
            )
            
            self.ep_in = usb.util.find_descriptor(
                intf,
                custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
            )
            
            if self.ep_out is None or self.ep_in is None:
                logger.warning("Could not find endpoints")
                return False
            
            logger.info(f"Endpoints found: OUT={self.ep_out.bEndpointAddress:02x}, IN={self.ep_in.bEndpointAddress:02x}")
            return True
            
        except usb.core.USBError as e:
            logger.error(f"USB error: {e}")
            return False
        except Exception as e:
            logger.error(f"Error finding device: {e}")
            return False
    
    def write(self, data: bytes) -> bool:
        """
        Write data to device
        
        Args:
            data: bytes to write
        
        Returns:
            bool: True if successful
        """
        if self.device is None or self.ep_out is None:
            logger.error("Device not connected")
            return False
        
        try:
            self.ep_out.write(data, TIMEOUT)
            logger.debug(f"Sent {len(data)} bytes")
            return True
        except usb.core.USBError as e:
            logger.error(f"Write error: {e}")
            return False
    
    def read(self, size: int = 64) -> Optional[bytes]:
        """
        Read data from device
        
        Args:
            size: number of bytes to read
        
        Returns:
            bytes or None if error
        """
        if self.device is None or self.ep_in is None:
            logger.error("Device not connected")
            return None
        
        try:
            data = self.ep_in.read(size, TIMEOUT)
            logger.debug(f"Received {len(data)} bytes")
            return bytes(data)
        except usb.core.USBError as e:
            logger.error(f"Read error: {e}")
            return None
    
    def send_image(self, image_data: bytes) -> bool:
        """
        Send image to device
        
        Args:
            image_data: binary image data
        
        Returns:
            bool: True if successful
        """
        try:
            command = ProFlowProtocol.create_image_command(image_data)
            return self.write(command)
        except Exception as e:
            logger.error(f"Error sending image: {e}")
            return False
    
    def set_brightness(self, brightness: int) -> bool:
        """
        Set display brightness
        
        Args:
            brightness: brightness level (0-100)
        
        Returns:
            bool: True if successful
        """
        try:
            command = ProFlowProtocol.create_brightness_command(brightness)
            return self.write(command)
        except Exception as e:
            logger.error(f"Error setting brightness: {e}")
            return False
    
    def set_contrast(self, contrast: int) -> bool:
        """
        Set display contrast
        
        Args:
            contrast: contrast level (0-100)
        
        Returns:
            bool: True if successful
        """
        try:
            command = ProFlowProtocol.create_contrast_command(contrast)
            return self.write(command)
        except Exception as e:
            logger.error(f"Error setting contrast: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from device"""
        try:
            if self.device:
                usb.util.dispose_resources(self.device)
            self.device = None
            self.ep_out = None
            self.ep_in = None
            logger.info("Device disconnected")
        except Exception as e:
            logger.error(f"Error disconnecting: {e}")
