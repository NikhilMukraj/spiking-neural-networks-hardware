module mult #( // https://github.com/Mehdi0xC/SystemVerilog-FixedPoint-Arithmetic/blob/master/multiplier.sv
    parameter N = 16,
    parameter F = 8
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

module booth_mult #(
	parameter N = 8,
	parameter Q = 4,
	parameter bits = 8
)(
	input clk,
	input enable,
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
	assign p_init = { {(N){1'b0}}, b, 1'b0 };

	reg [$clog2(N)-1:0] count;
	reg [$clog2(N)-1:0] max_count = N - 1;

	// test p_new = p + 1'b1
	add #(.N(N * 2 + 1), .Q(Q * 2 + 1)) adder2( p, to_add, p_new );

	always @ (posedge clk) begin
		if (rst) begin
			p <= p_init;
			count <= 4'b000;
			done <= 1'b0;
		end
		if (!done & enable) begin
			case (p[1:0])
				2'b10 : to_add <= s;
				2'b01 : to_add <= a_static;
				// 2'b00 :
				// 2'b11 :
				default : to_add <= {(N * 2 + 1){1'b0}};
			endcase

			p <= { p_new[N * 2], p[N * 2:1] };
			count <= count + 1;

			done <= count == max_count;
		end
	end

	// sign bit + rest of string
	// this will only work when same number of fractional and integer bits
	// or if just using integers
	assign c = {p[N * 2], p[bits + 1:bits * 2 + 1]};
endmodule
