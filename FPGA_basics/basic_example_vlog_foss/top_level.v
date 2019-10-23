module top_level (
   input  CLK,
   input  RST,
   input  [3:0] BUTTON,
   output [7:0] LED,
   input  UART_RX,
   output UART_TX
);

   wire [7:0] DATA_TO_TX;
   wire [7:0] DATA_FROM_RX;
   wire TX_ENABLE, TX_IDLE, RX_READY;
   wire DATA_VALID;
   wire UART_RX_S, UART_TX_S;

   reg [127:0] KEY;
   reg [7:0] LED_STATE;
   reg ERR;

   uart uart_inst (
      .clkin ( CLK ),
      .rstin ( RST ),
      .txdatain ( DATA_TO_TX ),
      .txrdyin ( TX_ENABLE ),
      .rxpin ( UART_RX_S ),
      .rxdataout ( DATA_FROM_RX ),
      .rxrdyout ( RX_READY ),
      .txrdyout ( DATA_VALID ),
      .txpin ( UART_TX_S ),
      .errout ( ERR )
   );
   defparam uart_inst.CLKS_PER_BIT = 104;

   assign UART_TX = UART_TX_S;
   assign UART_RX_S = UART_RX;
   assign KEY = 'h2b7e151628aed2a6abf7158809cf4f3c;
   assign LED = LED_STATE;

   always @(posedge CLK) begin
     TX_ENABLE <= 0;
     if (RX_READY == 1) begin
        // receive ascii 'S' or 's' and reply with 'h80 on UART
        // also sets the LED to the bits of the respective ASCII 's' or 'S'
        // try to experiment with it to get different results
        if (DATA_FROM_RX == 'h53 | DATA_FROM_RX == 'h73) begin
           LED_STATE <= DATA_FROM_RX;
           TX_ENABLE <= 1;
           DATA_TO_TX <= 'h80;
        end else begin
           LED_STATE <= 'h00;
           TX_ENABLE <= 0;
        end
     end
   end

endmodule
