`include "../ops.sv"
`include "../calc_dv.sv"
`include "../calc_dw.sv"


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
    input rst,
	output reg [N-1:0] voltage,
    output reg [N-1:0] w
);
    wire eq, gt, lt;
    reg apply_edge;
    reg [N-1:0] dv, dw, new_voltage, new_w, actual_voltage, actual_w;

    fixed_point_cmp threshold ( actual_voltage, v_th, eq, gt, lt );

    calc_dv calc_dv1 ( actual_voltage, w, i, dv );
    calc_dw calc_dw1 (
        a,
        b,
        c,
        d,
        actual_voltage,
        actual_voltage,
        dt,
        t,
        dw
    );

    add adder1 ( actual_voltage, dv, new_voltage );
    add adder2 ( actual_w, dw, new_w );

    always @ (*) begin
        if (rst) begin
            actual_voltage = v_init;
            actual_w = w_init;
            voltage = v_init;
            w = w_init;
        end
        else if (!apply) begin
            apply_edge <= 1; 
        end
        else if (apply_edge) begin
            if (eq | gt) begin
                actual_voltage <= c;
                actual_w <= d;
            end else if (apply) begin
                actual_voltage <= new_voltage;
                actual_w <= new_w;
            end
            apply_edge <= 0; 
        end

        voltage <= actual_voltage;
        w <= actual_w;
    end
endmodule
