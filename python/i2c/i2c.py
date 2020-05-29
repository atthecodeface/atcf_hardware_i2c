#a Copyright
#  
#  This file 'i2c.py' copyright Gavin J Stark 2018-2020
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

#a Useful functions
def int_of_bits(bits):
    l = len(bits)
    m = 1<<(l-1)
    v = 0
    for b in bits:
        v = (v>>1) | (m*b)
        pass
    return v

def bits_of_n(nbits, n):
    bits = []
    for i in range(nbits):
        bits.append(n&1)
        n >>= 1
        pass
    return bits

#a Structs
#t t_i2c
t_i2c = {"scl":1, "sda":1}

#t t_i2c_master_request
t_i2c_master_request = {"valid":1,
                      "cont":1,
                      "data":32,
                      "num_in":3,
                      "num_out":3,
}

#t t_i2c_master_response
t_i2c_master_response = {"ack":1,
                       "in_progress":1,
                       "response_valid":1,
                       "response_type":3,
                       "data":32,
}

#t t_i2c_conf
t_i2c_conf = {"divider":8, "period":8}

#a I2C mixin
#c i2c_mixin
class i2c_mixin:
    #f i2c_init
    def i2c_init(self, scl, sda, scl_in, sda_in, cfg):
        self.i2c__scl = scl
        self.i2c__sda = sda
        self.i2c__scl_in = scl_in
        self.i2c__sda_in = sda_in
        self.i2c__cfg = cfg
        pass
    #f i2c_wait
    def i2c_wait(self, n):
        self.bfm_wait(self.i2c__cfg["divider"]*n*5)
    #f i2c_idle - leaves clock high
    def i2c_idle(self):
        self.i2c__scl.drive(1)
        self.i2c__sda.drive(1)
        self.i2c_wait(3)
        pass
    #f i2c_start - leaves clock low
    def i2c_start(self):
        self.i2c__sda.drive(1)
        self.i2c__scl.drive(1)
        self.i2c_wait(1)
        self.i2c__sda.drive(0)
        self.i2c_wait(1)
        self.i2c__scl.drive(0)
        self.i2c_wait(1)
        pass
    #f i2c_stop - leaves bus quiescent (both high)
    def i2c_stop(self):
        self.i2c__sda.drive(0)
        self.i2c__scl.drive(1)
        self.i2c_wait(1)
        self.i2c__sda.drive(1)
        self.i2c_wait(1)
        pass
    #f i2c_cont - expects clock low, leaves bus quiescent
    def i2c_cont(self):
        self.i2c__sda.drive(1)
        self.i2c__scl.drive(0)
        self.i2c_wait(1)
        self.i2c__scl.drive(1)
        self.i2c_wait(1)
        pass
    #f i2c_bit_start - requires clock low, leaves clock high
    def i2c_bit_start(self, d=None):
        if d is not None:
            self.i2c__sda.drive(d)
            self.i2c_wait(1)
            pass
        else:
            pass
        self.i2c__scl.drive(1)
        d = self.i2c__sda_in.value()
        self.i2c_wait(1)
        return d
    #f i2c_bit_stop - requires clock high, leaves clock low
    def i2c_bit_stop(self):
        self.i2c__scl.drive(0)
        self.i2c_wait(1)
        pass
    #f i2c_ack - requires clock low, leaves clock low
    def i2c_ack(self):
        self.i2c_bit_start(0)
        self.i2c_bit_stop()
        self.i2c__sda.drive(1)
        self.i2c_wait(1)
        pass
    #f i2c_out_byte
    def i2c_out_byte(self, data):
        bits = bits_of_n(8, data)
        bits.reverse()
        for d in bits:
            self.i2c_bit_start(d)
            self.i2c_bit_stop()
            pass
        ack = self.i2c_bit_start(None)
        self.i2c_bit_stop()
        return ack==0
    #f i2c_read_byte
    def i2c_read_byte(self, do_ack=False):
        d = []
        for i in range(8):
            d.append(self.i2c_bit_start())
            self.i2c_bit_stop()
            pass
        d.reverse()
        data = int_of_bits(d)
        if do_ack:
            self.i2c_ack()
            pass
        return data
    #f i2c_write
    def i2c_write(self, data, cont=False):
        self.i2c_start()
        for d in data:
            ack = self.i2c_out_byte(d)
            if not ack: self.failtest(self.global_cycle(),"Expected an ack")
        if cont:
            self.i2c_cont()
        else:
            self.i2c_stop()
            pass
        return
    #f i2c_read
    def i2c_read(self, data, num, cont=False):
        self.i2c_start()
        for d in data:
            ack = self.i2c_out_byte(d)
            if not ack: self.failtest(self.global_cycle(),"Expected an ack")
        data = []
        for i in range(num):
            data.append(self.i2c_read_byte(do_ack=(i<num-1)))
        if cont:
            self.i2c_cont()
        else:
            self.i2c_stop()
            pass
        return data
