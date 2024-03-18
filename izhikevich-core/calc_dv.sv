module calc_dv #(
	parameter N=32,
	parameter Q=16
)(
	input [N-1:0] v,
	input [N-1:0] w,
	input [N-1:0] i,
	input [N-1:0] step,
	output [N-1:0] out 
);
	wire [N-1:0] term1, term2, term3, term4, term5, term6, term7, term8;

	mult multiplier1 ( v, v, term1 ); // v*v
	mult multiplier2 ( 32'b00000000000000000000101000111101, term1, term2 ); // 0.04*(v*v)
	mult multiplier3 ( 32'b00000000000001010000000000000000, v, term3 ); // 5*v
	add adder1 ( term2, term3, term4 ); // (0.04*(v*v))+(5*v)
	negator negator4 ( w, term5 ); // -1*w
	add adder2 ( term4, 32'b00000000100011000000000000000000, term6 ); // ((0.04*(v*v))+(5*v))+140
	add adder3 ( term5, i, term7 ); // (-1*w)+i
	add adder4 ( term6, term7, term8 ); // (((0.04*(v*v))+(5*v))+140)+((-1*w)+i)
	mult multiplier4 ( term8, step, out ); // ((((0.04*(v*v))+(5*v))+140)+((-1*w)+i))*step
endmodule
