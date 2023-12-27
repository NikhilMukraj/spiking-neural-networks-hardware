`include "../../spi_slave.sv"


module spi_reciever(
    input clk,
	input rst,
	input ss,
	input mosi,
	output miso,
	input sck,
	output done,
	input [7:0] din,
	output [7:0] led
);
    spi_slave peripheral(
        .clk(clk),
        .rst(rst),
        .ss(ss),
        .mosi(mosi),
        .miso(miso),
        .sck(sck),
        .done(done),
        .din(din),
        .dout(led)
    );
endmodule