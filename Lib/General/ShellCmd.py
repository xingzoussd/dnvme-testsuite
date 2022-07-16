#!usr/bin/python
# -*- coding: UTF-8 -*-
###################################################################
# All Contents Copyright 2022- for Xing Zou. All Rights Reserved.
# FileName: ShellCmd.py
# Auther: Xing Zou 
# Date: Jul-16-2022
# Description: For running linux shell commands.
###################################################################

import os
import subprocess
import re
from exceptions import Exception

class ShellCmd(object):
    def __init__(self, test_instance):
        self.test_instance = test_instance

    def execute(self, cmd):
        subp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) #, encoding="utf-8")
        out = subp.communicate()
        if out[1] != "":
            raise Exception("Command {} return code: {}".format(cmd, out[1]))
        return out[0]

    def lspci(self, keywords):
        cmd = "lspci -tv | grep {}".format(keywords)
        result = self.execute(cmd)
        pattern = "\+-(?P<slot>[0-9a-f]+\.[0-9a-f]+)-\[(?P<device>[0-9a-f]+)\]"
        matched = re.search(pattern, result, re.I)
        slot_bdf = None
        drive_bdf = None
        if matched:
            slot_bdf = "00:{}".format(matched.group("slot"))
            drive_bdf = "{}:00.0".format(matched.group("device"))
        return slot_bdf, drive_bdf

    def list_module(self, driver_name="nvme"):
        cmd = "sudo lsmod | grep {}".format(driver_name)
        result = self.execute(cmd)
        rows = result.split("\n")
        driver_modules = []
        for row in rows:
            module = row.split(' ')[0]
            if re.match(driver_name, module):
                driver_modules.append(module)
        if len(driver_modules) > 0:
            return True
        return False

    def remove_driver(self, driver_name="nvme"):
        if driver_name == "nvme":
            cmd = "sudo rmmod nvme"
            self.execute(cmd)
            cmd = "sudo rmmod nvme_core"
            self.execute(cmd)
        elif driver_name == "dnvme":
            cmd = "sudo rmmod dnvme"
            self.execute(cmd)
        else:
            raise Exception("Unknown nvme driver: {}".format(driver_name))

    def identify_driver(self):
        if self.list_module("dnvme"):
            driver = "dnvme"
        elif self.list_module("nvme"):
            driver = "nvme"
        else:
            driver = "unknown"
        return driver

    def install_driver(self, driver_name="nvme"):
        if driver_name == "nvme":
            driver_path = "/usr/src/kernels/3.10.0-1062.el7.x86_64/drivers/nvme/host"
            cmd = "sudo insmod {}".format(os.path.join(driver_path, "nvme-core.ko"))
            self.execute(cmd)
            cmd = "sudo insmod {}".format(os.path.join(driver_path, "nvme.ko"))
            self.execute(cmd)
        elif driver_name == "dnvme":
            driver_path = "/home/xingzou/work/github/dnvme"
            cmd = "sudo insmod {}".format(os.path.join(driver_path, "dnvme.ko"))
            self.execute(cmd)
        else:
            raise Exception("Unknown driver.")
