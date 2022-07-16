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
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../"))
import TestBase
import subprocess
import re

class TestInstance(TestBase.TestBase):
    def __init__(self):
        super(TestInstance, self).__init__()
        self.id_ctrl_data_len = 4096
        self.vendor = "Micron"
        self.slot_bdf = None
        self.drive_bdf = None
        self.dut = None

    def add_arguments(self):
        super(TestInstance, self).add_arguments()
        self.parser.add_argument('--project', default="MTK", type=str, help='the project')
        self.parser.add_argument('--version', default="1.0", type=str, help='the project version')
        self.parser.add_argument('--build_type', default="release", type=str, help='the software build type')

    def initialize(self):
        super(TestInstance, self).initialize()

    def test(self):
        super(TestInstance, self).test()

    def cleanup(self):
        super(TestInstance, self).cleanup()

if __name__ == "__main__":
    instance = TestInstance()
    instance.run()
