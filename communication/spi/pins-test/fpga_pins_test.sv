module top(
    input in1,
    input in2,
    output reg [7:0] leds
);
    assign leds = 8'b00000000;

    always @ (*) begin
        if (in1) begin
            leds[7:4] = 1'b1111;
        end else begin
            leds[7:4] = 1'b0000;
        end
        if (in2) begin 
            leds[3:0] = 1'b0000;
        end else begin
            leds[3:0] = 1'b0000;
        end
    end
endmodule
