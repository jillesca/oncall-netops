import os
from pyats_client import ApiClient, Configuration
from pyats_client.api.default_api import DefaultApi


PYATS_SERVER = os.environ.get("PYATS_API_SERVER")

configuration = Configuration(host=PYATS_SERVER)


def shut_interface(device_name: str, interface_name: str):
    """
    Shut down an interface on a device.

    Args:
        device_name (str): This parameter must come from the get_devices_list function.
        interface_name (str): The name of the interface to shut down.

    Returns:
        dict: A dictionary containing the result of the operation.
    """
    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        return api_instance.shut_interface(
            device_name=device_name, interface_name=interface_name
        )


def unshut_interface(device_name: str, interface_name: str):
    """
    Unshut an interface on a device.

    Args:
        device_name (str): This parameter must come from the get_devices_list function.
        interface_name (str): The name of the interface to be unshut.

    Returns:
        dict: A dictionary containing the result of the operation.
    """
    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        return api_instance.unshut_interface(
            device_name=device_name, interface_name=interface_name
        )
