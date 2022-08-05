import time
import numpy as np
import argparse

from tqdm import tqdm
from PIL import Image

import DecodeASCIIFile


class ASCIIConvert:
    """Convert an Image into ASCII characters and save it in a txt file.

    Use a custom codec which uses only 3 Bits for a single character.
    Current implementation is using block-code, however it could be
    further optimized with prefix-code using Huffman-algorithm.
    """
    def __init__(self):
        self.grayscale = "@#+-."

    def get_average(self, image):
        """Calculate grayscale average of given tile."""
        im = np.array(image)

        # get shape
        w, h = im.shape

        # get average
        return int(np.average(im.reshape(w * h)))

    def convert_image(self, file_name, cols, scale, encoder):
        """Calculate characters based on image and append to encoder."""
        image = Image.open(file_name).convert("L")

        width, height = image.size[0], image.size[1]
        print("input image dims: {} x {}".format(width, height))

        w = width / cols
        h = w / scale

        rows = int(height / h)

        print("cols: {}, rows: {}".format(cols, rows))
        print("tile dims: {} x {}".format(w, h))

        if cols > width or rows > height:
            raise ValueError("Image too small for specified cols!")

        for j in tqdm(range(rows), desc="Progress..."):
            y1 = int(j * h)
            y2 = int((j + 1) * h) if j != rows - 1 else height

            for i in range(cols):
                x1 = int(i * w)
                x2 = int((i + 1) * w) if i != cols - 1 else width

                img = image.crop((x1, y1, x2, y2))

                # get average luminance
                avg = self.get_average(img)

                char = self.grayscale[
                    int((avg * (len(self.grayscale) - 1)) / 255)]
                encoder.append_char(char)
            encoder.append_char("l")
        encoder.append_char("e")


class AscEncoder:
    """Encode ASCII text file into custom binary file.

    As of now, use block-code with 3 bits for each character.
    Potential of optimizing used disk-space by replace block-code
    with prefix-code using Huffman-algorithm."""
    def __init__(self, file):
        self.current_byte = ""
        self.bytes = bytearray()
        self.out_file = file

    def encode_char(self, char):
        """Encode given character using block-code."""
        if char == "@":
            return "000"
        elif char == "#":
            return "001"
        elif char == "+":
            return "010"
        elif char == "-":
            return "011"
        elif char == ".":
            return "100"
        elif char == "l":
            return "101"
        elif char == "e":
            return "111"
        elif char == "0":
            return "0"
        raise ValueError("Character does not exist in map", char)

    def append_char(self, char):
        """Append given character in encoded format."""
        if len(self.current_byte) == 24:
            self.bytes += int(self.current_byte[::-1], 2).to_bytes(3, 'little')
            self.current_byte = ""
        self.current_byte += self.encode_char(char)

    def write_bytes(self):
        """Write encoded text file in binary file."""
        for i in range(24):
            self.append_char("0")

        with open(self.out_file, "wb") as file:
            file.write(self.bytes)


def get_inputs():
    """Return file and image information."""
    desc_str = "This program converts an image into ASCII art."
    parser = argparse.ArgumentParser(description=desc_str)
    parser.add_argument('--file', dest='file', required=True)
    parser.add_argument('--cols', dest='cols', required=True)
    parser.add_argument('--scale', dest='scale', required=False)

    args = parser.parse_args()

    file = args.file
    cols = int(args.cols)
    out_file = 'encoded_image.asc'

    # set scale default as 0.43 which suits a Courier font
    scale = float(args.scale) if args.scale else 0.43

    return file, cols, out_file, scale


def main():
    img_file, cols, out_file, scale = get_inputs()

    converter = ASCIIConvert()
    encoder = AscEncoder(out_file)

    converter.convert_image(img_file, cols, scale, encoder)
    encoder.write_bytes()


if __name__ == '__main__':
    start = time.time()
    main()
    print("\nTerminated after: {}ms".format(int((time.time() - start) * 1000)))
    DecodeASCIIFile.main()
