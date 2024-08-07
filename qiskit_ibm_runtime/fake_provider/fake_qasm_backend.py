# This code is part of Qiskit.
#
# (C) Copyright IBM 2020, 2023.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Fake backend abstract class for mock backends.
"""

import json
import os

from qiskit.exceptions import QiskitError
from qiskit.providers.fake_provider.utils.json_decoder import (
    decode_backend_configuration,
    decode_backend_properties,
)
from .fake_backend import FakeBackend
from ..models import BackendProperties, QasmBackendConfiguration


class FakeQasmBackend(FakeBackend):
    """A fake OpenQASM backend."""

    dirname = None
    conf_filename = None
    props_filename = None
    backend_name = None

    def __init__(self):  # type: ignore
        configuration = self._get_conf_from_json()
        self._defaults = None
        self._properties = None
        super().__init__(configuration)

    def properties(self) -> BackendProperties:
        """Returns a snapshot of device properties"""
        if not self._properties:
            self._set_props_from_json()
        return self._properties

    def _get_conf_from_json(self) -> QasmBackendConfiguration:
        if not self.conf_filename:
            raise QiskitError("No configuration file has been defined")
        conf = self._load_json(self.conf_filename)  # type: ignore
        decode_backend_configuration(conf)
        configuration = self._get_config_from_dict(conf)
        configuration.backend_name = self.backend_name
        return configuration

    def _set_props_from_json(self) -> None:
        if not self.props_filename:
            raise QiskitError("No properties file has been defined")
        props = self._load_json(self.props_filename)  # type: ignore
        decode_backend_properties(props)
        self._properties = BackendProperties.from_dict(props)

    def _load_json(self, filename: str) -> dict:
        with open(  # pylint: disable=unspecified-encoding
            os.path.join(self.dirname, filename)
        ) as f_json:
            the_json = json.load(f_json)
        return the_json

    def _get_config_from_dict(self, conf: dict) -> QasmBackendConfiguration:
        return QasmBackendConfiguration.from_dict(conf)
