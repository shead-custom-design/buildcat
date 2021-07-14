import os

import coverage

os.environ["COVERAGE_PROCESS_START"] = ".coveragerc"
coverage.process_startup()
