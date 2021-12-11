import string
from argparse import ArgumentParser, ArgumentTypeError

from PIL import ImageFont, Image, ImageDraw
from SingleLog.log import Logger

# default value
frame = 4
delay = 100


def check_positive(value):
    value = int(value)
    if value <= 0:
        raise ArgumentTypeError("%s is an invalid positive int value" % value)
    return value


if __name__ == '__main__':
    logger = Logger('app')

    parser = ArgumentParser()
    parser.add_argument('-t', '--text', help="Any text you want to convert to gif", required=True)
    parser.add_argument('-f', '--frame', type=check_positive, default=5,
                        help="Frames number for each text between text")
    parser.add_argument('-d', '--delay', type=check_positive, default=100, help="The delay for each frame")
    args = parser.parse_args()

    input_string = ''.join(args.text.split())
    frame = args.frame
    delay = args.delay

    logger.debug('text', input_string)
    logger.debug('frame', frame)
    logger.debug('delay', delay)

    image_size = 100
    single_full_text_length = image_size
    # load font
    font = ImageFont.truetype('/System/Library/Fonts/Arial Unicode.ttf', image_size, index=0)

    img = Image.new('RGB', (image_size, image_size), (255, 255, 255))
    d = ImageDraw.Draw(img)
    text_total_width, _ = d.textsize(input_string, font=font)

    logger.debug('text_total_width', text_total_width)

    frame_offset = single_full_text_length // frame

    logger.debug('frame_offset', frame_offset)

    x = (frame - 1) * frame_offset
    images = []
    while abs(x) < text_total_width:

        img = Image.new('RGB', (image_size, image_size), (255, 255, 255))
        d = ImageDraw.Draw(img)

        d.text((x, -20), input_string, fill='black', font=font)

        # write image to file for debug
        if logger.level == Logger.TRACE:
            import io

            s = io.BytesIO()
            img.save(s, 'png')
            in_memory_file = s.getvalue()

            with open(f'{x}.png', 'wb') as f:
                f.write(in_memory_file)

        images.append(img)
        x -= frame_offset

    if frame > 1:
        images.pop()

    output_name = f'{input_string[:3]} in f {frame} d {delay}.gif'

    images[0].save(
        fp=output_name, format='GIF', append_images=images[1:], save_all=True,
        duration=delay,
        loop=0)

    logger.info(output_name, 'generated')

