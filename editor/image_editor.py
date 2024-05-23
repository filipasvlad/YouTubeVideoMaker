from PIL import Image, ImageStat, ImageFilter
import urllib.request
from PIL import Image
import ssl
import urllib


class ImageEditor():
    def __init__(self, user_name, project_name, firefox_path):
        self.user_name = user_name
        self.project_name = project_name
        self.firefox_path = firefox_path

    def run(self, images_list):
        has_thumbnail = 0
        num_images = 0
        for image in images_list:
            if not has_thumbnail:
                try:
                    self.download_img(image, "C:\\Users\\" + self.user_name + "\\PycharmProjects\\" + self.project_name + "\\utils\\media\\thumbnail")
                    self.resize_images("C:\\Users\\" + self.user_name + "\\PycharmProjects\\" + self.project_name + "\\utils\\media\\thumbnail")
                    self.put_center_background("C:\\Users\\" + self.user_name + "\\PycharmProjects\\" + self.project_name + "\\utils\\media\\thumbnail")
                    has_thumbnail = 1
                except:
                    pass
            num_images += 1
            try:
                self.download_img(image, str(num_images))
                self.resize_images(str(num_images))
                self.put_center_background(str(num_images))
            except:
                num_images -= 1
        return num_images

    def download_img(self, img_url, img_name):
        if img_url.find(".PNG") != -1:
            return 0
        if img_url.find("http://") != -1:
            img_url = img_url[:4] + "s" + img_url[4:]
        url = img_url
        if img_url.find("?") != -1:
            url = img_url[:img_url.find("?")]
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=context))
            opener.addheaders = [('User-Agent', 'whatever')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(url, img_name + ".jpg")
            im = Image.open(img_name + ".jpg", 'r').convert("RGB")
            im.save(img_name + ".jpg")
            im.close()
        except:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=context))
            opener.addheaders = [('User-Agent', 'whatever')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(img_url, img_name + ".jpg")
            im = Image.open(img_name + ".jpg", 'r').convert("RGB")
            im.save(img_name + ".jpg")
            im.close()

    def put_center_background(self, img_name):
        img = Image.open(
            "C:\\Users\\" + self.user_name + "\\PycharmProjects\\" + self.project_name + "\\" + img_name + ".jpg", 'r')
        img_w, img_h = img.size
        blurImage = img.filter(ImageFilter.BLUR)

        left = 0
        top = int((img_h) / 2) - int(int((img_w * 720) / 1280) / 2)
        right = img_w
        bottom = int((img_h) / 2) + int(int((img_w * 720) / 1280) / 2)

        blurImage = blurImage.crop((left, top, right, bottom))
        background = blurImage.resize((1280, 720))
        bg_w, bg_h = background.size

        offset = ((bg_w - img_w) // 2, 0)
        background.paste(img, offset)
        background.save(img_name + ".jpg")

    def resize_images(self, img_name):
        img = Image.open(
            "C:\\Users\\" + self.user_name + "\\PycharmProjects\\" + self.project_name + "\\" + img_name + ".jpg", 'r')
        new_h = 720
        new_w = int(new_h / img.height * img.width)
        new_size = img.resize((new_w, new_h))
        new_size.save(img_name + ".jpg")


