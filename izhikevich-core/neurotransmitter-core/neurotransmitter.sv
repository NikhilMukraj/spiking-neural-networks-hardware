// module for calculating concentration
// assume receptor is constantly at 1.0
// modulate for calculating currents

module neurotransmitter_concentration #(
    parameter N = 32,
    parameter Q = 16
)(
    input clk,
    input apply,
    input reg [N-1:0] voltage,
    input reg [N-1:0] clear_constant
    input reg [N-1:0] tmax,
    output reg [N-1:0] t
);
endmodule

module neurotransmitter_current #(
    parameter N = 32,
    parameter Q = 16
)(
    input clk,
    input apply,
    input reg [N-1:0] voltage,
    input reg [N-1:0] reversal_potential,
    input reg [N-1:0] max_synaptic_conductance,
    output reg [N-1:0] current
); 
endmodule
