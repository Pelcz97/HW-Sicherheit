/*
 * This component implements the AES MixColumns operation by applying the mixcolumn component on each 32bit column of the state matrix
 * Be careful how rows and columns are stored in the state!
 */

module mixcolumns(clk, rst, ena, state_in, state_out, done);
	
	input clk;
	input rst;
	input ena;
	input [127:0] state_in;
	output [127:0] state_out;
	output done;
	
	// TODO: Implement the MixColumns AES operation
	// ???
	reg[1:0] columnCount;
	reg[1:0] byteCount;

	reg[2:0] state;
	parameter NOT_ENA = 'b000, INIT = 'b001, NEXT_BYTE = 'b010, NEXT_COLUMN = 'b011, LOOP_BYTE = 'b100, LOOP_COLUMN = 'b101, DONE = 'b110;
	reg[31:0] workingColumn;
	reg[31:0] ColResult;

	reg[7:0] xtimes1_in,xtimes1_out,xtimes2_in,xtimes2_out,xtimes3_out;

	xtime xtimes1(.byte_in(xtimes1_in),.byte_out(xtimes1_out));
	xtime xtimes2(.byte_in(xtimes2_in),.byte_out(xtimes2_out));
	xtime xtimes3(.byte_in(xtimes2_out),.byte_out(xtimes3_out));


	
	

	always@(posedge clc) begin
		case (state)
			NOT_ENA: begin
				if (ena) begin
					state <= INIT;
				end
			end
			INIT: begin
				state_out <= 'b0;
				columnCount <= 'b0;
				byteCount <= 'b0;
				done <= 'b0;
				workingColumn <= state_in[0:31];
				state <= NEXT_BYTE;
			end
			NEXT_BYTE: begin
				case (byteCount) 
					'b00: begin
						byteCount <= 'b01;
						xtimes1_in <= workingColumn[7:0];
						xtimes2_in <= workingColumn[15:8];
						ColResult[7:0] <= xtimes1_out ^ xtimes3_out ^ workingColumn[23:16]^ workingColumn[31:24];
					end
					'b01: begin
						byteCount <= 'b10;
						xtimes1_in <= workingColumn[15:8];
						xtimes2_in <= workingColumn[23:16];
						ColResult[15:8] <= workingColumn[7:0] ^ xtimes1_out ^ xtimes3_out ^ workingColumn[31:24];
					end
					'b10: begin
						byteCount <= 'b11;
						xtimes1_in <= workingColumn[23:16];
						xtimes2_in <= workingColumn[31:24];
						ColResult[23:16] <= workingColumn[7:0] ^ workingColumn[15:8] ^ xtimes1_out ^ xtimes3_out;
					end
					'b11:begin
						byteCount <='b00;
						xtimes1_in <= workingColumn[31:24];
						xtimes2_in <= workingColumn[7:0];
						ColResult[31:24] <= xtimes3_out ^ workingColumn[15:8] ^ workingColumn[23:16] ^ xtimes1_out;
						state <= NEXT_COLUMN;
					end
				endcase
			end
			NEXT_COLUMN: begin
				case (columnCount) 
					'b00: begin
						byteCount <= 'b01;
						state_out[31:0] <= ColResult;
						workingColumn <= state_in[63:32];
						state <= NEXT_BYTE;
					end
					'b01: begin
						byteCount <= 'b10;
						state_out[63:32] <= ColResult;
						workingColumn <= state_in[95:64];
						state <= NEXT_BYTE;
					end
					'b10: begin
						byteCount <= 'b11;
						state_out[95:64] <= ColResult;
						workingColumn <= state_in[127:96];
						state <= NEXT_BYTE;
					end
					'b11:begin
						byteCount <='b00;
						state_out[127:96] <= ColResult;
						state <= DONE;
					end
				endcase
			end
			DONE: begin
				done <= 'b1;
				state <= NOT_ENA;
			end
		endcase
	end

endmodule


