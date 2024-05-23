from fetcher.content_fetcher import NewsFetcher
from editor.image_editor import ImageEditor
from editor.video_creator import VideoCreator
from rewriter.text_rewriter import TextRewriter
from audio.text_to_audio import TextToAudio
from uploader.youtube_uploader import YoutubeUploader

user_name = "filip"
project_name = "YouTube"
firefox_path = "mtmt2hol.default-release"

news_fetcher = NewsFetcher(user_name, project_name, firefox_path)
image_editor = ImageEditor(user_name, project_name, firefox_path)
video_creator = VideoCreator(user_name, project_name, firefox_path)
text_rewriter = TextRewriter(user_name, project_name, firefox_path)
text_to_audio = TextToAudio(user_name, project_name, firefox_path)
youtube_uploader = YoutubeUploader(user_name, project_name, firefox_path)


title, description, text, images_list = news_fetcher.run()
num_images = image_editor.run(images_list)
title, description, text = text_rewriter.run(title, description, text)
text_to_audio.run(text)
video_creator.run(num_images)
youtube_uploader.upload(title, description)






