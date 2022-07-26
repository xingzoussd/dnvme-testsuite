#!usr/bin/python
# -*- coding: UTF-8 -*-
###################################################################
# All Contents Copyright 2022- for Xing Zou. All Rights Reserved.
# FileName: Identify.py
# Auther: Xing Zou
# Date: Jul-19-2022
# Description: For identify data structure.
###################################################################

import os
import sys
from collections import *

class Identify(object):
    def __init__(self, test_instance):
        self.test_instance = test_instance

    def controller_data(self, buffer_obj, verbose=True):
        id_ctrl_data = OrderedDict()
        id_ctrl_data["VID"] = buffer_obj.data(1, 0)
        id_ctrl_data["SSVID"] = buffer_obj.data(3, 2)
        id_ctrl_data["SN"] = buffer_obj.data(23, 4, str)
        id_ctrl_data["MN"] = buffer_obj.data(63, 24, str)
        id_ctrl_data["FR"] = buffer_obj.data(71, 64, str)
        id_ctrl_data["RAB"] = buffer_obj.data(72)
        id_ctrl_data["IEEE"] = buffer_obj.data(75, 73)
        id_ctrl_data["CMIC"] = {"ANAR Support": (buffer_obj.data(76) >> 3) & 1,
                                "SR-IOV": (buffer_obj.data(76) >> 2) & 1,
                                "Multi CTRL": (buffer_obj.data(76) >> 1) & 1,
                                "Multi NSS": buffer_obj.data(76) & 1}
        id_ctrl_data["MDTS"] = buffer_obj.data(77)
        id_ctrl_data["CNTLID"] = buffer_obj.data(79, 78)
        id_ctrl_data["VER"] = buffer_obj.data(83, 80)
        id_ctrl_data["RTD3R"] = buffer_obj.data(87, 84)
        id_ctrl_data["RTD3E"] = buffer_obj.data(91, 88)
        id_ctrl_data["OAES"] = {"EGEALPCN Support": (buffer_obj.data(95, 92) >> 14) & 1,
                                "LSIN Support": (buffer_obj.data(95, 92) >> 13) & 1,
                                "PLEALCN Support": (buffer_obj.data(95, 92) >> 12) & 1,
                                "ANACN Support": (buffer_obj.data(95, 92) >> 11) & 1,
                                "FAN Support": (buffer_obj.data(95, 92) >> 9) & 1,
                                "NAN Support": (buffer_obj.data(95, 92) >> 8) & 1}
        id_ctrl_data["CTRATT"] = {"UUID List Support": (buffer_obj.data(99, 96) >> 9) & 1,
                                  "SQA Support": (buffer_obj.data(99, 96) >> 8) & 1,
                                  "NG Support": (buffer_obj.data(99, 96) >> 7) & 1,
                                  "TBKA Support": (buffer_obj.data(99, 96) >> 6) & 1,
                                  "PLM Support": (buffer_obj.data(99, 96) >> 5) & 1,
                                  "EG Support": (buffer_obj.data(99, 96) >> 4) & 1,
                                  "RRL Support": (buffer_obj.data(99, 96) >> 3) & 1,
                                  "NVM Sets Support": (buffer_obj.data(99, 96) >> 2) & 1,
                                  "NOPS Support": (buffer_obj.data(99, 96) >> 1) & 1,
                                  "128b Host ID Support": buffer_obj.data(99, 96) & 1}
        id_ctrl_data["RRLS"] = buffer_obj.data(101, 100)
        id_ctrl_data["CNTRLTYPE"] = buffer_obj.data(111)
        id_ctrl_data["FGUID"] = buffer_obj.data(127, 112)
        id_ctrl_data["CRDT1"] = buffer_obj.data(129, 128)
        id_ctrl_data["CRDT2"] = buffer_obj.data(131, 130)
        id_ctrl_data["CRDT3"] = buffer_obj.data(133, 132)
        id_ctrl_data["OACS"] = {"Get LBA Status": (buffer_obj.data(257, 256) >> 9) & 1,
                                "Doorbell Buffer Config": (buffer_obj.data(257, 256) >> 8) & 1,
                                "Virtualization Management": (buffer_obj.data(257, 256) >> 7) & 1,
                                "NVMe-MI Send/Receive": (buffer_obj.data(257, 256) >> 6) & 1,
                                "Directive Send/Receive": (buffer_obj.data(257, 256) >> 5) & 1,
                                "Device Self Test": (buffer_obj.data(257, 256) >> 4) & 1,
                                "Namespace Management": (buffer_obj.data(257, 256) >> 3) & 1,
                                "Firmware Commit/Download": (buffer_obj.data(257, 256) >> 2) & 1,
                                "Format NVM": (buffer_obj.data(257, 256) >> 1) & 1,
                                "Security Send/Receive": buffer_obj.data(257, 256) & 1}
        id_ctrl_data["ACL"] = buffer_obj.data(258)
        id_ctrl_data["AERL"] = buffer_obj.data(259)
        id_ctrl_data["FRMW"] = {"Without Reset": (buffer_obj.data(260) >> 4) & 1,
                                "Firmware Slots": (buffer_obj.data(260) >> 1) & 0x7,
                                "First Slot Readonly": buffer_obj.data(260) & 1}
        id_ctrl_data["LPA"] = {"Persistent Event": (buffer_obj.data(261) >> 4) & 1,
                               "Telemetry Host/Controller Initiated": (buffer_obj.data(261) >> 3) & 1,
                               "Extended Data": (buffer_obj.data(261) >> 2) & 1,
                               "Effects Log Page": (buffer_obj.data(261) >> 1) & 1,
                               "SMART/Health Information": buffer_obj.data(261) & 1}
        id_ctrl_data["ELPE"] = buffer_obj.data(262)
        id_ctrl_data["NPSS"] = buffer_obj.data(263)
        id_ctrl_data["AVSCC"] = buffer_obj.data(264)
        id_ctrl_data["APSTA"] = buffer_obj.data(265)
        id_ctrl_data["WCTEMP"] = buffer_obj.data(267, 266)
        id_ctrl_data["CCTEMP"] = buffer_obj.data(269, 268)
        id_ctrl_data["MTFA"] = buffer_obj.data(271, 270)
        id_ctrl_data["MMPRE"] = buffer_obj.data(275, 272)
        id_ctrl_data["MMMIN"] = buffer_obj.data(279, 276)
        id_ctrl_data["TNVMCAP"] = buffer_obj.data(295, 280, str)
        id_ctrl_data["UNVMCAP"] = buffer_obj.data(311, 296, str)
        id_ctrl_data["RPMBS"] = {"Access Size": (buffer_obj.data(315, 312) >> 24) & 0xF,
                                 "Total Size": (buffer_obj.data(315, 312) >> 16) & 0xF,
                                 "Authentication Method": (buffer_obj.data(315, 312) >> 3) & 0x7,
                                 "Number of RPMB Units": buffer_obj.data(315, 312) & 0x7}
        id_ctrl_data["EDSTT"] = buffer_obj.data(317, 316)
        id_ctrl_data["DSTO"] = buffer_obj.data(318)
        id_ctrl_data["FWUG"] = buffer_obj.data(319)
        id_ctrl_data["KAS"] = buffer_obj.data(321, 320)
        id_ctrl_data["HCTMA"] = buffer_obj.data(323, 322)
        id_ctrl_data["MNTMT"] = buffer_obj.data(325, 324)
        id_ctrl_data["MXTMT"] = buffer_obj.data(327, 326)
        id_ctrl_data["SANICAP"] = {"NODMMAS": (buffer_obj.data(331, 328) >> 30) & 0x3,
                                   "NDI": (buffer_obj.data(331, 328) >> 29) & 0x1,
                                   "OWS": (buffer_obj.data(331, 328) >> 2) & 0x1,
                                   "BES": (buffer_obj.data(331, 328) >> 1) & 0x1,
                                   "CES": buffer_obj.data(331, 328) & 0x1}
        id_ctrl_data["HMMINDS"] = buffer_obj.data(335, 332)
        id_ctrl_data["HMMAXD"] = buffer_obj.data(337, 336)
        id_ctrl_data["NSETIDMAX"] = buffer_obj.data(339, 338)
        id_ctrl_data["ENDGIDMAX"] = buffer_obj.data(341, 340)
        id_ctrl_data["ANATT"] = buffer_obj.data(342)
        id_ctrl_data["ANACAP"] = {"Non-Zero ANAGRPID": (buffer_obj.data(343) >> 7) & 0x1,
                                  "Not Change ANAGRPID": (buffer_obj.data(343) >> 6) & 0x1,
                                  "ANA Change state": (buffer_obj.data(343) >> 4) & 0x1,
                                  "ANA Persistent Loss state": (buffer_obj.data(343) >> 3) & 0x1,
                                  "ANA Inaccessible state": (buffer_obj.data(343) >> 2) & 0x1,
                                  "ANA Non-Optimized state": (buffer_obj.data(343) >> 1) & 0x1,
                                  "ANA Optimized state": buffer_obj.data(343) & 0x1}
        id_ctrl_data["ANAGRPMAX"] = buffer_obj.data(347, 344)
        id_ctrl_data["NANAGRPID"] = buffer_obj.data(351, 348)
        id_ctrl_data["PELS"] = buffer_obj.data(355, 352)
        id_ctrl_data["SQES"] = {"MAX": (buffer_obj.data(512) >> 4) & 0xF,
                                "Require": buffer_obj.data(512) & 0xF}
        id_ctrl_data["CQES"] = {"MAX": (buffer_obj.data(513) >> 4) & 0xF,
                                "Require": buffer_obj.data(513) & 0xF}
        id_ctrl_data["MAXCMD"] = buffer_obj.data(515, 514)
        id_ctrl_data["NN"] = buffer_obj.data(519, 516)
        id_ctrl_data["ONCS"] = {"Verify": (buffer_obj.data(521, 520) >> 7) & 0x1,
                                "Timestamp": (buffer_obj.data(521, 520) >> 6) & 0x1,
                                "Reservations": (buffer_obj.data(521, 520) >> 5) & 0x1,
                                "Save/Select in Set/Get Feature": (buffer_obj.data(521, 520) >> 4) & 0x1,
                                "Write Zeros": (buffer_obj.data(521, 520) >> 3) & 0x1,
                                "Dataset Management": (buffer_obj.data(521, 520) >> 2) & 0x1,
                                "Write Uncorrectable": (buffer_obj.data(521, 520) >> 1) & 0x1,
                                "Compare": buffer_obj.data(521, 520) & 0x1}
        id_ctrl_data["FUSES"] = buffer_obj.data(523, 522)
        id_ctrl_data["FNA"] = {"Crypto Erase": (buffer_obj.data(524) >> 2) & 0x1,
                               "Secure Erase for All Namespace": (buffer_obj.data(524) >> 1) & 0x1,
                               "Format for All Namespace": buffer_obj.data(524) & 0x1}
        id_ctrl_data["VWC"] = {"Flush Behavior": (buffer_obj.data(525) >> 1) & 0x3,
                               "Present": buffer_obj.data(525) & 0x1}
        id_ctrl_data["AWUN"] = buffer_obj.data(527, 526)
        id_ctrl_data["AWUPF"] = buffer_obj.data(529, 528)
        id_ctrl_data["NVSCC"] = buffer_obj.data(530)
        id_ctrl_data["NWPC"] = {"Permanent Write Protect": (buffer_obj.data(531) >> 2) & 0x1,
                                "Write Protect Until Power Cycle": (buffer_obj.data(531) >> 1) & 0x1,
                                "No Write Protect": buffer_obj.data(531) & 0x1}
        id_ctrl_data["ACWU"] = buffer_obj.data(533, 532)
        id_ctrl_data["SGLS"] = {"Transport SGL Data": (buffer_obj.data(539, 536) >> 21) & 0x1,
                                "Address field in SGL Data": (buffer_obj.data(539, 536) >> 20) & 0x1,
                                "MPTR Containing SGL Descriptor": (buffer_obj.data(539, 536) >> 19) & 0x1,
                                "SGL Length Larger Than Data": (buffer_obj.data(539, 536) >> 18) & 0x1,
                                "Use Aligned Contiguous Physical Buffer": (buffer_obj.data(539, 536) >> 17) & 0x1,
                                "SGL Bit Bucket Descriptor": (buffer_obj.data(539, 536) >> 16) & 0x1,
                                "Keyed SGL Data": (buffer_obj.data(539, 536) >> 2) & 0x1,
                                "SGL Support NVM Command": buffer_obj.data(539, 536) & 0x3}
        id_ctrl_data["MNAN"] = buffer_obj.data(543, 540)
        id_ctrl_data["SUBNQN"] = buffer_obj.data(1023, 768, str)
        base_offset_bytes = 2048
        for idx in range(32):
            psd_offset_bytes = base_offset_bytes + idx * 32
            psd = "PSD{}".format(idx)
            id_ctrl_data[psd] = {"MP": buffer_obj.data(psd_offset_bytes + 1, psd_offset_bytes),
                                 "MXPS": buffer_obj.data(psd_offset_bytes + 3) & 0x1,
                                 "NOPS": (buffer_obj.data(psd_offset_bytes + 3) >> 1) & 0x1,
                                 "ENLAT": buffer_obj.data(psd_offset_bytes + 7, psd_offset_bytes + 4),
                                 "EXLAT": buffer_obj.data(psd_offset_bytes + 11, psd_offset_bytes + 8),
                                 "RRT": buffer_obj.data(psd_offset_bytes + 12) & 0x1F,
                                 "RRL": buffer_obj.data(psd_offset_bytes + 13) & 0x1F,
                                 "RWT": buffer_obj.data(psd_offset_bytes + 14) & 0x1F,
                                 "RWL": buffer_obj.data(psd_offset_bytes + 15) & 0x1F,
                                 "IDLP": buffer_obj.data(psd_offset_bytes + 17, psd_offset_bytes + 16),
                                 "IPS": (buffer_obj.data(psd_offset_bytes + 18) >> 6) & 0x3,
                                 "ACTP": buffer_obj.data(psd_offset_bytes + 21, psd_offset_bytes + 20),
                                 "APW": buffer_obj.data(psd_offset_bytes + 22) & 0x7,
                                 "APS": (buffer_obj.data(psd_offset_bytes + 22) >> 6) & 0x3}


        if verbose:
            self.test_instance.logger.info("Identify controller data structure: \n{}".format(id_ctrl_data))
        return id_ctrl_data

    def namespace_data(self, buffer_obj, verbose=True):
        id_ns_data = OrderedDict()
        id_ns_data["NSZE"] = buffer_obj.data(7, 0)
        id_ns_data["NCAP"] = buffer_obj.data(15, 8)
        id_ns_data["NUSE"] = buffer_obj.data(23, 16)
        id_ns_data["NSFEAT"] = buffer_obj.data(24)
        id_ns_data["NLBAF"] = buffer_obj.data(25)
        id_ns_data["FLBAS"] = buffer_obj.data(26)
        id_ns_data["MC"] = buffer_obj.data(27)
        id_ns_data["DPC"] = buffer_obj.data(28)
        id_ns_data["DPS"] = buffer_obj.data(29)
        id_ns_data["NMIC"] = buffer_obj.data(30)
        id_ns_data["RESCAP"] = buffer_obj.data(31)
        id_ns_data["FPI"] = buffer_obj.data(32)
        id_ns_data["DLFEAT"] = buffer_obj.data(33)
        id_ns_data["NAWUN"] = buffer_obj.data(35, 34)
        id_ns_data["NAWUPF"] = buffer_obj.data(37, 36)
        id_ns_data["NACWU"] = buffer_obj.data(39, 38)
        id_ns_data["NABSN"] = buffer_obj.data(41, 40)
        id_ns_data["NABO"] = buffer_obj.data(43, 42)
        id_ns_data["NABSPF"] = buffer_obj.data(45, 44)
        id_ns_data["NOIOB"] = buffer_obj.data(47, 46)
        id_ns_data["NVMCAP"] = buffer_obj.data(63, 48)
        id_ns_data["NPWG"] = buffer_obj.data(65, 64)
        id_ns_data["NPWA"] = buffer_obj.data(67, 66)
        id_ns_data["NPDG"] = buffer_obj.data(69, 68)
        id_ns_data["NPDA"] = buffer_obj.data(71, 70)
        id_ns_data["NOWS"] = buffer_obj.data(73, 72)
        id_ns_data["ANAGRPID"] = buffer_obj.data(95, 92)
        id_ns_data["NSATTR"] = buffer_obj.data(99)
        id_ns_data["NVMSETID"] = buffer_obj.data(101, 100)
        id_ns_data["ENDGID"] = buffer_obj.data(103, 102)
        id_ns_data["NGUID"] = buffer_obj.data(119, 104)
        id_ns_data["EUI64"] = buffer_obj.data(127, 120)
        base_offset_bytes = 128
        for idx in range(16):
            lbaf_offset_bytes = base_offset_bytes + idx * 4
            lbaf = "LBAF{}".format(idx)
            id_ns_data[lbaf] = {"MS": buffer_obj.data(lbaf_offset_bytes + 1, lbaf_offset_bytes),
                                "LBADS": buffer_obj.data(lbaf_offset_bytes + 2),
                                "RP": buffer_obj.data(lbaf_offset_bytes + 3)}

        if verbose:
            self.test_instance.logger.info("Identify namespace data structure: \n{}".format(id_ns_data))
        return id_ns_data

