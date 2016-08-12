# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# EDITING INSTRUCTIONS
# This file was generated from the file
# https://github.com/google/googleapis/blob/master/google/cloud/speech/v1/cloud_speech.proto,
# and updates to that file get reflected here through a refresh process.
# For the short term, the refresh process will only be runnable by Google engineers.
#
# The only allowed edits are to method and file documentation. A 3-way
# merge preserves those additions if the generated source changes.
"""Accesses the google.cloud.speech.v1 Speech API."""

import json
import os
import pkg_resources
import platform

from google.gax import api_callable
from google.gax import config
from google.gax import path_template
import google.gax

from google.cloud.speech.v1 import cloud_speech_pb2


class SpeechApi(object):
    """Service that implements Google Cloud Speech API."""

    SERVICE_ADDRESS = 'speech.googleapis.com'
    """The default address of the service."""

    DEFAULT_SERVICE_PORT = 443
    """The default port of the service."""

    _CODE_GEN_NAME_VERSION = 'gapic/0.1.0'

    _GAX_VERSION = pkg_resources.get_distribution('google-gax').version

    # The scopes needed to make gRPC calls to all of the methods defined in
    # this service
    _ALL_SCOPES = ('https://www.googleapis.com/auth/cloud-platform', )

    def __init__(self,
                 service_path=SERVICE_ADDRESS,
                 port=DEFAULT_SERVICE_PORT,
                 channel=None,
                 metadata_transformer=None,
                 ssl_creds=None,
                 scopes=None,
                 client_config=None,
                 app_name='gax',
                 app_version=_GAX_VERSION):
        """Constructor.

        Args:
          service_path (string): The domain name of the API remote host.
          port (int): The port on which to connect to the remote host.
          channel (:class:`grpc.beta.implementations.Channel`): A ``Channel``
            object through which to make calls.
          ssl_creds (:class:`grpc.beta.implementations.ClientCredentials`):
            A `ClientCredentials` for use with an SSL-enabled channel.
          client_config (dict):
            A dictionary for call options for each method. See
            :func:`google.gax.construct_settings` for the structure of
            this data. Falls back to the default config if not specified
            or the specified config is missing data points.
          metadata_transformer (Callable[[], list]): A function that creates
             the metadata for requests.
          app_name (string): The codename of the calling service.
          app_version (string): The version of the calling service.

        Returns:
          A SpeechApi object.
        """
        if scopes is None:
            scopes = self._ALL_SCOPES
        if client_config is None:
            client_config = {}
        goog_api_client = '{}/{} {} gax/{} python/{}'.format(
            app_name, app_version, self._CODE_GEN_NAME_VERSION,
            self._GAX_VERSION, platform.python_version())
        metadata = [('x-goog-api-client', goog_api_client)]
        default_client_config = json.loads(
            pkg_resources.resource_string(
                __name__, 'speech_client_config.json').decode())
        defaults = api_callable.construct_settings(
            'google.cloud.speech.v1.Speech',
            default_client_config,
            client_config,
            config.STATUS_CODE_NAMES,
            kwargs={'metadata': metadata})
        self.stub = config.create_stub(
            cloud_speech_pb2.beta_create_Speech_stub,
            service_path,
            port,
            ssl_creds=ssl_creds,
            channel=channel,
            metadata_transformer=metadata_transformer,
            scopes=scopes)
        self._non_streaming_recognize = api_callable.create_api_call(
            self.stub.NonStreamingRecognize,
            settings=defaults['non_streaming_recognize'])

    # Service calls
    def non_streaming_recognize(self,
                                initial_request,
                                audio_request,
                                options=None):
        """
        Perform non-streaming speech-recognition: receive results after all audio
        has been sent and processed.

        Example:
          >>> from google.cloud.speech.v1.speech_api import SpeechApi
          >>> from google.cloud.speech.v1 import cloud_speech_pb2
          >>> api = SpeechApi()
          >>> initial_request = cloud_speech_pb2.InitialRecognizeRequest()
          >>> audio_request = cloud_speech_pb2.AudioRequest()
          >>> response = api.non_streaming_recognize(initial_request, audio_request)

        Args:
          initial_request (:class:`google.cloud.speech.v1.cloud_speech_pb2.InitialRecognizeRequest`): The ``initial_request`` message provides information to the recognizer
            that specifies how to process the request.

            The first ``RecognizeRequest`` message must contain an ``initial_request``.
            Any subsequent ``RecognizeRequest`` messages must not contain an
            ``initial_request``.
          audio_request (:class:`google.cloud.speech.v1.cloud_speech_pb2.AudioRequest`): The audio data to be recognized. For REST or ``NonStreamingRecognize``, all
            audio data must be contained in the first (and only) ``RecognizeRequest``
            message. For gRPC streaming ``Recognize``, sequential chunks of audio data
            are sent in sequential ``RecognizeRequest`` messages.
          options (:class:`google.gax.CallOptions`): Overrides the default
            settings for this call, e.g, timeout, retries etc.

        Returns:
          A :class:`google.cloud.speech.v1.cloud_speech_pb2.NonStreamingRecognizeResponse` instance.

        Raises:
          :exc:`google.gax.errors.GaxError` if the RPC is aborted.
        """
        request = cloud_speech_pb2.RecognizeRequest(
            initial_request=initial_request, audio_request=audio_request)
        return self._non_streaming_recognize(request, options)
