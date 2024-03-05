`include "../ops.sv"
`include "update_weight_neg.sv"
`includee "update_weight_pos.sv"


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
    input [N-1:0] m2,
    output [N-1:0] dw
);
    reg [N-1:0] pos_change, neg_change, inverted_m1, inverted_m2;
    reg eq, gt, lt;

    negator negator1(
        m1,
        inverted_m1
    );

    negator negator2(
        m2,
        inverted_m2
    );

    fixed_point_cmp fcmp(
        t_change,
        32'b00000000000000000000000000000000, // 0
        eq,
        gt,
        lt
    );

    // a and tau values should be prefit for in the linear piecewise

    update_weight_neg update_weight1(
        t_change,
        // a_minus,
        // tau_minus,
        m1,
        m2,
        b1,
        b2,        
        neg_change
    );
    update_weight_pos update_weight2(
        t_change,
        // a_plus,
        // tau_plus,
        inverted_m1,
        inverted_m2,
        b1,
        b2,
        pos_change
    );

    always @ (posedge clk) begin
        if (lt & apply) begin
            dw <= neg_change;
        end else if (!lt & apply) begin
            dw <= pos_change
        end else
    end
endmodule