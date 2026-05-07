"""ProFlow 240 Communication Protocol"""

import logging
import struct

logger = logging.getLogger(__name__)

# Protocol constants
PROTOCOL_VERSION = 1
MAX_PAYLOAD_SIZE = 4096
BUFFER_SIZE = 8192

# Command types
CMD_GET_INFO = 0x01
CMD_SET_IMAGE = 0x02
CMD_SET_VIDEO = 0x03
CMD_SET_BRIGHTNESS = 0x04
CMD_SET_CONTRAST = 0x05
CMD_SET_ANIMATION = 0x06
CMD_CLEAR = 0x07
CMD_RESET = 0x08


class ProFlowProtocol:
    """ProFlow 240 Communication Protocol"""
    
    @staticmethod
    def create_command(cmd_type: int, data: bytes = b'') -> bytes:
        """
        Create a protocol command
        
        Format:
        [START:1][CMD:1][LEN:2][DATA:N][CRC:1][END:1]
        """
        start_byte = 0xAA
        end_byte = 0xBB
        
        # Payload: CMD + DATA
        payload = struct.pack('B', cmd_type) + data
        
        # Calculate length
        length = len(payload)
        
        # Create frame
        frame = struct.pack('>BH', cmd_type, length) + data
        
        # Calculate CRC (simple XOR)
        crc = 0
        for byte in frame:
            crc ^= byte
        
        # Assemble command
        command = struct.pack('B', start_byte) + frame + struct.pack('BB', crc, end_byte)
        
        logger.debug(f"Comando criado: CMD={cmd_type:02x}, LEN={length}, CRC={crc:02x}")
        return command
    
    @staticmethod
    def create_image_command(image_data: bytes) -> bytes:
        """
        Create image send command
        
        Data format:
        [IMG_DATA:N]
        """
        if len(image_data) > MAX_PAYLOAD_SIZE:
            raise ValueError(f"Image data too large: {len(image_data)} > {MAX_PAYLOAD_SIZE}")
        
        return ProFlowProtocol.create_command(CMD_SET_IMAGE, image_data)
    
    @staticmethod
    def create_brightness_command(brightness: int) -> bytes:
        """
        Create brightness command
        
        Data format:
        [BRIGHTNESS:1] (0-100)
        """
        if not 0 <= brightness <= 100:
            raise ValueError(f"Invalid brightness value: {brightness}")
        
        data = struct.pack('B', brightness)
        return ProFlowProtocol.create_command(CMD_SET_BRIGHTNESS, data)
    
    @staticmethod
    def create_contrast_command(contrast: int) -> bytes:
        """
        Create contrast command
        
        Data format:
        [CONTRAST:1] (0-100)
        """
        if not 0 <= contrast <= 100:
            raise ValueError(f"Invalid contrast value: {contrast}")
        
        data = struct.pack('B', contrast)
        return ProFlowProtocol.create_command(CMD_SET_CONTRAST, data)
    
    @staticmethod
    def parse_response(data: bytes) -> dict:
        """
        Parse protocol response
        
        Returns:
            dict with response data
        """
        if len(data) < 3:
            raise ValueError("Invalid response length")
        
        start = data[0]
        if start != 0xAA:
            raise ValueError(f"Invalid start byte: {start:02x}")
        
        cmd = data[1]
        length = struct.unpack('>H', data[2:4])[0]
        
        if len(data) < 4 + length + 2:
            raise ValueError("Response data incomplete")
        
        payload = data[4:4+length]
        crc = data[4+length]
        end = data[4+length+1]
        
        if end != 0xBB:
            raise ValueError(f"Invalid end byte: {end:02x}")
        
        return {
            'cmd': cmd,
            'length': length,
            'payload': payload,
            'crc': crc
        }
