module update_weight #(
	parameter N=32,
	parameter Q=16
)(
	input [N-1:0] t_change,
	input [N-1:0] m1,
	input [N-1:0] m2,
	input [N-1:0] b1,
	input [N-1:0] b2,
    input [N-1:0] split,
	output [N-1:0] weight_change 
);
	reg [N-1:0] term1, term2;

	abs absolute_value1 ( t_change, term1 ); // abs|(t_change)
	negator negator2 ( term1, term2 ); // (abs|(t_change))*-1
	linear_piecewise piecewise1 ( 
        term2, 
        m1, 
        m2, 
        b1, 
        b2, 
        split, 
        weight_change 
    ); // e^((abs|(t_change))*-1)
endmodule
