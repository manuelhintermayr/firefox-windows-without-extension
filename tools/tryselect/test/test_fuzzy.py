# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import os

import mozunit
import pytest


@pytest.mark.skipif(os.name == "nt", reason="fzf not installed on host")
@pytest.mark.parametrize("show_chunk_numbers", [True, False])
def test_query_paths(run_mach, capfd, show_chunk_numbers):
    cmd = [
        "try",
        "fuzzy",
        "--no-push",
        "-q",
        "^test-linux '64-qr/debug-mochitest-chrome-1proc-",
        "caps/tests/mochitest/test_addonMayLoad.html",
    ]
    if show_chunk_numbers:
        cmd.append("--show-chunk-numbers")

    assert run_mach(cmd) == 0

    output = capfd.readouterr().out
    print(output)

    delim = "Calculated try_task_config.json:"
    index = output.find(delim)
    result = json.loads(output[index + len(delim) :])

    # If there are more than one tasks here, it means that something went wrong
    # with the path filtering.
    tasks = result["parameters"]["try_task_config"]["tasks"]
    assert tasks == ["test-linux1804-64-qr/debug-mochitest-chrome-1proc-1"]


@pytest.mark.skipif(os.name == "nt", reason="fzf not installed on host")
@pytest.mark.parametrize("full", [True, False])
def test_query(run_mach, capfd, full):
    cmd = ["try", "fuzzy", "--no-push", "-q", "'source-test-python-taskgraph-tests-py3"]
    if full:
        cmd.append("--full")
    assert run_mach(cmd) == 0

    output = capfd.readouterr().out
    print(output)

    delim = "Calculated try_task_config.json:"
    index = output.find(delim)
    result = json.loads(output[index + len(delim) :])

    # Should only ever mach one task exactly.
    tasks = result["parameters"]["try_task_config"]["tasks"]
    assert tasks == ["source-test-python-taskgraph-tests-py3"]


if __name__ == "__main__":
    mozunit.main()
