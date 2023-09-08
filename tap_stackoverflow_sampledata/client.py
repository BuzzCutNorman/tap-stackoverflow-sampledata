"""Custom client handling, including
StackOverflowSampleDataStream base class."""

from __future__ import annotations

import os

from typing import Any, Optional, Iterable

from singer_sdk.streams import Stream
from lxml import etree


class StackOverflowSampleDataStream(Stream):
    """Stream class for stackoverflow-sampledata streams."""
    
    file_name: str = None

    _file_path: str = None
    _file_directory: str = None

    @property
    def file_directory(self) -> str:
        if self._file_directory is None:
            self._file_directory = self.config.get("stackoverflow_data_directory")
        return self._file_directory

    @property
    def data_file(self) -> str:
        if self._file_path is None:
            self.get_data_file_path()
        return self._file_path

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        """Return a generator of row-type dictionary objects.

        Args:
            context: If partition context is provided, will read specifically
                from this data slice.

        Yields:
            One dict per record.
        """
        # Get the Stream Properties Dictornary from the Schema
        properties: dict = self.schema.get('properties')

        # Blank list to hold al the Primary Key columns
        column_names: list[str] = []
        column_value_types: dict[str, list[str]] = {}

        #  We grab the column names from the Stream Schema
        #  Then append them to the columns names list
        #  We also grab and append the data type to 
        #  Then insert it into column_value_types dict
        for column in properties.keys():
            name = str(column) 
            column_names.append(name)
            column_value_types[name] = properties.get(name).get('type')

        # Grab the rows from the xml file using by
        # opening the file using using a iternation parser
        element: etree._Element
        for _, element in etree.iterparse(self.data_file):

            # Dictionaries to place and raw refined rows
            row: dict = {}

            # We are under the assuption that
            # primary key(s) have values present
            primary_keys_have_value_present: bool = True

			# The data is held a attributes to each sub root row
            # We grab each attibute item and type it according to the schmea
            # We use the columns list to add columns that didn't
            # have any data in the xml row and set the
            # column value to none or null
            # Check each primary key in the row to make
            # sure it has a value if one does not have value
            # set the primary key not null flag to False
            column: str
            for column in column_names:
                if column in element.attrib.keys():
                    value = element.attrib.get(column)
                    if 'integer' in column_value_types.get(column):
                        row[column] = int(value)
                    else:
                        row[column] = value
                else:
                    row[column] = None
                    if column in self.primary_keys:
                        primary_keys_have_value_present = False

            # If the primary key not null flag is True
            # yeild the row as a dictrionary
            if primary_keys_have_value_present:
                yield row

            # We clear the element so we don't use memory
            # to hold rows we won't need again
            element.clear()
            if element.getparent() is not None:
                element.getparent().remove(element)

    def get_data_file_path(self):
        """Return a list of file paths to read.
        This tap accepts file names and directories so it will detect
        directories and iterate files inside.
        """

        # Check that the file_direcotry from the meltano.yaml exists
        # if it isn't we alert there is an issue
        if not os.path.exists(self.file_directory):
            raise Exception(f"File path does not exist {self.file_directory}")

        # Add the file Streams file_name to a direcotory path
        # Pass along file_path if it points to the Stream's file_name
        clean_file_path = os.path.normpath(self.file_directory) + os.sep
        data_file_path: str = clean_file_path + self.file_name
        if self.is_valid_filename(data_file_path):
            self._file_path = data_file_path

    def is_valid_filename(self, file_path: str) -> bool:
        """Return a boolean of whether the path is a file includes an XML extension."""
        is_valid = True

        # Check to see if this is a direcotry turn
        # the is valid flag to false and
        # say you are skipping the file
        if os.path.isdir(file_path):
            is_valid = False
            self.logger.info(f"Skipping folder {file_path}")

        # Check to see if the if the file has a .xml extention
        # if it doesn't turn the is valid flag to False and
        # say you are skipping the file
        elif file_path[-4:] != ".xml":
            is_valid = False
            self.logger.warning(f"Skipping non xml file '{file_path}'")

        return is_valid
