Q=@
CDL_REGRESS = ${CDL_ROOT}/libexec/cdl/cdl_regress.py

.PHONY:smoke
smoke:
	${CDL_REGRESS} --pyengine-dir=${BUILD_ROOT} --package-dir regress:${SRC_ROOT}/python --package-dir regress:$(abspath ${SRC_ROOT}/../atcf_hardware_apb/python) --suite-dir=python test_i2c

.PHONY:regress
regress:
	${CDL_REGRESS} --pyengine-dir=${BUILD_ROOT} --package-dir regress:${SRC_ROOT}/python --package-dir regress:$(abspath ${SRC_ROOT}/../atcf_hardware_apb/python) --suite-dir=python test_i2c
