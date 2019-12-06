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

	parameter NOT_ENA=3'b000, INIT=3'b001, SMALLER_NK=3'b010, LARGER_NK=3'b011, DECISION=3'b100, DONE=3'b101;

	reg [31:0] count;
	reg [31:0] rcon_in;
	reg [3:0] rcon_out;
	reg [7:0] sbox_in;
	reg [7:0] sbox_out;

	reg [127:0] tmp_key_out;
	reg [31:0] tmp_word;
	reg [15:0] cnter;

	rcon rcon_inst(.byte_in(rcon_in), .byte_out(rcon_out));
	sbox sbox_inst(.byte_in(sbox_in), .byte_out(sbox_out));

	always@(posedge clk) begin
		case (state)
			NOT_ENA: begin
				done <= 'b0;
				if (ena) begin
					state <= INIT;
				end
			end
			INIT: begin
				next_key_out <= 128'b0;
				tmp_key_out <= 128'b0;
				cnter <= 'b0;

				state <= SMALLER_NK;
			end
			SMALLER_NK: begin

				tmp_key_out[((cnter*32)+31):cnter*32] <= {{{prev_key_in[((cnter+3)*8)+7:(cnter+3)*8] , prev_key_in[((cnter+2)*8)+7:(cnter+2)*8] } , prev_key_in[((cnter+1)*8)+7:(cnter+1)*8] } , prev_key_in[(cnter*8)+7:cnter*8]}
				word(key[4*i], key[4*i+1], key[4*i+2], key[4*i+3])
				cnter <= cnter + 1;
				state <= DECISION;
			end
			LARGER_NK: begin

				tmp_word = tmp_key_out[cnter-1];

				if (cnter % NK == 0) begin

				tmp_word = { tmp_word[7:0] , tmp_word[31:8]}
				sbox_in <= tmp_word

				//temp = SubWord(RotWord(temp)) xor Rcon[i/Nk
				end else if (Nk > 6 and cnter % Nk == 4) begin
				sbox_in <= tmp_word;

				//temp = SubWord(temp)
				end
				w[cnter] = w[cnter-Nk] ^ tmp_word
				cnter <= cnter + 1

				state <= LARGER_NK;
			end
			DECISION: begin
			
				if (cnter < Nk) begin
				state <= SMALLER_NK;
				end else begin
				state <= LARGER_NK;
				end
			end
			DONE: begin
				done <= 'b1;
				state <= NOT_ENA;
			end
			default: state <= NOT_ENA;
		endcase
	end


endmodule


