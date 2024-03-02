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
    input [N-1:0] a_plus,
    input [N-1:0] a_minus,
    input [N-1:0] tau_plus,
    input [N-1:0] tau_minus,
    output [N-1:0] dw
);
    reg [N-1:0] pos_change, neg_change;
    reg eq, gt, lt;

    fixed_point_cmp fcmp(
        t_change,
        32'b00000000000000000000000000000000, // 0
        eq,
        gt,
        lt
    );

    update_weight_neg update_weight1(
        t_change,
        a_minus,
        tau_minus,
        neg_change
    );
    update_weight_pos update_weight2(
        t_change,
        a_plus,
        tau_plus,
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