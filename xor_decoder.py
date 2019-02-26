import sys
import os
def create_single_char_key(key, encrypt_len):
	key_string=""
	for x in range(int(encrypt_len/2)):
		key_string+= hex(int(key))[2:] #[2:] removes the 0x at the beginning
	return key_string


def cipher_single_char_key_from_input(encrypted_string):
	path = os.path.dirname(os.path.abspath(__file__))
	with open(path + "/decoded_input.txt", 'w+') as file:
		x = 0
		while x < 255:
			hex_string = xorWord(create_single_char_key(str(x), len(encrypted_string)), encrypted_string)
			try:
				file.write(bytes.fromhex(hex_string).decode('utf-8')+"\n")
			except:
				file.write("Invalid hex conversion\n")
			x+= 1

def cipher_single_char_key_from_file(filename):
	path = os.path.dirname(os.path.abspath(__file__))
	with open(path + "/decoded_file.txt", 'w+') as outFile:
		x = 0
		while x < 255:
			with open(path + "/" + filename, 'r') as inFile:
				encrypted_string = inFile.readline().strip()
				while encrypted_string:
					hex_string = xorWord(create_single_char_key(str(x), len(encrypted_string)), encrypted_string)
					try:
						cipher_string = bytes.fromhex(hex_string).decode('utf-8')
						outFile.write(hex_string + " = ")
						outFile.write(cipher_string + "\n")
					except:
						pass
					encrypted_string = inFile.readline().strip()
			x+=1

def xorWord(firstString, secondString):
	return hex(int(firstString, 16) ^ int(secondString, 16))[2:]

def main():
	if (sys.argv[2] == "-s_key"):
		if (len(sys.argv) > 3):
			if (sys.argv[3] == "-file"):
				cipher_single_char_key_from_file(sys.argv[1])
		else:
			cipher_single_char_key_from_input(sys.argv[1])
	else:
		print(xorWord(sys.argv[1], sys.argv[2]))


if __name__ == '__main__':
	main()
