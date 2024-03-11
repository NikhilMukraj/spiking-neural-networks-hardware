# Spiking Neural Networks Hardware

## Overview

- Uses Izhikevich integrate and fire model to simulate neurons
  - [Interactive simulation of Izhikevich core](https://digitaljs.tilk.eu/#151d9328ba8167cb317f220abd64ed396b5fa4aeef076a222a88ef91dcde7637)
- (todo...)
- (describe how everything works)

## Requirements

- Requires WSL or Ubuntu Linux
- Run `pip install -r requirements.txt`
- Requires Icarus Verilog, run `sudo apt-get install iverilog`
- Vivado Studio for loading FPGA programs
- Thonny for Raspberry Pi Pico

## General Flow

- Input parameters of model through spi (or ethernet)
- Input adjacency matrix through spi (or ethernet)
- Write adjacency matrix to ram
  - (Calculate inputs if layered neural network)
- Calculate inputs based on adjacency matrix
- Run izhikevich core calculaton
  - (Run stdp, or r-stdp)
- (Write state to ram)
- Repeat
- Send relevant information back through spi (or ethernet)

## Todo

- [ ] Equation high level synthesis
  - [ ] Preprocessing
    - [ ] To the power of an integer expansion
    - [ ] Simplification of expressions with only constants
    - [ ] Nest equations correctly based on order of operations
  - [x] Addition/Subtraction
  - [x] Multiplication
  - [x] Negation
  - [x] Reciprocal
  - [x] Division
  - [x] Absolute value
  - [ ] High precision $e^x$
  - [X] Limited range $e^x$
  - [ ] Preprocessing of equation
- [ ] Operations verification on chip
  - [ ] Addition/Subtraction
  - [ ] Multiplication
  - [ ] Negation
  - [ ] Reciprocal
  - [ ] Division
  - [ ] Absolute value
  - [ ] Limited range $e^x$
- [ ] Izhikevich core
  - [x] Voltage change
  - [x] Adaptive value change
  - [ ] Is spiking indicator
  - [ ] Verification on chip
- [ ] Hodgkin huxley core
- [ ] RAM interface
- [ ] Communication protocol
  - [ ] SPI
    - [ ] On chip verification
  - [ ] RPGA side communication
  - [ ] Raspberry Pi side communication
  - [ ] Distributed communication
- [ ] Izhikevich matrix
  - [ ] Interwoven matrix
    - Potentially could refactor with asynchronous execution of neurons and crossbar mechanisms in mind
    - [ ] Save each output of neuron to memory
    - [ ] Calculate inputs for each neuron by row from memory and save to hardware matrix
    - [ ] Run iteration of lattice
    - [ ] Send voltage values back to controller for visualization/history
    - [ ] Send other variables (neurotransmission values, `a`, `b`, `c`, and `d` values)
  - [ ] Feedforward network
- [ ] Fast Fourier transform
  - [ ] On chip comparison of spectral analyses
    - This can either be done by finding the most prominent frequency and comparing, binning the analyses and comparing with mean squared error, or approximating the earth-moving-distance
- [ ] STDP
  - [ ] Internals of update weight functionality should be fit to specific $\tau_{-}$ and $\tau_{+}$ values to linear piecewise functions
    - [x] In this scheme the linear piecewise function parameters should take the place of $\tau_{-}$ and $\tau_{+}$ as well as $a_{-}$ and $a_{+}$
    - [ ] A $\Delta{t}$ should return 0 for the change in weight
  - [ ] Since spikes are not likely to occur at the same time, spikes can be handled by a single module being fed the spike times
  - [ ] There should be an iteration counter, every time a spike occurs, the time is equal to the iteration counter
    - [ ] Iteration counter is 15 bits + sign bit, when inputting spike time into any equation it is shifted to -1 to 1 range in a 32 bit number
    - [ ] If the iteration counter resets, any spike that has occured before the reset is set to the spike time - maximum integer value
    - [ ] If the spike is still negative, it is set to the maximum negative value
    - [ ] Coupled test
- [ ] R-STDP
  - [ ] Input values to feed forward version
  - [ ] Classifier
  - [ ] Fit to eeg signaling
- [ ] Neurotransmission
  - [ ] Neurotranmission module per row of neurons to handle entire row's calculations

## Hardware Documentation

### Test Bench Convention

Should be named `hardware-tb`

```bash
.
├── Makefile
├── hardware.sv
└── test.py
```

When testing in CocoTB, use `dut._log.info(string)` for logging during the simulation

(hardware verilog file within directory is optional)

### Fixed Library

#### Adder

```verilog
module add #( parameter N=32, parameter Q=16 )( input [N-1:0] a, input [N-1:0] b, output [N-1:0] c )
```

$a + b = c$

- `[N-1:0] a` : First fixed point term
- `[N-1:0] b` : Second fixed point term
- `[N-1:0] c` : Output in fixed point form

#### Negator

```verilog
module negator #( parameter N = 32 )( input logic signed [N-1:0] a, output logic signed [N-1:0] out )
```

$-1 * a = out$

- `[N-1:0] a` : Input fixed point term
- `[N-1:0] out` : Output in fixed point form

#### Multiplier

```verilog
module mult #( parameter N = 32, parameter F = 16 )( input logic [N-1:0] a, input logic [N-1:0] b, output logic [N-1:0] c )
```

$a * b = c$

- `[N-1:0] a` : First fixed point term
- `[N-1:0] b` : Second fixed point term
- `[N-1:0] c` : Output in fixed point form

#### Reciprocal

```verilog
module reciprocal #( parameter N = 32 )( input [N-1:0] a, output reg [N-1:0] out )
```

$\frac{1}{a} = out$

(not implemented for N != 32)
(need to refactor with `casez` and `genvar`)

- `[N-1:0] a` : Input fixed point term
- `[N-1:0] out` : Output in fixed point form

#### Division

```verilog
module div #( parameter N = 32, parameter F = 16 )( input logic [N-1:0] a, input logic [N-1:0] b, output logic [N-1:0] c )
```

$\frac{a}{b} = c$

- `[N-1:0] a` : First fixed point term
- `[N-1:0] b` : Second fixed point term
- `[N-1:0] c` : Output in fixed point form

#### Absolute Value

```verilog
module abs #( parameter N = 32 )( input [N-1:0] x, output reg [N-1:0] out )
```

$|x| = out$

- `[N-1:0] x` : Input fixed point term
- `[N-1:0] out` : Output in fixed point form

#### Exponentiate

```verilog
module exp #( parameter N = 32 )( input [N-1:0] x, output reg [N-1:0] out )
```

${e}^{x}$

(not implemented for N != 32)
(needs to be re-implemented for higher precision)
([relevant link to cordic method](https://stackoverflow.com/questions/32409022/how-can-i-calculate-exponential-using-cordic-for-numbers-outside-1-1), calculate q by taking integer part of x * 1/ln(2), multiply by $\frac{1}{ln(2)}$, calculate r and ${e}^{r}$ with a look up table, r will always be between 0 and 1 so ${e}^{r}$ will only need to be from 0 to 1)

- `[N-1:0] x` : Input fixed point term
- `[N-1:0] out` : Output in fixed point form

#### Linear Piecewise

```verilog
module linear_piecewise #( parameter N = 32 ) ( input [N-1:0] x, input [N-1:0] m1, input [N-1:0] m2, input [N-1:0] b1, input [N-1:0] b2, input [N-1:0] split, output [N-1:0] out )
````

$
f(x)=
    \begin{cases}
        {m}_{1}x + {b}_{1} & x < q\\
        {m}_{2}x + {b}_{2} & x \geq q\\
    \end{cases}
$

- (can be refactored to use less LUTs)
- `[N-1:0] x` : Input to function in fixed point representation
- `[N-1:0] m1` : Fixed point slope of first half
- `[N-1:0] m2` : Fixed point slope of second half
- `[N-1:0] b1` : Fixed point intercept of first half
- `[N-1:0] b2` : Fixed point intercept of second
- `[N-1:0] split` : Where to split piecewise in fixed point form ($q$)
- `[N-1:0] out` : Output in fixed point form

<!-- should be special case of linear piecewise>
<!-- #### Limited Range Exponentiate

```verilog
module exp #( parameter N = 32 )( input [N-1:0] x, output reg [N-1:0] out )
```

${e}^{x}, x \in [-1, 0]$

(should be calculated by linear interpolation)

- `[N-1:0] x` : Input fixed point term
- `[N-1:0] out` : Output in fixed point form -->

#### Power

```verilog
// todo
module exp #( parameter N = 32, parameter P=power )( input [N-1:0] x, output reg [N-1:0] out )
```

${x}^{n}$

- **todo**
- Should be expanded to a processable form in the equation high level synthesis
- Expansion process:
  - `x^0` should be `1`
  - `x^1` should just be `x`
  - `x^2` should be `(x*x)`
  - `x^3` should be `((x*x)*x)`
  - `x^4` should be `((x*x)*(x*x))`
  - `x^5` should be `(((x*x)*(x*x))*x)`
  - `x^6` should be `(((x*x)*(x*x))*(x*x))`
  - ... etc

### Fixed Point Models Package

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

### Equation High Level Synthesis

#### Run from CLI

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

- `name: String` : Name of module
- `equation: String` : Equation to translate to hardware (see [operations](#operations))
- `variables: Array[String]` : Variables within equation (`e` is a reserved variable)
- `out_variable: String` : What to name output register
- `integer_bits: Integer` : Number of integer bits in fixed point representation
- `fractional_bits: Integer` : Number of fractional bits in fixed point representation
- `lower_bound: Float` : Lower bound of numbers to test in simulation
- `upper_bound: Float` : Upper bound of numbers to test in simulation
- `tolerance: Float` : Maximum error allowed within test

##### Operations

All operations must be enclosed by parentheses, `x` and `y` can either be variables specified in the `.json` file, constants within the specified `integer_bits` and `fractional_bits` minimum and maximum, or the result of other nested operations

- Addition/Subtraction : `(x+y)`
- Negation : `(-1*x)` or `(x*-1)`
- Multiplication : `(x*y)`
- Division : `(x/y)`
- Exponentation : `(e^x)`
  - To use a linear piecewise approximation of $e^x$, specify $m_1$, $m_2$, $b_1$, $b_2$, and `split` in arguments
- Absolute value: `(abs|x)`
- (todo) Power: `(x^n)` where `n` must be a constant

### Preprocessing

- **todo**
- Should take in regular plain text or Latex equation and convert it to one parseable by the CLI tool

### Izhikevich Core

#### Calculate Voltage Change

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

#### Calculate Adaptive Change

```verilog
module calc_dw #( parameter N=32, parameter Q=16 )( input [N-1:0] a, input [N-1:0] b, input [N-1:0] v, input [N-1:0] w, input [N-1:0] step, output [N-1:0] out )
```

$$
dw = \alpha(\beta V_m(t) - w)(\frac{dt}{\tau_m})
$$

- `[N-1:0] a` : Alpha value
- `[N-1:0] b` : Beta value
- `[N-1:0] v` : Current voltage
- `[N-1:0] w` : Current adaptive value
- `[N-1:0] i` : Input voltage
- `[N-1:0] step` : Timestep value divided by ${\tau}_{m}$
- `[N-1:0] out` : Calculated change in adaptive value

#### Izhikevich Neuron

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

### Hodgkin Huxley Core

- **todo**
- Needs to calculate each gate current
- Needs to update each gate state
- Needs to add gate currents together
- Needs to encapsulate ligand gated channel currents

#### Ion Channel Calculations

#### Multicompartment Current Calculations

#### Ligand Gated Ion Channel Calculations

#### Neurotransmitter Dynamics Calculations

### RAM

- **todo**
- Needs getting addresses and data
- Needs editing addresses and data

### Lattice

- **todo**
- Needs to generate neurons in a grid
  - Implementation must allow for Verilog to automatically generate different grid sizes on build
- Calculate neuron inputs based off voltages and connected inputs
  - How neurons are connected stored in RAM
- Apply voltage and adaptive value changes on clock cycle and apply signal
- Needs to be adaptable to allow an input layer and feedforward structure
- Potentially needs to be able to allow certain constants to change depending on neurotransmitter

### SPI Interface

#### SPI FPGA Peripheral

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

#### SPI CPU Controller

- **todo**
- Needs to transmit bytes
- Needs to receive bytes
- Needs to transmit and recieve to multiple peripherals

### AXI Interface

- **todo**
- Needs to interface a CPU via AXI (test with Raspberry Pi Pico/Zero)
- Needs to transmit data
- Needs to recieve data

### Ethernet Interface

- **todo**
- Either needs to transmit and recieve ethernet data from CPU through AXI or directly interface it with the FPGA

### RGB Display

- **todo**
- Needs to display voltages of lattice as iterations progress
