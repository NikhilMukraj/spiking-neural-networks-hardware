# notes

- 2 20k resistors to divide battery voltage
- [RC filter](https://www.electronics-tutorials.ws/filter/filter_2.html)
- Should demonstrate op amp adders with LEDs

## Operational Amplifiers

- [Integrator](https://www.electronics-tutorials.ws/opamp/opamp_6.html)
- [Digital to analog and summer circuit](https://www.electronics-tutorials.ws/opamp/opamp_4.html)

## Todo

- [ ] Schematics
  - [ ] Digital to analog
  - [ ] Voltage adder
    - [x] With disconnected power supplies
    - [ ] With singular power supply
  - [ ] Voltage multiplier
- [ ] Digital to analog conversions
- [ ] LM324N testing
  - [ ] Test simple addition
    - Power supply can just use Arduino for now
- [ ] AD633 testing
  - [ ] Simple multplication testing
- [ ] Scaling Izhikevich equations between 5 or 3 volt range
- [ ] Linking adders and multipliers together
- [ ] Reset circuit
- [ ] Analog pipeline synthesis similar to equation high level synthesis
  - [ ] PySpice testing
  - [ ] FPAA simulation (Anadigm probably)

## Basic Flow

- 5 analog ouputs
  - $a$, $b$, $voltage$, $w$, $i$
- Integrator at the end to add
- If sum is greater than threshold execute spike logic
