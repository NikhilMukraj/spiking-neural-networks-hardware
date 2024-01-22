module top(
    input in1,
    input in2,
    input rst_n,
    output reg [7:0] leds
);
    always @ (*) begin
        if (!rst_n) begin
            leds = 8'b00000000;
        end

        if (in1) begin
            leds[7:4] = 4'b1111;
        end else begin
            leds[7:4] = 4'b0000;
        end
        if (in2) begin 
            leds[3:0] = 4'b1111;
        end else begin
            leds[3:0] = 4'b0000;
        end
    end
endmodule
