import os
from pyats_client import ApiClient, Configuration
from pyats_client.api.default_api import DefaultApi


PYATS_SERVER = os.environ.get("PYATS_API_SERVER")

configuration = Configuration(host=PYATS_SERVER)


def get_devices_list():
    """
    Retrieves a list of existing devices.

    Returns:
        list: A list of device names.
    """
    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        return api_instance.get_devices_list()
