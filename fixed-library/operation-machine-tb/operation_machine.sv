// determine max number of numbers to store
// determine which operations to use (can be hardcoded and generated with eq hls)
// route correct numbers into operation
// store new numbers, potentially replacing old ones
// determine next operation

module operation_machine #(
    parameter N = 32,
    parameter Q = 16,
    parameter stack = 5
)(
    input clk,
    input [1:0] operand,
    input [$clog2(stack)+1:0] index1,
    input [$clog2(stack)+1:0] index2,
    input [N-1:0] value,
    output reg done,
    output [N-1:0] output
);
    // all clocked operations
    // input constants
    // choose operand and which operators
        // if absolute or negator function, choose 0 for other index
    // add output to stack
    // output when done
endmodule
