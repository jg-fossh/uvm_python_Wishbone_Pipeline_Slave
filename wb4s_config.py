##################################################################################################
# BSD 3-Clause License
# 
# Copyright (c) 2022, Jose R. Garcia
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##################################################################################################
# File name    : wb4s_config.py
# Author       : Jose R Garcia (jg-fossh@protonmail.com)
# Project Name : UVM-Python Verification Library
# Class Name   : wb4s_config
# Description  : Wishbone Bus Master Agent configuration object.
#
# Additional Comments:
#
##################################################################################################
from uvm.base.uvm_object import *
from uvm.macros import *
from wb4s_if import *

class wb4s_config(UVMObject):
    """         
       Class: Wishbone Master Agent Config
        
       Definition: Configuration of this agent.
    """

    
    def __init__(self, name="wb4s_config"):
        super().__init__(name)
        """         
           Function: new
          
           Definition: Config constructor.

           Args:
             name: This agents name.
             parent: NONE
        """
        self.vif              = None # wb4s_if
        self.has_driver       = None
        self.has_monitor      = None


    def build_phase(self, phase):
        """         
           Function: build_phase
          
           Definition: Create all its components.

           Args:
             phase: build_phase
        """
        self.vif = wb4s_if.type_id.create("vif", self)


uvm_object_utils(wb4s_config)