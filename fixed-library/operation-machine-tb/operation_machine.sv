// determine max number of numbers to store
// determine which operations to use (can be hardcoded and generated with eq hls)
// route correct numbers into operation
// store new numbers, potentially replacing old ones
// determine next operation

// 000 nothing
// 001 load into index 1
// 010 load into index 2
// 011 add
// 100 mult
// 101 negate
// 110 abs

// eventually modify for exp

module operations #(
    parameter N = 32,
    parameter Q = 16,
    parameter stack = 5
)(
    input clk,
    input continue,
    output [$clog2(stack)+1:0] index1,
    output [$clog2(stack)+1:0] index2,
    output [2:0] operand
);
endmodule

module operation_machine #(
    parameter N = 32,
    parameter Q = 16,
    parameter stack = 5
)(
    input rst,
    input clk,
    input [2:0] operand,
    input [$clog2(stack)+1:0] index1,
    input [$clog2(stack)+1:0] index2,
    input [$clog2(stack)+1:0] index3,
    input [N-1:0] value,
    output reg done,
    output [N-1:0] out
);
    // all clocked operations
    // input constants
    // choose operand and which operators
        // if absolute or negator function, choose 0 for other index
    // add output to stack
    // output when done

    reg [N-1:0] a, b, adder_out, mult_out, neg_out, abs_out;
    reg [N * stack - 1:0] stack;

    add #(.N(N), .Q(Q)) adder1 ( a, b, adder_out );
    mult #(.N(N), .Q(Q)) mult1 ( a, b, mult_out );
    negator #(.N(N), .Q(Q)) negator1 ( a, b, neg_out );
    abs #(.N(N), .Q(Q)) abs1 ( a, b, abs_out );

    always @ (posedge clk) begin
        if (rst) begin
            a <= {N{1'b0}};
            b <= {N{1'b0}};
            stack <= {(N * stack){1'b0}};
        end

        if (operand == 3'b001) begin
            stack[index1-1:index1-N-1] <= value;
        end else if (operand == 3'b010) begin
            stack[index2-1:index2-N-1] <= value;
        end else if (operand == 3'b011 | operand == 3'b100 | operand == 3'b101 | operand == 3'b110) begin
            a <= stack[index1-1:index1-N-1]; 
            b <= stack[index2-1:index2-N-1]; 
        end

        case (operand)
            3'b011 : stack[index3-1:index3-N-1] <= adder_out;
            3'b100 : stack[index3-1:index3-N-1] <= mult_out;
            3'b101 : stack[index3-1:index3-N-1] <= neg_out;
            3'b110 : stack[index3-1:index3-N-1] <= abs_out;
        endcase
    end

    assign out = stack[N-1:0];
endmodule
