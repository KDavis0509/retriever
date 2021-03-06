# -*- coding: latin-1 -*-
#retriever
from pkg_resources import parse_version

from retriever.lib.models import Table, Cleanup, correct_invalid_value
from retriever.lib.templates import Script

try:
    from retriever.lib.defaults import VERSION
except ImportError:
    from retriever import VERSION


class main(Script):
    def __init__(self, **kwargs):
        Script.__init__(self, **kwargs)
        self.title = "A Southern Ocean dietary database"
        self.citation = "Ben Raymond, Michelle Marshall, Gabrielle Nevitt, " \
                        "Chris L. Gillies, John van den Hoff, Jonathan " \
                        "S. Stark, Marcel Losekoot, Eric J. Woehler, and " \
                        "Andrew J. Constable. 2011. " \
                        "A Southern Ocean dietary database. Ecology 92:1188."
        self.name = "socean-diet-data"
        self.shortname = "socean-diet-data"
        self.ref = "https://figshare.com/articles/Full_Archive/3551304"
        self.description = "Diet-related data from published" \
                           " and unpublished data sets and studies"
        self.keywords = []
        self.retriever_minimum_version = '2.0.dev'
        self.version = '1.0.4'
        self.urls = {"zip": "https://ndownloader.figshare.com/files/5618823"}
        self.cleanup_func_table = Cleanup(
            correct_invalid_value, missing_values=[
                '', 'unknown'])

        if parse_version(VERSION) <= parse_version("2.0.0"):
            self.shortname = self.name
            self.name = self.title
            self.tags = self.keywords
            self.cleanup_func_table = Cleanup(
                correct_invalid_value, nulls=['', 'unknown'])

    def download(self, engine=None, debug=False):
        Script.download(self, engine, debug)
        engine = self.engine
        file_names = [('isotopes.csv', 'isotopes'),
                      ('sources.csv', 'sources'),
                      ('diet.csv', 'diet')
                      ]

        engine.download_files_from_archive(
            self.urls["zip"], [i[0] for i in file_names], "zip", False, "ECOL_92_97")

        for (filename, tablename) in file_names:
            data_path = self.engine.format_filename(filename)
            self.engine.auto_create_table(
                Table(str(tablename), cleanup=self.cleanup_func_table),
                filename=filename)
            self.engine.insert_data_from_file(data_path)


SCRIPT = main()
