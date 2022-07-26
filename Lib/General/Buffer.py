#!usr/bin/python
# -*- coding: UTF-8 -*-
###################################################################
# All Contents Copyright 2022- for Xing Zou. All Rights Reserved.
# FileName: Buffer.py
# Auther: Xing Zou
# Date: Jul-16-2022
# Description: For memory buffer allocation.
###################################################################

import ctypes
from exceptions import Exception

class Buffer(object):
    def __init__(self, test_instance):
        self.test_instance = test_instance
        self.addr = None
        self.description = None
        self.dut = self.test_instance.dut
        self.buf_size = None

    def create_buffer(self, size, count=1, src_data=None, data_len=None, description=""):
        self.addr = self.dut.create_buffer(size, count)
        self.description = description
        self.buf_size = size * count

    def get_byte(self, offset):
        return self.dut.dump_data(self.addr, self.buf_size, offset)

    def set_byte(self, offset, value):
        self.dut.set_data(self.addr, self.buf_size, offset, value)

    def data(self, end_offset, start_offset=None, data_type=int):
        ret = None
        if data_type == int:
            if start_offset is None:
                ret = self.get_byte(end_offset)
            else:
                ret = 0
                for idx in range(end_offset, start_offset, -1):
                    ret += self.get_byte(idx)
                    ret <<= 8
                ret += self.get_byte(start_offset)
        elif data_type == str:
            ret = ""
            for idx in range(start_offset, end_offset + 1):
                ret += chr(self.get_byte(idx))
        return ret

    def get_bytes(self, end_offset, start_offset=None):
        if start_offset is None or start_offset >= end_offset:
            return [self.get_byte(end_offset)]
        bytes = []
        for idx in range(start_offset, end_offset + 1):
            bytes.append(self.get_byte(idx))
        return bytes

    def set_bytes(self, end_offset, start_offset=None, src_data=None, data_len=None):
        if src_data is None:
            if start_offset is None or start_offset >= end_offset:
                self.set_byte(end_offset, 0x0)
            else:
                for idx in range(start_offset, end_offset + 1):
                    self.set_byte(idx, 0x0)
        else:
            if start_offset is None or start_offset >= end_offset:
                self.set_byte(end_offset, src_data[0])
            else:
                if data_len < end_offset + 1 - start_offset:
                    for idx in range(start_offset, min(end_offset - start_offset, data_len) + 1):
                        self.set_byte(idx, src_data[idx - start_offset])

    def get_word(self, offset):
        if offset % 2 != 0:
            raise Exception("Invalid offset, offset should be multiple of 2, acutal is {}".format(offset))
        return self.get_byte(offset) + (self.get_byte(offset + 1) << 8)

    def set_word(self, offset, src_data):
        if offset % 2 != 0:
            raise Exception("Invalid offset, offset should be multiple of 2, acutal is {}".format(offset))
        self.set_byte(offset, src_data & 0xFF)
        self.set_byte(offset + 1, (src_data >> 8) & 0xFF)

    def get_dword(self, offset):
        if offset % 4 != 0:
            raise Exception("Invalid offset, offset should be multiple of 4, acutal is {}".format(offset))
        return self.get_byte(offset) + (self.get_byte(offset + 1) << 8) + (self.get_byte(offset + 2) << 16) + (self.get_byte(offset + 3) << 24)

    def set_dword(self, offset, src_data):
        if offset % 4 != 0:
            raise Exception("Invalid offset, offset should be multiple of 4, acutal is {}".format(offset))
        self.set_byte(offset, src_data & 0xFF)
        self.set_byte(offset + 1, (src_data >> 8) & 0xFF)
        self.set_byte(offset + 2, (src_data >> 16) & 0xFF)
        self.set_byte(offset + 3, (src_data >> 24) & 0xFF)

    def dump_data(self):
        print_content = "Data dump:"
        for idx in range(self.buf_size):
            if idx % 0x10 == 0:
                print_content += "\n{:08X}h: {:02X} ".format(idx, self.get_byte(idx))
            else:
                print_content += "{:02X} ".format(self.get_byte(idx))
        if self.test_instance is not None:
            self.test_instance.logger.info(print_content)
        else:
            print(print_content)

# if __name__ == "__main__":
#     ins = Buffer(None)
#     data = ins.create_buffer(size=1024, description="1K buffer", src_data=[0xA5]*512)
#     ins.dump_data(data.buff)
#     ins.set_bytes(data.buff, 0x20, 0x15, [0x65, 0x66, 0x67, 0x68, 0x69, 0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x80], 16)
#     ins.dump_data(data.buff)
#     print(ins.get_bytes(data.buff, 0x20, 0x15))
#     ins.set_word(data.buff, 0x66, 0x4567)
#     print(hex(ins.get_word(data.buff, 0x66)))
#     ins.set_dword(data.buff, 0x80, 0xA4A5A6A7)
#     print(hex(ins.get_dword(data.buff, 0x80)))
#     ins.dump_data(data.buff)
