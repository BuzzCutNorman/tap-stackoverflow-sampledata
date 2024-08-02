"""stackoverflow-sampledata tap class."""

from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING, List

from singer_sdk import Stream, Tap
from singer_sdk import typing as th  # JSON schema typing helpers
from singer_sdk.helpers._classproperty import classproperty
from singer_sdk.helpers.capabilities import (
    CapabilitiesEnum,
    PluginCapabilities,
    TapCapabilities,
)

from tap_stackoverflow_sampledata.streams import (
    BadgesStream,
    CommentsStream,
    PostLinksStream,
    PostsStream,
    TagsStream,
    UsersStream,
    VotesStream,
)

if TYPE_CHECKING:
    from singer_sdk._singerlib import Catalog

# Used later to match Stream Class to files
STACKOVERFLOW_FILE_NAMES_TO_STREAMS = {
    "badges.xml": BadgesStream,
    "comments.xml": CommentsStream,
    "postlinks.xml": PostLinksStream,
    "posts.xml": PostsStream,
    "tags.xml": TagsStream,
    "users.xml": UsersStream,
    "votes.xml": VotesStream
}

STREAM_TYPES = List[Stream]


class TapStackOverflowSampleData(Tap):
    """stackoverflow-sampledata tap class."""

    name = "tap-stackoverflow-sampledata"

    @property
    def input_catalog(self) -> Catalog:
        """Get the tap's working catalog.

        Returns:
            A Singer catalog object.
        """
        # This has been set to return None so auto-detection
        # of streams based on files in the folder will work
        return None

    config_jsonschema = th.PropertiesList(
        th.Property(
            "stackoverflow_data_directory",
            th.StringType,
            description="A path to the StackOverflow XML data files.",
        ),
        th.Property(
            "batch_config",
            th.ObjectType(
                th.Property(
                    "encoding",
                    th.ObjectType(
                        th.Property(
                            "format",
                            th.StringType,
                            description="Currently the only format is jsonl",
                        ),
                        th.Property(
                            "compression",
                            th.StringType,
                            description="Currently the only compression options is gzip",  # noqa: E501
                        )
                    )
                ),
                th.Property(
                    "storage",
                    th.ObjectType(
                        th.Property(
                            "root",
                            th.StringType,
                            description=("the directory you want batch messages to be placed in\n"  # noqa: E501
                                        "example: file://test/batches"
                            )
                        ),
                        th.Property(
                            "prefix",
                            th.StringType,
                            description=("What prefix you want your messages to have\n"
                                        "example: test-batch-"
                            )
                        )
                    )
                )
            ),
            description="Optional Batch Message configuration",
        )
    ).to_dict()

    @classproperty
    def capabilities(self) -> list[CapabilitiesEnum]:
        """Get tap capabilities.

        Returns:
            A list of capabilities supported by this tap.
        """
        return [
            TapCapabilities.DISCOVER,
            PluginCapabilities.ABOUT,
        ]

    def get_streams(self) -> list[Stream]:
        """Return a list of file configs.

        Directly from the config.json or in an external file.
        """
        data_directory = self.config.get("stackoverflow_data_directory")
        stream_types: list[Stream] = []

        if data_directory is None:
            self.logger.error("No stackoverflow_data_directory configured.")
            sys.exit(1)

        if os.path.exists(data_directory):  # noqa: PTH110
            if os.path.isdir(data_directory):  # noqa: PTH112
                if len(os.listdir(data_directory)) > 0:
                    # If the file is in the dictionary
                    # we add it the Streams Classes that will be
                    # passed in the dicover_streams process.
                    stream_types.extend(
                        STACKOVERFLOW_FILE_NAMES_TO_STREAMS.get(file.lower())
                        for file in os.listdir(data_directory)
                        if STACKOVERFLOW_FILE_NAMES_TO_STREAMS.get(file.lower())
                    )
                else:
                    self.logger.error("There are no files in the directory")
                    sys.exit(1)
            else:
                self.logger.error("The path given is not a direcotry")
                sys.exit(1)
        else:
            self.logger.error("The path doesn't exist")
            sys.exit(1)

        if not stream_types:
            self.logger.error("No Stackovlerflow files found.")
            sys.exit(1)

        return stream_types

    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams."""
        stream_types = self.get_streams()

        return [stream_class(self) for stream_class in stream_types]

if __name__ == "__main__":
    TapStackOverflowSampleData.cli()
