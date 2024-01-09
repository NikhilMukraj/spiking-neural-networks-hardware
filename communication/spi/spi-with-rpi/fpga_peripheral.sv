`include "../spi_peripheral.sv"


module led_peripheral(
    input rst,
    input sck,
    input ss,
    input mosi,
    output miso,
    output reg [7:0] led,
);
    reg done_rx, done_tx;

    spi_peripheral spi_peripheral1(
        .rst(rst),
        .ss(ss),
        .mosi(mosi),
        .miso(miso)
        .sck(sck),
        .done_rx(done_rx),
        .done_tx(done_tx),
        .din(8'b00000000),
        .dout(led)
    );
endmodule
