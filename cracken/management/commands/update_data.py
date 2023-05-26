import cracken.utils as utils
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Update the data from the thread"

    def handle(self, *args, **options):
        data_frame = utils.extract_table_from_thread()
        utils.update_database(data_frame)
