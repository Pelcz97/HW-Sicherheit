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
	reg[2:0] index;
	
	parameter INIT = 'b111, MULT = 'b001, FINISHCALC = 'b010, LOOP_CONDITION = 'b011, NOT_ENA = 'b100, WAIT = 'b101;
	reg[2:0] state;

	reg[7:0] xtimes1_in,xtimes1_out,xtimes2_in,xtimes2_out,xtimes3_in,xtimes3_out, xtimes4_in,xtimes4_out, a1, a2, a3, a4;
	xtime xtimes1(.byte_in(xtimes1_in),.byte_out(xtimes1_out));
	xtime xtimes2(.byte_in(xtimes2_in),.byte_out(xtimes2_out));
	xtime xtimes3(.byte_in(xtimes3_in),.byte_out(xtimes3_out));
	xtime xtimes4(.byte_in(xtimes4_in),.byte_out(xtimes4_out));

	always@(posedge clk) begin
		case (state)
			NOT_ENA: begin
				done <= 'b0;
				if (ena) begin
					state <= INIT;
				end
			end
			INIT: begin
				index <= 0;
				state <= MULT;
			end
			MULT: begin
				xtimes1_in <= state_in[(7 + (32 * index)):(32 * index)];
				xtimes2_in <= state_in[(15 + (32 * index)):(8 + (32 * index))];
				xtimes3_in <= state_in[(23 + (32 * index)):(16 + (32 * index))];
				xtimes4_in <= state_in[(31  + (32 * index)):(24 + (32 * index))];

				a1 <= state_in[(7 + (32 * index)):(32 * index)];
				a2 <= state_in[(15 + (32 * index)):(8 + (32 * index))];
				a3 <= state_in[(23 + (32 * index)):(16 + (32 * index))];
				a4 <= state_in[(31  + (32 * index)):(24 + (32 * index))];
				state <= WAIT;
			end
			WAIT: begin
				state <= FINISHCALC;
			end
			FINISHCALC: begin
				state_out[(7 + (32 * index)):(32 * index)] = xtimes1_out ^ (xtimes2_out ^a2) ^ a3 ^a4; 
				state_out[(15 + (32 * index)):(8 + (32 * index))] = a1 ^ xtimes2_out ^ (xtimes3_out ^ a3) ^a4;
				state_out[(23 + (32 * index)):(16 + (32 * index))] = a1 ^ a2 ^ xtimes3_out ^ (xtimes4_out ^ a4);
				state_out[(31  + (32 * index)):(24 + (32 * index))] = (xtimes1_out ^a1) ^ a2 ^ a3 ^ xtimes4_out;

				// state_out[(7 + 32 * index):(32 * index)] = xtimes1_out ^ (xtimes2_out ^a2) ^ a3 ^a4; 
				// state_out[(15 + 32 * index):(8 + 32 * index)] = a1 ^ xtimes2_out ^ (xtimes3_out ^ a3) ^a4;
				// state_out[(23 + 32 * index):(16 + 32 * index)] = a1 ^ a2 ^ xtimes3_out ^ (xtimes4_out ^ a4);
				// state_out[(31  + 32 * index):(24 + 32 * index)] = (xtimes1_out ^a1) ^ a2 ^ a3 ^ xtimes4_out;


				state <= LOOP_CONDITION;
			end
			LOOP_CONDITION: begin
				if (index < 4) begin 
					index++;
					state <= MULT;
				end
				else begin
					done <= 'b1;
					state <= NOT_ENA;
				end
			end
			default: state <= NOT_ENA;
		endcase
	end

endmodule


