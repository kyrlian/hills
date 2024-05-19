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
    total_w = streamlit.slider("Total width", 1, 3000, 2000)
    shift_margin = (total_w - img_w) /2
    hill_height = img_h / nb_hills
    color_sky = streamlit.color_picker("Sky color", "#10EEEE")
    color_back = streamlit.color_picker("Back color", "#CCFFCC")
    color_front = streamlit.color_picker("Front color", "#00FF00")
    seed = streamlit.text_input("seed", "42")
    paralax = streamlit.slider("Paralax", 1, 10, 2)

def bind(x, min, max):
    if x < min:
        return min
    elif x > max:
        return max
    return x

def init_hill_summits(hill_index):
    nb_summits = 10
    summit_width = img_w / nb_summits
    hill_summits = []
    x = 0 - shift_margin
    max_x = img_w + shift_margin
    prev_y = (hill_index + .5) * hill_height
    while x < max_x:
        # y = (hill_index + random.random()) * hill_height
        # limit the variation between summits
        variation = .1 + (1 - (hill_index / nb_hills)) * .4
        y = bind(prev_y + random.random() * variation * hill_height  , hill_index * hill_height, (hill_index + 1) * hill_height)
        hill_summits.append((x, y))
        x += random.random() * summit_width
    return hill_summits

# @streamlit.cache_data
def init_hills():
    hills = []
    for hill_index in range(nb_hills):
        hills.append(init_hill_summits(hill_index))
    return hills

def shift_hill_summits(hill_summits, shift):
    shifted_summits=[]
    for summit in hill_summits:
        (x,y) = summit
        x_shift = x+shift
        # if x_shift>=0 and x_shift<=img_w:
        shifted_summits.append((x_shift,y))
    return shifted_summits

def close_hill_polygon(hill_summits):
    poly= []
    poly.append((0, img_h))
    if len(hill_summits) > 0:
        poly.append((0, hill_summits[0][1]))
        for s in hill_summits:
            poly.append(s)
        poly.append((img_w, hill_summits[-1][1]))
    poly.append((img_w, img_h))
    return poly

def hill_color(hill_index):
    # lower index = top of screen = further away
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
    shift_range = int(shift_margin / paralax /2)
    while True:
        for shift in range(-shift_range, shift_range, 1):
            time.sleep(.1)
            img = draw_hills(hills, shift * paralax)
            streamlit_image.image(img)

drawimg()
