// specify inputs to a given node
// each node that can connect to another node has a signal
// if on, then that node is considered inputted
// could feed these inputs into an aggregator of sorts
// aggregator would take one input at a time to an accumulator

// or could look at a crossbar impl

// try one implementation and check how many luts it needs as it scales
// adjust accordingly
// 2x2, 4x4, 8x8, 16x16...

module add_if_enabled(
    input clk,
    input [7:0] data1,
    input [7:0] data2,
    input [7:0] data3,
    input [1:0] on,
    output reg [7:0] output_data
);
    reg [7:0] added;

    always @ (posedge clk) begin
        case (on)
            2'b00 : added = 8'b00000000;
            2'b01 : added = data1;  
            2'b10 : added = data1;  
            2'b11 : added = data3;  
        endcase
        output_data <= output_data + added;
    end
endmodule

// test effectiveness of this
// try to create a system to store which connections are pulsed when (maybe adjacency matrix)
// test how many luts this uses as it scales
module matrix_flow (
    input clk,
    // replace inouts with matrix array
    inout [7:0] data1,
    inout [7:0] data2,
    inout [7:0] data3,
    inout [7:0] data4,
    input [1:0] on1,
    input [1:0] on2,
    input [1:0] on3,
    input [1:0] on4
);
    add_if_enabled adder1 ( clk, data2, data3, data4, on1, data1 );
    add_if_enabled adder2 ( clk, data1, data3, data4, on2, data2 );
    add_if_enabled adder3 ( clk, data1, data2, data4, on3, data3 );
    add_if_enabled adder4 ( clk, data1, data2, data3, on4, data4 );
endmodule
