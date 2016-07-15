import logging
import os
from request_factory import http_request_factory
import time

logger = logging.getLogger(__name__)


class QuayError(Exception):
    """Quay Exception from the QuayClient"""


class QuayClient(object):
    """Quay API client"""

    def __init__(self, **kwargs):
        """Quay client constructor

            Keyword Args:
                token (str): this is the quay token it can provide from environment variable or the kwargs
                host (str): this is the quay host it can provide from environment variable or the kwargs
                namespace (str): this is the quay namespace it can provide from environment variable or the kwargs
        """
        self.host = os.getenv("QUAY_HOST", kwargs.get("host", "quay.io"))
        self.token = os.getenv("QUAY_TOKEN", kwargs.get("token", None))
        self.headers = {"Authorization": "Bearer {}".format(self.token)}
        self.namespace = os.getenv('QUAY_NAMESPACE', kwargs.get("namespace", None))

    @staticmethod
    def _params_filter(params, filter_on=[None]):
        return {key: value for key, value in params.iteritems() if value not in filter_on}

    def get_repositories(self, **kwargs):
        """Fetch the list of repositories

        Keyword Args:
                next_page (string): The page token for the next page
                popularity (bool): Whether to include the repository's popularity metric.
                last_modified (bool): Whether to include when the repository was last modified.
                public (bool): Adds any repositories visible to the user by virtue of being public
                starred (bool): Filters the repositories returned to those starred by the user
                namespace (str): Filters the repositories returned to this namespace

        Returns:
            list of dict: List of repositories or None
        """
        endpoint = "/api/v1/repository"
        params = QuayClient._params_filter({
            "next_page": kwargs.get("next_page", None),
            "popularity": kwargs.get("popularity", None),
            "last_modified": kwargs.get("last_modified", None),
            "public": kwargs.get("public", None),
            "starred": kwargs.get("starred", None),
            "namespace": kwargs.get("namespace", None)
        })

        repositories_response = http_request_factory(self.host, "GET", endpoint, headers=self.headers, params=params)

        if repositories_response:
            repositories = repositories_response["repositories"]
            return repositories
        else:
            return None

    def get_tags(self, artifact, **kwargs):
        """Fetch x latest tag for a given repository

        Args:
            artifact (str): Name of the artifact

        Keyword Args:
            kwargs (dict):
                page (int): Page index for the results.
                limit (int): Maximum number of tags. Default value 10. Limited to 100.
                specific_tag (str): Query a specific tag name. Defaults to None

        Returns:
            list of dict: Tag list or None if the repository was not found
        """
        repository = "{}/{}".format(self.namespace, artifact)
        endpoint = "/api/v1/repository/{repository}/tag/".format(repository=repository)

        page = int(kwargs.get("page", 1))
        limit = int(kwargs.get("limit", 10))

        params = QuayClient._params_filter({
            "page": page,
            "limit": limit,
            "specificTag": kwargs.get("specific_tag", None),
        })

        if limit > 100:
            cycle = limit / 100
            rest = limit % 100
            latest_tags = list()

            logger.info("The limit is over 100, the request will take more time")

            params["limit"] = 100
            for _ in xrange(1, cycle + 1):
                history_response = http_request_factory(self.host, "GET", endpoint, headers=self.headers, params=params)
                latest_tags.extend([tag["name"] for tag in history_response["tags"]])
                params["page"] += 1

            if rest > 0:
                params["page"] += 1
                params["limit"] = rest
                history_response = http_request_factory(self.host, "GET", endpoint, headers=self.headers, params=params)
                latest_tags.extend([tag["name"] for tag in history_response["tags"]])

            return latest_tags

        else:
            history_response = http_request_factory(self.host, "GET", endpoint, headers=self.headers, params=params)

            return history_response["tags"] if history_response else None

    def set_tag(self, artifact, tag, image_id):
        """Change which image a tag points to or create a new tag.

        Args:
            artifact (str): Name of the artifact
            tag (str): The name of the tag
            image_id (str): Image identifier to which the tag should point

        """
        repository = "{}/{}".format(self.namespace, artifact)
        endpoint = "/api/v1/repository/{repository}/tag/{tag}".format(repository=repository, tag=tag)
        body = {"image": image_id}

        set_response = http_request_factory(self.host, "PUT", endpoint, headers=self.headers, body=body)

        return set_response

    def revert_tag(self, artifact, tag, image_id):
        """Change which image a tag point to but do not create a new tag.

        Args:
            artifact (str): Name of the artifact
            tag (str): The name of the tag
            image_id (str): Image identifier to which the tag should point

        """
        repository = "{}/{}".format(self.namespace, artifact)
        endpoint = "/api/v1/repository/{repository}/tag/{tag}/revert".format(repository=repository, tag=tag)
        payload = {"image": image_id}

        http_request_factory(self.host, "POST", endpoint, headers=self.headers, body=payload)

    def delete_tag(self, artifact, tag):
        """Change which image a tag points to or create a new tag.

        Args:
            artifact (str): Name of the artifact
            tag (str): The name of the tag

        """
        repository = "{}/{}".format(self.namespace, artifact)
        endpoint = "/api/v1/repository/{repository}/tag/{tag}".format(repository=repository, tag=tag)

        set_response = http_request_factory(self.host, "DELETE", endpoint, headers=self.headers)

        return set_response

    def set_tag_on_existing(self, artifact, new_tag, existing_tag):
        """Set or create a tag on the latest tag

        Args:
            artifact (str): Name of the artifact
            new_tag (str): Tag to set
            existing_tag (str): Existing tag ``new_tag`` must be set to
        """
        repository = "{}/{}".format(self.namespace, artifact)
        latest_tags = self.get_tags(artifact, limit=1, specific_tag=existing_tag)

        if not latest_tags:
            raise QuayError("The repository: {} hasn't tag: {}".format(repository, existing_tag))

        return self.set_tag(artifact, new_tag, latest_tags[0]["docker_image_id"])

    def find_trigger(self, artifact, service="github"):
        """Find the trigger for an artifact given a service.

        Args:
            artifact (str): Name of the artifact
            service (str): Service the trigger should correspond to. Defaults to "github".

        Returns:
            str: trigger uuid. Otherwise None

        """
        repository = "{}/{}".format(self.namespace, artifact)

        endpoint = "/api/v1/repository/{repository}/trigger/".format(repository=repository)

        list_triggers = http_request_factory(self.host, "GET", endpoint, headers=self.headers)

        for trigger in list_triggers["triggers"]:
            if trigger["service"] == service:
                return trigger["id"]

        return None

    def start_build_trigger(self, artifact, branch_name, trigger_id):
        """Start the build from a trigger

        Args:
            artifact (str): Name of the artifact
            branch_name (str): Name of the branch
            trigger_id (str): Trigger uuid

        Returns
            str: build_uuid

        """
        body = {"branch_name": branch_name}
        repository = "{}/{}".format(self.namespace, artifact)
        endpoint = "/api/v1/repository/{}/trigger/{}/start".format(repository,
                                                                   trigger_id)

        build_response = http_request_factory(self.host, "POST", endpoint, headers=self.headers, body=body)
        build_uuid = build_response["id"]
        logger.info("Build: https://{}/repository/{}/build/{}".format(self.host, repository, build_uuid))
        return build_uuid

    def start_build_url(self, artifact, branch_name, url, **kwargs):
        """Start the build from an URL

        Args:
            artifact (str): Name of the artifact
            branch_name (str): Name of the branch
            url (str): URL to the compressed artifact

        Keyword Args:
            robot_name (str): This is the quay robot name to use

        Returns:
            str: build_uuid
        """

        robot_name = os.getenv("QUAY_ROBOT_NAME", kwargs.get("robot_name", None))

        if robot_name is None:
            raise QuayError("robot_name must be set from environment variable QUAY_ROBOT_NAME or via a kwargs")

        body = {
            "docker_tags": [branch_name],
            "pull_robot": robot_name,
            "archive_url": url
        }
        repository = "{}/{}".format(self.namespace, artifact)
        endpoint = "/api/v1/repository/{repository}/build/".format(repository=repository)

        start_build = http_request_factory(self.host, "POST", endpoint, headers=self.headers, body=body)
        build_uuid = start_build["id"]
        logger.info("Build: https://{}/repository/{}/build/{}".format(self.host, repository, build_uuid))
        return build_uuid

    def get_build_status(self, artifact, build_uuid):
        """Get the status of a build

        Args:
            artifact (str): Name of the artifact
            build_uuid (str): ID of the build to fetch

        Raises:
            QuayError: general error

        Returns:
            dict: Build status dictionary
        """
        repository = "{}/{}".format(self.namespace, artifact)
        endpoint = "/api/v1/repository/{}/build/{}/status".format(repository, build_uuid)
        build_status = http_request_factory(self.host, "GET", endpoint, headers=self.headers)
        return build_status

    def wait_build_complete(self, artifact, build_uuid, build_timeout=30 * 60, refresh_interval=5):
        """Wait for the build to complete

        Args:
            artifact (str): Name of the artifact
            build_uuid (str): ID of the build to fetch
            build_timeout (int): The timeout of the build in seconds (default: 30 minutes).
            refresh_interval (int): The time between API calls in seconds (default: 5 seconds).

        Raises:
            QuayError: general error

        Returns:
            float: build time

        """
        repository = "{}/{}".format(self.namespace, artifact)

        start_time = time.time()
        current_phase = "start"

        while True:
            build_status = self.get_build_status(artifact, build_uuid)

            if build_status["phase"] == "complete":
                return time.time() - start_time

            if build_status["phase"] == "error":
                raise QuayError("Build failed: https://{}/repository/{}/build/{}".format(self.host,
                                                                                         repository,
                                                                                         build_uuid))

            if build_status["phase"] != current_phase:
                start_time = time.time()
                current_phase = build_status["phase"]
                logger.info("Build status: {0}".format(current_phase))

            # Avoid lock if there"s a problem from quay.io
            build_current_time = time.time() - start_time
            if build_current_time > build_timeout:
                raise QuayError("Build timeout")

            time.sleep(refresh_interval)

    def get_security_scan(self, artifact, image_id, information_vulnerabilities=True):
        """Get the security scan for a specific image

        Args:
            artifact (str): Name of the artifact
            image_id (str): id of the image for fetching the good security scan
            information_vulnerabilities (bool): include or not vulnerabilities informations

        Raises:
            HTTPErrorCode: Common http error

        Returns:
            The security scan payload (dict)
        """
        repository = "{}/{}".format(self.namespace, artifact)
        endpoint = "/api/v1/repository/{}/image/{}/security".format(repository, image_id)

        params = {"vulnarabilities": information_vulnerabilities}

        return http_request_factory(self.host, "GET", endpoint, headers=self.headers, params=params)

    def wait_security_scan_complete(self, artifact, image_id,
                                    information_vulnerabilities=True, scan_timeout=30 * 60, refresh_interval=5):
        """Get the security scan for a specific image

        Args:
            artifact (str): Name of the artifact
            image_id (str): id of the image for fetching the good security scan
            information_vulnerabilities (bool): include or not vulnerabilities informations
            scan_timeout (int): The timeout of the build in seconds (default: 30 minutes).
            refresh_interval (int): The time between API calls in seconds (default: 5 seconds).

        Raises:
            QuayError

        Returns:
            A dict with the security scan payload (dict) and the duration of the scan (float)
            example :
            {

            }
        """
        repository = "{}/{}".format(self.namespace, artifact)

        start_time = time.time()

        while True:
            scan_payload = self.get_security_scan(artifact,
                                                  image_id,
                                                  information_vulnerabilities=information_vulnerabilities)

            if scan_payload["status"] == "scanned":
                return {"duration": time.time() - start_time, "scan_result": scan_payload}

            scan_current_time = time.time() - start_time
            if scan_current_time > scan_timeout:
                raise QuayError("Scan timeout: https://{}/repository/{}/image/{}?tab=vulnerabilities"
                                .format(self.host, repository, image_id))

            time.sleep(refresh_interval)
