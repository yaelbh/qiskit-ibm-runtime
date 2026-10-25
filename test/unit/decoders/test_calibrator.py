# This code is part of Qiskit.
#
# (C) Copyright IBM 2026.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Tests the decoder for the calibrator result model."""

import datetime
import json

import pytest

from qiskit_ibm_runtime.decoders.calibrator.decoder import CalibratorResultDecoder
from qiskit_ibm_runtime.results import CalibratorResult


class TestCalibratorResultDecoder:
    """Tests the decoder for the calibrator model."""

    @pytest.mark.parametrize("schema_version", ["v0.1", "v0.2"])
    def test_decoder(self, schema_version: str) -> None:
        """Tests the decoder for supported schema versions."""
        start = datetime.datetime.now(datetime.timezone.utc)
        stop = start + datetime.timedelta(seconds=10)
        raw_result = json.dumps(
            {
                "schema_version": schema_version,
                "start": start.isoformat(),
                "stop": stop.isoformat(),
            }
        )

        decoded = CalibratorResultDecoder.decode(raw_result)
        assert isinstance(decoded, CalibratorResult)
        assert decoded.start == start
        assert decoded.stop == stop

    def test_no_schema_version(self) -> None:
        """Verify an error is raised if the encoded string does not specify any schema version."""
        start = datetime.datetime.now(datetime.timezone.utc)
        stop = start + datetime.timedelta(seconds=10)
        raw_result = json.dumps(
            {
                "start": start.isoformat(),
                "stop": stop.isoformat(),
            }
        )
        with pytest.raises(ValueError, match="Missing schema version."):
            CalibratorResultDecoder.decode(raw_result)

    def test_unknown_schema_version(self) -> None:
        """Verify an error is raised if the schema version specified does not exist."""
        start = datetime.datetime.now(datetime.timezone.utc)
        stop = start + datetime.timedelta(seconds=10)
        raw_result = json.dumps(
            {
                "schema_version": "v999.0",
                "start": start.isoformat(),
                "stop": stop.isoformat(),
            }
        )
        with pytest.raises(ValueError, match="No decoder found for schema version v999.0."):
            CalibratorResultDecoder.decode(raw_result)
