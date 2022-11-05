#!usr/bin/python
#
# -*- coding: UTF-8 -*-
# FileName: NvmeCommands.py
# Auther: Xing Zou
# Date: Jan-02-2022
# Description: Create test lib for NVMe commands.
#

import os
import sys
from collections import *

class NvmeCommands(object):
    def __init__(self, test_instance):
        self.test_instance = test_instance
        self.dnvme = self.test_instance.dut
        self.id_ctrl_data_len = 4096
        self.admin_opcode_dict = {
            "DELETE_IO_SUBMISSION_QUEUE":                       0X0,
            "CREATE_IO_SUBMISSION_QUEUE":                       0X1,
            "GET_LOG_PAGE":                                     0X2,
            "DELETE_IO_COMPLETION_QUEUE":                       0X4,
            "CREATE_IO_COMPLETION_QUEUE":                       0X5,
            "IDENTIFY":                                         0X6,
            "ABORT":                                            0X8,
            "SET_FEATURES":                                     0X9,
            "GET_FEATURES":                                     0XA,
            "ASYNCHRONOUS_EVENT_REQUEST":                       0XC,
            "NAMESPACE_MANAGEMENT":                             0XD,
            "FIRMWARE_COMMIT":                                  0X10,
            "FIRMWARE_IMAGE_DOWNLOAD":                          0X11,
            "DEVICE_SELF_TEST":                                 0X14,
            "NAMESPACE_ATTACHMENT":                             0X15,
            "KEEP_ALIVE":                                       0X18,
            "DIRECTIVE_SEND":                                   0X19,
            "DIRECTIVE_RECEIVE":                                0X1A,
            "VIRTUALIZATION_MANAGEMENT":                        0X1C,
            "NVME_MI_SEND":                                     0X1D,
            "NVME_MI_RECEIVE":                                  0X1E,
            "DOORBELL_BUFFER_CONFIG":                           0X7C,
        }
        self.admin_cmd_dict = OrderedDict()
        self.admin_cmd_dict["CREATE_IOCQ"] = self.create_io_completion_queue
        self.admin_cmd_dict["CREATE_IOSQ"] = self.create_io_submission_queue
        self.admin_cmd_dict["DELETE_IOSQ"] = self.delete_io_submission_queue
        self.admin_cmd_dict["DELETE_IOCQ"] = self.delete_io_completion_queue
        self.features_id_dict = {
            "ARBITRATION":                                      0x1,
            "POWER_MANAGEMENT":                                 0x2,
            "LBA_RANGE_TYPE":                                   0x3,
            "TEMPERATURE_THRESHOLD":                            0x4,
            "ERROR_RECOVERY":                                   0x5,
            "VOLATILE_WRITE_CACHE":                             0x6,
            "NUMBER_OF_QUEUES":                                 0x7,
            "INTERRUPT_COALESCING":                             0x8,
            "INTERRUPT_VECTOR_CONFIGURATION":                   0x9,
            "WRITE_ATOMICITY_NORMAL":                           0xA,
            "ASYNCHRONOUS_EVENT_CONFIGURATION":                 0xB,
            "AUTONOMOUS_POWER_STATE_TRANSITION":                0xC,
            "HOST_MEMORY_BUFFER":                               0xD,
            "TIMESTAMP":                                        0xE,
            "KEEP_ALIVE_TIMER":                                 0xF,
            "HOST_CONTROLLED_THERMAL_MANAGEMENT":               0x10,
            "NON_OPERATIONAL_POWER_STATE_CONFIG":               0x11,
            "READ_RECOVERY_LEVEL_CONFIG":                       0x12,
            "PREDICTABLE_LATENCY_MODE_CONFIG":                  0x13,
            "PREDICTABLE_LATENCY_MODE_WINDOW":                  0x14,
            "LBA_STATUS_INFORMATION_REPORT_INTERVAL":           0x15,
            "HOST_BEHAVIOR_SUPPORT":                            0x16,
            "SANITIZE_CONFIG":                                  0x17,
            "ENDURANCE_GROUP_EVENT_CONFIGURATION":              0x18,
        }

    def delete_io_submission_queue(self, qid=1, nsid=0):
        pass
        # self.testInstance.dut.send_cmd(opcode=self.admin_opcode_dict["Delete IO Submission Queue"],
        #                                buf=None,
        #                                nsid=nsid,
        #                                cdw10=cdw10,
        #                                cdw11=0,
        #                                cdw12=0,
        #                                cdw13=0,
        #                                cdw14=0,
        #                                cdw15=0,
        #                                cb=cb).waitdone()
        # self.testInstance.logger.info("CDW0: 0x{:08X}, SQID: 0x{:04X}, SQ Head: 0x{:04X}, Phase Tag: {}, status: 0x{:04X}.".format(
        #     cdw0, sqid, sqhead, p, status))

    def create_io_submission_queue(self, qid=1, cqid=1, buf=None, qsize=4096, qprio=1, pc=1, nsid=0, nvmsetid=0, cb=None):
        pass
        # self.testInstance.dut.send_cmd(opcode=self.admin_opcode_dict["Create IO Submission Queue"],
        #                                buf=buf,
        #                                nsid=nsid,
        #                                cdw10=cdw10,
        #                                cdw11=cdw11,
        #                                cdw12=cdw12,
        #                                cdw13=0,
        #                                cdw14=0,
        #                                cdw15=0,
        #                                cb=cb).waitdone()
        # self.testInstance.logger.info("CDW10: 0x{:08X}, SQID: 0x{:04X}, SQ Head: 0x{:04X}, Phase Tag: {}, status: 0x{:04X}.".format(
        #     cdw0, sqid, sqhead, p, status))

    def delete_io_completion_queue(self, qid=1, nsid=0, cb=None):
        pass
        # self.testInstance.dut.send_cmd(opcode=self.admin_opcode_dict["Delete IO Completion Queue"],
        #                                buf=None,
        #                                nsid=nsid,
        #                                cdw10=cdw10,
        #                                cdw11=0,
        #                                cdw12=0,
        #                                cdw13=0,
        #                                cdw14=0,
        #                                cdw15=0,
        #                                cb=cb).waitdone()
        # self.testInstance.logger.info("CDW10: 0x{:08X}, SQID: 0x{:04X}, SQ Head: 0x{:04X}, Phase Tag: {}, status: 0x{:04X}.".format(
        #     cdw0, sqid, sqhead, p, status))

    def create_io_completion_queue(self, qid=1, buf=None, qsize=4096, iv=0, ien=0, pc=1, nsid=0, cb=None):
        pass
        # self.testInstance.dut.send_cmd(opcode=self.admin_opcode_dict["Create IO Completion Queue"],
        #                                buf=buf,
        #                                nsid=nsid,
        #                                cdw10=cdw10,
        #                                cdw11=cdw11,
        #                                cdw12=0,
        #                                cdw13=0,
        #                                cdw14=0,
        #                                cdw15=0,
        #                                cb=cb).waitdone()
        # self.testInstance.logger.info("CDW10: 0x{:08X}, SQID: 0x{:04X}, SQ Head: 0x{:04X}, Phase Tag: {}, status: 0x{:04X}.".format(
        #     cdw0, sqid, sqhead, p, status))

    def identify(self, nsid=0, cns=1, cntid=0, csi=0, nvmsetid=0, uuid_idx=0):
        pass
        # self.testInstance.dut.identify(buf, nsid=nsid, cns=cns, cntid=cntid, csi=csi, nvmsetid=nvmsetid, cb=cb).waitdone()

    def get_feature(self, fid, sel=0, buf=None, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, cb=None):
        pass

    def set_feature(self, fid, sv=0, buf=None, cdw11=0, cdw12=0, cdw13=0, cdw14=0, cdw15=0, cb=None):
        pass
