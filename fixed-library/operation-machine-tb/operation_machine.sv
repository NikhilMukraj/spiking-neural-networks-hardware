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
    parameter count = 3,
    parameter stack = 5
)(
    input rst,
    input clk,
    input apply,
    output [$clog2(stack):0] index1,
    output [$clog2(stack):0] index2,
    output [$clog2(stack):0] index3,
    output [N:0] 
    output [2:0] operand,
    output done
);
    reg [counter-1:0] counter;

    always @ (posedge clk) begin
        if (rst) begin
            index1 <= {$clog2(stack){1'b0}};
            index2 <= {$clog2(stack){1'b0}};
            index3 <= {$clog2(stack){1'b0}};
            operand <= 3'b000;
            done <= 1'b0;
        end

        // try implementing (x+y)*z

        // try implementing (5+y)*z
        // 5 is static so it should be in some reserve part of memory

        // then generalize this

        if (apply) begin
            // change index and operation according to finite state machine

            // first load in all values into memory

            // once loaded pick 0 for index1 and 1 for index2
            // with plus operand, index3 should be 3

            // mult operand, 3 for index1 and 2 for index2, 4 for index3

            // if (counter == 3'b000) begin
                
            // end
        end
    end
endmodule

module operation_machine #(
    parameter N = 32,
    parameter Q = 16,
    parameter stack = 5
)(
    input rst,
    input clk,
    input [2:0] operand,
    input [$clog2(stack):0] index1,
    input [$clog2(stack):0] index2,
    input [$clog2(stack):0] index3,
    input [N-1:0] value,
    output [N-1:0] out
);
    // all clocked operations
    // input constants
    // choose operand and which operators
        // if absolute or negator function, choose 0 for other index
    // add output to stack
    // output when done

    reg [N-1:0] a, b, adder_out, mult_out, neg_out, abs_out;
    reg [N*stack-1:0] stack;

    add #(.N(N), .Q(Q)) adder1 ( a, b, adder_out );
    mult #(.N(N), .Q(Q)) mult1 ( a, b, mult_out );
    negator #(.N(N), .Q(Q)) negator1 ( a, b, neg_out );
    abs #(.N(N), .Q(Q)) abs1 ( a, b, abs_out );

    // https://stackoverflow.com/questions/38134217/how-do-i-access-an-array-element-using-a-variable-as-index
    // rewrite with above link in mind ^
    // probably can automatically generate index values and then 
    // index the pregenerated values based on index1, index2, and index3 in a table

    // https://electronics.stackexchange.com/questions/67983/accessing-rows-of-an-array-using-variable-in-verilog
    // test variable indexing separately before continuing

    reg do_operation;
    assign do_operation = operand == 3'b011 | operand == 3'b100 | operand == 3'b101 | operand == 3'b110;

    always @ (posedge clk) begin
        if (rst) begin
            a <= {N{1'b0}};
            b <= {N{1'b0}};
            adder_out <= {N{1'b0}};
            mult_out <= {N{1'b0}};
            neg_out <= {N{1'b0}};
            abs_out <= {N{1'b0}};
            stack <= {(N * stack){1'b0}};
        end

        if (operand == 3'b001) begin
            stack[(index1*N)-1+:N] <= value;
        end else if (operand == 3'b010) begin
            stack[(index2*N)-1+:N] <= value;
        end else if (do_operation) begin
            a <= stack[(index1*N)-1+:N]; 
            b <= stack[(index2*N)-1+:N]; 
        end

        case (operand)
            3'b011 : stack[(index3*N)-1+:N] <= adder_out;
            3'b100 : stack[(index3*N)-1+:N] <= mult_out;
            3'b101 : stack[(index3*N)-1+:N] <= neg_out;
            3'b110 : stack[(index3*N)-1+:N] <= abs_out;
        endcase
    end

    assign out = stack[N-1:0];
endmodule
