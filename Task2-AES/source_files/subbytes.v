/*
 * This component applies the AES sbox to each of the 16 bytes of the AES state
 * This implements the AES SubBytes operation
 */

module subbytes(clk, rst, ena, state_in, state_out, done);
	
	input clk;
	input rst;
	input ena;
	input [127:0] state_in;
	output [127:0] state_out;
	output done;

	wire [7:0] sbox_out;
	wire [7:0] sbox_in;

	sbox sbox_inst(.byte_in(sbox_in), .byte_out(sbox_out));

	parameter endCounter = 16;
	reg[3:0] index;

	parameter NOT_ENA=2'b00, INIT=2'b01, TRANSLATE=2'b10, LOOP_CONDITION=2'b11;
	reg[1:0] state;


	
	// TODO: Implement the SubBytes AES operation
	// ???
	always @(posedge clk, posedge rst) begin
		case (state) 
			NOT_ENA: begin
				done <= 'b0;
				if (ena) begin
					state <= INIT;
				end
			end
			INIT: begin
				index <= 'b0;
				done <= 'b0;
				state <= TRANSLATE;
			end
			TRANSLATE: begin
				sbox_in = state_in[index*8+8:index*8];
				state = LOOP_CONDITION;
			end
			LOOP_CONDITION: begin
				if (index < endCounter) begin
					state_out[index*8+8:index*8] = sbox_out;
					index++;
					state <= TRANSLATE;
				end
				else begin
					state <= INIT;
				end
			end
	end
	
endmodule


