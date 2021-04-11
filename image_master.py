import os
from PIL import Image, ImageFont, ImageDraw, ImageTk
import shutil
from time import sleep
from typing import Union
from pathlib import Path


class ImageMaster:
    def __init__(self):
        self.default_img = "assets/images/default_imgs/default_img.png"
        self.preview_img_loc = "assets/images/preview_imgs"
        self.uploaded_img_loc = r"assets/images/uploaded/uploaded_img.png"
        self.preview_watermarks_loc = "assets/images/preview_watermarks"
        self.custom_fonts_loc = "assets/fonts/uploaded_fonts"
        self.default_font = "Arial.ttf"
        self.current_font_list = sorted(Path(self.custom_fonts_loc).iterdir(), key=os.path.getmtime)
        self.preview_watermarks = sorted(Path(self.preview_watermarks_loc).iterdir(), key=os.path.getmtime)
        self.width, self.height = self.get_internal_image()
        self.default_sizing = (self.default_sizing())

    def default_sizing(self):
        if int(self.width) > 2000:
            return int(self.width / 6), int(self.height / 6)
        elif 800 <= int(self.width) < 2000:
            return int(self.width / 2), int(self.height / 2)
        elif self.height > 800:
            return int(self.width / 2), int(self.height / 2)
        else:
            return self.width, self.height

    def get_internal_image(self):
        try:
            image_tuple = Image.open(self.uploaded_img_loc).size
        except FileNotFoundError:
            image_tuple = Image.open(self.default_img).size
            return image_tuple
        else:
            return image_tuple

    def refresh_pre_watermarks(self):
        self.preview_watermarks = sorted(Path(self.preview_watermarks_loc).iterdir(), key=os.path.getmtime)

    def transfer_file(self, original_dir, file_type):
        if file_type == "img":
            original = original_dir
            target = self.uploaded_img_loc
            shutil.copyfile(original, target)
        elif file_type == "font":
            with open(original_dir) as file:
                file_name = os.path.basename(file.name)
            original = original_dir
            target = f"{self.custom_fonts_loc}/{file_name}"
            shutil.copyfile(original, target)
            self.current_font_list = sorted(Path(self.custom_fonts_loc).iterdir(), key=os.path.getmtime)

    def get_last_preview_watermarks(self):
        self.refresh_pre_watermarks()
        self.preview_watermarks.reverse()
        last_watermark_name = self.preview_watermarks[0]
        return last_watermark_name

    def get_image_object(self):
        """
        If no preview images found, returns Image object to default img
        :return:
        """
        self.refresh_pre_watermarks()
        if len(self.preview_watermarks) > 0:
            max_no = 0
            for watermark_file in self.preview_watermarks:
                splitted_file_no = int(watermark_file.stem.split("-")[1].split(".")[0])
                if splitted_file_no > max_no:
                    max_no = splitted_file_no
            return ImageTk.PhotoImage(Image.open(f"assets/images/preview_imgs/preview_img-{max_no}.png")
                                      .resize(self.default_sizing, Image.ANTIALIAS))
        elif len(os.listdir("assets/images/uploaded")) == 1:
            return ImageTk.PhotoImage(Image.open(self.uploaded_img_loc)
                                      .resize(self.default_sizing, Image.ANTIALIAS))
        else:
            return ImageTk.PhotoImage(Image.open(self.default_img)
                                      .resize(self.default_sizing, Image.ANTIALIAS))

    def text_to_image(self, font_name: str, text: str, coordinates: tuple, colour: Union[str, tuple], font_size: int, ):
        """
        This method does 2 things:
        1. It takes the parameters given and generates a transparent image with text ton it
        2. It then merges the uploaded image with the generated transparent watermark image and saves it.

        If colour arguement is None, defaults to the colour black
        :param font_name:
        :param text:
        :param coordinates:
        :param colour:
        :param font_size:
        :param rotation:
        :return:
        """
        self.refresh_pre_watermarks()
        print(f"Font Name ---> {font_name}")
        font = ImageFont.truetype(f"assets/fonts/uploaded_fonts/{font_name}", font_size)
        img = Image.new("RGBA", (self.width, self.height))
        draw = ImageDraw.Draw(img)
        draw.text(coordinates, text, colour, font=font)
        if len(self.preview_watermarks) == 0:
            img.save("assets/images/preview_watermarks/watermark-1.png")
        else:
            last_img_name = self.get_last_preview_watermarks()
            splitted_img_name = last_img_name.stem.split("-")[1].split(".")[0]
            new_str = int(splitted_img_name) + 1
            img.save(f"assets/images/preview_watermarks/watermark-{new_str}.png")
            self.preview_watermarks.reverse()

        self.refresh_pre_watermarks()
        last_watermark = str(self.get_last_preview_watermarks()).split("\\")[-1]
        foreground = Image.open(f"assets/images/preview_watermarks/{last_watermark}")
        raw_img = Image.open("assets/images/uploaded/uploaded_img.png")
        self.preview_watermarks.reverse()
        background = raw_img.convert("RGBA")
        sleep(1)
        max_no = 0
        for file in self.preview_watermarks:
            splitted_file_no = int(file.stem.split("-")[1].split(".")[0])
            if splitted_file_no > max_no:
                max_no = splitted_file_no
        Image.alpha_composite(background, foreground).save(f"assets/images/preview_imgs/preview_img-{max_no}.png")

    def clean_up(self):
        print(self.preview_watermarks_loc)
        for file in os.listdir(self.preview_watermarks_loc):
            os.remove(f"assets/images/preview_watermarks/{file}")

        for file in os.listdir(self.preview_img_loc):
            os.remove(f"assets/images/preview_imgs/{file}")
