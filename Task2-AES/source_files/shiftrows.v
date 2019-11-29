/*
 * This components implements the AES ShiftRows operation
 * It represents a cyclic byte shift of the rows of the state matrix (see NIST.FIPS.197 for details)
 * Be careful with how columns/rows are stored in the state matrix!
 */

module shiftrows(clk, rst, ena, state_in, state_out, done);
	
	input clk;
	input rst;
	input ena;
	input [127:0] state_in;
	output [127:0] state_out;
	output done;
	
	// TODO: Implement the ShiftRows AES operation
	// ???
	reg[1:0] state;
	parameter NOT_ENA = 'b00, INIT = 'b01, TRANSLATE = 'b10, DONE = 'b11;

	always@(posedge clk) begin
		case (state)
			NOT_ENA: begin
				done <= 'b0;
				if (ena) begin
					state <= INIT;
				end
			end
			INIT: begin
				state_out <= 127'b0;
				state <= TRANSLATE;
			end
			TRANSLATE: begin

			state_out[7:0] <= state_in[7:0];
			state_out[15:8] <= state_in[47:40];
			state_out[23:16] <= state_in[87:80];
			state_out[31:24] <= state_in[127:120];
			state_out[39:32] <= state_in[39:32];
			state_out[47:40] <= state_in[89:72];
			state_out[55:48] <= state_in[119:112];
			state_out[63:56] <= state_in[31:24];
			state_out[71:64] <= state_in[71:64];
			state_out[79:72] <= state_in[111:104];
			state_out[87:80] <= state_in[23:16];
			state_out[95:88] <= state_in[63:56];
			state_out[127:120] <= state_in[95:88];
			state_out[119:112] <= state_in[55:48];
			state_out[111:104] <= state_in[15:8];
			state_out[103:96] <= state_in[103:96];
		
			state <= DONE;
			end
			DONE: begin
				done <= 'b1;
				state <= NOT_ENA;
			end
		endcase
	end
	
endmodule


