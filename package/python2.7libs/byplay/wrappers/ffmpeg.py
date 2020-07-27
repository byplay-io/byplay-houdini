from __future__ import absolute_import
import logging
import os

from byplay.config import Config


class FFMPEG(object):
    def extract_frames(self, video_path, frames_path):
        return self.run(u"-i $VIDEO_PATH -vsync 0 $FRAMES_PATH", {u'VIDEO_PATH': video_path, u"FRAMES_PATH": frames_path})

    def combine_frames_to_video(self, frames_path, video_path):
        cmd = u"""-y -r 30 -i $FRAMES_PATH
        -vb 20M
        -f mp4 -pix_fmt yuv420p
        $VIDEO_PATH
        """
        return self.run(cmd, {u'VIDEO_PATH': video_path, u"FRAMES_PATH": frames_path})

    def crop_video(self, src_video_path, dst_video_path, byplaycrop_params):
        cmd = u"""-y -i $SRC_VIDEO_PATH
            -vb 20M
            -f mp4 -pix_fmt yuv420p
            -vf byplaycrop=w=$WIDTH:h=$HEIGHT:bpl_x_seq=$BPL_X_SEQ:bpl_y_seq=$BPL_Y_SEQ
            $DST_VIDEO_PATH
        """
        params = {
            u"SRC_VIDEO_PATH": src_video_path,
            u"DST_VIDEO_PATH": dst_video_path,
        }
        for k, v in byplaycrop_params.items():
            params[k] = v

        return self.run(cmd, params)

    def run(self, command, params={}):
        args = command.replace(u"\n", u" ")
        for k, v in params.items():
            args = args.replace(u"${}".format(k), v)
        final_cmd = u"{} {}".format(Config.ffmpeg_path(), args)
        logging.debug(u"Executing ffmpeg '{}'".format(final_cmd))
        os.system(final_cmd)
