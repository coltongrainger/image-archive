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

class Directory:

    """Abstraction for file operations in a directory"""

    def __init__(self, *, abspath, **kwargs):
        """Initializes the Directory, creating one if it doesn't exist.

        :abspath: str, absolute path to directory

        """
        self.abspath = abspath
        Path(abspath).mkdir(parents=True, exist_ok=True)

    @classmethod
    def from_relpath(cls, relpath):
        """Initializes the Directory from a relative path."""
        return cls(abspath=os.path.abspath(relpath))

    def __repr__(self):
        return f"Directory(abspath='{self.abspath}')"

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

    def create_tar_archive(self, outdir=None):
        """Creates a gzipped tar archive of the Directory's contents, in the
        Directory itself, unless 'outdir' is specified. I recommend leaving
        outdir as None. In good OO-design, objects should be responsible for
        mutating themselves.

        :outdir: (optional) a Directory instance, not recommended
        :returns: path to gzipped tar archive

        """
        # for the tar archive filename, we need a timestamp 
        timestamp = datetime.now().strftime('%F-%H%M%S') # e.g., '2020-04-21-132052'
        directory_basename = os.path.basename(self.abspath)
        tar_archive_name = f"{timestamp}-{directory_basename}.tar.gz"
        try:
            tar_archive_abspath = os.path.join(outdir.abspath, tar_archive_name)
        except AttributeError:
            tar_archive_abspath = os.path.join(self.abspath, tar_archive_name)
        with tarfile.open(tar_archive_abspath, mode="w:gz") as tar:
            print(f"Creating tar archive {tar_archive_abspath} ...")
            tar.add(self.abspath, arcname=f"{timestamp}-{directory_basename}")
        return tar_archive_abspath

    def remove_tar_archive(self):
        """
        Removes any gzipped tar archives contained in the Directory, if they exist.
        """
        for item in os.listdir(self.abspath):
            if item.endswith(".tar.gz"):
                tar_archive_abspath = os.path.join(self.abspath, item)
                print(f"Removing tar archive {tar_archive_abspath} ...")
                os.remove(tar_archive_abspath)

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

 
