module pn_gen #(
  parameter N=32
)( 
	input clk,
	input rst,
	input next,
	input [N-1:0] init, // 32'b01101011110010110111011010011100
	input [N-1:0] seed,
	output [N-1:0] num
);
	reg [31:0] pn_d, pn_q = init;

	assign num = pn_q;

	always @(*) begin
		if (next) begin
			// pn_d = {pn_q[N-2:0], pn_q[N-3] ^ pn_q[N-8] ^ pn_q[N-12] ^ pn_q[N-14]};
			pn_d = {pn_q[30:0], pn_q[30] ^ pn_q[24] ^ pn_q[10] ^ pn_q[6]};
		end else begin
			pn_d = pn_q;
		end
	end

	always @(posedge clk) begin
		if (rst) begin
			pn_q <= INIT ^ seed;
		end else begin
			pn_q <= pn_d;
		end
	end

endmodule