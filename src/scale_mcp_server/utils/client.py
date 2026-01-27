import httpx
from typing import Optional, Dict, Any
from pathlib import Path
from fastmcp.utilities.logging import get_logger
from scale_mcp_server.utils.read_config import read_config

logger = get_logger(__name__)


class StorageScaleAPIError(Exception):
    """Exception raised for Storage Scale API errors."""
    pass


class StorageScaleClient:
    """IBM Storage Scale REST API Client."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        verify_ssl: Optional[bool] = None,
        timeout: Optional[float] = None,
        api_version: Optional[str] = None,
    ):
        config_path = (
            Path(__file__).parent.parent.parent.parent / "config" / "scale_config.ini"
        )
        config = read_config(config_path=config_path)

        api_config = config.get("scale_api", {})
        hostname = api_config.get("hostname", "localhost")
        if api_version == "v2":
            port = api_config.get("v2_port", 443)
        else:
            port = api_config.get("v3_port", 46443)
        config_base_url = f"https://{hostname}:{port}"

        auth_config = config.get("authorization", "")
        config_username = auth_config.get("username", "")
        config_password = auth_config.get("password", "")

        # Override if provided via api
        self.base_url = (base_url or config_base_url).rstrip("/")
        self.username = username or config_username or "admin"
        self.password = password or config_password or ""
        verify = (
            verify_ssl
            if verify_ssl is not None
            else not auth_config.get("allow_insecure", False)
        )
        timeout_val = timeout or float(api_config.get("timeout", 5.0))

        self.session = httpx.AsyncClient(
            base_url=self.base_url,
            auth=(self.username, self.password),
            timeout=httpx.Timeout(timeout=timeout_val),
            verify=verify,
        )

        logger.debug(f"Initialized StorageScaleClient for {self.base_url}")

    async def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Execute GET request."""
        try:
            logger.debug(f"GET {endpoint}")
            response = await self.session.get(endpoint, **kwargs)
            response.raise_for_status()
            logger.debug(f"GET {endpoint} - Status: {response.status_code}")
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"GET {endpoint} failed: {e}")
            try:
                error_body = e.response.text
                logger.error(f"Response body: {error_body}")
            except Exception:
                pass
            raise StorageScaleAPIError(f"API request failed: {e}")
        except httpx.HTTPError as e:
            logger.error(f"GET {endpoint} failed: {e}")
            raise StorageScaleAPIError(f"API request failed: {e}")

    async def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Execute POST request."""
        try:
            logger.debug(f"POST {endpoint}")
            logger.debug(f"POST payload: {kwargs.get('json', {})}")
            response = await self.session.post(endpoint, **kwargs)
            response.raise_for_status()
            logger.debug(f"POST {endpoint} - Status: {response.status_code}")
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"POST {endpoint} failed: {e}")
            try:
                error_body = e.response.text
                logger.error(f"Response body: {error_body}")
            except Exception:
                pass
            raise StorageScaleAPIError(f"API request failed: {e}")
        except httpx.HTTPError as e:
            logger.error(f"POST {endpoint} failed: {e}")
            raise StorageScaleAPIError(f"API request failed: {e}")

    async def put(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Execute PUT request."""
        try:
            logger.debug(f"PUT {endpoint}")
            response = await self.session.put(endpoint, **kwargs)
            response.raise_for_status()
            logger.debug(f"PUT {endpoint} - Status: {response.status_code}")
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"PUT {endpoint} failed: {e}")
            try:
                error_body = e.response.text
                logger.error(f"Response body: {error_body}")
            except Exception:
                pass
            raise StorageScaleAPIError(f"API request failed: {e}")
        except httpx.HTTPError as e:
            logger.error(f"PUT {endpoint} failed: {e}")
            raise StorageScaleAPIError(f"API request failed: {e}")

    async def patch(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Execute PATCH request."""
        try:
            logger.debug(f"PATCH {endpoint}")
            response = await self.session.patch(endpoint, **kwargs)
            response.raise_for_status()
            logger.debug(f"PATCH {endpoint} - Status: {response.status_code}")
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"PATCH {endpoint} failed: {e}")
            try:
                error_body = e.response.text
                logger.error(f"Response body: {error_body}")
            except Exception:
                pass
            raise StorageScaleAPIError(f"API request failed: {e}")
        except httpx.HTTPError as e:
            logger.error(f"PATCH {endpoint} failed: {e}")
            raise StorageScaleAPIError(f"API request failed: {e}")

    async def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Execute DELETE request."""
        try:
            logger.debug(f"DELETE {endpoint}")
            response = await self.session.delete(endpoint, **kwargs)
            response.raise_for_status()
            logger.debug(f"DELETE {endpoint} - Status: {response.status_code}")
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"DELETE {endpoint} failed: {e}")
            try:
                error_body = e.response.text
                logger.error(f"Response body: {error_body}")
            except Exception:
                pass
            raise StorageScaleAPIError(f"API request failed: {e}")
        except httpx.HTTPError as e:
            logger.error(f"DELETE {endpoint} failed: {e}")
            raise StorageScaleAPIError(f"API request failed: {e}")

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.session.aclose()
