import os
from image_master import ImageMaster
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
from ttkthemes import ThemedTk
import math
from tkinter import colorchooser
from tkinter import messagebox
from reinit_app import reinit_app

GREY = "#dddddd"
FONT_DATA = ("TkMenuFont", 10, "normal")
window = ThemedTk(theme="arc", background=True)
window.iconphoto(False, tk.PhotoImage(file='assets/images/default_imgs/icon.png'))
window.title("OpenWater")
window.config(padx=50, pady=50)
image_controller = ImageMaster()
font_colour = ("black", "black")
text_rotation_angle = 0


def plus_angle():
    global text_rotation_angle
    text_rotation_angle += 10
    rotation_label.config(text=f"{text_rotation_angle}°")


def minus_angle():
    global text_rotation_angle
    text_rotation_angle -= 10
    rotation_label.config(text=f"{text_rotation_angle}°")


def change_notification_label(text):
    notification_label.config(text=text)


def choose_color():
    global font_colour
    # variable to store hexadecimal code of color
    font_colour = colorchooser.askcolor(title="Choose color")
    select_colour_canvas.config(bg=font_colour[1])
    print(font_colour)


def preview_font():
    chosen_font = font_dropdown_variable.get()
    font_size = math.floor(font_size_var.get())
    fontcolour = font_colour[1]
    font = (chosen_font, font_size, "normal")
    font_preview_window = tk.Tk()
    font_preview_window.title("Font Preview")
    font_preview_window.config(padx=50, pady=50)
    font_preview_label = ttk.Label(font_preview_window, text='Sample Text', font=font, foreground=fontcolour)
    font_preview_label.grid(row=0, column=0)
    note_preview_label = ttk.Label(font_preview_window, text="Note, some fonts don't work with the "
                                                             "text preview feature.\n"
                                                             "It should aid in determining the "
                                                             "correct font size of the watermark.\n"
                                                             "The selected fonts will work"
                                                             " in the watermark.",
                                   font=FONT_DATA)
    note_preview_label.grid(row=1, column=0, pady=(5, 0))


def save_image():
    global preview_img
    save_to_dir = filedialog.askdirectory()
    image_controller.save_image(save_to_dir)
    change_notification_label("Image Saved Succesfully.")


# function to be called when mouse is clicked
def generate_watermark(eventorigin):
    print(text_rotation_angle)
    if watermark_enter.get() == ".code__debug.":
        cx = math.ceil(eventorigin.x * image_controller.image_scale)
        cy = math.ceil(eventorigin.y * image_controller.image_scale) - 50
        print(f"({cx}, {cy})")
        change_notification_label(f"Coordinates of Click: ({cx}, {cy})")
    elif watermark_enter.get() == ".code__cleanup.":
        image_controller.clean_up()
    else:
        def search():
            for i in image_controller.current_font_list:
                if str(i).split("\\")[-1].upper().split(".")[0] == font_dropdown_variable.get().upper():
                    return str(i).split("\\")[-1]

        # outputting x and y coords to console
        cx = math.ceil(eventorigin.x * image_controller.image_scale)
        cy = math.ceil(eventorigin.y * image_controller.image_scale) - 40
        font_size = math.floor(font_size_var.get())
        font_colour_rgb = font_colour[0]
        # print(font_colour_rgb)
        input_text = watermark_enter.get()
        chosen_font = search()
        colour_list = []
        if font_colour_rgb is None:
            colour = "black"
        else:
            try:
                for i in font_colour_rgb:
                    rounded_num = math.ceil(float(i))
                    colour_list.append(rounded_num)
            except ValueError:
                colour = font_colour_rgb
            else:
                colour = tuple(colour_list)
        image_controller.text_to_image(font_name=chosen_font, text=input_text, coordinates=(cx, cy + 20), colour=colour,
                                       font_size=font_size, rotation_angle=text_rotation_angle)
        reinit_app(window)


def font_scale(event):
    font_size = math.floor(font_size_var.get())
    font_size_label.config(text=f"Select Font Size: {font_size}")


def get_uploaded_img_location():
    if len(image_controller.preview_watermarks) > 0:
        are_you_sure = messagebox.askyesno("Are you sure?", "Do you want to discard the changes made?")
        if are_you_sure:
            file_path = filedialog.askopenfilename(initialdir="/", title="Select Image File",
                                                   filetypes=(
                                                       ("jfif files", "*.jfif"), ("jpeg files", "*.jpg"),
                                                       ("png files", "*.png"),
                                                       ("all files", "*.*")))
            if file_path != "":
                image_controller.transfer_file(file_path, "img")
                image_controller.clean_up()
                reinit_app(window)
    else:
        file_path = filedialog.askopenfilename(initialdir="/", title="Select Image File",
                                               filetypes=(
                                                   ("jfif files", "*.jfif"), ("jpeg files", "*.jpg"),
                                                   ("png files", "*.png"),
                                                   ("all files", "*.*")))
        if file_path != "":
            image_controller.transfer_file(file_path, "img")
            image_controller.clean_up()
            reinit_app(window)


