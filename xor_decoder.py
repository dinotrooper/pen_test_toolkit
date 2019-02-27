import sys
import os
from binascii import hexlify as convertToHex

def create_repeating_key(key, encrypt_len):
	key_string = ""
	repeat_key_len = int(encrypt_len/len(key))
	char_left = encrypt_len % len(key)

	for x in range(repeat_key_len):
		key_string += key

	if (char_left > 0):
		for x in range(char_left - 1):
			key_string += key[x]

	hex_string = ""
	for x in key_string:
		hex_string += hex(int(ord(x)))[2:]

	return hex_string

def create_single_char_key(key, encrypt_len):
	key_string=""
	for x in range(int(encrypt_len/2)):
		key_string+= hex(int(key))[2:] #[2:] removes the 0x at the beginning
	return key_string


def cipher_single_char_key_from_input(encrypted_string):
	path = os.path.dirname(os.path.abspath(__file__))
	with open(path + "/decoded_input.txt", 'w+') as file:
		for x in range(255):
			hex_string = xorLetters(create_single_char_key(str(x), len(encrypted_string)), encrypted_string)
			try:
				file.write(bytes.fromhex(hex_string).decode('utf-8')+"\n")
			except:
				pass

def cipher_single_char_key_from_file(filename):
	path = os.path.dirname(os.path.abspath(__file__))
	with open(path + "/decoded_file.txt", 'w+') as outFile:
		for x in range(255):
			with open(path + "/" + filename, 'r') as inFile:
				encrypted_string = inFile.readline().strip()
				while encrypted_string:
					hex_string = xorLetters(create_single_char_key(str(x), len(encrypted_string)), encrypted_string)
					try:
						cipher_string = bytes.fromhex(hex_string).decode('utf-8')
						outFile.write(hex_string + " = ")
						outFile.write(cipher_string + "\n")
					except:
						pass
					encrypted_string = inFile.readline().strip()

def cipher_repeating_key_from_input(key, encrypted_string):
	path = os.path.dirname(os.path.abspath(__file__))
	repeating_key = create_repeating_key(key, len(encrypted_string))

	xor_string = ""
	for x in range(len(encrypted_string)):
		xor_string += xorLetters(repeating_key[x], encrypted_string[x])

	try:
		cipher_string = bytes.fromhex(xor_string).decode('utf-8')
	except:
		ciphter_string = "Unable to convert to UTF-8"

	return cipher_string

def xorLetters(firstString, secondString):
	return hex(int(firstString, 16) ^ int(secondString, 16))[2:]

def main():
	if (len(sys.argv) > 3):
		if (sys.argv[3] == "-r_key"):
			print(cipher_repeating_key_from_input(sys.argv[1], sys.argv[2]))
		elif (sys.argv[2] == "-s_key"):
			if (len(sys.argv) > 3):
				if (sys.argv[3] == "-file"):
					cipher_single_char_key_from_file(sys.argv[1])
			else:
				cipher_single_char_key_from_input(sys.argv[1])
	else:
		xor_string = xorLetters(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	main()
