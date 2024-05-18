module signed_mult #(
    parameter N=18
)(
    input signed [N-1:0] a, 
    input signed [N-1:0] b,
    output reg signed [N-1] out;
);
	wire signed	[N * 2 - 1:0] mult_out;

	assign mult_out = a * b;
	assign out = {mult_out[N * 2 - 1], mult_out[N * 2 - 4:N - 2]};
endmodule

// input as hex from py tb

// a <=  18'sh0_051E ; // 0.02
// b <=  18'sh0_3333 ; // 0.2
// c <=  18'sh3_8000 ; // -0.5
// d <=  18'sh0_051E ; // 0.02
// p <=  18'sh0_4CCC ; // 0.30
// c14 <= 18'sh1_6666; // 1.4
// I <= 18'sh0_2666 ;  // 0.15

module izhikevich_core #(
    parameter N=18
)(
    input clk,
    input reset,
	input apply,
    input signed [N-1:0] v_init, // 18'sh3_4CCD ; // -0.7
    input signed [N-1:0] u_init, // 18'sh3_CCCD ; // -0.2
    input signed [N-1:0] v_th, // 18'sh0_4CCC ; // 0.30
    input signed [N-1:0] i,
    input signed [N-1:0] a,
    input signed [N-1:0] b,
    input signed [N-1:0] c,
    input signed [N-1:0] d,
    output reg signed [N-1:0] voltage,
    output reg signed [N-1:0] u,
    output reg is_spiking,
);
	reg signed [17:0] v1,u1;
	wire signed	[17:0] u1reset, v1new, u1new, du1;
	wire signed	[17:0] v1xv1, v1xb;
	wire signed	[17:0] p, c14;
	
	assign c14 = 18'sh1_6666; // 1.4
	
	assign voltage = v1;  //copy state var to output
    assign u = u1;
	
	always @ (posedge clk) 
	begin
		if (reset) 
		begin	
			v1 <= v_init; // -0.7
			u1 <= u_init; // -0.2
			spike <= 0;
		end	
		else 
		begin
			if (apply & (v1 > p)) 
			begin 
				v1 <= c; 		
				u1 <= u1reset;
				spike <= 1;
			end
			else if (apply)
			begin
				v1 <= v1new;
				u1 <= u1new; 
				spike <= 0;	
			end
		end 
	end
	
	// dt = 1/16 or 2>>4
	// v1(n+1) = v1(n) + dt*(4*(v1(n)^2) + 5*v1(n) +1.40 - u1(n) + I)
	// but note that what is actually coded is
	// v1(n+1) = v1(n) + (v1(n)^2) + 5/4*v1(n) +1.40/4 - u1(n)/4 + I/4)/4
	signed_mult v1sq(v1xv1, v1, v1);
	assign v1new = v1 + ((v1xv1 + v1+(v1>>>2) + (c14>>>2) - (u1>>>2) + (I>>>2))>>>2);
	
	// u1(n+1) = u1 + dt*a*(b*v1(n) - u1(n))
	assign v1xb = v1>>>b;         //mult (v1xb, v1, b);
	assign du1 = (v1xb-u1)>>>a ;  //mult (du1, (v1xb-u1), a);
	assign u1new = u1 + (du1>>>4) ; 
	assign u1reset = u1 + d ;
endmodule