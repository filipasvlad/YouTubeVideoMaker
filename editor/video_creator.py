import random
from pydub import AudioSegment
from PIL import Image
import os
import time

class VideoCreator():
    def __init__(self, user_name, project_name, firefox_path):
        self.__user_name = user_name
        self.__project_name = project_name
        self.__firefox_path = firefox_path

    def run(self, num_images):
        num_images = self.duplicate_photos(num_images)
        print(num_images)
        self.audio_and_images_to_video(num_images, "videoclip")
        self.delete_images()
        self.add_subscribe_button("videoclip", "video")

    def duplicate_photos(self, num_images):
        initial_images = num_images
        num_images_needed = int(
            self.get_duration('utils\\media\\audio.wav') / 7.5) + 1
        num_images = num_images + 1
        images_list = []
        for x in range(1, num_images):
            images_list.append(Image.open(
                "C:\\Users\\" + self.__user_name + "\\PycharmProjects\\" + self.__project_name + "\\" + str(x) + ".jpg"))
        while num_images <= num_images_needed:
            n = num_images % initial_images
            im = images_list[n].copy()
            im = im.convert("RGB")
            im.save(str(num_images) + ".jpg")
            num_images += 1
        return num_images_needed

    def get_duration(self, filename):
        sound = AudioSegment.from_file(filename)
        seconds_duration = int(sound.duration_seconds)
        return seconds_duration

    def delete_images(self):
        for image in range(1, 101):
            try:
                os.remove("C:\\Users\\" + self.__user_name + "\\PycharmProjects\\" + self.__project_name + "\\" + str(image) + ".jpg")
            except:
                break

    def audio_and_images_to_video(self, num_images, video_name):
        script_list = []
        script_list.append(
            "scale=-2:10*720,zoompan=z='min(zoom+0.0007,1.25)':d=225:x='iw/2-(iw/zoom/2)',fade=t=in:st=0:d=1,fade=t=out:st=20:d=1")
        script_list.append(
            "scale=-2:10*720,zoompan=z='if(lte(zoom,1.0),1.5,max(1.001,zoom-0.0015))':d=225:x='iw/2-(iw/zoom/2)',fade=t=in:st=0:d=1,fade=t=out:st=20:d=1")
        script_list.append("zoompan=z='min(zoom+0.0007,1.25)':d=225,fade=t=in:st=0:d=1,fade=t=out:st=20:d=1")
        script_list.append(
            "zoompan=z='if(lte(zoom,1.0),1.15,max(1.001,zoom-0.0007))':d=225,fade=t=in:st=0:d=1,fade=t=out:st=20:d=1")
        try:
            os.remove("C:\\Users\\" + self.__user_name + "\\PycharmProjects\\" + self.__project_name + "\\" + video_name + ".mp4")
        except:
            pass
        video_length = self.get_duration('utils\\media\\audio.wav')
        script_command = "ffmpeg "
        for num in range(num_images):
            script_command += "-t 5 -i " + str(num + 1) + ".jpg "
        script_command += '-filter_complex_script utils/config/temp.txt '
        f = open("utils/config/temp.txt", 'w')
        last_r_num = -1
        for num in range(num_images):
            f.write("[" + str(num) + ":v]")
            r_nr = random.randint(0, 3)
            while r_nr == last_r_num:
                r_nr = random.randint(0, 3)
            last_r_num = r_nr
            f.write(script_list[r_nr])
            f.write("[v" + str(num) + "]; ")
        for num in range(num_images):
            f.write("[v" + str(num) + "]")
        f.write('concat=n=' + str(num_images) + ':v=1:a=0,format=yuv420p[v]')
        f.close()
        script_command += '-map "[v]" -s "1280x720" -t ' + str(video_length) + ' ' + video_name + '.mp4'
        os.system(script_command)
        time.sleep(1)

    def add_subscribe_button(self, initial_video_name, final_video_name):
        video_length = self.get_duration('utils\\media\\audio.wav')
        duration = 40
        script_command = 'ffmpeg -i ' + initial_video_name + '.mp4 -i C:\\Users\\' + self.__user_name + '\\PycharmProjects\\' + self.__project_name + '\\utils\\media\\audio.wav '
        num = int((video_length) / duration)
        f = open("utils\\config\\temp.txt", 'w', encoding="utf-8")
        for i in range(1, num + 1):
            script_command += '-i C:\\Users\\' + self.__user_name + '\\PycharmProjects\\' + self.__project_name + '\\utils\\media\\subscribe.mov '
        script_command += '-filter_complex_script C:\\Users\\' + self.__user_name + '\\PycharmProjects\\' + self.__project_name + '\\utils\\config\\temp.txt '
        for i in range(1, num + 1):
            if i == 1:
                f.write('[' + str(i + 1) + ':v]setpts=PTS-STARTPTS+25/TB[v' + str(i) + '];')
            else:
                f.write(
                    '[' + str(i + 1) + ':v]setpts=PTS-STARTPTS+' + str(25 + duration * (i - 1)) + '/TB[v' + str(i) + '];')

        f.write('[0:v][v1]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)[vid1]')
        if num != 1:
            f.write(";")
        for i in range(1, num):
            f.write('[vid' + str(i) + '][v' + str(i + 1) + ']overlay=(main_w-overlay_w)/2:(main_h-overlay_h)[vid' + str(
                i + 1) + ']')
            if i != num - 1:
                f.write(";")
        script_command += ' -map "[vid' + str(
            num) + ']" -map 1:a? -c:v libx264 -crf 23 -c:a aac -movflags +faststart C:\\Users\\' + self.__user_name + '\\PycharmProjects\\' + self.__project_name + '\\utils\\media\\' + final_video_name + '.mp4'
        f.close()

        try:
            os.remove('C:\\Users\\' + self.__user_name + '\\PycharmProjects\\' + self.__project_name + '\\utils\\media\\' + final_video_name + '.mp4')
        except:
            pass

        os.system(script_command)

        try:
            os.remove("C:\\Users\\" + self.__user_name + "\\PycharmProjects\\" + self.__project_name + "\\" + initial_video_name + ".mp4")
        except:
            pass