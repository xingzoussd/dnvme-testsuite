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
import time
from exceptions import Exception
from collections import *

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
        self.identify_ns_buffer_size = 4096
        self.admin_opcode_dict = {
            "Delete IO Submission Queue":                       0x0,
            "Create IO Submission Queue":                       0x1,
            "Get Log Page":                                     0x2,
            "Delete IO Completion Queue":                       0x4,
            "Create IO Completion Queue":                       0x5,
            "Identify":                                         0x6,
            "Abort":                                            0x8,
            "Set Features":                                     0x9,
            "Get Features":                                     0xA,
            "Asynchronous Event Request":                       0xC,
            "Namespace Management":                             0xD,
            "Firmware Commit":                                  0x10,
            "Firmware Image Download":                          0x11,
            "Device Self Test":                                 0x14,
            "Namespace Attachment":                             0x15,
            "Keep Alive":                                       0x18,
            "Directive Send":                                   0x19,
            "Directive Receive":                                0x1A,
            "Virtualization Management":                        0x1C,
            "NVMe MI Send":                                     0x1D,
            "NVMe MI Receive":                                  0x1E,
            "Doorbell Buffer Config":                           0x7C
        }
        self.sq_unit_size = 64
        self.cq_unit_size = 16
        self.admin_cmd_dict = OrderedDict()
        self.admin_cmd_dict["Create IOCQ"] = self.create_iocq
        self.admin_cmd_dict["Create IOSQ"] = self.create_iosq
        self.admin_cmd_dict["Delete IOSQ"] = self.delete_iosq
        self.admin_cmd_dict["Delete IOCQ"] = self.delete_iocq
        self.features_id_dict = {
            "Arbitration":                                      0x1,
            "Power Management":                                 0x2,
            "LBA Range Type":                                   0x3,
            "Temperature Threshold":                            0x4,
            "Error Recovery":                                   0x5,
            "Volatile Write Cache":                             0x6,
            "Number of Queues":                                 0x7,
            "Interrupt Coalescing":                             0x8,
            "Interrupt Vector Configuration":                   0x9,
            "Write Atomicity Normal":                           0xA,
            "Asynchronous Event Configuration":                 0xB,
            "Autonomous Power State Transition":                0xC,
            "Host Memory Buffer":                               0xD,
            "Timestamp":                                        0xE,
            "Keep Alive Timer":                                 0xF,
            "Host Controlled Thermal Management":               0x10,
            "Non-Operational Power State Config":               0x11,
            "Read Recovery Level Config":                       0x12,
            "Predictable Latency Mode Config":                  0x13,
            "Predictable Latency Mode Window":                  0x14,
            "LBA Status Information Report Interval":           0x15,
            "Host Behavior Support":                            0x16,
            "Sanitize Config":                                  0x17,
            "Endurance Group Event Configuration":              0x18
        }

    def init_drive(self):
        self.device_handle = self.clib.open_dev("/dev/nvme0")
        if self.device_handle < 0:
            raise Exception("Open nvme device failed, error code: {}".format(self.device_handle))
        err_code = self.clib.init_drive(self.device_handle)
        if err_code != 0:
            raise Exception("Init drive get error: {}".format(self.function_status[err_code]))

    def create_buffer(self, size, count):
        return self.clib.create_buffer(size, count)

    def dump_data(self, addr, size, offset):
        return self.clib.dump_data(addr, size, offset)

    def set_data(self, addr, size, offset, value):
        self.clib.set_data(addr, size, offset, value)

    def identify_controller(self, nsid=0, ctrl_id=0):
        # import pdb
        # pdb.set_trace()
        identify_buffer = self.test_instance.lib.Buffer
        identify_buffer.create_buffer(self.identify_ctrl_buffer_size, 1, "Identify Controller")
        self.clib.dnvme_admin_identify_ctrl(self.device_handle, nsid, ctrl_id, identify_buffer.addr)
        self.clib.dnvme_ring_doorbell(self.device_handle, 0)
        self.clib.dnvme_cq_remain(self.device_handle, 0)
        time.sleep(1)
        identify_buffer.dump_data()
        return identify_buffer

    def identify_namespace(self, nsid=1, ctrl_id=0):
        identify_buffer = self.test_instance.lib.Buffer
        identify_buffer.create_buffer(self.identify_ns_buffer_size, 1, "Identify Namespace")
        self.clib.dnvme_admin_identify_ns(self.device_handle, nsid, ctrl_id, identify_buffer.addr)
        self.clib.dnvme_ring_doorbell(self.device_handle, 0)
        self.clib.dnvme_cq_remain(self.device_handle, 0)
        time.sleep(1)
        identify_buffer.dump_data()
        return identify_buffer

    def delete_iosq(self, qid=1, nsid=0, trigger_db=True):
        pass

    def create_iosq(self, qid=1, cqid=1, qsize=4096, qprio=1, contig=1, nsid=0, nvmsetid=0, trigger_db=True):
        iosq_buffer = self.clib.create_buffer(self.sq_unit_size, qsize)
        self.clib.dnvme_admin_create_iosq(self.device_handle, 0, qid, cqid, qsize, contig, iosq_buffer, qprio, nvmsetid)
        if trigger_db:
            self.clib.dnvme_ring_doorbell(self.device_handle, 0)
            ret = self.clib.dnvme_cq_reap(self.device_handle, 0, cq_remaining, cq_buffer, cq_buffer_size);
            if ret:
                return ret

    def delete_iocq(self, qid=1, nsid=0, trigger_db=True):
        pass

    def create_iocq(self, qid=1, buf=None, qsize=4096, iv=0, ien=0, pc=1, nsid=0, trigger_db=True):
        pass

