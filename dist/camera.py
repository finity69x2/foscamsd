"""
This component provides basic support for Foscam (SD) IP cameras.
NOTE: This is just a small adaptation of the 'official' foscam component,
      in order to support SD (old) versions.
INSTALL:
1. Create the file <config dir>/custom_components/camera/foscamsd.py and copy
the code below to there.
2. In your <config dir>/configuration.yaml enter:
camera:
  platform: foscamsd
  ip: IP_ADDRESS
  username: USERNAME
  password: PASSWORD
CONFIGURATION VARIABLES:
-----------------------
ip
(string)(Required) The IP address your camera.
port
(integer)(Optional) The port that the camera is running on.
Default value: 88
username
(string)(Required) The username for accessing your camera.
password
(string)(Required) The password for accessing your camera.
name
(string)(Optional) This parameter allows you to override the name of your camera.
"""
import logging

import requests
import voluptuous as vol

from homeassistant.components.camera import (Camera, PLATFORM_SCHEMA)
from homeassistant.const import (
    CONF_NAME, CONF_USERNAME, CONF_PASSWORD, CONF_PORT)
from homeassistant.helpers import config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_IP = 'ip'

DEFAULT_NAME = 'Foscam Camera (SD)'
DEFAULT_PORT = 88

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_IP): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
})


# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup a Foscam IP Camera (SD)."""
    add_devices([FoscamSDCamera(config)])


class FoscamSDCamera(Camera):
    """An implementation of a Foscam IP camera (SD)."""

    def __init__(self, device_info):
        """Initialize a Foscam camera."""
        super(FoscamSDCamera, self).__init__()
            
        ip_address = device_info.get(CONF_IP)
        port = device_info.get(CONF_PORT)
        self._base_url = 'http://{}:{}/'.format(ip_address, port)
      
        uri_template = self._base_url \
            + 'snapshot.cgi?user={}&pwd={}'
        self._username = device_info.get(CONF_USERNAME)
        self._password = device_info.get(CONF_PASSWORD)
        self._snap_picture_url = uri_template.format(
            self._username,
            self._password
        )
      
        self._name = device_info.get(CONF_NAME)
            
        _LOGGER.info('Using the following URL for %s: %s',
                     self._name, uri_template.format('***', '***'))

    def camera_image(self):
        """Return a still image reponse from the camera."""
        # Send the request to snap a picture and return raw jpg data
        try:
            response = requests.get(self._snap_picture_url, timeout=10)
        except requests.exceptions.ConnectionError:
            return None
        else:
            return response.content

    @property
    def name(self):
        """Return the name of this camera."""
        return self._name
