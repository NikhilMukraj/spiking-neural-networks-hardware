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

```verilog
module calc_dv #( parameter N=32, parameter Q=16 ) ( input [N-1:0] v, input [N-1:0] w, input [N-1:0] i, input [N-1:0] step, output [N-1:0] out )
```

- `v` : Current voltage
- `w` : Current adaptive value
- `i` : Input voltage
- `step` : Timestep value divided by ${\tau}_{m}$
- `out` : Calculated change in voltage

### Calculate Adaptive Change

```verilog
module calc_dw #( parameter N=32, parameter Q=16 )( input [N-1:0] a, input [N-1:0] b, input [N-1:0] v, input [N-1:0] w, input [N-1:0] step, output [N-1:0] out )
```

- `a` : Alpha value
- `b` : Beta value
- `c` : C value
- `d` : D value
- `v` : Current voltage
- `w` : Current adaptive value
- `i` : Input voltage
- `step` : Timestep value divided by ${\tau}_{m}$
- `out` : Calculated change in adaptive value

### Izhikevich Neuron

```verilog
module izhikevich_core #( parameter N=32, parameter Q=16 )( input clk, input [N-1:0] i, input [N-1:0] v_init, input [N-1:0] w_init, input [N-1:0] v_th, input [N-1:0] step, input [N-1:0] a, input [N-1:0] b, input [N-1:0] c, input [N-1:0] d, input apply, input rst, output reg [N-1:0] voltage, output reg [N-1:0] w )
```

- `clk` : Clock signal
- `i` : Input voltage
- `v_init` : Initial voltage value
- `w_init` : Initial adaptive value
- `v_th` : Voltage reset threshold
- `step` : Timestep value divided by ${\tau}_{m}$
- `a` : Alpha value
- `b` : Beta value
- `c` : C value
- `d` : D value
- `apply` : Whether to change voltage and adaptive value this clock cycle
- `rst` : Active high reset back to initial voltage and adaptive values
- `voltage` : Current voltage
- `w` : Current adaptive value

## RAM

## Lattice

## SPI Interface

### SPI FPGA Peripheral

```verilog
module spi_peripheral ( input rst, input ss, input mosi, output reg miso, input sck, output reg done_rx, output reg done_tx, input [7:0] din, output reg [7:0] dout )
```

- `rst` : Active high reset
- `ss` : Select signal
- `mosi` : Bit from controller to peripheral
- `miso` : Bit from peripheral to controller
- `sck` : Controller clock signal
- `done_rx` : Whether byte is recieved
- `done_tx` : Whether byte is transmitted
- `din` : Byte to send
- `dout` : Byte received

### SPI CPU Controller

## AXI Interface

## Ethernet Interface

## RGB Display
