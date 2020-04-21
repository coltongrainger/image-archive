#! /usr/bin/env python3
#
# 2020-04-20 
# Colton Grainger 
# CC-0 Public Domain

"""
Personal Image Archive
"""

import os
import shutil
import tarfile
from datetime import datetime
from pathlib import Path

##

class Directory(object):

    """Abstraction for file operations in a directory"""

    def __init__(self, *, abspath, **kwargs):
        """Initializes the Directory, creating one if it doesn't exist.

        :abspath: str, absolute path to directory

        """
        self.abspath = abspath
        Path(abspath).mkdir(parents=True, exist_ok=True)

    def __repr__(self):
        return f"Directory(abspath='{self.abspath}')"

##

    def empty(self):
        """Empties the Directory."""
        for filename in os.listdir(self.abspath):
            file_path = os.path.join(self.abspath, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

    def create_tar_archive(self, outdir=self):
        """Creates a gzipped tar archive of the Directory's contents, in the
        Directory itself, unless 'outdir' is specified.

        :outdir: (optional) a different instance of a Directory
        :returns: path to gzipped tar archive

        """
        # for the tar archive filename, we need
        # the local datetime formatted as '2020-04-21T132052'
         = datetime.now().strftime('%FT%H%M%S') 
        filename = os.path.join(outdir.abspath, date
        with tarfile.open(#, "w:gz") as tar:
            for name in glob.glob('*.txt'):
                print(f'Adding {name} to sample.tar archive.')
                tar.add(name)


##

class IngestDirectory(Directory):

    """Images are to be ingest from an IngestDirectory"""

    def __init__(self, **kwargs):
        """Initializes InDirectory as a Directory"""
        super().__init__(**kwargs)

    # def generate_metadata_catalog(self, metadata_file=None):
    #     """Generates metadata catalog for ingest.

    #     :metadata_file: str, relative path to JSON file in IngestDirectory
    #     :returns: TODO

    #     """
    #     pass

 
