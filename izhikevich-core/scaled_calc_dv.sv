module scaled_calc_dv #(
	parameter N=16,
	parameter Q=8
)(
	input [N-1:0] v,
	input [N-1:0] w,
	input [N-1:0] i,
	input [N-1:0] step,
	output [N-1:0] out 
);
	wire [N-1:0] term1, term2, term3, term4, term5, term6, term7, term8;

	mult #(.N(N), .Q(Q)) multiplier1 ( v, v, term1 ); // v*v
	mult #(.N(N), .Q(Q)) multiplier2 ( 16'b0000010000000000, term1, term2 ); // 4*(v*v)
	mult #(.N(N), .Q(Q)) multiplier3 ( 16'b0000010100000000, v, term3 ); // 5*v
	add #(.N(N), .Q(Q)) adder1 ( term2, term3, term4 ); // (4*(v*v))+(5*v)
	negator #(.N(N), .Q(Q)) negator4 ( w, term5 ); // -1*w
	add #(.N(N), .Q(Q)) adder2 ( term4, 16'b0000000101100110, term6 ); // ((4*(v*v))+(5*v))+1.4
	add #(.N(N), .Q(Q)) adder3 ( term5, i, term7 ); // (-1*w)+i
	add #(.N(N), .Q(Q)) adder4 ( term6, term7, term8 ); // (((4*(v*v))+(5*v))+1.4)+((-1*w)+i)
	mult #(.N(N), .Q(Q)) multiplier4 ( term8, step, out ); // ((((4*(v*v))+(5*v))+1.4)+((-1*w)+i))*step
endmodule
