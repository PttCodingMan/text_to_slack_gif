from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from SingleLog.log import Logger

if __name__ == '__main__':
    logger = Logger('app')

    image_size = 100
    # load font
    font = ImageFont.truetype('/System/Library/Fonts/Arial Unicode.ttf', image_size, index=0)

    input_string = '臣亮言：先帝創業未半，而中道崩殂。今天下三分，益州疲弊，此誠危急存亡之秋也。'
    images = []
    for i, text in enumerate(input_string):

        logger.debug('target', text)

        # create image with white
        img = Image.new('RGB', (image_size, image_size), (255, 255, 255))
        d = ImageDraw.Draw(img)

        # draw text in image
        d.text((0, -20), text, fill=(0, 0, 0), font=font)

        # write image to file
        # for debug
        # s = io.BytesIO()
        # img.save(s, 'png')
        # in_memory_file = s.getvalue()
        #
        # with open(f'{i}.png', 'wb') as f:
        #     f.write(in_memory_file)

        images.append(img)

    # img, *imgs = [Image.open(f) for f in sorted(glob.glob('*.png'))]
    # print(imgs)
    img.save(fp='result.gif', format='GIF', append_images=images,
             save_all=True, duration=500, loop=0)

    logger.info('finish')
