#!/usr/bin/env python3
"""Serial Communication Handler for ProFlow 240"""

import logging
import serial
import serial.tools.list_ports
from typing import Optional
import time

logger = logging.getLogger(__name__)

# Device IDs
VENDOR_ID = 0x33C3
PRODUCT_ID = 0x7792

# Serial settings
BAUD_RATE = 115200
TIMEOUT = 1.0


class SerialHandler:
    """Handle serial communication with ProFlow 240 via /dev/ttyACM0"""
    
    def __init__(self):
        self.device = None
        self.port = None
    
    def find_device(self) -> bool:
        """
        Find ProFlow 240 device by VID/PID
        
        Returns:
            bool: True if device found, False otherwise
        """
        try:
            ports = serial.tools.list_ports.comports()
            
            for port in ports:
                logger.debug(f"Found port: {port.device} - {port.description}")
                
                # Check for Jungle Leopard/ProFlow 240
                if (port.vid == VENDOR_ID and port.pid == PRODUCT_ID) or \
                   ('33c3' in str(port.hwid).lower() or '7792' in str(port.hwid).lower()):
                    
                    logger.info(f"ProFlow 240 found at {port.device}")
                    self.port = port.device
                    return self._connect()
            
            # Fallback: try /dev/ttyACM0 (common Linux default)
            logger.warning("Device not found by VID/PID, trying /dev/ttyACM0")
            self.port = "/dev/ttyACM0"
            return self._connect()
            
        except Exception as e:
            logger.error(f"Error finding device: {e}")
            return False
    
    def _connect(self) -> bool:
        """Connect to serial port"""
        try:
            self.device = serial.Serial(
                port=self.port,
                baudrate=BAUD_RATE,
                timeout=TIMEOUT,
                write_timeout=TIMEOUT
            )
            logger.info(f"Connected to {self.port} at {BAUD_RATE} baud")
            return True
        except serial.SerialException as e:
            logger.error(f"Cannot open serial port {self.port}: {e}")
            return False
        except Exception as e:
            logger.error(f"Connection error: {e}")
            return False
    
    def write(self, data: bytes) -> bool:
        """
        Write data to device
        
        Args:
            data: bytes to write
        
        Returns:
            bool: True if successful
        """
        if self.device is None or not self.device.is_open:
            logger.error("Device not connected")
            return False
        
        try:
            self.device.write(data)
            self.device.flush()
            logger.debug(f"Sent {len(data)} bytes")
            return True
        except serial.SerialException as e:
            logger.error(f"Write error: {e}")
            return False
    
    def read(self, size: int = 1024) -> Optional[bytes]:
        """
        Read data from device
        
        Args:
            size: number of bytes to read
        
        Returns:
            bytes or None if error
        """
        if self.device is None or not self.device.is_open:
            logger.error("Device not connected")
            return None
        
        try:
            data = self.device.read(size)
            if data:
                logger.debug(f"Received {len(data)} bytes")
            return data if data else None
        except serial.SerialException as e:
            logger.error(f"Read error: {e}")
            return None
    
    def send_command(self, command: bytes) -> bool:
        """
        Send command and wait for response
        
        Args:
            command: command bytes
        
        Returns:
            bool: True if successful
        """
        if not self.write(command):
            return False
        
        time.sleep(0.1)
        response = self.read()
        
        if response:
            logger.debug(f"Got response: {response.hex()}")
            return True
        
        return False
    
    def disconnect(self):
        """Disconnect from device"""
        try:
            if self.device and self.device.is_open:
                self.device.close()
            self.device = None
            logger.info("Device disconnected")
        except Exception as e:
            logger.error(f"Error disconnecting: {e}")
