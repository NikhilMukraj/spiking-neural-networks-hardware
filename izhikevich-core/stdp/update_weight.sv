`include "../ops.sv"


module update_weight #(
	parameter N=32,
	parameter Q=16
)(
	input [N-1:0] t_change,
	// input [N-1:0] a_minus,
	// input [N-1:0] tau_minus,
	input [N-1:0] m1, // 32'b00000000000000000111011111010011
	input [N-1:0] m2, // 32'b00000000000000110111010101101010
	input [N-1:0] b1, // 32'b00000000000000001000000100110100
	input [N-1:0] b2, // 32'b00000000000000100000000000000000
	output [N-1:0] weight_change 
);
	reg [N-1:0] term1;

	abs absolute_value1 ( t_change, term1 ); // abs|(t_change)
	negator negator2 ( term1, term2 ); // (abs|(t_change))*-1
	// split is -0.5
	linear_piecewise piecewise1 ( term2, m1, m2, b1, b2, 32'b10000000000000001000000000000000, term3 ); // e^((abs|(t_change*tau_minus))*-1)
	// mult multiplier2 ( a_minus, term4, term5 ); // a_minus*(e^((abs|(t_change*tau_minus))*-1))
	// negator negator3 ( term3, weight_change ); // -1*(a_minus*(e^((abs|(t_change*tau_minus))*-1)))
endmodule
