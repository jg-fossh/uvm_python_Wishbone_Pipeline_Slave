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
# File name    : wb4s_monitor.py
# Author       : Jose R Garcia (jg-fossh@protonmail.com)
# Project Name : UVM Python Verification Library
# Class Name   : wb4s_monitor
# Description  : Wishbone Slave Monitor.
#
# Additional Comments:
#
##################################################################################################
import cocotb
from cocotb.triggers import *
#
from uvm.base.uvm_callback import *
from uvm.comps.uvm_monitor import UVMMonitor
from uvm.tlm1 import *
from uvm.macros import *
#
from wb4s_seq import *
from wb4s_if import *

class wb4s_monitor(UVMMonitor):
    """
       Class: Wishbone Slave Monitor

       Definition: Contains functions, tasks and methods of this agent's monitor.
    """

    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        """
           Function: new

           Definition: Class Constructor.

           Args:
             name: This agents name.
             parent: NONE
        """
        self.ap        = None
        self.vif       = None  # connected at the agent
        self.cfg       = None  # config loaded by the agent
        self.errors    = 0
        self.num_items = 0
        self.tag       = "wb4s_monitor_" + name


    def build_phase(self, phase):
        super().build_phase(phase)
        """
           Function: build_phase

           Definition:

           Args:
             phase: build_phase
        """
        self.ap = UVMAnalysisPort("ap", self)


    async def run_phase(self, phase):
        """
           Function: run_phase

           Definition: Task executed during run phase. Drives the signals in
                       response to a DUT read request.

           Args:
             phase: run_phase
        """
        while True:
            tr = None  # Clean transaction for every loop.
            # Create sequence item for this transaction.
            tr = wb4s_seq.type_id.create("tr", self)

            await RisingEdge(self.vif.clk_i)

            if (self.vif.cyc_i == 1 and self.vif.stb_i == 1 and self.vif.stall_o == 0):
                # Load signals values into sequence item to describe the transaction
                tr.address     = self.vif.adr_i.value.integer
                tr.data_in     = self.vif.dat_i.value.integer
                tr.select      = self.vif.sel_i.value.integer
                tr.cycle       = self.vif.cyc_i.value.integer
                tr.strobe      = self.vif.stb_i.value.integer
                tr.address_tag = self.vif.tga_i.value.integer
                tr.data_tag    = self.vif.tgd_i.value.integer
                tr.cycle_tag   = self.vif.tgc_i.value.integer
                
                if (self.vif.we_i == 0):
                    while(self.vif.cyc_i == 1 or self.vif.ack_o == 0):
                        await RisingEdge(self.vif.clk_i)
                    #await RisingEdge(self.vif.ack_o) # wait for read response
                    #tr.data_tag    = self.vif.tgd_o.value.integer
                    #tr.data_out    = self.vif.dat_o.value.integer

                # Load response values into sequence item to describe the transaction
                #tr.data_in     = self.vif.dat_i.value.integer
                tr.data_tag    = self.vif.tgd_o.value.integer
                tr.data_out    = self.vif.dat_o.value.integer
                tr.stall       = self.vif.stall_o.value.integer
                tr.acknowledge = self.vif.ack_o.value.integer

                self.num_items += 1       # Increment transactions count
                self.ap.write(tr) # Send transaction through analysis port
                uvm_info(self.tag, tr.convert2string(), UVM_FULL)
                #uvm_info(self.tag, tr.convert2string(), UVM_NONE)


uvm_component_utils(wb4s_monitor)
