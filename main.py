#!/usr/bin/env python
import os
import db
import csv
import pandas as pd
from datetime import datetime
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from models import Metadata


class Video():

    def __init__(self, video, dir_name, csv_dir_name):
        self.video = video
        self.dir_name = dir_name
        self.csv_dir_name = csv_dir_name

    def process(self, video, dir_name):
        df = pd.DataFrame()
        begin = 0
        clip = VideoFileClip(video)
        duration = clip.duration
        total_frames = round(clip.fps * duration)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        while duration > 0:
            frame_per_time = round(clip.fps * begin)
            end = begin + 60
            clip_name = str(frame_per_time)+"thFrame.mov"
            clip_name_no_ext = str(frame_per_time) + "thFrame"
            clip_extension = ".mov"
            clip_location = os.path.join("video_clips/", "", clip_name)
            ffmpeg_extract_subclip(video, begin, end, targetname=clip_location)
            short_clip = VideoFileClip(clip_location)
            clip_duration = short_clip.duration
            clip_timestamp = datetime.now()
            video_info = Metadata(clip_name_no_ext, clip_extension, clip_duration, clip_location, clip_timestamp)
            db.session.add(video_info)
            db.session.commit()
            data = {'clip_name': clip_name_no_ext, 'clip_extension': clip_extension, 'clip_duration': clip_duration, 'clip_location': clip_location, 'clip_timestamp': clip_timestamp}
            df = df.append(data, ignore_index=True)
            print(df)
            begin += 60
            duration -= 60
        return df

    def report(self, csv_dir_name, df):
        if not os.path.exists(csv_dir_name):
            os.makedirs(csv_dir_name)
        file_name = os.path.join(csv_dir_name + "/generated_video_files.csv")
        df.to_csv(file_name, encoding='utf-8')
        

    if __name__ == '__main__':

        engine = db.db
        db.Base.metadata.create_all(engine)


video = Video("media/airshow.mp4", "video_clips", "report")
df = video.process(video.video, video.dir_name)
video.report("report", df)