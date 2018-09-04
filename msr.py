"""This module is library for manupulate MSR

Depends:
    The 'msr' kernel module.
"""
import os
import struct

class Msr(object):
    """Msr(integer) -> Callable object to R/W MSR of CPU specified by integer."""
    def __init__(self, cpu):
        self.cpu = cpu
        self.fd = None
    def __call__(self, index, value=None):
        """Msr(index) -> Read MSR [index] and return;
        Msr(index, value) -> Write value to MSR[index], then read and return.
        
        This function will return the value of the specified MSR. If value is
        specified, the MSR will be updated with value first.
       
        Args:
            index: [integer] specify the MSR index.
            value: [integer] new MSR value.
            
        Returns:
            The value of specified MSR.
    
        Exceptions:
            FileNotFoundError: 'msr' not loaded or CPU index out of range.
            PermissionError: run this module as normal user.
        """
        if self.fd is None:
            file_path = "/dev/cpu/%d/msr" % self.cpu
            flags = os.O_RDWR
            self.fd = os.open(file_path, flags)
        os.lseek(self.fd, index, os.SEEK_SET)
        if value is not None:
            os.write(self.fd, value)
        value_str = os.read(self.fd, 8)
        (msr_value, ) = struct.unpack('<Q', value_str)
        return msr_value
    def __del__(self):
        try:
            os.close(self.fd)
        except Exception:
            pass
