// as soon as ss is selected, din should be filled with 0s 
module spi_peripheral(
	input rst,
	input ss,
	input mosi,
	output reg miso,
	input sck,
	output reg done_rx,
	output reg done_tx,
	input [7:0] din,
	output reg [7:0] dout
);
	reg [2:0] bit_count_rx, bit_count_tx;
	reg [7:0] data_rx;

	always @ (posedge sck) begin 
		if (ss) begin
			bit_count_rx <= 3'b000;
		end else begin
			bit_count_rx <= bit_count_rx + 1'b1;
			data_rx = {data_rx[6:0], mosi};

			if (bit_count_rx == 3'b111) begin 
				done_rx <= 1'b1;
				dout <= data_rx;
			end else begin
				done_rx <= 1'b0;
			end
		end
	end

	always @ (negedge sck) begin
		if (ss) begin
			bit_count_tx <= 3'b000;
		end else begin
			bit_count_tx <= bit_count_tx + 1'b1;
			miso <= din[~bit_count_tx];
			
			if (bit_count_tx == 3'b111) begin 
				done_tx <= 1'b1;
			end else begin
				done_tx <= 1'b0;
			end
		end
	end

	always @ (*) begin
		if (rst) begin
			done_tx <= 1'b0;
			done_rx <= 1'b0;
			bit_count_tx <= 3'b000;
			bit_count_rx <= 3'b000;
			data_rx <= 8'b00000000;
			miso <= 1'b0;
		end
	end
endmodule
