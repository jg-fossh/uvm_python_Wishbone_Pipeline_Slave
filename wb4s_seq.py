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
# File name    : wb4s_seq.py
# Author       : Jose R Garcia (jg-fossh@protonmail.com)
# Project Name : UVM Python Verification Library
# Class Name   : wb4s_seq, wb4s_base_sequence
# Description  : Wishbone Pipeline Interface Sequence Item and Sequences.
#
# Additional Comments:
#   Create read or write transaction sequences.
##################################################################################################
from uvm import *

class wb4s_seq(UVMSequenceItem):
    """         
       Class: Wishbone Pipeline Master Sequence Item
        
       Definition: Contains functions, tasks and methods of this
    """

    def __init__(self, name="wb4s_seq"):
        super().__init__(name)
        self.data_in        = 0 
        self.data_out       = 0 
        self.address        = 0 
        self.select         = 0 
        self.we             = 0 
        self.strobe         = 0
        self.acknowledge    = 0
        self.cycle          = 0 
        self.data_tag       = 0 
        self.address_tag    = 0
        self.cycle_tag      = 0
        self.transmit_delay = 0 
        

    def do_copy(self, rhs):
        self.data_in        = rhs.data_in       
        self.data_out       = rhs.data_out      
        self.address        = rhs.address       
        self.select         = rhs.select        
        self.we             = rhs.we        
        self.strobe         = rhs.strobe        
        self.cycle          = rhs.cycle         
        self.data_tag       = rhs.data_tag      
        self.address_tag    = rhs.address_tag   
        self.cycle_tag      = rhs.cycle_tag
        self.acknowledge    = rhs.acknowledge
        self.transmit_delay = rhs.transmit_delay


    def do_clone(self):
        new_obj = wb4s_seq()
        new_obj.copy(self)
        return new_obj

    def compare(self, rhs):
        if (self.data_in        == rhs.data_in and
            self.data_out       == rhs.data_out and
            self.address        == rhs.address and
            self.select         == rhs.select and
            self.we             == rhs.we and
            self.strobe         == rhs.strobe and
            self.cycle          == rhs.cycle and
            self.stall          == rhs.stall and
            self.data_tag       == rhs.data_tag and
            self.address_tag    == rhs.address_tag and
            self.cycle_tag      == rhs.cycle_tag and
            self.acknowledge    == rhs.acknowledge and
            self.transmit_delay == rhs.transmit_delay):
            # match
            return True
        else:
            return False

    def convert2string(self):
        return sv.sformatf("\n =================================== \
                            \n    CYC_i : %d \
                            \n    STB_i : %d \
                            \n   DATA_i : 0x%h \
                            \n    TGC_i : 0x%h \
                            \n    TGD_i : 0x%h \
                            \n    ACK_i : %d \
                            \n   DATA_o : 0x%h \
                            \n    Delay : %d  clocks \
                            \n =================================== \n ", \
            self.cycle, self.strobe, self.data_in, self.cycle_tag, self.data_tag, self.acknowledge, self.data_out, self.transmit_delay)


uvm_object_utils(wb4s_seq)


class wb4s_base_sequence(UVMSequence):

    def __init__(self, name="wb4s_base_sequence"):
        super().__init__(name)
        self.set_automatic_phase_objection(1)
        self.req = wb4s_seq()
        self.rsp = wb4s_seq()


uvm_object_utils(wb4s_base_sequence)


class wb4s_single_read_seq(wb4s_base_sequence):
    """         
       Class: Wishbone Pipeline Read Sequence
        
       Definition: Contains functions, tasks and methods
    """
    def __init__(self, name="wb4s_single_read_seq"):
        wb4s_base_sequence.__init__(self, name)
        self.data           = 0
        self.address        = 0
        self.cycle          = 0
        self.cycle_tag      = 0
        self.strobe         = 0
        self.transmit_delay = 0
        self.data_tag       = 0
        self.acknowledge    = 0
        self.we             = 0


    async def body(self):
        # Build the sequence item
        self.req.we             = self.we
        self.req.data_in        = self.data
        self.req.address        = self.address
        self.req.cycle          = self.cycle
        self.req.cycle_tag      = self.cycle_tag
        self.req.strobe         = self.strobe
        self.req.data_tag       = self.data_tag
        self.req.acknowledge    = self.acknowledge
        self.req.transmit_delay = self.transmit_delay

        await uvm_do_with(self, self.req) # start_item 


uvm_object_utils(wb4s_single_read_seq)


class wb4s_single_write_seq(wb4s_base_sequence):
    """         
       Class: Wishbone Pipeline Write Sequence
        
       Definition: Contains functions, tasks and methods
    """
    def __init__(self, name="wb4s_single_write_seq"):
        wb4s_base_sequence.__init__(self, name)
        self.data           = 0
        self.address        = 0
        self.cycle          = 0
        self.cycle_tag      = 0
        self.strobe         = 0
        self.transmit_delay = 0
        self.data_tag       = 0
        self.acknowledge    = 0
        self.we             = 1


    async def body(self):
        # Build the sequence item
        self.req.we             = self.we
        self.req.data_in        = self.data
        self.req.address        = self.address
        self.req.cycle          = self.cycle
        self.req.cycle_tag      = self.cycle_tag
        self.req.strobe         = self.strobe
        self.req.data_tag       = self.data_tag
        self.req.acknowledge    = self.acknowledge
        self.req.transmit_delay = self.transmit_delay

        await uvm_do_with(self, self.req) # start_item 


uvm_object_utils(wb4s_single_write_seq)
