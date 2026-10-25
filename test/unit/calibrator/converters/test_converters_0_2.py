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

"""Tests the converters for calibrator jobs."""

import datetime

from ibm_quantum_schemas.calibrator.version_0_2_dev import CalibratorResultModel

from qiskit_ibm_runtime.calibrator.converters import (
    calibrator_program_from_0_2,
    calibrator_program_to_0_2,
)
from qiskit_ibm_runtime.decoders.calibrator.converters import calibrator_result_from_0_2
from qiskit_ibm_runtime.options_models.calibrator import (
    CalibratorOptions,
    OneAndTwoQubitOptions,
    ReadoutAngleOptions,
    TlsBiasOptions,
    TwoQubitFractionalOptions,
    TwoQubitOptions,
)


class TestCalibratorConverters:
    """Tests the converters for calibrator jobs."""

    def test_calibrator_program_to_from__0_2_default(self) -> None:
        """Test the function ``calibrator_program_to/from_0_2`` with default options."""
        options = CalibratorOptions()
        params_model = calibrator_program_to_0_2(options)

        assert params_model.schema_version == "v0.2"
        assert params_model.options.readout_angle.enable is True
        assert params_model.options.one_and_two_qubit.enable is False
        assert params_model.options.two_qubit.enable is False
        assert params_model.options.two_qubit_fractional.enable is False
        assert params_model.options.tls_bias.enable is False
        assert params_model.options.experimental == {}

        new_options = calibrator_program_from_0_2(params_model)
        assert new_options == options

    def test_calibrator_program_to_from__0_2_custom(self) -> None:
        """Test the function ``calibrator_program_to/from_0_2`` with custom options."""
        options = CalibratorOptions(
            readout_angle=ReadoutAngleOptions(enable=False),
            one_and_two_qubit=OneAndTwoQubitOptions(enable=True),
            two_qubit=TwoQubitOptions(enable=True),
            two_qubit_fractional=TwoQubitFractionalOptions(enable=True),
            tls_bias=TlsBiasOptions(enable=True),
            experimental={"custom_param": 42, "flag": True},
        )
        params_model = calibrator_program_to_0_2(options)

        assert params_model.schema_version == "v0.2"
        assert params_model.options.readout_angle.enable is False
        assert params_model.options.one_and_two_qubit.enable is True
        assert params_model.options.two_qubit.enable is True
        assert params_model.options.two_qubit_fractional.enable is True
        assert params_model.options.tls_bias.enable is True
        assert params_model.options.experimental == {"custom_param": 42, "flag": True}

        new_options = calibrator_program_from_0_2(params_model)
        assert new_options == options

    def test_calibrator_result_from_0_2(self) -> None:
        """Test the function ``calibrator_result_from_0_2``."""
        start = datetime.datetime.now()
        stop = start + datetime.timedelta(seconds=10)
        result_model = CalibratorResultModel(start=start, stop=stop)
        result = calibrator_result_from_0_2(result_model)
        assert result.start == start
        assert result.stop == stop
