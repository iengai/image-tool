from PIL import Image, ImageOps
from rembg import remove


class Manipulator:
    origin_path = None
    png_path = None
    image = None

    def __init__(self, image_path: str):
        self.origin_path = self.png_path = image_path
        self.image = Image.open(image_path)
        with Image.open(image_path) as im:
            if im.format == 'PNG':
                self.image = im
            else:
                self.__convert_to_png()
        if self.image.mode != "RGBA":
            self.image = self.image.convert("RGBA")

    def __convert_to_png(self):
        self.png_path = self.origin_path.split('.')[0] + '.png'
        self.image.save(self.png_path, 'PNG')
        self.image = Image.open(self.png_path)

    def __1_resize(self, new_size: int):
        width, height = self.image.size

        # 如果图片宽高比大于1，那么将宽度调整为512，同时保持宽高比不变
        if width > height:
            new_width = new_size
            new_height = int(height * (new_width / width))
        # 如果图片宽高比小于1，那么将高度调整为512，同时保持宽高比不变
        else:
            new_height = new_size
            new_width = int(width * (new_height / height))

        # 调整图片大小
        self.image = self.image.resize((new_width, new_height))

        self.image.save('1-resized-' + self.png_path)

        return '1-resized-' + self.png_path

    def __2_remove_background(self):
        self.image = remove(self.image)
        self.image.save('2-bgrem-' + self.png_path)

    def __3_square(self):

        # 获取图片宽度和高度
        width, height = self.image.size

        # 计算需要调整的边长
        new_size = max(width, height)

        # 创建一个白色背景的正方形图片
        new_image = Image.new('RGBA', (new_size, new_size), (255, 255, 255, 0))

        # 将原始图片复制到正方形图片的中央
        x = (new_size - width) // 2
        y = (new_size - height) // 2

        # 使用alpha_composite()方法合并两个图片
        new_image.alpha_composite(self.image, (x, y))
        self.image = new_image

        # 保存图片
        self.image.save('3-squared-' + self.png_path, format='png')
        return self.image

    def __4_transparent_to_bw(self):
        # 提取透明度通道
        alpha_channel = self.image.split()[3]
        self.image = ImageOps.invert(alpha_channel)

        # 保存黑白形式的透明度通道
        self.image.save('4-bw-' + self.png_path)
        return self.image



    def generate_bgrem_and_masked(self):
        self.__1_resize(512)
        self.__2_remove_background()
        squared_bgrem = self.__3_square()
        masked = self.__4_transparent_to_bw()

        return [squared_bgrem, masked]

    @staticmethod
    def merge(overlay, background, output):
        if overlay.mode != "RGBA":
            overlay = overlay.convert("RGBA")
        if background.mode != 'RGBA':
            background = background.convert("RGBA")
        background.alpha_composite(overlay)

        background.save(output)

        return output


def merge(overlay, background, output):
    overlay = overlay.convert("RGBA")
    background = background.convert("RGBA")
    background.alpha_composite(overlay)

    background.save(output)

    return output