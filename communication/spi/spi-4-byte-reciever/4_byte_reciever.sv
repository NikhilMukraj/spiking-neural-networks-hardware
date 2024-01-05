`include "../spi_peripheral.sv"


module bytes_reciever_top(
    input clk,
	input rst,
	input ss,
	input mosi,
	input sck,
    input apply,
	output reg done_rx,
	output reg done_tx,
	output reg [31:0] out
);
    reg miso, done_bytes;
    reg [7:0] temp_out;

    spi_peripheral spi_peripheral1(
        .clk(clk),
        .rst(rst),
        .ss(ss),
        .mosi(mosi),
        .miso(miso)
        .sck(sck),
        .done_rx(done_rx),
        .done_tx(done_tx),
        .din(8'b00000000),
        .dout(temp_out)
    );

    bytes_reciever bytes_reciever1(
        .rst(rst),
        .done_rx(done_rx),
        .apply(apply),
        .recieved_byte(temp_out),
        .out(out),
        .done_bytes(done_bytes)
    );
endmodule

module bytes_reciever(
    input rst,
    input done_rx,
    input apply,
    input reg [7:0] recieved_byte,
    output reg [31:0] out,
    output done_bytes
);
    reg [1:0] bytes_count;
    reg [32:0] data;

    always @ (*) begin
        if (rst) begin
            bytes_count = 2'b00;
            done_bytes = 1'b0;
            data = 32'b00000000000000000000000000000000;
        end
        if (done_rx & apply) begin
            bytes_count <= bytes_count + 1'b1;
			data = {data[23:0], recieved_byte};

			if (bytes_count == 2'b11) begin 
				done_bytes <= 1'b1;
				out <= data;
			end else begin
				done_rx <= 1'b0;
			end
        end
    end
endmodule
