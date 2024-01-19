

//SD_AXB_DEFINE_begin
//MSTN = 4
//SLVN = 8
//xprefix = a
//mst_attr = rw, rw, rw, rw
//mst_num = 0, 1, 3, 
//mst0_to_slv = 0, 4, 5, 7
//SD_AXB_DEFINE_end


module AXB_R52 (

//SD_AXB_PORT_GEN_begin
input   [4:0]               m_a_0_Aw_apple              ,
input                       m_a_0_Ar_banana             ,
input   [3:0]               m_a_0_Aw_Id                 ,
input   [4:0]               m_a_0_Aw_IdCode             ,
output  [7:0]               m_a_0_R_cherry              ,
input   [5:0]               m_a_0_B_date                ,
output  [6:0]               m_a_0_W_elderberry          ,
input   [4:0]               m_a_1_Aw_apple              ,
input                       m_a_1_Ar_banana             ,
input   [3:0]               m_a_1_Aw_Id                 ,
input   [4:0]               m_a_1_Aw_IdCode             ,
output  [7:0]               m_a_1_R_cherry              ,
input   [5:0]               m_a_1_B_date                ,
output  [6:0]               m_a_1_W_elderberry          ,
input   [4:0]               m_a_2_Aw_apple              ,
input                       m_a_2_Ar_banana             ,
input   [3:0]               m_a_2_Aw_Id                 ,
input   [4:0]               m_a_2_Aw_IdCode             ,
output  [7:0]               m_a_2_R_cherry              ,
input   [5:0]               m_a_2_B_date                ,
output  [6:0]               m_a_2_W_elderberry          ,
input   [4:0]               m_a_3_Aw_apple              ,
input                       m_a_3_Ar_banana             ,
input   [3:0]               m_a_3_Aw_Id                 ,
input   [4:0]               m_a_3_Aw_IdCode             ,
output  [7:0]               m_a_3_R_cherry              ,
input   [5:0]               m_a_3_B_date                ,
output  [6:0]               m_a_3_W_elderberry          ,
output  [4:0]               s_a_0_Aw_apple              ,
output                      s_a_0_Ar_banana             ,
output  [6:0]               s_a_0_Aw_Id                 ,
output  [4:0]               s_a_0_Aw_IdCode             ,
input   [7:0]               s_a_0_R_cherry              ,
output  [5:0]               s_a_0_B_date                ,
input   [6:0]               s_a_0_W_elderberry          ,
output  [4:0]               s_a_1_Aw_apple              ,
output                      s_a_1_Ar_banana             ,
output  [6:0]               s_a_1_Aw_Id                 ,
output  [4:0]               s_a_1_Aw_IdCode             ,
input   [7:0]               s_a_1_R_cherry              ,
output  [5:0]               s_a_1_B_date                ,
input   [6:0]               s_a_1_W_elderberry          ,
output  [4:0]               s_a_2_Aw_apple              ,
output                      s_a_2_Ar_banana             ,
output  [6:0]               s_a_2_Aw_Id                 ,
output  [4:0]               s_a_2_Aw_IdCode             ,
input   [7:0]               s_a_2_R_cherry              ,
output  [5:0]               s_a_2_B_date                ,
input   [6:0]               s_a_2_W_elderberry          ,
output  [4:0]               s_a_3_Aw_apple              ,
output                      s_a_3_Ar_banana             ,
output  [6:0]               s_a_3_Aw_Id                 ,
output  [4:0]               s_a_3_Aw_IdCode             ,
input   [7:0]               s_a_3_R_cherry              ,
output  [5:0]               s_a_3_B_date                ,
input   [6:0]               s_a_3_W_elderberry          ,
output  [4:0]               s_a_4_Aw_apple              ,
output                      s_a_4_Ar_banana             ,
output  [6:0]               s_a_4_Aw_Id                 ,
output  [4:0]               s_a_4_Aw_IdCode             ,
input   [7:0]               s_a_4_R_cherry              ,
output  [5:0]               s_a_4_B_date                ,
input   [6:0]               s_a_4_W_elderberry          ,
output  [4:0]               s_a_5_Aw_apple              ,
output                      s_a_5_Ar_banana             ,
output  [6:0]               s_a_5_Aw_Id                 ,
output  [4:0]               s_a_5_Aw_IdCode             ,
input   [7:0]               s_a_5_R_cherry              ,
output  [5:0]               s_a_5_B_date                ,
input   [6:0]               s_a_5_W_elderberry          ,
output  [4:0]               s_a_6_Aw_apple              ,
output                      s_a_6_Ar_banana             ,
output  [6:0]               s_a_6_Aw_Id                 ,
output  [4:0]               s_a_6_Aw_IdCode             ,
input   [7:0]               s_a_6_R_cherry              ,
output  [5:0]               s_a_6_B_date                ,
input   [6:0]               s_a_6_W_elderberry          ,
output  [4:0]               s_a_7_Aw_apple              ,
output                      s_a_7_Ar_banana             ,
output  [6:0]               s_a_7_Aw_Id                 ,
output  [4:0]               s_a_7_Aw_IdCode             ,
input   [7:0]               s_a_7_R_cherry              ,
output  [5:0]               s_a_7_B_date                ,
input   [6:0]               s_a_7_W_elderberry          ,
//SD_AXB_PORT_GEN_end

input                       clk                         ,
input                       rst_n                       ,
input                       tm                           

);

