module calc_dv #(
	parameter N=20,
	parameter Q=10
)(
	input [N-1:0] v,
	input [N-1:0] w,
	input [N-1:0] i,
	input [N-1:0] step,
	output [N-1:0] out 
);
	wire [N-1:0] term1, term2, term3, term4, term5, term6, term7, term8;

	mult #(.N(N), .Q(Q)) multiplier1 ( v, v, term1 ); // v*v
	mult #(.N(N), .Q(Q)) multiplier2 ( 20'b00000000000000101000, term1, term2 ); // 0.04*(v*v)
	mult #(.N(N), .Q(Q)) multiplier3 ( 20'b00000001010000000000, v, term3 ); // 5*v
	add #(.N(N), .Q(Q)) adder1 ( term2, term3, term4 ); // (0.04*(v*v))+(5*v)
	negator #(.N(N), .Q(Q)) negator4 ( w, term5 ); // -1*w
	add #(.N(N), .Q(Q)) adder2 ( term4, 20'b00100011000000000000, term6 ); // ((0.04*(v*v))+(5*v))+140
	add #(.N(N), .Q(Q)) adder3 ( term5, i, term7 ); // (-1*w)+i
	add #(.N(N), .Q(Q)) adder4 ( term6, term7, term8 ); // (((0.04*(v*v))+(5*v))+140)+((-1*w)+i)
	mult #(.N(N), .Q(Q)) multiplier4 ( term8, step, out ); // ((((0.04*(v*v))+(5*v))+140)+((-1*w)+i))*step
endmodule
