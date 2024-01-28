# Hardware Documentation

## Test Bench Convention

Should be named `hardware-tb`

```bash
.
├── Makefile
├── hardware.sv
└── test.py
```

(hardware verilog file within directory is optional)

## Fixed Library

## Equation High Level Synthesis

### Run from CLI

```bash
python3 equation_to_module.py <filename>.json
```

\<filename>.json example

```json
{
    "name": "name",
    "equation": "((x+y)*z)",
    "variables": ["x", "y", "z"],
    "out_variable": "out",
    "integer_bits": 16,
    "fractional_bits": 16,
    "lower_bound": -4,
    "upper_bound": 4,
    "tolerance": 1
}
```

### Preprocessing

## Izhikevich Core

### Calculate Voltage Change

### Calculate Adaptive Change

## RAM

## Lattice

## SPI Interface

### SPI FPGA Peripheral

### SPI CPU Controller

## AXI Interface

## Ethernet Interface

## RGB Display
