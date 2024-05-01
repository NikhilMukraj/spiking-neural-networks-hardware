`include "../ops.sv"
`include "calc_dv.sv"
`include "calc_dw.sv"


module izhikevich_core #(
	parameter N=24,
	parameter Q=8
)(
    input clk,
	input [N-1:0] i,
	input [N-1:0] v_init,
	input [N-1:0] w_init,
    input [N-1:0] v_th,
    input [N-1:0] dv_step,
    input [N-1:0] dw_step,
	input [N-1:0] a,
	input [N-1:0] b,
	input [N-1:0] c,
	input [N-1:0] d,
    input apply,
    input rst,
    output reg is_spiking,
	output reg [N-1:0] voltage,
    output reg [N-1:0] w,
    output reg [N-1:0] last_dv
);
    reg eq, gt, lt, apply_edge;
    wire [N-1:0] dv, dw, new_voltage, new_w, w_at_th;

    calc_dv #(.N(N), .Q(Q)) calc_dv1 ( voltage, w, i, dv_step, dv );
    calc_dw #(.N(N), .Q(Q)) calc_dw1 (
        a,
        b,
        voltage,
        w,
        dw_step,
        dw
    );

    add #(.N(N), .Q(Q)) adder1 ( voltage, dv, new_voltage );
    add #(.N(N), .Q(Q)) adder2 ( w, dw, new_w );
    add #(.N(N), .Q(Q)) adder3 ( w, d, w_at_th );

    always @ (posedge clk) begin
        if (rst) begin
            voltage = v_init;
            w = w_init;
            is_spiking <= 1'b0;
            last_dv <= 20'b00000000000000000000; // 0
        end

        if (apply & ($signed(voltage) > $signed(v_th))) begin
            voltage <= c;
            w <= w_at_th;
            is_spiking <= 1'b1;
            last_dv <= dv;
        end else if (apply) begin
            voltage <= new_voltage;
            w <= new_w;
            is_spiking <= 1'b0;
            last_dv <= dv;
        end
    end
endmodule
