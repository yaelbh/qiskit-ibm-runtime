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

"""Transport conversion functions."""

from __future__ import annotations

from ibm_quantum_schemas.calibrator.version_0_2_dev import (
    OneAndTwoQubitOptions as SchemaOneAndTwoQubitOptions,
    OptionsModel,
    ParamsModel,
    ReadoutAngleOptions as SchemaReadoutAngleOptions,
    TlsBiasOptions as SchemaTlsBiasOptions,
    TwoQubitFractionalOptions as SchemaTwoQubitFractionalOptions,
    TwoQubitOptions as SchemaTwoQubitOptions,
)

from ...options_models.calibrator import (
    CalibratorOptions,
    OneAndTwoQubitOptions,
    ReadoutAngleOptions,
    TlsBiasOptions,
    TwoQubitFractionalOptions,
    TwoQubitOptions,
)


def calibrator_program_from_0_2(model: ParamsModel) -> CalibratorOptions:
    """Convert a V0.2 model to the inputs of a calibrator program."""
    options = CalibratorOptions(
        readout_angle=ReadoutAngleOptions(enable=model.options.readout_angle.enable),
        one_and_two_qubit=OneAndTwoQubitOptions(enable=model.options.one_and_two_qubit.enable),
        two_qubit=TwoQubitOptions(enable=model.options.two_qubit.enable),
        two_qubit_fractional=TwoQubitFractionalOptions(
            enable=model.options.two_qubit_fractional.enable
        ),
        tls_bias=TlsBiasOptions(enable=model.options.tls_bias.enable),
        experimental=model.options.experimental,
    )
    return options


def calibrator_program_to_0_2(options: CalibratorOptions) -> ParamsModel:
    """Convert the inputs of a calibrator program to a V0.2 model."""
    return ParamsModel(
        options=OptionsModel(
            readout_angle=SchemaReadoutAngleOptions(enable=options.readout_angle.enable),
            one_and_two_qubit=SchemaOneAndTwoQubitOptions(enable=options.one_and_two_qubit.enable),
            two_qubit=SchemaTwoQubitOptions(enable=options.two_qubit.enable),
            two_qubit_fractional=SchemaTwoQubitFractionalOptions(
                enable=options.two_qubit_fractional.enable
            ),
            tls_bias=SchemaTlsBiasOptions(enable=options.tls_bias.enable),
            experimental=options.experimental,
        )
    )
