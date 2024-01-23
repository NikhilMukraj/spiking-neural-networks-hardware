# spiking-neural-networks-hardware

## requirements

- requires wsl or ubuntu linux
- run `pip install -r requirements.txt`
- requires icarus verilog, run `sudo apt-get install iverilog`

## general flow

- input parameters of model through spi (or ethernet)
- input adjacency matrix through spi (or ethernet)
- write adjacency matrix to ram
  - (calculate inputs if layered neural network)
- calculate inputs based on adjacency matrix
- run izhikevich core calculaton
  - (run stdp, or r-stdp)
- (write state to ram)
- repeat
- send relevant information back through spi (or ethernet)

## todo

- [ ] equation high level synthesis
  - [ ] preprocessing of equation
- [x] izhikevich core
- [ ] hodgkin huxley core
- [ ] communication protocol
- [ ] izhikevich matrix

## notes

- use `dut._log.info(string)` for logging cocotb simulations
