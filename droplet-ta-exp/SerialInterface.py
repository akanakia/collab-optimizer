import serial
import time

class SerialInterface:
	def __init__(self):
		self.port = None
		self.in_dat = ''
		
    def open(self, port_name):
        """ Function init(port_name): Opens the serial port supplied as input 
        (e.g. 'COM9') and tests to make sure it's working. WARNING: The caller 
        of this function is responsible for closing the serial port connection 
        using <returned_port_handle>.close() when they are done.
        Returns True if the port was succesfully opened, False otherwise.
        """
        try:
            self.port = serial.Serial(port_name, baudrate=115200, timeout=5)
        except serial.SerialException as e:
            print("ERROR: Port " + port_name + " is already open!\n")
            return False
    
        if(self.port.closed):
            self.port.open()
		
		return True

    def read(self):
		"""
		Read data from the serial port and store it to access later
		"""
        while self.port.inWaiting() > 0:
            self.in_dat = self.port.readline()
         
        
    def write(self, data):
		"""
		Write data out to the serial port as a newline terminated string
		"""
        out_dat = data + '\n';
        self.port.write(out_dat)
        self.port.flush()
        time.sleep(0.05)
        
    def close(self, type, value, traceback):
		"""
		Close the serial port
		"""
        self.port.close()
