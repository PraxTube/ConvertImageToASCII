from math import ceil

from PIL import (
    Image,
    ImageFont,
    ImageDraw,
)

font_filename = "DejaVuSansMono.ttf"


def main():
    image = textfile_to_image('ASCII_image.txt')
    image.show()
    image.save('content.png')


def textfile_to_image(textfile_path):
    """Convert text file to a grayscale image.

    arguments:
    textfile_path - the content of this file will be converted to an image
    font_path - path to a font file (for example impact.ttf)
    """
    # parse the file into lines stripped of whitespace on the right side
    with open(textfile_path) as f:
        lines = tuple(line.rstrip() for line in f.readlines())

    # choose a font (you can see more detail in the linked library on github)
    font = None
    font_size = 12  # get better resolution with larger size

    try:
        font = ImageFont.truetype(font_filename, size=font_size)
        print(f'Using font "{font_filename}".')
    except IOError:
        raise IOError("Could not load font", font_filename)

    if font is None:
        font = ImageFont.load_default()
        print('Using default font.')

    # draw the background
    background_color = 255  # white
    image = Image.new("L", (2560, 1440), color=background_color)
    draw = ImageDraw.Draw(image)

    # draw each line of text
    font_color = 0  # black
    margin_pixels = 20
    horizontal_position = -800
    for i, line in enumerate(lines):
        vertical_position = int(round(margin_pixels + (i * font_size))) - 500
        draw.text((horizontal_position, vertical_position), line, fill=font_color, font=font)

    return image


if __name__ == '__main__':
    main()
