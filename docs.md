# Hardware Documentation

## Test Bench Convention

Should be named `hardware-tb`

```bash
.
├── Makefile
├── hardware.sv
└── test.py
```

When testing in CocoTB, use `dut._log.info(string)` for logging during the simulation

(hardware verilog file within directory is optional)

## Fixed Library

### Adder

```verilog
module add #( parameter N=32, parameter Q=16 )( input [N-1:0] a, input [N-1:0] b, output [N-1:0] c )
```

$a + b = c$

- `[N-1:0] a` : First fixed point term
- `[N-1:0] b` : Second fixed point term
- `[N-1:0] c` : Output in fixed point form

### Negator

```verilog
module negator #( parameter N = 32 )( input logic signed [N-1:0] a, output logic signed [N-1:0] out )
```

$-1 * a = out$

- `[N-1:0] a` : Input fixed point term
- `[N-1:0] out` : Output in fixed point form

### Multiplier

```verilog
module mult #( parameter N = 32, parameter F = 16 )( input logic [N-1:0] a, input logic [N-1:0] b, output logic [N-1:0] c )
```

$a * b = c$

- `[N-1:0] a` : First fixed point term
- `[N-1:0] b` : Second fixed point term
- `[N-1:0] c` : Output in fixed point form

### Reciprocal

```verilog
module reciprocal #( parameter N = 32 )( input [N-1:0] a, output reg [N-1:0] out )
```

$\frac{1}{a} = out$

(not implemented for N != 32)
(need to refactor with `casez` and `genvar`)

- `[N-1:0] a` : Input fixed point term
- `[N-1:0] out` : Output in fixed point form

### Division

```verilog
module div #( parameter N = 32, parameter F = 16 )( input logic [N-1:0] a, input logic [N-1:0] b, output logic [N-1:0] c )
```

$\frac{a}{b} = c$

- `[N-1:0] a` : First fixed point term
- `[N-1:0] b` : Second fixed point term
- `[N-1:0] c` : Output in fixed point form

### Exponentiate

```verilog
module exp #( parameter N = 32 )( input [N-1:0] x, output reg [N-1:0] out )
```

${e}^{x}$

(not implemented for N != 32)
(needs to be re-implemented for higher precision)

- `[N-1:0] x` : Input fixed point term
- `[N-1:0] out` : Output in fixed point form

## Fixed Point Models Package

- `fixed_point_to_decimal(binary_str: str, integer_bits: int, fractional_bits: int)` : Converts a fixed point represention of a number into a decimal
  - `binary_str: str` : Fixed point representation of a number as a string
  - `integer_bits: int` : Number of integer bits in fixed point representation
  - `fractional_bits: int` : Number of fractional bits in fixed point representation
- `decimal_to_fixed_point(number: float, integer_bits: float, fractional_bits: float)` : Converts a decimal to a fixed point representation
  - `number: float` : Number to convert to a fixed point representation
  - `integer_bits: int` : Number of integer bits in fixed point representation
  - `fractional_bits: int` : Number of fractional bits in fixed point representation
- `check_with_tolerance(expected: float, actual: float, tolerance=1e-5)` : Checks how close an expected value is to an actual given tolerance with overflow
  - `expected: float` : Expected numeric value
  - `actual: float` : Actual numeric value
  - `tolerance: float` : Degree of acceptable error
- `adder_model(a: int, b: int, n_bits: int = 4) -> int` : Performs fixed point addition on two integers with overflow
  - `a: int` : First integer term
  - `b: int` : Second integer term
  - `n_bits: int` : Number of bits in binary representation (must be >=1)
- `multiplier_model(a: int, b: int, n_bits: int = 4) -> int` : Performs fixed point multiplication on two integers with overflow
  - `a: int` : First integer term
  - `b: int` : Second integer term
  - `n_bits: int` : Number of bits in binary representation (must be >=1)
- `divider_model(a: int, b: int, n_bits: int = 4) -> int` : Performs fixed point division on two integers with overflow
  - `a: int` : First integer term
  - `b: int` : Second integer term
  - `n_bits: int` : Number of bits in binary representation (must be >=1)

## Equation High Level Synthesis

### Run from CLI

```bash
python3 equation_to_module.py <filename>.json
```

\<filename>.json example:

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

- **todo**

## Izhikevich Core

### Calculate Voltage Change

```verilog
module calc_dv #( parameter N=32, parameter Q=16 ) ( input [N-1:0] v, input [N-1:0] w, input [N-1:0] i, input [N-1:0] step, output [N-1:0] out )
```

$$
dv_m = (0.04V_m(t)^2 + 5V_m(t) + 140 - w)(\frac{dt}{\tau_m})
$$

- `[N-1:0] v` : Current voltage
- `[N-1:0] w` : Current adaptive value
- `[N-1:0] i` : Input voltage
- `[N-1:0] step` : Timestep value divided by ${\tau}_{m}$
- `[N-1:0] out` : Calculated change in voltage

### Calculate Adaptive Change

```verilog
module calc_dw #( parameter N=32, parameter Q=16 )( input [N-1:0] a, input [N-1:0] b, input [N-1:0] v, input [N-1:0] w, input [N-1:0] step, output [N-1:0] out )
```

$$
dw = \alpha(\beta V_m(t) - w)(\frac{dt}{\tau_m})
$$

- `[N-1:0] a` : Alpha value
- `[N-1:0] b` : Beta value
- `[N-1:0] c` : C value
- `[N-1:0] d` : D value
- `[N-1:0] v` : Current voltage
- `[N-1:0] w` : Current adaptive value
- `[N-1:0] i` : Input voltage
- `[N-1:0] step` : Timestep value divided by ${\tau}_{m}$
- `[N-1:0] out` : Calculated change in adaptive value

### Izhikevich Neuron

```verilog
module izhikevich_core #( parameter N=32, parameter Q=16 )( input clk, input [N-1:0] i, input [N-1:0] v_init, input [N-1:0] w_init, input [N-1:0] v_th, input [N-1:0] step, input [N-1:0] a, input [N-1:0] b, input [N-1:0] c, input [N-1:0] d, input apply, input rst, output reg [N-1:0] voltage, output reg [N-1:0] w )
```

Given Izhikevich neuron parameters, does iterations on the neuron at each clock cycle if `apply` signal is on

- `clk` : Clock signal
- `[N-1:0] i` : Input voltage
- `[N-1:0] v_init` : Initial voltage value
- `[N-1:0] w_init` : Initial adaptive value
- `[N-1:0] v_th` : Voltage reset threshold
- `[N-1:0] step` : Timestep value divided by ${\tau}_{m}$
- `[N-1:0] a` : Alpha value
- `[N-1:0] b` : Beta value
- `[N-1:0] c` : C value
- `[N-1:0] d` : D value
- `apply` : Whether to change voltage and adaptive value this clock cycle
- `rst` : Active high reset back to initial voltage and adaptive values
- `[N-1:0] voltage` : Current voltage
- `[N-1:0] w` : Current adaptive value

## RAM

## Lattice

## SPI Interface

### SPI FPGA Peripheral

```verilog
module spi_peripheral ( input rst, input ss, input mosi, output reg miso, input sck, output reg done_rx, output reg done_tx, input [7:0] din, output reg [7:0] dout )
```

Peripheral for an SPI interface that writes and recieves one byte at a time and depends on the `sck` clock signal from a controller

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
