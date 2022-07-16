#!usr/bin/python
# -*- coding: UTF-8 -*-
###################################################################
# All Contents Copyright 2022- for Xing Zou. All Rights Reserved.
# FileName: ShellCmd.py
# Auther: Xing Zou 
# Date: Jul-16-2022
# Description: For running linux shell commands.
###################################################################

import subprocess
import re

class ShellCmd(object):
    def __init__(self, test_instance):
        self.test_instance = test_instance

    def execute(self, cmd):
        subp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) #, encoding="utf-8")
        out = subp.communicate()
        return out

    def lspci(self, keywords):
        cmd = "lspci -tv | grep {}".format(keywords)
        out = self.execute(cmd)
        pattern = "\+-(?P<slot>[0-9a-f]+\.[0-9a-f]+)-\[(?P<device>[0-9a-f]+)\]"
        matched = re.search(pattern, out[0], re.I)
        slot_bdf = None
        drive_bdf = None
        if matched:
            slot_bdf = "00:{}".format(matched.group("slot"))
            drive_bdf = "{}:00.0".format(matched.group("device"))
        return slot_bdf, drive_bdf
