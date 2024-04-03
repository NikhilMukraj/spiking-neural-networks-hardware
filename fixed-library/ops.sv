module div #(
	parameter N = 32,
	parameter Q = 16
) (
	input [N-1:0] a, b,
	output reg [N-1:0] c
);
	reg [N-1:0] intermediate;
	reciprocal rec(
		.a(b),
		.out(intermediate)
	);

	mult multiplier(
		.a(a),
		.b(intermediate),
		.c(c)
	);
endmodule

module add #( // https://github.com/freecores/verilog_fixed_point_math_library/blob/master/qadd.v
	parameter Q = 16,
	parameter N = 32
)(
    input [N-1:0] a,
    input [N-1:0] b,
    output [N-1:0] c
);

    reg [N-1:0] res;

    assign c = res;

    always @(a,b) begin
        if (a[N-1] == b[N-1]) begin						
            res[N-2:0] = a[N-2:0] + b[N-2:0];		
            res[N-1] = a[N-1];							                                    
        end												
        else if(a[N-1] == 0 && b[N-1] == 1) begin		
            if ( a[N-2:0] > b[N-2:0] ) begin					
                res[N-2:0] = a[N-2:0] - b[N-2:0];			
                res[N-1] = 0;										
            end
            else begin												
                res[N-2:0] = b[N-2:0] - a[N-2:0];			
                if (res[N-2:0] == 0)
                    res[N-1] = 0;										
                else
                    res[N-1] = 1;										
            end
        end
        else begin												
            if ( a[N-2:0] > b[N-2:0] ) begin					
                res[N-2:0] = a[N-2:0] - b[N-2:0];			
                if (res[N-2:0] == 0)
                    res[N-1] = 0;										
                else
                    res[N-1] = 1;										
                end
            else begin												
                res[N-2:0] = b[N-2:0] - a[N-2:0];			
                res[N-1] = 0;										
            end
        end
    end
endmodule

