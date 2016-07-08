# coding=utf-8
u"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of kudubot.

    kudubot makes use of various third-party python modules to serve
    information via online chat services.

    kudubot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    kudubot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with kudubot.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
from __future__ import absolute_import
import os
import sys

from yowsup.layers.interface import YowInterfaceLayer
from yowsup.layers.interface import ProtocolEntityCallback
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.layers.protocol_messages.protocolentities import MessageProtocolEntity
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities import RequestUploadIqProtocolEntity
from yowsup.layers.protocol_media.protocolentities import ResultRequestUploadIqProtocolEntity
from yowsup.layers.protocol_media.protocolentities import ImageDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities import AudioDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities import VideoDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities.builder_message_media_downloadable \
    import DownloadableMediaMessageBuilder


from kudubot.logger.PrintLogger import PrintLogger


class YowsupEchoLayer(YowInterfaceLayer):
    u"""
    The Yowsup Echo layer class
    The layer component of the whatsapp connection. Used to receive messages.
    """

    # Required local variables
    disconnect_action_prompt = 0
    accountDelWarnings = 0
    connected = False
    username = None
    sendReceipts = True
    disconnectAction = 0
    credentials = None
    jid_aliases = {}

    @ProtocolEntityCallback(u"receipt")
    def on_receipt(self, entity):
        u"""
        method run whenever a whatsapp receipt is issued

        :param entity: The receipt entity
        :return: void
        """
        self.toLower(entity.ack())

    def send_media(self, number, path, media_type,
                   caption = None):
        u"""
            Sends a media file

            :param number: the receiver of the media file
            :param path: the path to the media file
            :param media_type: The type of media to send
            :param caption: the caption to be shown
            :return: void
            """
        jid = self.alias_to_jid(number)
        entity = RequestUploadIqProtocolEntity(media_type, filePath=path)

        def success_fn(success_entity, original_entity):
            u"""
            Function called on successful media upload

            :param success_entity: the success entity
            :param original_entity: the original entity
            :return: None
            """
            # noinspection PyTypeChecker
            self.on_request_upload_result(jid, media_type, path, success_entity, original_entity, caption)

        def error_fn(error_entity, original_entity):
            u"""
            Function called on failed media upload

            :param error_entity: the error entity
            :param original_entity: the original entity
            :return: None
            """
            YowsupEchoLayer.on_request_upload_error(jid, path, error_entity, original_entity)

        self._sendIq(entity, success_fn, error_fn)

    def send_image(self, number, path, caption = None):
        u"""
        Sends an image

        :param number: the receiver of the image
        :param path: the path to the image file
        :param caption: the caption to be shown
        :return: void
        """
        self.send_media(number, path, RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE, caption)

    def send_audio(self, number, path):
        u"""
        Sends an audio file

        :param number: the number of the receiver of the file
        :param path: the path to the audio file
        :return: None
        """
        self.send_media(number, path, RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO)

    def send_video(self, number, path, caption = None):
        u"""
        Sends a video file

        :param number: the number of the receiver of the file
        :param path: the path to the video file
        :param caption: an optional caption to be displayed together with the video file
        :return: None
        """
        self.send_media(number, path, RequestUploadIqProtocolEntity.MEDIA_TYPE_VIDEO, caption)

    def do_send_media(self, media_type,
                      file_path, url, to, ip = None, caption = None):
        u"""
        Sends a media file

        :param media_type: The type of media to send
        :param file_path: the path to the file
        :param url: the whatsapp upload url
        :param to: the receiver
        :param ip: the ip of the receiver
        :param caption: the caption to be displayed together with the media file
        :return: None
        """
        entity = None
        if media_type == RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE:
            entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(file_path, url, ip, to, caption=caption)
        elif media_type == RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO:
            entity = self.create_audio_media(file_path, url, to, ip)
        elif media_type == RequestUploadIqProtocolEntity.MEDIA_TYPE_VIDEO:
            entity = VideoDownloadableMediaMessageProtocolEntity.fromFilePath(file_path, url, ip, to, caption=caption)
        self.toLower(entity)

    @staticmethod
    def create_audio_media(file_path, url, to, ip = None):
        u"""
        Creates an Audio Message Entity as a workaround for the missing fromFilePath method in
        AudioDownloadableMediaMessageProtocolEntity's parent class

        :param file_path: the path to the file
        :param url: the whatsapp upload url
        :param to: the receiver
        :param ip: the ip of the receiver
        :return: None
        :return: the generatd audio entity
        """
        builder = DownloadableMediaMessageBuilder(AudioDownloadableMediaMessageProtocolEntity, to, file_path)
        builder.set(u"url", url)
        builder.set(u"ip", ip)
        return AudioDownloadableMediaMessageProtocolEntity.fromBuilder(builder)

    def on_request_upload_result(self, jid, media_type, file_path,
                                 result_request_upload_iq_protocol_entity,
                                 request_upload_iq_protocol_entity,
                                 caption = None):
        u"""
        Method run when a media upload result is positive

        :param jid: the jid to receive the media
        :param media_type: The media type to send
        :param file_path: the path to the media file
        :param result_request_upload_iq_protocol_entity: the result entity
        :param request_upload_iq_protocol_entity: the request entity
        :param caption: the media caption, if applicable
        :return: None
        """
        unicode(request_upload_iq_protocol_entity)
        if result_request_upload_iq_protocol_entity.isDuplicate():
            self.do_send_media(media_type, file_path, result_request_upload_iq_protocol_entity.getUrl(), jid,
                               result_request_upload_iq_protocol_entity.getIp(), caption)
        else:

            def success_fn(inner_file_path, inner_jid, url):
                u"""
                Function called when upload was successful

                :param inner_file_path: path to the media file
                :param inner_jid: the receiver's jid
                :param url: the whatsapp media url
                :return: None
                """
                self.do_send_media(media_type, inner_file_path, url, inner_jid,
                                   result_request_upload_iq_protocol_entity.getIp(), caption)

            media_uploader = MediaUploader(jid, self.getOwnJid(), file_path,
                                           result_request_upload_iq_protocol_entity.getUrl(),
                                           result_request_upload_iq_protocol_entity.getResumeOffset(), success_fn,
                                           YowsupEchoLayer.on_upload_error, YowsupEchoLayer.on_upload_progress,
                                           async=False)
            media_uploader.start()

    @staticmethod
    def on_request_upload_error(jid, path, error_request_upload_iq_protocol_entity,
                                request_upload_iq_protocol_entity):
        u"""
        Method run when a media upload result is negative

        :param jid: the jid to receive the media
        :param path: the file path to the media
        :param error_request_upload_iq_protocol_entity: the error result entity
        :param request_upload_iq_protocol_entity: the request entity
        :return: None
        """
        if error_request_upload_iq_protocol_entity and request_upload_iq_protocol_entity:
            PrintLogger.print(u"Request upload for file %s for %s failed" % (path, jid))

    @staticmethod
    def on_upload_error(file_path, jid, url):
        u"""
        Method run when an upload error occurs

        :param file_path: the file path of the file to upload
        :param jid: the jid of the receiver of the file
        :param url: the upload url
        :return: None
        """
        PrintLogger.print(u"Upload file %s to %s for %s failed!" % (file_path, url, jid))

    @staticmethod
    def on_upload_progress(file_path, jid, url, progress):
        u"""
        Method that keeps track of the upload process

        :param file_path: the file path of the media file
        :param jid: the jid of the receiver
        :param url: the whatsapp upload url
        :param progress: the current progress
        :return:None
        """
        if url:
            sys.stdout.write(u"%s => %s, %d%% \r" % (os.path.basename(file_path), jid, progress))
            sys.stdout.flush()

    def alias_to_jid(self, c_alias):
        u"""
        Turns an alias into a jid

        :param c_alias: the current alias
        :return: the jid
        """
        for alias, a_jid in self.jid_aliases.items():
            if c_alias.lower() == alias.lower():
                return YowsupEchoLayer.normalize_jid(a_jid)

        return YowsupEchoLayer.normalize_jid(c_alias)

    @staticmethod
    def normalize_jid(number):
        u"""
        Normalizes a jid

        :param number: the number to be receive a normalized jid
        :return: the normalized jid
        """
        if u'@' in number:
            return number
        elif u"-" in number:
            return number + u"@g.us"

        return number + u"@s.whatsapp.net"

    def send_receipt(self, message_protocol_entity):
        u"""
        Sends the whatsapp servers that the message was received

        :param message_protocol_entity: the message protocol entity that was received
        :return: None
        """
        self.toLower(message_protocol_entity.ack())
        self.toLower(message_protocol_entity.ack(True))
