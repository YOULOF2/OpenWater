from image_master import ImageMaster
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk
from ttkthemes import ThemedTk
import math
from tkinter import colorchooser
from reinit_app import reinit_app

GREY = "#dddddd"
FONT_DATA = ("Futura", 10, "normal")
window = ThemedTk(theme="arc", background=True)
# window.iconphoto(False, tk.PhotoImage(file='/path/to/ico/icon.png'))
window.title("Password Manager")
window.config(padx=50, pady=50)
image_controller = ImageMaster()
font_colour = ("black", "black")


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
                                                             "It should aid in determining the c"
                                                             "orrect font size of the watermark.\n"
                                                             "The selected fonts will work"
                                                             " in the watermark.",
                                   font=("Futura", 10, "normal"))
    note_preview_label.grid(row=1, column=0, pady=(5, 0))


# function to be called when mouse is clicked
def generate_watermark(event):
    def search():
        for i in image_controller.current_font_list:
            if str(i).split("\\")[-1].upper().split(".")[0] == font_dropdown_variable.get().upper():
                return str(i).split("\\")[-1]
    # outputting x and y coords to console
    event2canvas = lambda e, c: (c.canvasx(e.x), c.canvasy(e.y))
    cx, cy = event2canvas(event, preview_img_canvas)
    font_size = math.floor(font_size_var.get())
    font_colour_rgb = font_colour[0]
    # print(font_colour_rgb)
    input_text = watermark_enter.get()
    chosen_font = search()
    print(chosen_font)
    colour_list = []
    try:
        for i in font_colour_rgb:
            rounded_num = math.ceil(float(i))
            colour_list.append(rounded_num)
    except ValueError:
        colour = font_colour_rgb
    else:
        colour = tuple(colour_list)
    image_controller.text_to_image(font_name=chosen_font, text=input_text, coordinates=(cx, cy), colour=colour, font_size=font_size)
    reinit_app(window)


def font_scale(event):
    font_size = math.floor(font_size_var.get())
    font_size_label.config(text=f"Select Font Size: {font_size}")


def get_uploaded_img_location():
    file_path = filedialog.askopenfilename(initialdir="/", title="Select Image File",
                                           filetypes=(
                                               ("jfif files", "*.jfif"), ("jpeg files", "*.jpg"),
                                               ("png files", "*.png"),
                                               ("all files", "*.*")))
    if file_path != "":
        image_controller.transfer_file(file_path, "img")
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
rotate_left = ttk.Button(font_frame, text="Rotate Watermark Left", width=23)
rotate_right = ttk.Button(font_frame, text="Rotate Watermark Right", width=23)
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

watermark_label.grid(row=0, column=0, columnspan=2)
watermark_enter.grid(row=1, column=0, columnspan=2)

rotate_right.grid(row=0, column=1)
rotate_left.grid(row=0, column=0)
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
upload_img_btn = ttk.Button(file_options, text="Load Image", width=48, command=get_uploaded_img_location)
save_img_btn = ttk.Button(file_options, text="Save Image", width=48, command=image_controller.clean_up)
upload_img_btn.grid(row=0, column=0)
save_img_btn.grid(row=1, column=0)
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
preview_img_canvas.create_image(image_controller.default_sizing[0] / 2, image_controller.default_sizing[1] / 2,
                                image=preview_img)
preview_img_canvas.grid(row=0, column=0)
preview_frame.grid(row=0, column=0, padx=(0, 50), rowspan=5)

preview_img_canvas.bind("<ButtonPress-1>", generate_watermark)

window.mainloop()
