# This code is part of Qiskit.
#
# (C) Copyright IBM 2019, 2023.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Fake Cambridge device (20 qubit).
"""

import os
from qiskit_ibm_runtime.fake_provider import fake_backend


class FakeCambridgeV2(fake_backend.FakeBackendV2):
    """A fake Cambridge backend.

    .. code-block:: text

                  00 ↔ 01 ↔ 02 ↔ 03 ↔ 04
                  ↕                    ↕
                  05                  06
                  ↕                    ↕
        07 ↔ 08 ↔ 09 ↔ 10 ↔ 11 ↔ 12 ↔ 13 ↔ 14 ↔ 15
        ↕                   ↕                    ↕
        16                  17                  18
        ↕                   ↕                    ↕
        19 ↔ 20 ↔ 21 ↔ 22 ↔ 23 ↔ 24 ↔ 25 ↔ 26 ↔ 27
    """

    dirname = os.path.dirname(__file__)  # type: ignore
    conf_filename = "conf_cambridge.json"  # type: ignore
    props_filename = "props_cambridge.json"  # type: ignore
    backend_name = "fake_cambridge"  # type: ignore
