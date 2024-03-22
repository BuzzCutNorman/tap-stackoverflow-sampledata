"""stackoverflow-sampledata tap class."""

from __future__ import annotations

import os
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
                            description="Currently the only compression options is gzip",
                        )
                    )
                ),
                th.Property(
                    "storage",
                    th.ObjectType(
                        th.Property(
                            "root",
                            th.StringType,
                            description=("the directory you want batch messages to be placed in\n"
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
            exit(1)

        if os.path.exists(data_directory):
            if os.path.isdir(data_directory):
                if len(os.listdir(data_directory)) > 0:
                    for file in os.listdir(data_directory):
                        # If the file is in the dictionary
                        # we add it the Streams Classes that will be
                        # passed in the dicover_streams process.
                        if STACKOVERFLOW_FILE_NAMES_TO_STREAMS.get(file.lower()):
                            stream_types.append(STACKOVERFLOW_FILE_NAMES_TO_STREAMS.get(file.lower()))
                else:
                    self.logger.error("There are no files in the directory")
                    exit(1)
            else:
                self.logger.error("The path given is not a direcotry")
                exit(1)
        else:
            self.logger.error("The path doesn't exist")
            exit(1)

        if not stream_types:
            self.logger.error("No Stackovlerflow files found.")
            exit(1)

        return stream_types

    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams."""
        STREAM_TYPES = self.get_streams()

        return [stream_class(self) for stream_class in STREAM_TYPES]

if __name__ == "__main__":
    TapStackOverflowSampleData.cli()
