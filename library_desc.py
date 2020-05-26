import cdl_desc
from cdl_desc import CdlModule, CdlSimVerilatedModule, CModel, CSrc

class Library(cdl_desc.Library):
    name="i2c"
    pass

class I2CModules(cdl_desc.Modules):
    name = "i2c"
    src_dir      = "cdl"
    tb_src_dir   = "tb_cdl"
    libraries = {"std":True}
    cdl_include_dirs = ["cdl"]
    export_dirs = cdl_include_dirs + [ src_dir ]
    modules = []
    modules += [ CdlModule("i2c_interface") ]
    modules += [ CdlModule("i2c_master") ]
    modules += [ CdlModule("i2c_slave") ]
    pass

class ApbModules(cdl_desc.Modules):
    name = "apb"
    src_dir      = "cdl"
    tb_src_dir   = "tb_cdl"
    libraries = {"std":True, "apb":True}
    cdl_include_dirs = ["cdl"]
    export_dirs = cdl_include_dirs + [ src_dir ]
    modules = []
    modules += [ CdlModule("apb_target_i2c_master") ]
    modules += [ CdlModule("i2c_slave_apb_master") ]
    pass

