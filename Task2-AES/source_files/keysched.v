/*
 * This entity computes a new AES round key using the current round (to get the round constant rcon) and 
 * the previous round key.
 * For the key schedule, operations are performed on 32bit words.
 * Details can be found in NIST.FIPS.197.
 */

module keysched(clk, rst, ena, round_in, prev_key_in, next_key_out, done);
	
	input clk;
	input rst;
	input ena;
	input [3:0] round_in;
	input [127:0] prev_key_in;
	output [127:0] next_key_out;
	output done;

	// TODO: Implement the key scheduling algorithm
	// ???
	reg[2:0] state;
	parameter NOT_ENA=3'b000, INIT=3'b001, INPUTS=3'b010, WAIT=3'b011, CALC=3'b100, DONE=3'b101;

	reg [31:0] rcon_out;
	reg [3:0] rcon_in;
	reg [7:0] sbox_in1, sbox_in2, sbox_in3, sbox_in4, sbox_out1, sbox_out2, sbox_out3, sbox_out4;

	reg [31:0] w1, w2, w3, w4, temp;

	rcon rcon_inst(.round_in(rcon_in), .rcon_out(rcon_out));

	sbox sbox_inst1(.byte_in(sbox_in1), .byte_out(sbox_out1));
	sbox sbox_inst2(.byte_in(sbox_in2), .byte_out(sbox_out2));
	sbox sbox_inst3(.byte_in(sbox_in3), .byte_out(sbox_out3));
	sbox sbox_inst4(.byte_in(sbox_in4), .byte_out(sbox_out4));


	always@(posedge clk) begin
		case (state)
		NOT_ENA: begin
			w1 <= 0;
			w2 <= 0;
			w3 <= 0;
			w4 <= 0;
			temp <= 0;
			done <= 0;
			next_key_out <= 0;
			if (ena) begin
				state <= INIT;
			end
		end
		INIT: begin
			w4 <= prev_key_in[127:96];
			w3 <= prev_key_in[95:64];
			w2 <= prev_key_in[63:32];
			w1 <= prev_key_in[31:0];
			state <= INPUTS;
		end
		INPUTS: begin
			sbox_in1 <= w4[23:16];
			sbox_in2 <= w4[15:8];
			sbox_in3 <= w4[7:0];
			sbox_in4 <= w4[31:24];

			rcon_in <= round_in;

			state <= WAIT;

		end
		WAIT: begin
			temp[15:8] <= sbox_out1;
			temp[7:0] <= sbox_out2;
			temp[31:24] <= sbox_out3;
			temp[23:16] <= sbox_out4;
			state <= CALC;
		end
		CALC: begin
			next_key_out[31:0] <= w1 ^ temp ^ rcon_out;
			next_key_out[63:32] <= w1 ^ w2 ^ temp ^ rcon_out;
			next_key_out[95:64] <= w1 ^ w2 ^ w3 ^ temp ^ rcon_out;
			next_key_out[127:96] <= w1 ^ w2 ^ w3 ^ w4 ^ temp ^ rcon_out;

			state <= DONE;
		end
		DONE: begin
			done <= 'b1;
			state <= NOT_ENA;
		end
		default : state <= NOT_ENA;
		endcase
	end


endmodule