def get_uploaded_font_location():
    file_path = filedialog.askopenfilename(initialdir="/", title="Select Custom Font File",
                                           filetypes=(
                                               ("True Type Font file", "*.ttf"),
                                               ("all files", "*.*")))
    if file_path != "":
        image_controller.transfer_file(file_path, "font")
        reinit_app(window)


# -------------------------------------------------------------------------------------------------------------------- #
master_controls_frame = ttk.Frame(window)
# -------------------------------------------------------------------------------------------------------------------- #
font_list_raw = image_controller.current_font_list
font_list_raw.insert(0, image_controller.default_font)
font_list = []
for i in font_list_raw:
    font_name_list = str(i).split(".")[0].split("\\")
    font_name_list.reverse()
    font_list.append(font_name_list[0])

font_dropdown_variable = tk.StringVar(window)
font_dropdown_variable.set(font_list)

image_controls_frame = ttk.LabelFrame(master_controls_frame, text="Image Controls")

watermark_label = ttk.Label(image_controls_frame)
watermark_label.config(text="Enter the Text to be Watermarked", font=FONT_DATA)
watermark_enter = ttk.Entry(image_controls_frame, width=51)
watermark_enter.focus()

font_frame = ttk.Frame(image_controls_frame)
font_selector_dropdown = ttk.OptionMenu(font_frame, font_dropdown_variable, *font_list)
font_selector_label = ttk.Label(font_frame)
font_selector_label.config(text="Select a Font to Use", font=FONT_DATA)
font_selector_dropdown.config(width=20)
load_font = ttk.Button(font_frame, text="Upload Custom Font", width=50, command=get_uploaded_font_location)

font_size_var = tk.DoubleVar()

font_size_label = ttk.Label(font_frame, text="Select Font Size: ", font=FONT_DATA)
font_size_scale = ttk.Scale(font_frame, from_=0, to=190, orient=tk.HORIZONTAL, length=150, variable=font_size_var,
                            command=font_scale)
font_size_scale.set(20)
select_colour_btn = ttk.Button(font_frame, text="Select Font Colour", width=23, command=choose_color)
select_colour_canvas = tk.Canvas(font_frame, width=153, height=20, bg=font_colour[1], highlightthickness=5)

image_rotation_frame = ttk.Frame(font_frame)
rotate_left = ttk.Button(image_rotation_frame, text="Rotate Left", width=20, command=minus_angle)
rotate_right = ttk.Button(image_rotation_frame, text="Rotate Right", width=20, command=plus_angle)
rotation_label = ttk.Label(image_rotation_frame, text=f"{text_rotation_angle}°", font=FONT_DATA)
rotate_left.grid(row=0, column=0)
rotate_right.grid(row=0, column=1)
rotation_label.grid(row=0, column=2, padx=(10, 0))

watermark_label.grid(row=0, column=0, columnspan=2)
watermark_enter.grid(row=1, column=0, columnspan=2)

image_rotation_frame.grid(row=0, column=0, columnspan=2, sticky=tk.W)
font_selector_label.grid(row=1, column=0)
font_selector_dropdown.grid(row=1, column=1)
load_font.grid(row=2, column=0, columnspan=2)
font_size_label.grid(row=3, column=0)
font_size_scale.grid(row=3, column=1)
select_colour_btn.grid(row=4, column=0)
select_colour_canvas.grid(row=4, column=1)
font_submit_preview = ttk.Button(font_frame, text="Preview Text", width=50, command=preview_font)
font_submit_preview.grid(row=5, column=0, columnspan=2)
font_frame.grid(row=2, column=0)

image_controls_frame.grid(row=1, column=1, pady=(0, image_controller.default_sizing[1] - 260))
# -------------------------------------------------------------------------------------------------------------------- #


file_options = ttk.Frame(master_controls_frame)
notification_label = ttk.Label(file_options, text="", font=FONT_DATA)
upload_img_btn = ttk.Button(file_options, text="Load Image", width=48, command=get_uploaded_img_location)
save_img_btn = ttk.Button(file_options, text="Save Image", width=48, command=save_image)
notification_label.grid(row=0, column=0)
upload_img_btn.grid(row=1, column=0)
save_img_btn.grid(row=2, column=0)
file_options.grid(row=2, column=1)

# -------------------------------------------------------------------------------------------------------------------- #
master_controls_frame.grid(row=0, column=1)
# -------------------------------------------------------------------------------------------------------------------- #

preview_frame = ttk.LabelFrame(window, text=f"{image_controller.width} x {image_controller.height} - Image Preview")
preview_img_canvas = tk.Canvas(preview_frame,
                               width=(image_controller.default_sizing[0]),
                               height=(image_controller.default_sizing[1]),
                               highlightthickness=1)
preview_img = image_controller.get_image_object()
preview_img_canvas.create_image(image_controller.default_sizing[0], image_controller.default_sizing[1],
                                image=preview_img, anchor=tk.SE)
preview_img_canvas.grid(row=0, column=0)
preview_frame.grid(row=0, column=0, padx=(0, 50), rowspan=5)

preview_img_canvas.bind("<ButtonPress-1>", generate_watermark)

window.mainloop()
