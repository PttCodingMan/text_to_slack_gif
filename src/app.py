import os
import string
from argparse import ArgumentParser, ArgumentTypeError

from PIL import ImageFont, Image, ImageDraw
from SingleLog import Logger

# default value
default_frame = 5
default_delay = 100
image_size = 50
y_offset = -10
default_color = 'black'
default_width = 1
flash_modes = ['none', 'blink', 'rainbow']
rainbow_colors = ['#ff3b30', '#ff9500', '#ffcc00', '#34c759', '#00c7be', '#007aff', '#af52de']

logger = Logger('app')

_script_path = os.path.dirname(os.path.abspath(__file__))


def check_positive(value):
    value = int(value)
    if value <= 0:
        raise ArgumentTypeError("%s is an invalid positive int value" % value)
    return value


def new_image(width, background_color):
    return Image.new('RGB', (image_size * width, image_size), background_color)


def text_to_gif(text: str, frame: int, delay: int, font: str, save: bool, text_color: str, width: int,
                background_color: str, flash: str = 'none'):
    input_string = ' '.join(text.split())

    if font is None:
        font = f'{_script_path}/../font/Arial Unicode.ttf'

    logger.debug('text', input_string)
    logger.debug('frame', frame)
    logger.debug('delay', delay)
    logger.debug('flash', flash)

    single_full_text_length = image_size
    # load font
    font = ImageFont.truetype(font, image_size, index=0)

    d = ImageDraw.Draw(new_image(width, background_color))

    # each entry is (x, text) drawn on one frame
    draws = []
    if frame == 1:
        for char in input_string:
            if char in string.whitespace:
                continue

            if char in string.ascii_letters:
                w = d.textlength(char, font=font)
                start_x = int((image_size - w) / 2)
            else:
                start_x = 0

            draws.append((start_x, char))
    else:
        text_total_width = d.textlength(input_string, font=font)
        logger.debug('text_total_width', text_total_width)

        frame_offset = single_full_text_length // frame
        logger.debug('frame_offset', frame_offset)

        x = (frame - 1) * frame_offset * width
        while (text_total_width + x) >= frame_offset:
            draws.append((x, input_string))
            x -= frame_offset

        # start the loop with text already on screen instead of a blank tile
        for _ in range((frame - 1) * width):
            draws.append(draws.pop(0))

    if not draws:
        raise ValueError('text is empty')

    if flash == 'rainbow' and len(draws) < len(rainbow_colors):
        # a short animation needs enough frames to go through every color
        draws = draws * -(-len(rainbow_colors) // len(draws))
    elif flash == 'blink' and len(draws) % 2:
        # an even frame count keeps the blinking steady when the gif loops
        draws = draws * 2

    images = []
    for i, (x, t) in enumerate(draws):
        bg, fg = background_color, text_color
        if flash == 'blink' and i % 2:
            # every other frame swaps the background and text colors
            bg, fg = fg, bg
        elif flash == 'rainbow':
            bg = rainbow_colors[i % len(rainbow_colors)]

        img = new_image(width, bg)
        ImageDraw.Draw(img).text((x, y_offset), t, fill=fg, font=font)
        images.append(img)

    if save:
        # output_name = f'{input_string[:5].strip()} in f {frame} d {delay}.gif'
        output_name = "output.gif"
        images[0].save(
            fp=output_name, format='GIF', append_images=images[1:], save_all=True,
            duration=delay,
            optimize=True,
            loop=0)

        logger.info(output_name, 'generated')

    return images


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-t', '--text', help="Any text you want to convert to gif", required=True)
    parser.add_argument('-f', '--frame', type=check_positive, default=default_frame,
                        help="Frames number for each text between text")
    parser.add_argument('-d', '--delay', type=check_positive, default=default_delay, help="The delay for each frame")
    parser.add_argument('-c', '--color', type=str, default=None,
                        help="The text HTML/CSS Color Name; string, default: black")
    parser.add_argument('-w', '--width', type=check_positive, default=default_width,
                        help="The width of image; integer; default: 1")
    parser.add_argument('--theme', type=str, default='dark', choices=['dark', 'light'],
                        help="The theme of the gif; string, default: dark")
    parser.add_argument('--flash', type=str, default='none', choices=flash_modes,
                        help="Flashing background: none, blink (background and text colors swap every frame), "
                             "rainbow (background cycles through colors); default: none")
    args = parser.parse_args()

    if args.theme == 'dark':
        background_color = 'black'
        text_color = 'white'
    else:
        background_color = 'white'
        text_color = 'black'

    if args.color:
        text_color = args.color

    text_to_gif(args.text, args.frame, args.delay, None, True, text_color, args.width, background_color, args.flash)
