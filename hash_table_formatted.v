

//SD_AXB_DEFINE_begin
//MSTN = 4
//SLVN = 8
//xprefix = a
//mst_attr = rw, rw, rw, rw
//mst_num = 0, 1, 3, 
//mst0_to_slv = 0, 4, 5, 7
//SD_AXB_DEFINE_end


module AB_R52 (

//SD_PORT_GEN_begin
input   [4:0]               m_a_0_AW_apple              ,
input                       m_a_0_AR_banana             ,
output  [7:0]               m_a_0_R_cherry              ,
input   [5:0]               m_a_0_B_date                ,
output  [6:0]               m_a_0_W_elderberry          ,
input   [4:0]               m_a_1_AW_apple              ,
input                       m_a_1_AR_banana             ,
output  [7:0]               m_a_1_R_cherry              ,
input   [5:0]               m_a_1_B_date                ,
output  [6:0]               m_a_1_W_elderberry          ,
input   [4:0]               m_a_2_AW_apple              ,
input                       m_a_2_AR_banana             ,
output  [7:0]               m_a_2_R_cherry              ,
input   [5:0]               m_a_2_B_date                ,
output  [6:0]               m_a_2_W_elderberry          ,
input   [4:0]               m_a_3_AW_apple              ,
input                       m_a_3_AR_banana             ,
output  [7:0]               m_a_3_R_cherry              ,
input   [5:0]               m_a_3_B_date                ,
output  [6:0]               m_a_3_W_elderberry          ,
output  [4:0]               s_a_0_AW_apple              ,
output                      s_a_0_AR_banana             ,
input   [7:0]               s_a_0_R_cherry              ,
output  [5:0]               s_a_0_B_date                ,
input   [6:0]               s_a_0_W_elderberry          ,
output  [4:0]               s_a_1_AW_apple              ,
output                      s_a_1_AR_banana             ,
input   [7:0]               s_a_1_R_cherry              ,
output  [5:0]               s_a_1_B_date                ,
input   [6:0]               s_a_1_W_elderberry          ,
output  [4:0]               s_a_2_AW_apple              ,
output                      s_a_2_AR_banana             ,
input   [7:0]               s_a_2_R_cherry              ,
output  [5:0]               s_a_2_B_date                ,
input   [6:0]               s_a_2_W_elderberry          ,
output  [4:0]               s_a_3_AW_apple              ,
output                      s_a_3_AR_banana             ,
input   [7:0]               s_a_3_R_cherry              ,
output  [5:0]               s_a_3_B_date                ,
input   [6:0]               s_a_3_W_elderberry          ,
output  [4:0]               s_a_4_AW_apple              ,
output                      s_a_4_AR_banana             ,
input   [7:0]               s_a_4_R_cherry              ,
output  [5:0]               s_a_4_B_date                ,
input   [6:0]               s_a_4_W_elderberry          ,
output  [4:0]               s_a_5_AW_apple              ,
output                      s_a_5_AR_banana             ,
input   [7:0]               s_a_5_R_cherry              ,
output  [5:0]               s_a_5_B_date                ,
input   [6:0]               s_a_5_W_elderberry          ,
output  [4:0]               s_a_6_AW_apple              ,
output                      s_a_6_AR_banana             ,
input   [7:0]               s_a_6_R_cherry              ,
output  [5:0]               s_a_6_B_date                ,
input   [6:0]               s_a_6_W_elderberry          ,
output  [4:0]               s_a_7_AW_apple              ,
output                      s_a_7_AR_banana             ,
input   [7:0]               s_a_7_R_cherry              ,
output  [5:0]               s_a_7_B_date                ,
input   [6:0]               s_a_7_W_elderberry          ,
//SD_PORT_GEN_end

input                       clk                         ,
input                       rst_n                       ,
input                       tm                           

);

//SD_MODULE_CONNECT_begin
//SD_MODULE_CONNECT_end

//SD_STUB_GEN_begin
assign m_a_0_R_cherry = 8'hAC;
assign m_a_0_W_elderberry = {7{1'b0}};
assign m_a_1_R_cherry = 8'hAC;
assign m_a_1_W_elderberry = {7{1'b0}};
assign m_a_2_R_cherry = 8'hAC;
assign m_a_2_W_elderberry = {7{1'b0}};
assign m_a_3_R_cherry = 8'hAC;
assign m_a_3_W_elderberry = {7{1'b0}};
assign s_a_0_AW_apple = {5{1'b0}};
assign s_a_0_AR_banana = 1'b0;
assign s_a_0_B_date = {6{1'b0}};
assign s_a_1_AW_apple = {5{1'b0}};
assign s_a_1_AR_banana = 1'b0;
assign s_a_1_B_date = {6{1'b0}};
assign s_a_2_AW_apple = {5{1'b0}};
assign s_a_2_AR_banana = 1'b0;
assign s_a_2_B_date = {6{1'b0}};
assign s_a_3_AW_apple = {5{1'b0}};
assign s_a_3_AR_banana = 1'b0;
assign s_a_3_B_date = {6{1'b0}};
assign s_a_4_AW_apple = {5{1'b0}};
assign s_a_4_AR_banana = 1'b0;
assign s_a_4_B_date = {6{1'b0}};
assign s_a_5_AW_apple = {5{1'b0}};
assign s_a_5_AR_banana = 1'b0;
assign s_a_5_B_date = {6{1'b0}};
assign s_a_6_AW_apple = {5{1'b0}};
assign s_a_6_AR_banana = 1'b0;
assign s_a_6_B_date = {6{1'b0}};
assign s_a_7_AW_apple = {5{1'b0}};
assign s_a_7_AR_banana = 1'b0;
assign s_a_7_B_date = {6{1'b0}};
//SD_STUB_GEN_end


endmodule

