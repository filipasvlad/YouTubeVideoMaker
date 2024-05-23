# Automated News Video Creation and Publishing Pipeline

This application automatically generates news videos and posts them on YouTube to generate revenue from views.

## How It Works

- **Content Processing**:

It uses web scraping (selenium) to extract textual content from news pages and to find relevant images on the internet for the discovered news story. The text is rewritten using QuillBot to avoid copyright issues.

- **Audio Preparation**:

The text is converted into audio using Microsoft Azure's text-to-speech feature through Balabolka.

- **Video Creation**:

Once the audio file and downloaded images are ready, the program will create a video compilation using ffmpeg. The images will be displayed with audio in the background, and every 40 seconds, an animation with a subscribe button will appear.

- **YouTube Upload**:

Once the video is ready, it will be automatically uploaded to YouTube using Selenium, preparing it to generate revenue from views.
