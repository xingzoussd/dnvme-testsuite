#!usr/bin/python
# -*- coding: UTF-8 -*-
###################################################################
# All Contents Copyright 2022- for Xing Zou. All Rights Reserved.
# FileName: TestBase.py
# Auther: Xing Zou
# Date: Jul-16-2022
# Description: For libraries loading.
###################################################################

import os
import imp

class LibLoader(object):
    def __init__(self, test_instance):
        self.test_instance = test_instance

    def load_libs(self, lib_files):
        for lib in lib_files:
            module_name = os.path.basename(lib).split(".")[0]
            module_folder = os.path.dirname(lib)
            fp, pathname, description = imp.find_module(module_name, [module_folder])
            module = imp.load_module(module_name, fp, pathname, description)
            setattr(self.test_instance, module_name, getattr(module, module_name))
        return self.test_instance
