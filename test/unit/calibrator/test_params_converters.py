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

"""Tests the param converters for the calibrator model."""

import pytest

from qiskit_ibm_runtime.calibrator.params_converters import CALIBRATOR_PARAMS_CONVERTERS
from qiskit_ibm_runtime.options_models.calibrator import (
    CalibratorOptions,
    OneAndTwoQubitOptions,
    ReadoutAngleOptions,
    TlsBiasOptions,
    TwoQubitFractionalOptions,
    TwoQubitOptions,
)


class TestParamsConverters:
    """Tests for ParamConverters."""

    @pytest.mark.parametrize("schema_version", [*list(CALIBRATOR_PARAMS_CONVERTERS)])
    def test_round_trip(self, schema_version: str) -> None:
        """Test a round trip with default options."""
        options = CalibratorOptions(experimental={"test_key": "test_val"})

        converters = CALIBRATOR_PARAMS_CONVERTERS[schema_version]
        encoded = converters.encoder(options).model_dump()
        decoded = converters.decoder(converters.model(**encoded))

        assert decoded.experimental == options.experimental
        if schema_version != "v0.1":
            assert decoded == options

    def test_round_trip_v0_2_custom(self) -> None:
        """Test round trip for v0.2 with non-default options."""
        options = CalibratorOptions(
            readout_angle=ReadoutAngleOptions(enable=False),
            one_and_two_qubit=OneAndTwoQubitOptions(enable=True),
            two_qubit=TwoQubitOptions(enable=True),
            two_qubit_fractional=TwoQubitFractionalOptions(enable=True),
            tls_bias=TlsBiasOptions(enable=True),
            experimental={"custom": 123},
        )
        converters = CALIBRATOR_PARAMS_CONVERTERS["v0.2"]
        encoded = converters.encoder(options).model_dump()
        decoded = converters.decoder(converters.model(**encoded))

        assert decoded == options
