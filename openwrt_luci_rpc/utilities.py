from .constants import OpenWrtConstants
import logging

log = logging.getLogger(__name__)


def normalise_keys(result):
    """Replace 17.06 keys with newer ones."""

    # named tuple keys cannot have spaces or begin with dots. Replace
    # those with underscores
    result = \
        {k.replace(".", "_").replace(" ", "_"): v for k, v in result.items()}

    for old_key, new_key in OpenWrtConstants.MODERN_KEYS.items():
        if old_key in result:
            result[new_key] = result[old_key]
            del result[old_key]

    return result


def get_hostname_from_dhcp(dhcp_result, mac):
    """Determine the hostname for this mac."""
    if dhcp_result:

        host = [x for x in dhcp_result.values()
                if x['.type'] == 'host'
                and 'mac' in x
                and 'name' in x
                and x['mac'].upper() == mac]

        if host:
            log.debug("DNS name lookup for mac {} "
                      "found {}".format(mac, host[0]['name']))
            return host[0]['name']

    return None