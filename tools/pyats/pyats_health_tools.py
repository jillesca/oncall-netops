import os
from pyats_client import ApiClient, Configuration
from pyats_client.api.default_api import DefaultApi


PYATS_SERVER = os.environ.get("PYATS_API_SERVER")

configuration = Configuration(host=PYATS_SERVER)


def get_health_memory(device_name: str):
    """
    Retrieves the memory health information for a given device.

    Args:
        device_name (str): This parameter must come from the get_devices_list function.

    If no memory health issues are detected, the function returns 'No memory health issues detected on the device'.

    Returns:
        dict: A dictionary containing the memory health information.
    """
    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        return api_instance.get_health_memory(device_name=device_name)


def get_health_cpu(device_name: str):
    """
    Retrieves the CPU health information for a given device.

    Args:
        device_name (str): This parameter must come from the get_devices_list function.

    If no CPU health issues are detected, the function returns 'No CPU health issues detected on the device'.

    Returns:
        dict: A dictionary containing the CPU health information.
    """
    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        return api_instance.get_health_cpu(device_name=device_name)


def get_health_logging(device_name: str, keywords: list = None):
    """
    Retrieves health logging information from a device.

    Args:
        device_name (str): This parameter must come from the get_devices_list function.
        keywords (list[str], optional): List of keywords to filter the health logging information.
            Defaults to traceback, error, down and adjchange.

    If no issues are detected, the function returns 'No issues detected on the logs of the device'.

    Returns:
        dict: The health logging information in JSON format.
    """
    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        return api_instance.get_health_logging(
            device_name=device_name, keywords=keywords
        )
