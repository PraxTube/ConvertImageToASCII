class AscDecoder:
    def __init__(self, input_file, output_file):
        self.output_file = output_file
        self.bytes = ""
        self.read_bytes(input_file)

    def decode_num(self, char):
        if char == "000":
            return "@"
        elif char == "001":
            return "#"
        elif char == "010":
            return "+"
        elif char == "011":
            return "-"
        elif char == "100":
            return "."
        elif char == "101":
            return "l"
        elif char == "111":
            return "e"
        raise ValueError("Character does not exist in map", char)

    def decode_bytes(self):
        output = ""

        for i in range(0, len(self.bytes), 3):
            char = self.decode_num(
                self.bytes[i] + self.bytes[i+1] + self.bytes[i+2]
            )

            if char == "e":
                break
            elif char == "l":
                output += "\n"
            else:
                output += char

        self.write_chars(output)

    def read_bytes(self, input_file):
        with open(input_file, "rb") as file:
            self.bytes = format(int.from_bytes(file.read(), 'little'), '023b')[::-1]

    def write_chars(self, output):
        with open(self.output_file, "w") as file:
            file.write(output)


def main():
    decoder = AscDecoder("encoded_image.asc", "ASCII_image.txt")
    decoder.decode_bytes()


if __name__ == "__main__":
    main()
    print("Decoding finished.")
