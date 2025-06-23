"""Tests standard tap features using the built-in SDK tests library."""


from singer_sdk.testing import get_tap_test_class
from tap_stackoverflow_sampledata.tap import TapStackOverflowSampleData

SAMPLE_CONFIG = {
    "stackoverflow_data_directory" : "./tests/test_files/"
}

BLANK_CONFIG = {}

# Run standard built-in tap tests from the SDK:
TestTapStackOverflowSampleData = get_tap_test_class(
    tap_class=TapStackOverflowSampleData,
    config=SAMPLE_CONFIG,
)


# TODO: Create additional tests as appropriate for your tap.