module negator #(
	parameter N = 32
)(
	input [N-1:0] a,
	output reg [N-1:0] out
);	
	always @ (*) begin
		if (a == {N{1'b0}}) begin
			out = a;
		end else begin
			out = {~a[N-1], a[N-2:0]};
		end
	end
endmodule

module mult #( // https://github.com/Mehdi0xC/SystemVerilog-FixedPoint-Arithmetic/blob/master/multiplier.sv
    parameter N = 32,
    parameter F = 16
)(
	input [N-1:0] a, 
	input [N-1:0] b,
	output [N-1:0] c
);
	reg [2*N-1:0] result;
	reg [N-1:0] finalresult;
	assign c = finalresult;

	always @ (*) begin						
		result <= a[N-2:0] * b[N-2:0];													
	end
	
	always @ (*) begin 										
		finalresult[N-1] <= a[N-1] ^ b[N-1];	
		finalresult[N-2:0] <= result[N-2+F:F];							
	end
endmodule

module booth_mult #(
	parameter N = 32,
	parameter Q = 16
)(
	input clk,
	input rst,
	input [N-1:0] a,
	input [N-1:0] b,
	output [N-1:0] c,
	output reg done
);
	reg [N-1:0] two_comp_m;

	add #(.N(N), .Q(Q)) adder1( ~a, {{(N-1){1'b0}}, 1'b1}, two_comp_m );

	reg [N * 2:0] a_static, s, p_init, p, to_add, p_new;

	assign a_static = { a, {(N+1){1'b0}} };
	assign s = { two_comp_m, {(N+1){1'b0}} };
	assign p_init = { {(N+1){1'b0}}, b };

	reg [4:0] count;
	reg [4:0] max_count = $bits(N);

	add #(.N(N * 2 + 1), .Q(Q * 2 + 1)) adder2( p, to_add, p_new );

	always @ (posedge clk) begin
		if (rst) begin
			p <= p_init;
			count <= 4'b000;
			done <= 1'b0;
		end
		if (!done) begin
			case (p[1:0])
				2'b10 : to_add <= s;
				2'b01 : to_add <= a_static;
				// 2'b00 :
				// 2'b11 :
				default : to_add <= {(N * 2 + 1){1'b0}};
			endcase

			p <= { p_new[N-1], p[N-1:1] };
			count <= count + 1;

			done <= count == max_count;
		end
	end

	assign c = {p[N * 2], p[N-2:0]};
endmodule

module abs #(
	parameter N = 32
)(
	input [N-1:0] x,
	output reg [N-1:0] out
);
	assign out = {1'b0, x[N-2:0]};
endmodule

module reciprocal #(
	parameter N = 32,
	parameter Q = 16
) (
	input [N-1:0] a,
	output reg [N-1:0] out
);
	reg [N-1:0] estimate;
	reg [4:0] msb;
	reg [5:0] signed_msb;
	always @ (a) begin
		msb = 5'b00000;
	
		if (a[30] == 1'b1) msb = 5'b00000;
		else if (a[29] == 1'b1) msb = 5'b00001;
		else if (a[28] == 1'b1) msb = 5'b00010;
		else if (a[27] == 1'b1) msb = 5'b00011;
		else if (a[26] == 1'b1) msb = 5'b00100;
		else if (a[25] == 1'b1) msb = 5'b00101;
		else if (a[24] == 1'b1) msb = 5'b00110;
		else if (a[23] == 1'b1) msb = 5'b00111;
		else if (a[22] == 1'b1) msb = 5'b01000;
		else if (a[21] == 1'b1) msb = 5'b01001;
		else if (a[20] == 1'b1) msb = 5'b01010;
		else if (a[19] == 1'b1) msb = 5'b01011;
		else if (a[18] == 1'b1) msb = 5'b01100;
		else if (a[17] == 1'b1) msb = 5'b01101;
		else if (a[16] == 1'b1) msb = 5'b01110;
		else if (a[15] == 1'b1) msb = 5'b01111;
		else if (a[14] == 1'b1) msb = 5'b10000;
		else if (a[13] == 1'b1) msb = 5'b10001;
		else if (a[12] == 1'b1) msb = 5'b10010;
		else if (a[11] == 1'b1) msb = 5'b10011;
		else if (a[10] == 1'b1) msb = 5'b10100;
		else if (a[9] == 1'b1) msb = 5'b10101;
		else if (a[8] == 1'b1) msb = 5'b10110;
		else if (a[7] == 1'b1) msb = 5'b10111;
		else if (a[6] == 1'b1) msb = 5'b11000;
		else if (a[5] == 1'b1) msb = 5'b11001;
		else if (a[4] == 1'b1) msb = 5'b11010;
		else if (a[3] == 1'b1) msb = 5'b11011;
		else if (a[2] == 1'b1) msb = 5'b11100;
		else if (a[1] == 1'b1) msb = 5'b11101;
		else if (a[0] == 1'b1) msb = 5'b11110;		
			
		signed_msb = { a[31], msb };
	end

	// if zero just return max for now
	// n = 32
	// print('\n'.join([f"5'b{bin(i)[2:].zfill(int(log2(n)))}: estimate = 32'b{bin(1 << i)[2:].zfill(n)};" for i in range(n)]))
	always @ (signed_msb) begin
		case (signed_msb)
			6'b000000: estimate = 32'b00000000000000000000000000000001;
			6'b000001: estimate = 32'b00000000000000000000000000000010;
			6'b000010: estimate = 32'b00000000000000000000000000000100;
			6'b000011: estimate = 32'b00000000000000000000000000001000;
			6'b000100: estimate = 32'b00000000000000000000000000010000;
			6'b000101: estimate = 32'b00000000000000000000000000100000;
			6'b000110: estimate = 32'b00000000000000000000000001000000;
			6'b000111: estimate = 32'b00000000000000000000000010000000;
			6'b001000: estimate = 32'b00000000000000000000000100000000;
			6'b001001: estimate = 32'b00000000000000000000001000000000;
			6'b001010: estimate = 32'b00000000000000000000010000000000;
			6'b001011: estimate = 32'b00000000000000000000100000000000;
			6'b001100: estimate = 32'b00000000000000000001000000000000;
			6'b001101: estimate = 32'b00000000000000000010000000000000;
			6'b001110: estimate = 32'b00000000000000000100000000000000;
			6'b001111: estimate = 32'b00000000000000001000000000000000;
			6'b010000: estimate = 32'b00000000000000010000000000000000;
			6'b010001: estimate = 32'b00000000000000100000000000000000;
			6'b010010: estimate = 32'b00000000000001000000000000000000;
			6'b010011: estimate = 32'b00000000000010000000000000000000;
			6'b010100: estimate = 32'b00000000000100000000000000000000;
			6'b010101: estimate = 32'b00000000001000000000000000000000;
			6'b010110: estimate = 32'b00000000010000000000000000000000;
			6'b010111: estimate = 32'b00000000100000000000000000000000;
			6'b011000: estimate = 32'b00000001000000000000000000000000;
			6'b011001: estimate = 32'b00000010000000000000000000000000;
			6'b011010: estimate = 32'b00000100000000000000000000000000;
			6'b011011: estimate = 32'b00001000000000000000000000000000;
			6'b011100: estimate = 32'b00010000000000000000000000000000;
			6'b011101: estimate = 32'b00100000000000000000000000000000;
			6'b011110: estimate = 32'b01000000000000000000000000000000;
			6'b011111: estimate = 32'b10000000000000000000000000000000;
			6'b100000: estimate = 32'b10000000000000000000000000000001;
			6'b100001: estimate = 32'b10000000000000000000000000000010;
			6'b100010: estimate = 32'b10000000000000000000000000000100;
			6'b100011: estimate = 32'b10000000000000000000000000001000;
			6'b100100: estimate = 32'b10000000000000000000000000010000;
			6'b100101: estimate = 32'b10000000000000000000000000100000;
			6'b100110: estimate = 32'b10000000000000000000000001000000;
			6'b100111: estimate = 32'b10000000000000000000000010000000;
			6'b101000: estimate = 32'b10000000000000000000000100000000;
			6'b101001: estimate = 32'b10000000000000000000001000000000;
			6'b101010: estimate = 32'b10000000000000000000010000000000;
			6'b101011: estimate = 32'b10000000000000000000100000000000;
			6'b101100: estimate = 32'b10000000000000000001000000000000;
			6'b101101: estimate = 32'b10000000000000000010000000000000;
			6'b101110: estimate = 32'b10000000000000000100000000000000;
			6'b101111: estimate = 32'b10000000000000001000000000000000;
			6'b110000: estimate = 32'b10000000000000010000000000000000;
			6'b110001: estimate = 32'b10000000000000100000000000000000;
			6'b110010: estimate = 32'b10000000000001000000000000000000;
			6'b110011: estimate = 32'b10000000000010000000000000000000;
			6'b110100: estimate = 32'b10000000000100000000000000000000;
			6'b110101: estimate = 32'b10000000001000000000000000000000;
			6'b110110: estimate = 32'b10000000010000000000000000000000;
			6'b110111: estimate = 32'b10000000100000000000000000000000;
			6'b111000: estimate = 32'b10000001000000000000000000000000;
			6'b111001: estimate = 32'b10000010000000000000000000000000;
			6'b111010: estimate = 32'b10000100000000000000000000000000;
			6'b111011: estimate = 32'b10001000000000000000000000000000;
			6'b111100: estimate = 32'b10010000000000000000000000000000;
			6'b111101: estimate = 32'b10100000000000000000000000000000;
			6'b111110: estimate = 32'b11000000000000000000000000000000;
			// 6'b111111: estimate = 32'b110000000000000000000000000000000;		
		endcase 
	end

	reg [N-1:0] ax1, axsubtracted1, x1;
	reg [N-1:0] ax2, axsubtracted2, x2;
	reg [N-1:0] ax3, axsubtracted3, x3;
	reg [N-1:0] ax4, axsubtracted4, x4;
	reg [N-1:0] ax5, axsubtracted5;

	reg [N-1:0] minus_a; 
	reg [N-1:0] negative_one = 32'b10000000000000010000000000000000;
	reg [N-1:0] two = 32'b00000000000000100000000000000000;

	mult negator(
		.a(negative_one), // -1
		.b(a),
		.c(minus_a)
	);

	// - a * x
	mult multiplier1_1(
		.a(minus_a), 
		.b(estimate),
		.c(ax1)
	);

	// 2 - a * x 
	add adder1_1(
		.a(two),
		.b(ax1),
		.c(axsubtracted1)
	);

	// x * (2 - a * x)
	mult multiplier1_2(
		.a(estimate),
		.b(axsubtracted1),
		.c(x1)
	);

	// - a * x
	mult multiplier2_1(
		.a(minus_a), 
		.b(x1),
		.c(ax2)
	);

	// 2 - a * x
	add adder2_1(
		.a(two),
		.b(ax2),
		.c(axsubtracted2)
	);

	// x * (2 - a * x)
	mult multiplier2_2(
		.a(x1),
		.b(axsubtracted2),
		.c(x2)
	);

	// - a * x
	mult multiplier3_1(
		.a(minus_a), 
		.b(x2),
		.c(ax3)
	);

	// 2 - a * x
	add adder3_1(
		.a(two),
		.b(ax3),
		.c(axsubtracted3)
	);

	// x * (2 + a * x)
	mult multiplier3_2(
		.a(x2),
		.b(axsubtracted3),
		.c(x3)
	);

	// a * x
	mult multiplier4_1(
		.a(minus_a), 
		.b(x3),
		.c(ax4)
	);

	// 2 - a * x
	add adder4_1(
		.a(two),
		.b(ax4),
		.c(axsubtracted4)
	);

	// x * (2 - a * x)
	mult multiplier4_2(
		.a(x3),
		.b(axsubtracted4),
		.c(x4)
	);	

	// - a * x
	mult multiplier5_1(
		.a(minus_a), 
		.b(x4),
		.c(ax5)
	);

	// 2 - a * x
	add adder5_1(
		.a(two),
		.b(ax5),
		.c(axsubtracted5)
	);

	// x * (2 - a * x)
	mult multiplier5_2(
		.a(x4),
		.b(axsubtracted5),
		.c(out)
	);	
endmodule

module exp #(
	parameter N = 32
) (
	input [N-1:0] x,
	output reg [N-1:0] out
);
	reg [N-1:0] one = 32'b00000000000000010000000000000000;
	reg [N-1:0] onehalf = 32'b00000000000000001000000000000000;
	reg [N-1:0] onesixth = 32'b00000000000000000010101010101010;

	reg [N-1:0] xterm, term1, xsquare, term2, term3, xcube, term4, term5, recval;

	assign xterm = { 1'b0, x[N-2:0] };

	// 1 + x
	add adder1(
		.a(one),
		.b(xterm),
		.c(term1) 
	);

	// x ^ 2
	mult multiplier1(
		.a(xterm),
		.b(xterm),
		.c(xsquare)
	);

	// x ^ 2 / 2!
	mult multiplier2(
		.a(xsquare),
		.b(onehalf),
		.c(term2)
	);

	// 1 + x + (x ^ 2 / 2!)
	add adder2(
		.a(term1),
		.b(term2),
		.c(term3)
	);

	// x ^ 3
	mult multiplier3(
		.a(xterm),
		.b(xsquare),
		.c(xcube)
	);

	// x ^ 3 / 3!
	mult multiplier4(
		.a(xcube),
		.b(onesixth),
		.c(term4)
	);

	// 1 + x + (x ^ 2 / 2!) + (x ^ 3 / 3!)
	add adder3(
		.a(term3),
		.b(term4),
		.c(term5)
	);

	reciprocal rec(
		.a(term5),
		.out(recval)
	);

	// if negative take 1/e^-x
	always @ (*) begin
		if (x[N-1] == 1'b1) begin
			out = recval;
		end else begin
			out = term5;
		end
	end
endmodule

module exp_higher_precision #(
	parameter N = 32,
	parameter Q = 16
) (
	input [N-1:0] x,
	output reg [N-1:0] out
);
	reg [N-1:0] q_intermediate, q, q_minus_one, two_power;
	reg [N-1:0] r_intermediate, neg_r_intermediate, r, m_x, exp_r;

	// x / ln(2)
	mult multiplier1(
		x, 
		32'b00000000000000010111000101010100, // 1 / ln(2),
		q_intermediate
	);

	// q = floor(x / ln(2))
	assign q = {x[N-1:Q], 16'b0}; // gets floor

	// q - 1
	add adder1(
		q, 
		32'b10000000000000010000000000000000, // -1
		q_minus_one
	);

	// 2^q
	// assign out 32'b00000000000000010000000000000000 << q_minus_one;

	// r = x - q * ln(2)

	// q * ln(2)
	mult multiplier2(
		q,
		32'b00000000000000001011000101110010, // ln(2)
		r_intermediate
	);

	// - q * ln(2)
	negator negate(
		r_intermediate,
		neg_r_intermediate
	);

	// r = x - q * ln(2)
	add adder2(
		x, 
		neg_r_intermediate,
		r
	);

	// e^r approximated linearly, y = 1.71828182846 * x + 1
	// if r is negative then y = 0.632120558829 * x + 1

	reg [N-1:0] m;

	always @ (r) begin
		if (r[N-1] == 1'b0) begin
			m = 32'b00000000000000011011011111100001; // 1.71828182846
		end else begin
		m = 32'b00000000000000001010000111010010; // 0.632120558829
		end
	end

	mult multiplier3(
		m, 
		r,
		m_x
	);

	add adder3(
		32'b00000000000000010000000000000000, // 1
		m_x,
		exp_r
	);

	always @ (q_minus_one) begin
		if (x[N-2:Q] == 15'b000000000000000) begin
			two_power = 32'b00000000000000010000000000000000; // 1
		end else if (x[N-1:Q] != 16'b0000000000000000 & q[N-1] == 1'b0) begin
			two_power = 32'b00000000000000000000000000000001 << q; // 2 << q-1
		end else begin
			// needs to be negated after
			// two_power = 32'b01000000000000000000000000000000 >> {1'b0, q_minus_one[N-2:0]}; // max >> q-1
		end
	end

	// replace above always block with a lookup
	// or linear interpolation

	// create function for e^x but only between -1 and 1

	// assign two_power = 32'b00000000000000000000000000000001 << q_minus_one; // 2 << q-1

	mult multiplier4(
		two_power,
		exp_r,
		out
	);

	// should be tested between -15 and 15
endmodule

module linear_piecewise #(
	parameter N = 32
) (
	input [N-1:0] x,
	input [N-1:0] m1,
	input [N-1:0] m2,
	input [N-1:0] b1,
	input [N-1:0] b2,
	input [N-1:0] split,
	output reg [N-1:0] out
);
	reg [N-1:0] mx1, mx2, mxb1, mxb2;

	// m1 * x
	mult multiplier1(
		m1,
		x,
		mx1
	);

	// m1 * x + b1
	add adder1(
		mx1,
		b1,
		mxb1
	);

	// m2 * x
	mult multiplier2(
		m2,
		x,
		mx2
	);

	// m2 * x + b1	
	add adder2(
		mx2,
		b2,
		mxb2
	);

	reg eq, gt, lt;

	// see if can be simplified
	fixed_point_cmp cmp1(
		x,
		split,
		eq,
		gt,
		lt
	);

	always @ (*) begin
		if (lt) begin
			out <= mxb1;
		end else begin
			out <= mxb2;
		end
	end
endmodule

module fixed_point_cmp #(
    parameter N = 32
) (
    input [N-1:0] a,
    input [N-1:0] b,
    output reg eq,
    output reg gt,
    output reg lt
);
	always @ (*) begin
        if ((a[N-1] == 1'b0) && (b[N-1] == 1'b0)) begin
            if (a[N-2:0] > b[N-2:0]) begin
                eq = 1'b0;
                gt = 1'b1;
                lt = 1'b0;
            end else if (a[N-2:0] < b[N-2:0]) begin
                eq = 1'b0;
                gt = 1'b0;
                lt = 1'b1;
            end else begin
                eq = 1'b1;
                gt = 1'b0;
                lt = 1'b0;
            end
        end else if ((a[N-1] == 1'b1) && (b[N-1] == 1'b1)) begin
            if (a[N-2:0] < b[N-2:0]) begin
                eq = 1'b0;
                gt = 1'b1;
                lt = 1'b0;
            end else if (a[N-2:0] > b[N-2:0]) begin
                eq = 1'b0;
                gt = 1'b0;
                lt = 1'b1;
            end else begin
                eq = 1'b1;
                gt = 1'b0;
                lt = 1'b0;
            end
        end else begin
            if (a[N-1] == 1'b1) begin
                eq = 1'b0;
                gt = 1'b0;
                lt = 1'b1;
            end else begin
                eq = 1'b0;
                gt = 1'b1;
                lt = 1'b0;
            end
        end
    end
endmodule
