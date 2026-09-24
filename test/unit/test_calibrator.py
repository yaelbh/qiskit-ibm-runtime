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

"""Tests the `Calibrator` class."""

from unittest.mock import patch

from pydantic import ValidationError

from qiskit_ibm_runtime.batch import Batch
from qiskit_ibm_runtime.calibrator import Calibrator
from qiskit_ibm_runtime.options_models.calibrator import CalibratorOptions, ReadoutAngleOptions
from qiskit_ibm_runtime.options_models.environment import EnvironmentOptions
from qiskit_ibm_runtime.qiskit_runtime_service import QiskitRuntimeService
from qiskit_ibm_runtime.session import Session

from ..decorators import mock_responses
from ..ibm_test_case import IBMTestCase
from ..utils import get_mocked_backend, get_mocked_session


class TestCalibratorOptions(IBMTestCase):
    """Tests option setting on the ``Calibrator`` class."""

    def test_default_options(self):
        """Test that default options are set when none are provided."""
        calibrator = Calibrator(mode=get_mocked_backend())
        self.assertIsInstance(calibrator.options, CalibratorOptions)
        self.assertEqual(calibrator.options, CalibratorOptions())

    def test_options_from_instance(self):
        """Test constructing with a CalibratorOptions instance."""
        opts = CalibratorOptions(readout_angle=ReadoutAngleOptions(enable=False))
        calibrator = Calibrator(mode=get_mocked_backend(), options=opts)
        self.assertIs(calibrator.options, opts)
        self.assertFalse(calibrator.options.readout_angle.enable)

    def test_options_from_dict(self):
        """Test constructing with a nested dict."""
        opts_dict = {
            "readout_angle": {"enable": False},
            "environment": {"log_level": "DEBUG"},
        }
        calibrator = Calibrator(mode=get_mocked_backend(), options=opts_dict)
        self.assertFalse(calibrator.options.readout_angle.enable)
        self.assertEqual(calibrator.options.environment.log_level, "DEBUG")

    def test_options_from_partial_dict(self):
        """Test constructing with a nested dict when only specifying some of the options."""
        calibrator = Calibrator(
            mode=get_mocked_backend(), options={"readout_angle": {"enable": False}}
        )
        self.assertFalse(calibrator.options.readout_angle.enable)
        self.assertEqual(calibrator.options.environment, EnvironmentOptions())

    def test_options_constructor_invalid_type(self):
        """Test that an invalid options type raises TypeError."""
        with self.assertRaisesRegex(TypeError, "Expected CalibratorOptions or dict"):
            Calibrator(mode=get_mocked_backend(), options="invalid")

    def test_setter_with_instance(self):
        """Test setting options via the setter with a CalibratorOptions instance."""
        calibrator = Calibrator(mode=get_mocked_backend())
        new_opts = CalibratorOptions(readout_angle=ReadoutAngleOptions(enable=False))
        calibrator.options = new_opts
        self.assertIs(calibrator.options, new_opts)

    def test_setter_with_dict(self):
        """Test setting options via the setter with a dict."""
        calibrator = Calibrator(mode=get_mocked_backend())
        calibrator.options = {"readout_angle": {"enable": False}}
        self.assertIsInstance(calibrator.options, CalibratorOptions)
        self.assertFalse(calibrator.options.readout_angle.enable)

    def test_setter_invalid_type(self):
        """Test that setting options with an invalid type raises TypeError."""
        calibrator = Calibrator(mode=get_mocked_backend())
        with self.assertRaisesRegex(TypeError, "Expected CalibratorOptions or dict"):
            calibrator.options = 42

    def test_setter_replaces_options(self):
        """Test that the setter replaces (not updates) the options."""
        calibrator = Calibrator(
            mode=get_mocked_backend(), options={"environment": {"log_level": "DEBUG"}}
        )
        calibrator.options = {"readout_angle": {"enable": False}}
        # environment should be back to defaults since we replaced, not updated
        self.assertEqual(calibrator.options.environment.log_level, "WARNING")
        self.assertFalse(calibrator.options.readout_angle.enable)

    def test_experimental_options_default_empty(self):
        """Test that experimental options default to empty dict."""
        calibrator = Calibrator(mode=get_mocked_backend())
        self.assertEqual(calibrator.options.experimental, {})

    def test_experimental_options_from_dict(self):
        """Test constructing with experimental options in dict."""
        opts_dict = {"experimental": {"foo": "bar", "baz": 123}}
        calibrator = Calibrator(mode=get_mocked_backend(), options=opts_dict)
        self.assertEqual(calibrator.options.experimental, {"foo": "bar", "baz": 123})

    def test_experimental_options_from_instance(self):
        """Test constructing with a CalibratorOptions instance with experimental options."""
        opts = CalibratorOptions(experimental={"custom_key": "custom_value"})
        calibrator = Calibrator(mode=get_mocked_backend(), options=opts)
        self.assertEqual(calibrator.options.experimental, {"custom_key": "custom_value"})

    def test_experimental_options_setter(self):
        """Test setting experimental options via the setter."""
        calibrator = Calibrator(mode=get_mocked_backend())
        calibrator.options = {"experimental": {"test": "value"}}
        self.assertEqual(calibrator.options.experimental, {"test": "value"})

    def test_validation_on_mutation(self):
        """Test validation errors are raised on mutation, not just construction."""
        options = ReadoutAngleOptions(enable=True)
        with self.assertRaises(ValidationError):
            options.enable = "not_a_bool"

    def test_extra_variables_are_forbidden(self):
        """Test that we can not set variables undefined by the model."""
        options = ReadoutAngleOptions()
        with self.assertRaises(ValidationError):
            options.not_a_variable = 0


class TestCalibrator(IBMTestCase):
    """Tests the ``Calibrator`` class."""

    def test_run_of_session_is_selected(self):
        """Test ``Calibrator.run`` selects the service ``run`` method, if session is specified."""
        backend_name = "ibm_hello"
        session = get_mocked_session(get_mocked_backend(backend_name))
        with (
            patch.object(session, "_run", return_value="session"),
            patch.object(session.service, "_run", return_value="service"),
        ):
            calibrator = Calibrator(mode=session)
            selected_run = calibrator.run()
            self.assertEqual(selected_run, "session")

    def test_run_of_service_is_selected(self):
        """Test ``Calibrator.run`` selects the service ``run`` method.

        This is tested when session is not specified.
        """
        backend = get_mocked_backend()
        with patch.object(backend.service, "_run", return_value="service"):
            calibrator = Calibrator(mode=backend)
            selected_run = calibrator.run()
            self.assertEqual(selected_run, "service")

    @mock_responses
    def test_mode(self, registry):
        """Calibrator `mode` and `backend()` is based on `mode` init argument."""
        service = QiskitRuntimeService(token="my_token")

        # Job mode, online backend.
        backend = service.backend("common_backend")
        calibrator = Calibrator(mode=backend)
        self.assertEqual(calibrator.backend(), backend)
        self.assertEqual(calibrator.mode, None)

        # Session mode.
        session = Session(backend)
        calibrator = Calibrator(mode=session)
        self.assertEqual(calibrator.backend(), backend)
        self.assertEqual(calibrator.mode, session)

        # Batch mode.
        batch = Batch(backend)
        calibrator = Calibrator(mode=batch)
        self.assertEqual(calibrator.backend(), backend)
        self.assertEqual(calibrator.mode, batch)

        # `None` mode (inside session).
        with Session(backend) as session:
            calibrator = Calibrator()
            self.assertEqual(calibrator.backend(), backend)
            self.assertEqual(calibrator.mode, session)
