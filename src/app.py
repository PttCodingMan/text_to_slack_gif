import string
from argparse import ArgumentParser

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from SingleLog.log import Logger

input_string = None
delay = 500

if __name__ == '__main__':
    logger = Logger('app')

    parser = ArgumentParser()
    parser.add_argument('-t', '--text', help="any text you want to convert to gif")
    args = parser.parse_args()

    logger.info('text', args.text)
    input_string = args.text

    image_size = 100
    # load font
    font = ImageFont.truetype('/System/Library/Fonts/Arial Unicode.ttf', image_size, index=0)

    images = []
    for i, text in enumerate(input_string):

        logger.debug('text', text)
        text = text.strip()
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

        # write image to file for debug
        # s = io.BytesIO()
        # img.save(s, 'png')
        # in_memory_file = s.getvalue()
        #
        # with open(f'{i}.png', 'wb') as f:
        #     f.write(in_memory_file)

        images.append(img)

    images.append(Image.new('RGB', (image_size, image_size), (255, 255, 255)))
    images[0].save(fp=f'{input_string}.gif', format='GIF', append_images=images[1:], save_all=True, duration=delay,
                   loop=0)

    logger.info(f'{input_string}.gif', 'generated')
