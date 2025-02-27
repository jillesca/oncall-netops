import os
from pyats_client import ApiClient, Configuration
from pyats_client.api.default_api import DefaultApi


PYATS_SERVER = os.environ.get("PYATS_API_SERVER")

configuration = Configuration(host=PYATS_SERVER)


def get_interfaces_status(device_name: str):
    """
    Get the status of all interfaces on a device.

    Args:
        device_name (str): This parameter must come from the get_devices_list function.

    Returns:
        dict: A dictionary containing the status of the interfaces on the device.
    """
    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        return api_instance.get_interfaces_status(device_name=device_name)


def get_interface_running_config(device_name: str, interface_name: str):
    """
    Get the running config of a single interface on a device.

    Args:
        device_name (str): This parameter must come from the get_devices_list function.
        interface_name (str): The name of the interface.

    Returns:
        dict: The running configuration of the specified interface.
    """
    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        return api_instance.get_interface_running_config(
            device_name=device_name, interface_name=interface_name
        )


def get_interfaces_status_and_description(device_name: str):
    """
    Get the status and description of the interfaces per device.

    Args:
        device_name (str): This parameter must come from the get_devices_list function.

    Returns:
        dict: A dictionary containing the status, protocol, and description of the interfaces.
    """
    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        return api_instance.get_interfaces_status_and_description(
            device_name=device_name
        )


def get_interface_detailed_status(device_name: str, interface_name: str):
    """
    Get detailed status information for a single interface.

    Including admin state, line protocol, operational status, bandwidth, duplex, speed and other interface-specific details.

    if not interface is found, the function returns "ERROR_INTERFACE_NOT_FOUND"

    Args:
        device_name (str): This parameter must come from the get_devices_list function.
        interface_name (str): The name of the interface.

    Returns:
        dict: A dictionary containing detailed status information for the interface.
    """
    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        return api_instance.get_interface_detailed_status(
            device_name=device_name, interface_name=interface_name
        )


def get_interface_information(device_name: str, interfaces_name: list):
    """
    Get interface information from device for a list of interfaces. Interfaces must be in a single list.

    Args:
      device_name (str): This parameter must come from the get_devices_list function.
      interfaces_name (list[str]): A list of interface names. This should be a single list of interface names, not multiple query parameters.

    Returns:
        list[dict]: A list of dictionaries containing interface information

    Example:
      Correct usage:
      GET /interface/information?device_name=cat8000v-0&interfaces_name=["GigabitEthernet0/0", "GigabitEthernet0/1", "GigabitEthernet0/2", "GigabitEthernet0/3"]

      Erroneous usage:
      GET /interface/information?device_name=cat8000v-0&interfaces_name=GigabitEthernet0/0&interfaces_name=GigabitEthernet0/1&interfaces_name=GigabitEthernet0/2&interfaces_name=GigabitEthernet0/3
    """
    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        return api_instance.get_interface_information(
            device_name=device_name, interfaces_name=interfaces_name
        )


def get_interface_admin_status(device_name: str, interface_name: str):
    """
    Get the administrative status of a single interface on a device.

    Args:
        device_name (str): This parameter must come from the get_devices_list function.
        interface_name (str): The name of the interface.

    Returns:
        str: The administrative status of the interface.
    """
    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        return api_instance.get_interface_admin_status(
            device_name=device_name, interface_name=interface_name
        )


def verify_interface_state_up(device_name: str, interface_name: str):
    """
    Verify interface state is up and line protocol is up.

    Args:
        device_name (str): This parameter must come from the get_devices_list function.
        interface_name (str): The name of the interface

    Returns:
        bool: True if the interface state is up and line protocol is up, False otherwise
    """
    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        return api_instance.verify_interface_state_up(
            device_name=device_name, interface_name=interface_name
        )


def get_interface_events(device_name: str, interface_name: str):
    """
    Retrieves the events for single interface on a device. Multiple interfaces are not supported. Split the request for multiple interfaces into multiple requests.

    Args:
        device_name (str): This parameter must come from the get_devices_list function.
        interface_name (str): The name of the interface.

    Returns:
        dict: A dictionary containing the events for the specified interface.
    """
    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        return api_instance.get_interface_events(
            device_name=device_name, interface_name=interface_name
        )
