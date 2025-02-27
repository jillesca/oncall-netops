import os
from pyats_client import ApiClient, Configuration
from pyats_client.api.default_api import DefaultApi


PYATS_SERVER = os.environ.get("PYATS_API_SERVER")

configuration = Configuration(host=PYATS_SERVER)


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


def get_vrf_present(device_name: str):
    """
    Get all vrfs from device.

    Args:
        device_name (str): This parameter must come from the get_devices_list function.

    Returns:
        list: List of vrfs present on the device. If no vrfs are found, returns ["NO_VRFs_FOUND"].
    """
    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        return api_instance.get_vrf_present(device_name=device_name)


def get_interfaces_under_vrf(device_name: str, vrf_name: str = None):
    """
    Get interfaces configured under specific Vrf.

    Args:
        device_name (str): This parameter must come from the get_devices_list function.
        vrf_name (str, optional): Name of the VRF. Defaults to None.

    Returns:
        list: List of interfaces configured under the specified VRF
    """
    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        return api_instance.get_interfaces_under_vrf(
            device_name=device_name, vrf_name=vrf_name
        )


def get_routing_routes(
    device_name: str,
    vrf_name: str = None,
    address_family: str = "ipv4",
):
    """
    Execute 'show ip route vrf <vrf>' and retrieve the routes.

    Args:
        device_name (str): This parameter must come from the get_devices_list function.
        vrf_name (str, optional): The name of the VRF. Defaults to None.
        address_family (str, optional): The address family name. Defaults to "ipv4".

    TODO: Need to reduce the amount of information returned

    Returns:
        dict: A dictionary containing the received routes.
    """
    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        return api_instance.get_routing_routes(
            device_name=device_name,
            vrf_name=vrf_name,
            address_family=address_family,
        )
