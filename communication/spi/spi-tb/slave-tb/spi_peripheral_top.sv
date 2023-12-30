// `include "../../spi_slave.sv"

module spi_peripheral(
	input clk,
	input rst,
	input ss,
	input mosi,
	output reg miso,
	input sck,
	output reg done,
	input [7:0] din,
	output reg [7:0] dout
);
	// reg current_bit;
	reg [2:0] bit_count;
	reg [7:0] data;

	always @ (posedge sck) begin 
		if (ss) begin
			bit_count <= 3'b000;
		end else begin
			// current_bit <= mosi;
			bit_count <= bit_count + 1'b1;
			data = {data[6:0], mosi};
			if (bit_count == 3'b111) begin 
				done <= 1'b1;
				dout <= data;
			end else begin
				done <= 1'b0;
			end
		end
	end

	always @ (*) begin
		if (rst) begin
			// current_bit <= 1'b0;
			bit_count <= 3'b000;
			data <= 8'b00000000;
		end
	end
endmodule
