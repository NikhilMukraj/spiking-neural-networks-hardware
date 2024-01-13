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
    input [7:0] input_data,
    input on,
    output reg [7:0] output_data
);
    always @ (posedge clk) begin
        output_data = on ? output_data + input_data : output_data;
    end
endmodule

// test effectiveness of this
// try to create a system to store which connections are pulsed when
// test how many luts this uses as it scales
module matrix_flow (
    input clk,
    // replace inouts with matrix array
    inout [7:0] data1,
    inout [7:0] data2,
    inout [7:0] data3,
    inout [7:0] data4,
    input on[3:0]
);
    add_if_enabled adder1_1 ( clk, data2, on[1], data1 );
    add_if_enabled adder1_2 ( clk, data3, on[2], data1 );
    add_if_enabled adder1_3 ( clk, data4, on[3], data1 );

    add_if_enabled adder2_1 ( clk, data1, on[0], data2 );
    add_if_enabled adder2_2 ( clk, data3, on[2], data2 );
    add_if_enabled adder2_3 ( clk, data4, on[3], data2 );

    add_if_enabled adder3_1 ( clk, data1, on[0], data3 );
    add_if_enabled adder3_2 ( clk, data2, on[1], data3 );
    add_if_enabled adder3_3 ( clk, data4, on[3], data3 );

    add_if_enabled adder4_1 ( clk, data1, on[0], data4 );
    add_if_enabled adder4_2 ( clk, data2, on[1], data4 );
    add_if_enabled adder4_3 ( clk, data3, on[2], data4 );
endmodule
