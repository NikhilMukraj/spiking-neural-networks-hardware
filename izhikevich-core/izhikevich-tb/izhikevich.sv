`include "../ops.sv"
`include "../calc_dv.sv"
`include "../calc_dw.sv"


module izhikevich_core #(
	parameter N=32,
	parameter Q=16
)(
    input clk,
	input [N-1:0] i,
	input [N-1:0] v_init,
	input [N-1:0] w_init,
    input [N-1:0] v_th,
    input [N-1:0] step,
	input [N-1:0] a,
	input [N-1:0] b,
	input [N-1:0] c,
	input [N-1:0] d,
    input apply,
    input rst,
	output reg [N-1:0] voltage,
    output reg [N-1:0] w
);
    reg eq, gt, lt, apply_edge;
    reg [N-1:0] dv, dw, new_voltage, new_w, w_at_th;

    calc_dv calc_dv1 ( voltage, w, i, step, dv );
    calc_dw calc_dw1 (
        a,
        b,
        voltage,
        w,
        step,
        dw
    );

    add adder1 ( voltage, dv, new_voltage );
    add adder2 ( w, dw, new_w );
    add adder3 ( w, d, w_at_th );

    always @ (posedge clk) begin
        if (rst) begin
            voltage = v_init;
            w = w_init;
        end

        if (apply) begin
            if ($signed(voltage) > $signed(v_th)) begin
                voltage <= c;
                w <= w_at_th;
            end else begin
                voltage <= new_voltage;
                w <= new_w;
            end
        end
    end
endmodule
