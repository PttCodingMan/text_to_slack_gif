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

    if frame == 1:
        images = []
        for i, text in enumerate(input_string):

            logger.debug('text', text)
            if text in string.whitespace:
                logger.debug('pass')
                continue

            # create image with white
            img = Image.new('RGB', (image_size, image_size), (255, 255, 255))
            d = ImageDraw.Draw(img)

            if text in string.ascii_letters:
                w, h = d.textsize(text, font=font)
                start_x = int((image_size - w) / 2)
            else:
                start_x = 0

            logger.debug('start x', start_x)
            # draw text in image
            d.text((start_x, -20), text, fill='black', font=font)

            images.append(img)
    else:
        text_total_width, _ = d.textsize(input_string, font=font)
        logger.debug('text_total_width', text_total_width)

        frame_offset = single_full_text_length // frame
        logger.debug('frame_offset', frame_offset)

        x = (frame - 1) * frame_offset
        images = []
        while (text_total_width + x) >= frame_offset:

            img = Image.new('RGB', (image_size, image_size), (255, 255, 255))
            d = ImageDraw.Draw(img)

            d.text((x, -20), input_string, fill='black', font=font)

            images.append(img)
            x -= frame_offset

        for _ in range(frame - 1):
            images.append(images.pop(0))

    output_name = f'{input_string} in f {frame} d {delay}.gif'

    images[0].save(
        fp=output_name, format='GIF', append_images=images[1:], save_all=True,
        duration=delay,
        loop=0)

    logger.info(output_name, 'generated')

