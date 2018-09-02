"""This module is library for get CPUID info.

Depends:
    The 'cpuid' kernel module.
"""
import os
import struct

def cpuid(cpu, EAX):
    """Execute CPUID function specified by EAX on CPU and return the result.
    
    This function will return the result of the specified CPUID function.
   
    Args:
        cpu: [integer] specifies CPU on which the CPUID execute.
        EAX: [integer] specifies the CPUID function.
        
    Returns:
        The result of the CPUID function in term of (EAX, EBX, ECX, EDX).

    Exceptions:
        FileNotFoundError: 'msr' not loaded or CPU index out of range.
        PermissionError: run this module as normal user.
    """
    
    file_path = "/dev/cpu/%d/cpuid" % cpu
    flags = os.O_RDONLY
    fd = os.open(file_path, flags)
    os.lseek(fd, EAX, os.SEEK_SET)
    value_str = os.read(fd, 16)
    (A, B, C, D) = struct.unpack('<4I', value_str)
    os.close(fd)
    return (A, B, C, D)
