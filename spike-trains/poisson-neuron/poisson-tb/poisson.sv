module poisson #(
    parameter N=18,
)(
    input clk,
    input apply,
    input [N-1:0] seed,
    input [N-1:0] chance_of_spiking,
    input [N-1:0] height,
    output reg [N-1:0] voltage,
);

endmodule
