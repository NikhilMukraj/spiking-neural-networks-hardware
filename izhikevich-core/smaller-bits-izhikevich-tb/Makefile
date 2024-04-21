# defaults
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(PWD)/izhikevich.sv
# use VHDL_SOURCES for VHDL files

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = izhikevich_core

# MODULE is the basename of the Python test file
MODULE = izhikevich_test

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