//SD_AXB_CONNECT_begin
//SD_AXB_CONNECT_end

//SD_AXB_STUB_GEN_begin
assign m_a_0_R_cherry = 8'hAC;
assign m_a_0_W_elderberry = {7{1'b0}};
assign m_a_1_R_cherry = 8'hAC;
assign m_a_1_W_elderberry = {7{1'b0}};
assign m_a_2_R_cherry = 8'hAC;
assign m_a_2_W_elderberry = {7{1'b0}};
assign m_a_3_R_cherry = 8'hAC;
assign m_a_3_W_elderberry = {7{1'b0}};
assign s_a_0_Aw_apple = {5{1'b0}};
assign s_a_0_Ar_banana = 1'b0;
assign s_a_0_Aw_Id = {7{1'b0}};
assign s_a_0_Aw_IdCode = {5{1'b0}};
assign s_a_0_B_date = {6{1'b0}};
assign s_a_1_Aw_apple = {5{1'b0}};
assign s_a_1_Ar_banana = 1'b0;
assign s_a_1_Aw_Id = {7{1'b0}};
assign s_a_1_Aw_IdCode = {5{1'b0}};
assign s_a_1_B_date = {6{1'b0}};
assign s_a_2_Aw_apple = {5{1'b0}};
assign s_a_2_Ar_banana = 1'b0;
assign s_a_2_Aw_Id = {7{1'b0}};
assign s_a_2_Aw_IdCode = {5{1'b0}};
assign s_a_2_B_date = {6{1'b0}};
assign s_a_3_Aw_apple = {5{1'b0}};
assign s_a_3_Ar_banana = 1'b0;
assign s_a_3_Aw_Id = {7{1'b0}};
assign s_a_3_Aw_IdCode = {5{1'b0}};
assign s_a_3_B_date = {6{1'b0}};
assign s_a_4_Aw_apple = {5{1'b0}};
assign s_a_4_Ar_banana = 1'b0;
assign s_a_4_Aw_Id = {7{1'b0}};
assign s_a_4_Aw_IdCode = {5{1'b0}};
assign s_a_4_B_date = {6{1'b0}};
assign s_a_5_Aw_apple = {5{1'b0}};
assign s_a_5_Ar_banana = 1'b0;
assign s_a_5_Aw_Id = {7{1'b0}};
assign s_a_5_Aw_IdCode = {5{1'b0}};
assign s_a_5_B_date = {6{1'b0}};
assign s_a_6_Aw_apple = {5{1'b0}};
assign s_a_6_Ar_banana = 1'b0;
assign s_a_6_Aw_Id = {7{1'b0}};
assign s_a_6_Aw_IdCode = {5{1'b0}};
assign s_a_6_B_date = {6{1'b0}};
assign s_a_7_Aw_apple = {5{1'b0}};
assign s_a_7_Ar_banana = 1'b0;
assign s_a_7_Aw_Id = {7{1'b0}};
assign s_a_7_Aw_IdCode = {5{1'b0}};
assign s_a_7_B_date = {6{1'b0}};
//SD_AXB_STUB_GEN_end


endmodule

