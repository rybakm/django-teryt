from django.core.management.base import BaseCommand, CommandError
import zipfile
from optparse import make_option

from teryt.utils_zip import update_database


class Command(BaseCommand):
    args = '[xml file list]'
    help = 'Import TERYT data from XML/ZIP files prepared by GUS'
    option_list = BaseCommand.option_list + (
        make_option('--update',
                    action='store_true',
                    dest='update',
                    default=False,
                    help='Update exisitng data'),
    )

    def handle(self, *args, **options):
        force_ins = not options['update']

        if not args:
            raise CommandError('At least 1 file name required')

        for file in args:
            if zipfile.is_zipfile(file):
                file = zipfile.ZipFile(file)
                fname = file.namelist()[0]
                with file.open(fname) as xml_file:
                    update_database(xml_file, fname, force_ins)
            else:
                with open(file) as xml_file:
                    update_database(xml_file, file, force_ins)

        print("Done.")
