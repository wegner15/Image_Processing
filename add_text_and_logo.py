from PIL import Image, ImageDraw, ImageFont, ImageEnhance

# picture setup - it is set up for Twitter recommendations
WIDTH = 1024
HEIGHT = 512
# the margin are set by my preferences
MARGIN = 50
MARGIN_TOP = 50
MARGIN_BOTTOM = 150
LOGO_MARGIN = 25

# font variables
FONT_SIZES = [110, 100, 90, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20]
FONT_QUOTE = 'font-text'
FONT_QUOTED_BY = 'font-quoted-by'
FONT_SIZE = 'font-size'
FONT_QUOTED_BY_SIZE = 'font-quoted-by-size'

# Font colors
WHITE = 'rgb(255, 255, 255)'
GREY = 'rgb(200, 200, 200)'

# output text
OUTPUT_QUOTE = 'quote'
OUTPUT_QUOTED_BY = 'quoted-by'
OUTPUT_LINES = 'lines'


def text_wrap_and_font_size(output, font_style, max_width, max_height):
    for font_size in FONT_SIZES:
        output[OUTPUT_LINES] = []
        font = ImageFont.truetype(font_style[FONT_QUOTE], size=font_size, encoding="unic")
        output[OUTPUT_QUOTE] = " ".join(output[OUTPUT_QUOTE].split())
        if font.getsize(output[OUTPUT_QUOTE])[0] <= max_width:
            output[OUTPUT_LINES].append(output[OUTPUT_QUOTE])
        else:
            words = output[OUTPUT_QUOTE].split()
            line = ""
            for word in words:
                if font.getsize(line + " " + word)[0] <= max_width:
                    line += " " + word
                else:
                    output[OUTPUT_LINES].append(line)
                    line = word
            output[OUTPUT_LINES].append(line)
        line_height = font.getsize('lp')[1]

        quoted_by_font_size = font_size
        quoted_by_font = ImageFont.truetype(font_style[FONT_QUOTED_BY], size=quoted_by_font_size, encoding="unic")
        while quoted_by_font.getsize(output[OUTPUT_QUOTED_BY])[0] > max_width // 2:
            quoted_by_font_size -= 1
            quoted_by_font = ImageFont.truetype(font_style[FONT_QUOTED_BY], size=quoted_by_font_size, encoding="unic")

        if line_height * len(output[OUTPUT_LINES]) + quoted_by_font.getsize('lp')[1] < max_height:
            font_style[FONT_SIZE] = font_size
            font_style[FONT_QUOTED_BY_SIZE] = quoted_by_font_size
            return True

    # we didn't succeed find a font size that would match within the block of text
    return False


def draw_text(image, output, font_style):
    draw = ImageDraw.Draw(image)
    lines = output[OUTPUT_LINES]
    font = ImageFont.truetype(font_style[FONT_QUOTE], size=font_style[FONT_SIZE], encoding="unic")
    line_height = font.getsize('lp')[1]

    y = MARGIN_TOP
    for line in lines:
        x = (WIDTH - font.getsize(line)[0]) // 2
        draw.text((x, y), line, fill=WHITE, font=font)

        y = y + line_height

    quoted_by = output[OUTPUT_QUOTED_BY]
    quoted_by_font = ImageFont.truetype(font_style[FONT_QUOTED_BY], size=font_style[FONT_QUOTED_BY_SIZE],
                                        encoding="unic")
    # position the quoted_by in the far right, but within margin
    x = WIDTH - quoted_by_font.getsize(quoted_by)[0] - MARGIN
    draw.text((x, y), quoted_by, fill=GREY, font=quoted_by_font)
    return image


def generate_image_with_text(input_image, quote, quote_by, font_style, output_image, logo_path):
    image = Image.open(input_image).convert("RGBA")

    # darken the image to make output more visible
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(0.6)

    # resize the image to fit Twitter
    image = image.resize((WIDTH, HEIGHT))

    # set logo on image
    logo_im = Image.open(logo_path).convert("RGBA")
    logo_im = logo_im.resize((100, 100))
    l_width, l_height = logo_im.size
    image.paste(logo_im, (WIDTH - l_width - LOGO_MARGIN, HEIGHT - l_height - LOGO_MARGIN), logo_im)

    output = {OUTPUT_QUOTE: quote, OUTPUT_QUOTED_BY: quote_by}

    # we should check if it returns true, but it is ignorred here
    text_wrap_and_font_size(output, font_style, WIDTH - 2 * MARGIN, HEIGHT - MARGIN_TOP - MARGIN_BOTTOM)

    # now it is time to draw the quote on our image and save it
    image = draw_text(image, output, font_style)
    image.save(output_image, quality=10, optimize=True)


def main(directory, target_directory):

    import os

    #directory = 'processed_images'
    try:
        os.makedirs(directory, exist_ok=True)
        print("Directory '%s' created successfully" % directory)
    except OSError as error:
        print("Directory '%s' can not be created" % directory)
    for index in range(0, 2):
        # setup input and output image
        input_image = target_directory + "/image_" + str(index) + ".png"

        output_image = directory + "/processed_" + str(index) + ".png"

        # setup font type
        font_style = {FONT_QUOTE: "Roboto-Bold.ttf", FONT_QUOTED_BY: "Roboto-Bold.ttf"}

        main_text = "This is a sample main text that can be used on the image"

        subtext = "mysite.com #subtext"

        generate_image_with_text(input_image, main_text, subtext, font_style, output_image, "sample-logo.png")


if __name__ == "__main__":
    main()
