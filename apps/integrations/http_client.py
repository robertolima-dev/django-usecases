import json
import logging
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from apps.integrations.models import HttpCallLog

logger = logging.getLogger(__name__)


class HTTPClient:
    def __init__(self, retries=3, backoff_factor=1, timeout=10):
        self.timeout = timeout
        self.session = requests.Session()

        retry_strategy = Retry(
            total=retries,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT"],
            backoff_factor=backoff_factor,
            raise_on_status=False
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def request(self, method, url, **kwargs):
        start = time.time()
        try:
            response = self.session.request(method=method, url=url, timeout=self.timeout, **kwargs)  # noqa: E501
            HttpCallLog.objects.create(
                url=url,
                method=method.upper(),
                status_code=response.status_code,
                request_type='success',
                response_time=time.time() - start,
                response_body=response.text,
                error_message=None,
            )
            return {"type": "success", "duration": time.time() - start}
        except requests.RequestException as e:
            HttpCallLog.objects.create(
                url=url,
                method=method.upper(),
                status_code=None,
                request_type='error',
                response_time=time.time() - start,
                response_body=None,
                error_message=str(e),
            )
            logger.error(f"Erro na requisição HTTP: {e}")
            return {"type": "error", "details": str(e), "duration": time.time() - start}  # noqa: E501

    def get(self, url, **kwargs):
        self.debug_logger("GET Request Kwargs", kwargs)
        return self.request("get", url, **kwargs)

    def post(self, url, **kwargs):
        self.debug_logger("POST Request Kwargs", kwargs)
        return self.request("post", url, **kwargs)

    def put(self, url, **kwargs):
        self.debug_logger("PUT Request Kwargs", kwargs)
        return self.request("put", url, **kwargs)

    def debug_logger(self, title: str, data: dict):
        formatted_data = json.dumps(data, indent=2, ensure_ascii=False)
        logger.debug(f"\n📘 {title}:\n{formatted_data}")
