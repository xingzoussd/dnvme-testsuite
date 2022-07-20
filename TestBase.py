#!usr/bin/python
# -*- coding: UTF-8 -*-
###################################################################
# All Contents Copyright 2022- for Xing Zou. All Rights Reserved.
# FileName: TestBase.py
# Auther: Xing Zou
# Date: Jul-16-2022
# Description: For test base function define.
###################################################################

import imp
import os
import logging
import argparse
import pdb
import traceback
import time
import LibLoader

class TestBase(object):
    def __init__(self):
        self.status_pass = "STATUS_PASS"
        self.status_fail = "STATUS_FAIL"
        self.status_skip = "STATUS_SKIP"
        self.test_status = self.status_pass
        self.time_start = time.time()
        try:
            self.add_arguments()
            self.args = self.parser.parse_args()
            self.config_logger()
            self.load_libs()
        except:
            self.error_handle()

    def add_arguments(self):
        self.parser = argparse.ArgumentParser(self.__class__.__name__)
        self.parser.add_argument('--do_pdb', default=False, type=bool, help='if enter pdb when fail')
        self.parser.add_argument('--log_file', default="/var/log/log.txt", type=str, help='the log to save')

    def config_logger(self):
        formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        # self.logger.propagate = False
        # self.logger.setFormatter(formatter)
        if os.path.exists(self.args.log_file):
            backupPath = "{0}.1".format(self.args.log_file)
            if os.path.exists(backupPath):
                os.remove(backupPath)
            os.rename(self.args.log_file, backupPath)
        handler = logging.FileHandler(self.args.log_file)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.addHandler(console)

    def load_libs(self):
        currentPath = os.path.dirname(os.path.realpath(__file__))
        libPath = os.path.join(currentPath, "Lib/General")
        if os.path.exists(libPath):
            files = os.listdir(libPath)
            libFiles = list()
            for f in files:
                fullPath = os.path.join(libPath, f)
                fileNameWithoutExt = os.path.splitext(f)[0]
                fileExt = os.path.splitext(f)[1]
                if os.path.isfile(fullPath) and fileExt == ".py" and fileNameWithoutExt != "__init__":
                    libFiles.append(fullPath)
            libs = LibLoader.LibLoader(self)
            self.lib = libs.load_libs(libFiles)

    def initialize(self):
        pass

    def test(self):
        pass

    def cleanup(self):
        self.timeDuration = time.time() - self.time_start
        self.logger.info("{} duration: {:.02f} seconds.".format(self.__class__.__name__, self.timeDuration))
        self.logger.info("{} STATUS: {}.".format(self.__class__.__name__, self.test_status))

    def error_handle(self):
        self.test_status = self.status_fail
        for line in traceback.format_stack():
            self.logger.info(line)
        if self.args.do_pdb:
            pdb.post_mortem()

    def run(self):
        try:
            self.initialize()
            self.test()
        except:
            self.error_handle()
        finally:
            self.cleanup()

if __name__ == "__main__":
    tb = TestBase()
    tb.run()
