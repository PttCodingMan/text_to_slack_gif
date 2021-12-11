import string
from argparse import ArgumentParser

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from SingleLog.log import Logger

input_string = None
delay = 100
frame = 4

if __name__ == '__main__':
    logger = Logger('app')

    parser = ArgumentParser()
    parser.add_argument('-t', '--text', help="any text you want to convert to gif")
    parser.add_argument('-f', '--frame', default=4, help="frames number for each text between text")
    parser.add_argument('-d', '--delay', default=100, help="delay for each frame")
    args = parser.parse_args()

    logger.info('text', args.text)
    input_string = args.text
    frame = args.frame
    delay = args.delay

    image_size = 100
    # load font
    font = ImageFont.truetype('/System/Library/Fonts/Arial Unicode.ttf', image_size, index=0)

    images = [Image.new('RGB', (image_size, image_size), (255, 255, 255))]
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

    output_img = [images[0]]
    for i, image in enumerate(images[:-1]):

        for f in range(1, frame):
            img = Image.new('RGB', (image_size, image_size), (255, 255, 255))
            w_crop_size_before = f * image_size // frame
            w_crop_size_after = image_size - w_crop_size_before
            img.paste(image.crop((w_crop_size_before, 0, image_size, image_size)), (0, 0))
            img.paste(images[i + 1].crop((0, 0, w_crop_size_before, image_size)), (w_crop_size_after, 0))
            output_img.append(img)

        output_img.append(images[i + 1])

    output_img.append(images[-1])

    output_img[0].save(fp=f'{input_string}.gif', format='GIF', append_images=output_img[1:], save_all=True,
                       duration=delay,
                       loop=0)

    logger.info(f'{input_string}.gif', 'generated')
