import math
import os
import re
import string
from argparse import ArgumentParser, ArgumentTypeError

from PIL import ImageColor, ImageFont, Image, ImageDraw
from SingleLog import Logger

# default value
default_frame = 5
default_delay = 100
image_size = 50
y_offset = -10
default_color = 'black'
default_width = 1
default_flash_delay = 50
flash_modes = ['none', 'blink', 'rainbow']
rainbow_colors = ['#ff3b30', '#ff9500', '#ffcc00', '#34c759', '#00c7be', '#007aff', '#af52de']

logger = Logger('app')

_script_path = os.path.dirname(os.path.abspath(__file__))


def check_positive(value):
    value = int(value)
    if value <= 0:
        raise ArgumentTypeError("%s is an invalid positive int value" % value)
    return value


def check_frame(value):
    value = check_positive(value)
    if value > image_size:
        # the scroll step is image_size // frame pixels, which would be 0 and never finish
        raise ArgumentTypeError("%s is too large; frame must be between 1 and %d" % (value, image_size))
    return value


def check_color(value):
    value = value.strip()
    try:
        ImageColor.getrgb(value)
    except ValueError:
        raise ArgumentTypeError("%r is not a color; use a name like red or a hex code like #ff8800" % value)
    return value


def check_color_list(value):
    # split on commas outside parentheses, so rgb(255, 0, 0) stays one color
    colors = [c for c in re.split(r',(?![^()]*\))', value) if c.strip()]
    if len(colors) < 2:
        raise ArgumentTypeError("need at least 2 comma-separated colors, got %r" % value)
    return [check_color(c) for c in colors]


def new_image(width, background_color):
    return Image.new('RGB', (image_size * width, image_size), background_color)


def split_delay(delay, flash_delay):
    """Split one frame's delay into flash steps, in whole centiseconds (the GIF time unit)."""
    cs = max(1, round(delay / 10))
    # browsers slow down frames shorter than 20 ms, so keep each step at least that long
    n = max(1, min(round(delay / flash_delay), cs // 2))
    return [(cs // n + (1 if k < cs % n else 0)) * 10 for k in range(n)]


def text_to_gif(text: str, frame: int, delay: int, font: str, save: bool, text_color: str, width: int,
                background_color: str, flash: str = 'none', flash_delay: int = default_flash_delay,
                flash_colors=None):
    if not 1 <= frame <= image_size:
        raise ValueError(f'frame must be between 1 and {image_size}, got {frame}')

    input_string = ' '.join(text.split())

    if font is None:
        font = f'{_script_path}/../font/Arial Unicode.ttf'

    logger.debug('text', input_string)
    logger.debug('frame', frame)
    logger.debug('delay', delay)
    logger.debug('flash', flash)

    # backgrounds the rainbow mode cycles through
    cycle_colors = list(flash_colors or rainbow_colors)

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

    if flash == 'none':
        steps = [(x, t, delay) for x, t in draws]
    else:
        # the background flashes every flash_delay ms, independent of how long the text stays put
        sub_delays = split_delay(delay, flash_delay)
        steps = [(x, t, d) for x, t in draws for d in sub_delays]

        if flash == 'rainbow' and len(steps) < len(cycle_colors):
            # a short animation repeats until it goes through every color and loops back cleanly
            steps = steps * (math.lcm(len(steps), len(cycle_colors)) // len(steps))
        elif flash == 'blink' and len(steps) % 2:
            # an even frame count keeps the blinking steady when the gif loops
            steps = steps * 2

    images = []
    for i, (x, t, _) in enumerate(steps):
        bg, fg = background_color, text_color
        if flash == 'blink' and i % 2:
            # every other frame swaps the background and text colors
            bg, fg = fg, bg
        elif flash == 'rainbow':
            bg = cycle_colors[i % len(cycle_colors)]

        img = new_image(width, bg)
        ImageDraw.Draw(img).text((x, y_offset), t, fill=fg, font=font)
        images.append(img)

    if save:
        # output_name = f'{input_string[:5].strip()} in f {frame} d {delay}.gif'
        output_name = "output.gif"
        images[0].save(
            fp=output_name, format='GIF', append_images=images[1:], save_all=True,
            duration=delay if flash == 'none' else [d for _, _, d in steps],
            optimize=True,
            loop=0)

        logger.info(output_name, 'generated')

    return images


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-t', '--text', help="Any text you want to convert to gif", required=True)
    parser.add_argument('-f', '--frame', type=check_frame, default=default_frame,
                        help="Frames number for each text between text; 1 to %d" % image_size)
    parser.add_argument('-d', '--delay', type=check_positive, default=default_delay, help="The delay for each frame")
    parser.add_argument('-c', '--color', type=check_color, default=None,
                        help="Text color, an HTML/CSS color name or hex code; overrides the theme")
    parser.add_argument('-b', '--background', type=check_color, default=None,
                        help="Background color, an HTML/CSS color name or hex code; overrides the theme")
    parser.add_argument('-w', '--width', type=check_positive, default=default_width,
                        help="The width of image; integer; default: 1")
    parser.add_argument('--theme', type=str, default='dark', choices=['dark', 'light'],
                        help="The theme of the gif; string, default: dark")
    parser.add_argument('--flash', type=str, default='none', choices=flash_modes,
                        help="Flashing background: none, blink (background and text colors swap every frame), "
                             "rainbow (background cycles through colors); default: none")
    parser.add_argument('--flash-delay', type=check_positive, default=default_flash_delay,
                        help="Milliseconds between background color changes when flashing; "
                             "smaller is faster; default: 50")
    parser.add_argument('--flash-colors', type=check_color_list, default=None,
                        help="Comma-separated backgrounds for --flash rainbow to cycle through, "
                             "e.g. 'red,gold'; default: the 7 rainbow colors")
    args = parser.parse_args()

    if args.flash_colors and args.flash != 'rainbow':
        parser.error('--flash-colors only works with --flash rainbow')

    if args.theme == 'dark':
        background_color = 'black'
        text_color = 'white'
    else:
        background_color = 'white'
        text_color = 'black'

    if args.color:
        text_color = args.color
    if args.background:
        background_color = args.background

    text_to_gif(args.text, args.frame, args.delay, None, True, text_color, args.width, background_color, args.flash,
                args.flash_delay, args.flash_colors)
