import os
from pyats_client import ApiClient, Configuration
from pyats_client.api.default_api import DefaultApi

PYATS_SERVER = os.environ.get("PYATS_API_SERVER")

configuration = Configuration(host=PYATS_SERVER)


def get_isis_interface_information(device_name: str):
    """
    Retrieves a list of ISIS interfaces for a given device and VRF.

    Args:
        device_name (str): This parameter must come from the get_devices_list function.

    Returns:
        list: A list of ISIS interfaces.
    """
    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        return api_instance.get_isis_interface_information(
            device_name=device_name
        )


def get_isis_neighbors(device_name: str):
    """
    Retrieves the ISIS neighbors for a given device. Neighbors down are not included.

    Args:
        device_name (str): This parameter must come from the get_devices_list function.

    Returns:
        dict: A dictionary containing the ISIS neighbors information.
    """
    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        return api_instance.get_isis_neighbors(device_name=device_name)


def get_isis_interface_events(device_name: str):
    """
    Retrieves ISIS interface events for a given device.

    Args:
        device_name (str): This parameter must come from the get_devices_list function.

    Returns:
        dict: A dictionary containing the ISIS interface events.
    """
    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        return api_instance.get_isis_interface_events(device_name=device_name)
