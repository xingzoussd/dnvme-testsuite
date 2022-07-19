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
        self.buff = None
        self.description = None

    def create_buffer(self, size, count=1, src_data=None, data_len=None, description=""):
        data = Buffer(self.test_instance)
        data.buff = ctypes.create_string_buffer(size * count)
        data.description = description
        if src_data is not None:
            self.set_bytes(data.buff, size * count - 1, 0, src_data, data_len)
        return data

    def data(self, buff, end_offset, start_offset=None, data_type=int):
        ret = None
        if data_type == int:
            if start_offset is None:
                ret = ord(buff[end_offset])
            else:
                ret = 0
                for idx in range(end_offset, start_offset, -1):
                    ret += ord(buff[idx])
                    ret <<= 8
                ret += ord(buff[start_offset])
        elif data_type == str:
            ret = buff[start_offset: end_offset + 1]
        return ret

    def get_bytes(self, buff, end_offset, start_offset=None):
        if start_offset is None or start_offset >= end_offset:
            return [buff.raw[end_offset]]
        return buff.raw[start_offset: end_offset + 1]

    def set_bytes(self, buff, end_offset, start_offset=None, src_data=None, data_len=None):
        if src_data is None:
            if start_offset is None or start_offset >= end_offset:
                buff.raw[end_offset] = 0x0
            else:
                buff[start_offset: end_offset + 1] = [chr(0)] * (end_offset + 1 - start_offset)
        else:
            if start_offset is None or start_offset >= end_offset:
                buff[end_offset] = chr(src_data[0])
            else:
                if data_len < end_offset + 1 - start_offset:
                    buff[start_offset: start_offset + data_len] = [chr(item) for item in src_data]
                else:
                    buff[start_offset: end_offset + 1] = [chr(item) for item in src_data[: end_offset + 1 - start_offset]]

    def get_word(self, buff, offset):
        if offset % 2 != 0:
            raise Exception("Invalid offset, offset should be multiple of 2, acutal is {}".format(offset))
        return ord(buff[offset]) + (ord(buff[offset + 1]) << 8)

    def set_word(self, buff, offset, src_data):
        if offset % 2 != 0:
            raise Exception("Invalid offset, offset should be multiple of 2, acutal is {}".format(offset))
        buff[offset: offset + 2] = [chr(src_data & 0xFF), chr((src_data >> 8) & 0xFF)]

    def get_dword(self, buff, offset):
        if offset % 4 != 0:
            raise Exception("Invalid offset, offset should be multiple of 4, acutal is {}".format(offset))
        return ord(buff[offset]) + (ord(buff[offset + 1]) << 8) + (ord(buff[offset + 2]) << 16) + (ord(buff[offset + 3]) << 24)

    def set_dword(self, buff, offset, src_data):
        if offset % 4 != 0:
            raise Exception("Invalid offset, offset should be multiple of 4, acutal is {}".format(offset))
        buff[offset: offset + 4] = [chr(src_data & 0xFF), chr((src_data >> 8) & 0xFF), chr((src_data >> 16) & 0xFF), chr((src_data >> 24) & 0xFF)]

    def dump_data(self, buff):
        print_content = "Data dump:"
        for idx in range(len(buff.raw)):
            if idx % 0x10 == 0:
                print_content += "\n{:08X}h: {:02X} ".format(idx, ord(buff.raw[idx]))
            else:
                print_content += "{:02X} ".format(ord(buff.raw[idx]))
        if self.test_instance is not None:
            self.test_instance.logger.info(print_content)
        else:
            print(print_content)

if __name__ == "__main__":
    ins = Buffer(None)
    data = ins.create_buffer(size=1024, description="1K buffer", src_data=[0xA5]*512)
    ins.dump_data(data.buff)
    ins.set_bytes(data.buff, 0x20, 0x15, [0x65, 0x66, 0x67, 0x68, 0x69, 0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x80], 16)
    ins.dump_data(data.buff)
    print(ins.get_bytes(data.buff, 0x20, 0x15))
    ins.set_word(data.buff, 0x66, 0x4567)
    print(hex(ins.get_word(data.buff, 0x66)))
    ins.set_dword(data.buff, 0x80, 0xA4A5A6A7)
    print(hex(ins.get_dword(data.buff, 0x80)))
    ins.dump_data(data.buff)
