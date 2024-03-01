`include "../ops.sv"


module update_weight_neg #(
	parameter N=32,
	parameter Q=16
)(
	input [N-1:0] t_change,
	input [N-1:0] a_minus,
	input [N-1:0] tau_minus,
	output [N-1:0] weight_change 
);
	reg [N-1:0] term1, term2, term3, term4, term5;

	mult multiplier1 ( t_change, tau_minus, term1 ); // t_change*tau_minus
	abs absolute_value1 ( term1, term2 ); // abs|(t_change*tau_minus)
	negator negator2 ( term2, term3 ); // (abs|(t_change*tau_minus))*-1
	linear_piecewise piecewise1 ( term3, 32'b00000000000000000111011111010011, 32'b00000000000000110111010101101010, 32'b00000000000000001000000100110100, 32'b00000000000000100000000000000000, 32'b10000000000000001000000000000000, term4 ); // e^((abs|(t_change*tau_minus))*-1)
	mult multiplier2 ( a_minus, term4, term5 ); // a_minus*(e^((abs|(t_change*tau_minus))*-1))
	negator negator3 ( term5, weight_change ); // -1*(a_minus*(e^((abs|(t_change*tau_minus))*-1)))
endmodule
