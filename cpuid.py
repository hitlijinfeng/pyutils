"""This module is library for get CPUID info.

Depends:
    The 'cpuid' kernel module.
"""
import os
import struct

class CpuId(object):
    """CpuId(integer) -> Callable object to execute CPUID on CPU specified by 
    integer.
    """
    def __init__(self, cpu):
        self.cpu = cpu
        self.fd = None
    def __call__(self, EAX):
        """Execute CPUID function specified by EAX and return the result.
        
        This function will return the result of the specified CPUID function.
       
        Args:
            EAX: [integer] specifies the CPUID function.
            
        Returns:
            The result of the CPUID function in term of (EAX, EBX, ECX, EDX).
    
        Exceptions:
            FileNotFoundError: 'msr' not loaded or CPU index out of range.
            PermissionError: run this module as normal user.
        """
        if self.fd is None:
            file_path = "/dev/cpu/%d/cpuid" % self.cpu
            flags = os.O_RDONLY
            self.fd = os.open(file_path, flags)
        os.lseek(self.fd, EAX, os.SEEK_SET)
        value_str = os.read(self.fd, 16)
        (A, B, C, D) = struct.unpack('<4I', value_str)
        return (A, B, C, D)
    def __del__(self):
        try:
            os.close(self.fd)
        except Exception:
            pass
