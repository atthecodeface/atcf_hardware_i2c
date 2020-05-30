#a Copyright
#  
#  This file 'test_jtag.py' copyright Gavin J Stark 2017
#  
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#a Documentation
"""
"""

#a Imports
from regress.i2c.i2c     import t_i2c, t_i2c_conf
from regress.i2c.i2c     import i2c_mixin
from regress.apb.structs import t_apb_request, t_apb_response
from regress.apb.bfm     import ApbMaster
from cdl.sim     import ThExecFile
from cdl.sim     import HardwareThDut
from cdl.sim     import TestCase

#c apb_target_i2c_test_base
class apb_target_i2c_test_base(ThExecFile, i2c_mixin):
    th_name = "APB I2C test harness"
    def run_start(self) -> None:
        self.apb = ApbMaster(self, "apb_request",  "apb_response")
        self.bfm_wait(10)
        pass
    def run(self) -> None:
        self.run_start()
        self.passtest("Test succeeded")
        pass
#c apb_target_i2c_test_one
class apb_target_i2c_test_one(apb_target_i2c_test_base):
    #f run
    def run(self):
        super(apb_target_i2c_test_one, self).run_start()
        self.i2c_init(scl    = self.i2c_th__scl,
                      sda    = self.i2c_th__sda,
                      scl_in = self.i2c_in__scl,
                      sda_in = self.i2c_in__sda,
                      cfg    = {"divider":3})
        self.i2c_idle()
        
        i2c_conf = 0x02460a03
        self.apb.write( address=0, data=i2c_conf )
        d = self.apb.read( address=0 )
        if d != i2c_conf:
            self.failtest("Mismatch in reading back I2C conf")
            pass
        self.apb.write( address=0x00000, data=i2c_conf )
        self.apb.write( address=0x00003, data=0xf00020 )
        self.apb.write( address=0x10000, data=i2c_conf )
        self.apb.write( address=0x10003, data=0xf00040 )
        self.apb.write( address=0x00002, data=0x303 )
        self.apb.write( address=0x10002, data=0x303 )
        for i in range(20):
            status = self.apb.read( address=1 )
            print("Status %08x"%status)
            if (status&3)==0: break
            self.bfm_wait(1000)
            pass
        if i>18:
            self.failtest("Expected I2C transaction to complete")
            pass
        if self.gpio_output.value()!=0xc:
            self.failtest("Expected GPIO to have been written over I2C to 0xc")
            pass
        self.apb.write( address=0x00000, data=i2c_conf )
        self.apb.write( address=0x00003, data=0x21 )
        self.apb.write( address=0x00002, data=0x201 )
        for i in range(20):
            status = self.apb.read( address=1 )
            print("Status %08x"%status)
            if (status&3)==0: break
            self.bfm_wait(1000)
            pass
        if i>18:
            self.failtest("Expected I2C transaction to complete")
            pass
        if self.gpio_output.value()!=0xc:
            self.failtest("Expected GPIO to have been written over I2C to 0xc")
            pass
        self.passtest("Test completed")
        pass
    pass


#c ApbI2cHardware
class ApbI2cHardware(HardwareThDut):
    clock_desc = [("clk",(0,1,1))]
    reset_desc = {"name":"reset_n", "init_value":0, "wait":5}
    module_name = "tb_apb_target_i2c"
    dut_inputs  = {"apb_request":t_apb_request,
                   "i2c_th":t_i2c,
                   "i2c_conf":t_i2c_conf,
    }
    dut_outputs = {"apb_response":t_apb_response,
                   "i2c_in":t_i2c,
                   "gpio_output":16,
                   "gpio_output_enable":16,
    }
    pass

#c TestApbI2c
class TestApbI2c(TestCase):
    hw = ApbI2cHardware
    _tests = {"simple": (apb_target_i2c_test_one, 100*1000, {}),
              }
    pass

