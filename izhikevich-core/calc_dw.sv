module calc_dw #(
	parameter N=32,
	parameter Q=16
)(
	input [N-1:0] a,
	input [N-1:0] b,
	input [N-1:0] c,
	input [N-1:0] d,
	input [N-1:0] v,
	input [N-1:0] w,
	input [N-1:0] step,
	output [N-1:0] out 
);
	reg [N-1:0] term1, term2, term3, term4;

	mult multiplier1 ( b, v, term1 ); // b*v
	mult multiplier2 ( 32'b10000000000000010000000000000000, w, term2 ); // -1*w
	add adder1 ( term1, term2, term3 ); // (b*v)+(-1*w)
	mult multiplier3 ( a, term3, term4 ); // a*((b*v)+(-1*w))
	mult multiplier4 ( term4, step, out ); // (a*((b*v)+(-1*w)))*step
endmodule
