"""This module is library for manupulate MSR

Depends:
    The 'msr' kernel module.
"""
import os
import struct

def msr(cpu,  index,  value=None):
    """Read or write MSR [index] of CPU specified by cpu.
    
    This function will return the value of the specified MSR. If value is
    specified, the MSR will be updated with value first.
   
    Args:
        cpu: [integer] specify the MSR of which CPU.
        index: [integer] specify the MSR index.
        value: [integer] new MSR value.
        
    Returns:
        The value of specified MSR.

    Exceptions:
        FileNotFoundError: 'msr' not loaded or CPU index out of range.
        PermissionError: run this module as normal user.
    """
    
    file_path = "/dev/cpu/%d/msr" % cpu
    if value is None:
        flags = os.O_RDONLY
    else:
        flags = os.O_RDWR
    fd = os.open(file_path,  flags)
    os.lseek(fd,  index,  os.SEEK_SET)
    if value is not None:
        os.write(fd,  value)
    value_str = os.read(fd,  8)
    (msr_value, ) = struct.unpack('<Q',  value_str)
    os.close(fd)
    return msr_value
