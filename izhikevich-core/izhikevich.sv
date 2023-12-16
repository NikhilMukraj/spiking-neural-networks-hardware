`include "ops.sv"
`include "calc_dv.sv"
`include "calc_dw.sv"


module izhikevich_core #(
	parameter N=32,
	parameter Q=16
)(
	input [N-1:0] i,
	input [N-1:0] v_init,
	input [N-1:0] w_init,
    input [N-1:0] v_th,
    input [N-1:0] dt,
    input [N-1:0] t,
	input [N-1:0] a,
	input [N-1:0] b,
	input [N-1:0] c,
	input [N-1:0] d,
    // input calculate,
    input apply,
	output reg [N-1:0] voltage,
    output reg [N-1:0] w
);
    wire eq, gt, lt;
    reg [N-1:0] dv, dw, new_voltage, new_w;

    assign voltage = v_init;
    assign w = w_init;

    fixed_point_cmp threshold ( voltage, v_th, eq, gt, lt );

    calc_dv calc_dv1 ( voltage, w, i, dv );
    calc_dw calc_dw1 (
        a,
        b,
        c,
        d,
        voltage,
        w,
        dt,
        t,
        dw
    );

    add adder1 ( voltage, dv, new_voltage );
    add adder2 ( w, dw, new_w );

    always @ (*) begin
        if (eq | gt) begin
            voltage <= c;
            w <= d;
        end else if (apply) begin
            voltage <= new_voltage;
            w <= new_w;
        end
    end
endmodule