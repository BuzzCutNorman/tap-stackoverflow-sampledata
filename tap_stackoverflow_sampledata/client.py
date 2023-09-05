"""Custom client handling, including
StackOverflowSampleDataStream base class."""

from __future__ import annotations

import os

from typing import Optional, Iterable

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

        # Grab the rows from the xml file using by
        # opening the file using using a iternation parser
        for event, element in etree.iterparse(self.data_file):

            # Dictionaries to place and raw refined rows
            xml_row = dict()
            row = dict()

            # The data is held a attributes to each sub root row
            # We grab each attibute item and type it according to the schmea
            for attribute in element.attrib.items():
                # Each attribut is a key and value pair "ID"=1
                key: str = attribute[0]
                value: str = attribute[1]

                # We try to grab to schema type property for the attibute
                # Then type the value. If a type can no be grabbed we
                # pass the default string type.
                try:
                    value_type: str = self.schema['properties'][key]['type'][0]
                except:
                    value_type: str = 'string'

                if value_type == 'integer':
                    value = int(value)

                # We add the key value pair to the xml_row dictionary
                xml_row[key] = value

            # Blank list to hold al the Primary Key columns
            column_names = list()

            #  We grab the column names from the Stream Schema
            #  Then append them to the columns names list
            for column in self.schema['properties'].keys():
                column_names.append(str(column))

            # We use the columns list to add columns that didn't
            # have any data in the xml row and set the
            # column value to none or null
            for column in column_names:
                if column in xml_row:
                    row[column] = xml_row[column]
                else:
                    row[column] = None

            # We are under the assuption that
            # primary key(s) have valus present
            primary_key_not_null = True

            # Check each primary key in the row to make
            # sure it has a value if one does not have value
            # set the primary key not null flag to False
            for key_col in self.primary_keys:
                if row.get(key_col) is None:
                    primary_key_not_null = False

            # If the primary key not null flag is True
            # yeild the row as a dictrionary
            if primary_key_not_null:
                yield dict(row)

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
