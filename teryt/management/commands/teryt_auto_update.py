from django.core.management.base import BaseCommand

from teryt.utils_zip import (
    get_zip_files, update_database
)


class Command(BaseCommand):
    help = 'Import TERYT data from ZIP files prepared by GUS,\
            auto download, unpack and update with them.'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        zip_files = get_zip_files()

        for zfile in zip_files:
            fname = zfile.namelist()[0]
            with zfile.open(fname) as xml_file:
                update_database(xml_file, fname, False)

        print("Done.")
