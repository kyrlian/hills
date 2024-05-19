# kyrlian 20240518

import streamlit
import random
from PIL import Image, ImageColor, ImageDraw
import time

streamlit.title("Hills")

# streamlit side pane
with streamlit.sidebar:
    streamlit.write("Image size")
    img_w = streamlit.slider("Image width", 1, 1800, 800)
    img_h = streamlit.slider("Image height", 1, 1200, 600)
    nb_hills = streamlit.slider("Number of hills", 1, 10, 5)
    hill_height = img_h / nb_hills
    color_sky = streamlit.color_picker("Sky color", "#10EEEE")
    color_back = streamlit.color_picker("Back color", "#FFCCCC")
    color_front = streamlit.color_picker("Front color", "#FF0000")
    seed = streamlit.text_input("seed", "42")
    manual_shift = streamlit.slider("Manual shift", 1, 10, 5)

def bind(x, min, max):
    if x < min:
        return min
    elif x > max:
        return max
    return x

def init_hill_summits(hill_index):
    nb_summits = 5
    summit_width = img_w / nb_summits
    hill_summits = []
    x = 0
    while x < img_w:
        y = (hill_index + random.random()) * hill_height
        hill_summits.append((x, y))
        x += random.random() * summit_width
    return hill_summits

def shift_hill_summits(hill_summits, shift):
    shifted_summits=[]
    for summit in hill_summits:
        (x,y) = summit
        shifted_summits.append((x+shift,y))
    return shifted_summits

def close_hill_polygon(hill_summits):
    poly= [(0, img_h),(0, hill_summits[0][1])]
    for s in hill_summits:
        poly.append(s)
    poly.append((img_w, hill_summits[-1][1]))
    poly.append((img_w, img_h))
    return poly


@streamlit.cache_data
def init_hills():
    hills = []
    for hill_index in range(nb_hills):
        hills.append(init_hill_summits(hill_index))
    return hills


def hill_color(hill_index):
    (color_front_r, color_front_g, color_front_b)=ImageColor.getrgb(color_front)
    (color_back_r, color_back_g, color_back_b)=ImageColor.getrgb(color_back)
    r = int(bind(color_back_r + (color_front_r - color_back_r) * hill_index / nb_hills,0,255))
    g = int(bind(color_back_g + (color_front_g - color_back_g) * hill_index / nb_hills,0,255))
    b  = int(bind(color_back_b + (color_front_b - color_back_b) * hill_index / nb_hills,0,255))
    return (r,g,b)


def draw_hills(hills, shift):
    img = Image.new("RGB", (img_w, img_h), color=color_sky)
    imgdraw = ImageDraw.Draw(img)
    for hill_index, hill_summits in enumerate(hills):
        hillcolor = hill_color(hill_index)
        hillshift  = shift * (hill_index+1)
        shifted_summits = shift_hill_summits(hill_summits,hillshift)
        poly = close_hill_polygon(shifted_summits)
        imgdraw.polygon(poly, fill=hillcolor, outline=(0, 0, 0), width=1)
    return img


# create PIL image
def drawimg():
    # convert PIL image to Streamlit image and display
    streamlit_image = streamlit.image(Image.new("RGB", (img_w, img_h), color=color_sky))
    hills = init_hills()
    while True:
        for tick in range(10):
            time.sleep(.5)
            img = draw_hills(hills, manual_shift + tick)
            streamlit_image.image(img)

drawimg()
