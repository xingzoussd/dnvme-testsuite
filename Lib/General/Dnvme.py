#!usr/bin/python
# -*- coding: UTF-8 -*-
###################################################################
# All Contents Copyright 2022- for Xing Zou. All Rights Reserved.
# FileName: Dnvme.py
# Auther: Xing Zou
# Date: Jul-17-2022
# Description: For dnvme interface with c lib.
###################################################################

import os
import sys
import re
import ctypes
from exceptions import Exception

class Dnvme(object):
    def __init__(self, test_instance):
        self.test_instance = test_instance
        self.clib = ctypes.cdll.LoadLibrary(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dnvme.so'))
        self.device_handle = None
        self.function_status = [
            "SUCCESS",
            "MALLOC BUFFER ERROR",
            "CREATE ADMIN CQ BUFFER ERROR",
            "CREATE ADMIN SQ BUFFER ERROR",
            "DISABLE CONTROLLER ERROR",
            "ENABLE IRQ ERROR",
            "CREATE ADMIN CQ ERROR",
            "CREATE ADMIN SQ ERROR",
            "ENABLE CONTROLLER ERROR",
        ]
        self.identify_ctrl_buffer_size = 4096

    def init_drive(self):
        self.device_handle = self.clib.open_dev("/dev/nvme0")
        if self.device_handle < 0:
            raise Exception("Open nvme device failed, error code: {}".format(self.device_handle))
        err_code = self.clib.init_drive(self.device_handle)
        if err_code != 0:
            raise Exception("Init drive get error: {}".format(self.function_status[err_code]))

    def identify_controller(self, nsid=0xFFFFFFFF, ctrl_id=0):
        buffer_obj = self.test_instance.lib.Buffer(self.test_instance)
        identify_buffer = buffer_obj.create_buffer(size=self.identify_ctrl_buffer_size, description="controller data")
        self.clib.dnvme_admin_identify_ctrl(self.device_handle, nsid, ctrl_id, identify_buffer.buff)
        buffer_obj.dump_data(identify_buffer.buff)
