`include "../izhikevich-tb/izhikevich.sv"

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

module voltage_to_current #(
    parameter N=32,
    parameter Q=16
)(
    input [N-1:0] dv,
    input [N-1:0] dt_reciprocal,
    input [N-1:0] cm_reciprocal,
    output reg [N-1:0] current
);
    reg [N-1:0] term1;
    mult multiplier1(dv, dt_reciprocal, term1);
    mult multiplier2(term1, cm_reciprocal, current);
endmodule

module top #(
    parameter N=32,
    parameter Q=16
)(
    input clk,
    input apply,
    input enable_stdp,
    input rst,
    input [N-1:0] i, // input current not voltage
    input [N-1:0] v_init,
    input [N-1:0] v_th,
    input [N-1:0] w_init,
    input [N-1:0] a,
    input [N-1:0] b,
    input [N-1:0] c,
    input [N-1:0] d,
    input [N-1:0] dt,
    input [N-1:0] dt_reciprocal,
    input [N-1:0] cm_reciprocal,
    input [N-1:0] step,
    input [N-1:0] weight_init,
    input [N-1:0] m1,
    input [N-1:0] m2,
    input [N-1:0] b1,
    input [N-1:0] b2,
    output is_spiking1,
    output is_spiking2,
    output reg [N-1:0] voltage1,
    output reg [N-1:0] voltage2,
    output reg [N-1:0] dv1,
    output reg [N-1:0] dv2,
    output reg [N-1:0] w1,
    output reg [N-1:0] w2,
);
    // generate two izhikevich neurons
    // iterate at each clk and apply signal
    // if they are spiking do stdp
    // spike time is recorded as iterator current timestep - 1

    // use current as input
    // use last dv for current
    // izhikevich neurons need to be modified to output dv change
    // eventually try using multiple automatically generated neurons as input
    // potentially could use sign

    // STDP SHOULD ONLY OCCUR ON STDP ENABLED SIGNAL
    // allows for testing of coupled with and without stdp

    // beginning of coupled neurons

    reg is_spiking1, is_spiking2;
    reg [N-1:0] voltage1, w1, last_dv1, voltage2, w2, last_dv2;
    reg [N-1:0] input_current;

    izhikevich_core neuron1(
        clk,
        i,
        v_init,
        w_init,
        v_th,
        step,
        a,
        b,
        c,
        d,
        apply,
        rst,
        is_spiking1,
        voltage1,
        w1,
        last_dv1
    );

    voltage_to_current converter1(
        last_dv1,
        dt_reciprocal,
        cm_reciprocal,
        input_current
    );

    izhikevich_core neuron1(
        clk,
        input_current,
        v_init,
        w_init,
        v_th,
        step,
        a,
        b,
        c,
        d,
        apply,
        rst,
        is_spiking2,
        voltage2,
        w2,
        last_dv2
    );
endmodule