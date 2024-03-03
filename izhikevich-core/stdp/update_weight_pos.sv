`include "../ops.sv"


module update_weight_pos #(
	parameter N=32,
	parameter Q=16
)(
	input [N-1:0] t_change,
	input [N-1:0] a_plus,
	input [N-1:0] tau_plus,
	input [N-1:0] m1, // 32'b10000000000000000111011111010011
	input [N-1:0] m2, // 32'b10000000000000110111010101101010
	input [N-1:0] b1, // 32'b00000000000000001000000100110100
	input [N-1:0] b2, // 32'b00000000000000100000000000000000
	output [N-1:0] weight_change 
);
	reg [N-1:0] term1, term2, term3, term4;

	mult multiplier1 ( t_change, tau_plus, term1 ); // t_change*tau_plus
	abs absolute_value1 ( term1, term2 ); // abs|(t_change*tau_plus)
	negator negator2 ( term2, term3 ); // (abs|(t_change*tau_plus))*-1
	// split at 0.5
	linear_piecewise piecewise1 ( term3, m1, m2, b1, b2, 32'b00000000000000001000000000000000, term4 ); // e^((abs|(t_change*tau_plus))*-1)
	mult multiplier2 ( a_plus, term4, weight_change ); // a_plus*(e^((abs|(t_change*tau_plus))*-1))
endmodule
