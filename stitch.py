from pathlib import Path
from PIL import Image
from PIL import ImageDraw, ImageFont

class Painter:
    def __init__(self) -> None:
        self.source = ""
        self.n_suffix = []
        self.t_suffix = []
        self.horizontal_text = []
        self.vertical_text = []

        self.font_path = ""
        self.save_dir = ""
        self.filename = ""
    
    def set_source(self, image_folder: str):
        p = Path(image_folder)
        if not p.exists():
            raise FileNotFoundError
        elif not p.is_dir():
            raise ValueError(f"{image_folder} is not a directory")
        self.source = p
    
    def set_suffix(self, name_suffix: list, type_suffix: list):
        if not isinstance(name_suffix, list) or not isinstance(type_suffix, list):
            raise TypeError("suffix should be a list type")

        assert len(name_suffix) == len(type_suffix) - 1

        self.n_suffix = [s.lower().strip() for s in name_suffix]
        self.t_suffix = [s.lower().strip() for s in type_suffix]
    
    def set_result_directory(self, folder: str, save_filename: str = "result.png"):
        p = Path(folder)
        if not p.exists():
            raise FileNotFoundError
        elif not p.is_dir():
            raise ValueError(f"{folder} is not a directory")
        self.save_dir = p
        self.filename = save_filename
    
    def set_horizontal_text(self, horizontal_text: list):
        if not isinstance(horizontal_text, list):
            raise TypeError("horizontal text should be a list type")
        self.horizontal_text = horizontal_text
    
    def set_vertical_text(self, vertical_text: list):
        if not isinstance(vertical_text, list):
            raise TypeError("vertical text should be a list type")
        self.horizontal_text = vertical_text
    
    def generate(self, text_margin: int = 40, font_path: str = "times.ttf", font_size: int = 30, lr_margin: int = 5, tb_margin: int = 8):
        image_grid = []
        for img in self.source.glob(f"*.{self.t_suffix[0]}"):
            judgement = [suffix in img.stem for suffix in self.n_suffix]
            if any(judgement):
                continue
            else:
                line = [img.absolute().as_posix()]
                for idx, suffix in enumerate(self.n_suffix):
                    _img = img.parent.joinpath(f"{img.stem}_{suffix}.{self.t_suffix[idx + 1]}").absolute().as_posix()
                    line.append(_img)
                image_grid.append(line)
        for idx, line in enumerate(image_grid):
            img_line = [Image.open(img) for img in line]
            image_grid[idx] = img_line
        
        figure_width = -1
        figure_height = 0
        for line in image_grid:
            line_width = sum([img.size[0] for img in line]) + (len(line) - 1) * lr_margin
            line_height = max([img.size[1] for img in line]) + tb_margin
            
            figure_width = max(figure_width, line_width)
            figure_height += line_height
        
        canvas = Image.new("RGB", (figure_width + (len(image_grid[0]) - 1) * lr_margin, figure_height + (len(image_grid) - 1) * tb_margin), 'white')
        painter = ImageDraw.Draw(canvas)
        font = ImageFont.truetype(font_path, font_size)

        max_v_text_height = 0
        v_text_width = []
        for text in self.vertical_text:
            sz = font.getsize(text)
            max_v_text_height = max(max_v_text_height, sz[1])
            v_text_width.append(sz[0])

        max_h_text_height = 0
        h_text_width = []
        for text in self.horizontal_text:
            sz = font.getsize(text)
            max_h_text_height = max(max_h_text_height, sz[1])
            h_text_width.append(sz[0])
        
        canvas = Image.new("RGB", (figure_width + text_margin + max_v_text_height, figure_height + text_margin + max_h_text_height), 'white')
        painter = ImageDraw.Draw(canvas)

        cur_y = 0
        lines_height = []
        for idx, line_img in enumerate(image_grid):
            cur_x = max_v_text_height + text_margin
            for img in line_img:
                canvas.paste(img, box=(cur_x, cur_y))
                cur_x += img.size[0] + lr_margin

            image_max_height = max([img.size[1] for img in line_img])
            lines_height.append(image_max_height)
            cur_y += image_max_height + tb_margin

        canvas = canvas.rotate(270, expand=True)
        painter = ImageDraw.Draw(canvas)
        cur_x = tb_margin

        self.vertical_text.reverse()
        for idx, txt in enumerate(self.vertical_text):
            cur_xy = (cur_x + (lines_height[-(idx + 1)] - v_text_width[-(idx + 1)]) / 2, 0)
            painter.text(xy=cur_xy, text=txt, fill='black', font=font)
            cur_x += lines_height[-(idx + 1)] + tb_margin

        canvas = canvas.rotate(90, expand=True)
        painter = ImageDraw.Draw(canvas)

        cur_x = lr_margin
        for idx, txt in enumerate(self.horizontal_text):
            cur_xy = ((image_grid[-1][idx].size[0] - h_text_width[idx]) / 2 + cur_x, cur_y)
            painter.text(xy=cur_xy, text=txt, fill='black', font=font)
            cur_x += image_grid[-1][idx].size[0] + lr_margin
        
        canvas.save(self.save_dir.joinpath(f"{self.filename}").absolute().as_posix())


 
if __name__ == "__main__":
    p = Painter()
    p.set_source(r"C:\Users\Administrator\Desktop\test_data")
    p.set_result_directory(r"C:\Users\Administrator\Desktop")
    p.set_suffix(["ssn", "gt", "pred"], ['jpg', 'png', 'png', 'png'])
    p.set_horizontal_text(['Original Image', 'Superpixel Image', 'Ground Truth', 'Predict Image'])
    p.generate()