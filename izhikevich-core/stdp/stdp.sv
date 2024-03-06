`include "./../../ops.sv"
// `include "update_weight_neg.sv"
// `include "update_weight_pos.sv"
`include "./../update_weight.sv"


module stdp #(
    parameter N=32,
    parameter Q=32
)(
    input clk,
    input apply,
    input [N-1:0] t_change,
    // input [N-1:0] a_plus,
    // input [N-1:0] a_minus,
    // input [N-1:0] tau_plus,
    // input [N-1:0] tau_minus,
    input [N-1:0] m1,
    input [N-1:0] m2,
    input [N-1:0] b1,
    input [N-1:0] b2,
    output reg [N-1:0] dw
);
    reg [N-1:0] pos_change, neg_change, neg_change_intermediate, inverted_b1, inverted_b2;
    reg eq, gt, lt;

    negator negator1(
        b1,
        inverted_b1
    );

    negator negator2(
        b2,
        inverted_b2
    );

    fixed_point_cmp fcmp(
        t_change,
        32'b00000000000000000000000000000000, // 0
        eq,
        gt,
        lt
    );

    // a and tau values should be prefit for in the linear piecewise

    update_weight update_weight1(
        t_change,
        m1,
        m2,
        b1,
        b2,
        32'b10000000000000001000000000000000, // -0.5
        neg_change_intermediate
    );
    update_weight update_weight2(
        t_change,
        m1,
        m2,
        b1,
        b2,
        32'b10000000000000001000000000000000, // -0.5
        pos_change
    );

    negator negator3(
        neg_change_intermediate,
        neg_change
    );

    always @ (*) begin
        if (lt & !eq & apply) begin
            dw <= neg_change;
        end else if (!lt & !eq & apply) begin
            dw <= pos_change;
        end //else if (!lt & eq & apply) begin
            //dw <= 32'b00000000000000000000000000000000; // 0, return 0 if no difference in spike times
        //end
    end
endmodule
