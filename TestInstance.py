#!usr/bin/python
# -*- coding: UTF-8 -*-
###################################################################
# All Contents Copyright 2022- for Xing Zou. All Rights Reserved.
# FileName: TestInstance.py
# Auther: Xing Zou
# Date: Jul-16-2022
# Description: For test instance of nvme SSD test.
###################################################################

import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import TestBase
import Dnvme
import subprocess
import re

class TestInstance(TestBase.TestBase):
    def __init__(self):
        self.dut = Dnvme.Dnvme(self)
        super(TestInstance, self).__init__()
        self.id_ctrl_data_len = 4096
        self.vendor = "Micron"
        self.slot_bdf = None
        self.drive_bdf = None

    def add_arguments(self):
        super(TestInstance, self).add_arguments()
        self.parser.add_argument('--project', default="MTK", type=str, help='the project')
        self.parser.add_argument('--version', default="1.0", type=str, help='the project version')
        self.parser.add_argument('--build_type', default="release", type=str, help='the software build type')

    def initialize(self):
        super(TestInstance, self).initialize()
        cmd = ""
        for txt in sys.argv:
            cmd += txt + " "
        self.logger.info("Running command: {}".format(cmd))
        self.shell = self.lib.ShellCmd
        driver = self.shell.identify_driver()
        if driver == "nvme":
            self.logger.info("Remove current driver: nvme.")
            self.shell.remove_driver("nvme")
            self.logger.info("Install new driver: dnvme.")
            self.shell.install_driver("dnvme")
        elif driver != "dnvme":
            self.logger.info("Install new driver: dnvme.")
            self.shell.install_driver("dnvme")
        else:
            self.logger.info("Current driver is dnvme already.")
        self.identify = self.lib.Identify
        self.dut.init_drive()
        identify_ctrl_buffer = self.dut.identify_controller()
        self.identify_ctrl_data = self.identify.controller_data(identify_ctrl_buffer, verbose=False)
        self.logger.info("FW Revision: {}".format(self.identify_ctrl_data["FR"]))
        self.logger.info("Vendor: {:04X}".format(self.identify_ctrl_data["VID"]))
        self.logger.info("Subsystem Vendor: {:04X}".format(self.identify_ctrl_data["SSVID"]))
        self.logger.info("SN: {}".format(self.identify_ctrl_data["SN"]))
        self.logger.info("MN: {}".format(self.identify_ctrl_data["MN"]))
        identify_ns_buffer = self.dut.identify_namespace()
        self.identify_ns_data = self.identify.namespace_data(identify_ns_buffer, verbose=False)
        # self.logger.info("NSZE: {}".format(self.identify_ns_data["NSZE"]))

    def test(self):
        super(TestInstance, self).test()

    def cleanup(self):
        super(TestInstance, self).cleanup()

if __name__ == "__main__":
    instance = TestInstance()
    instance.run()
