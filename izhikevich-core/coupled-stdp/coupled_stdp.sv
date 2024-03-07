module iterator #(
    parameter N=32,
    parameter Q=16
)(
    input clk,
    input apply,
    output reg [Q-1:0] iteration_count
);
    // iterate over until you loop back around
endmodule

module top #(
    parameter N=32,
    parameter Q=16
)(
    input clk,
    input apply,
    input [N-1:0] v_init,
    input [N-1:0] v_th,
    input [N-1:0] w_init,
    input [N-1:0] a,
    input [N-1:0] b,
    input [N-1:0] c,
    input [N-1:0] d,
    input [N-1:0] weight_init,
    input [N-1:0] m1,
    input [N-1:0] m2,
    input [N-1:0] b1,
    input [N-1:0] b2,
    output is_spiking1,
    output is_spiking2,
    output reg [N-1:0] voltage1,
    output reg [N-1:0] voltage2,
    output reg [N-1:0] w1,
    output reg [N-1:0] w2,
);
    // generate two izhikevich neurons
    // iterate at each clk and apply signal
    // if they are spiking do stdp
endmodule