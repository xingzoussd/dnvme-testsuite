#!usr/bin/python
# -*- coding: UTF-8 -*-
###################################################################
# All Contents Copyright 2022- for Xing Zou. All Rights Reserved.
# FileName: TestBase.py
# Auther: Xing Zou
# Date: Jul-16-2022
# Description: For linux command test.
###################################################################

import os
import sys
#sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))
import TestInstance

class LinuxCmd(TestInstance.TestInstance):
    def __init__(self):
        super(LinuxCmd, self).__init__()
        self.shell = self.lib.ShellCmd(self)

    def add_arguments(self):
        super(LinuxCmd, self).add_arguments()
        self.parser.add_argument('--loop', default=3, type=int, help='Loop count for this test')

    def initialize(self):
        super(LinuxCmd, self).initialize()
        self.logger.info("Execute initialize.")

    def test(self):
        super(LinuxCmd, self).test()
        self.logger.info("Execute Test.")
        for loop in range(self.args.loop):
            self.logger.info("=========================({0}/{1})=========================".format(loop+1, self.args.loop))
            slot_bdf, drive_bdf = self.shell.lspci("Micron")
            self.logger.info("SLOT BDF: {}, DRIVE BDF:{}".format(slot_bdf, drive_bdf))

    def cleanup(self):
        self.logger.info("Execute Cleanup.")
        super(LinuxCmd, self).cleanup()

if __name__ == "__main__":
    ins = LinuxCmd()
    ins.run()
