import cracken.utils as utils
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Update the data from the thread"

    def handle(self, *args, **options):
        data_frame, time = utils.extract_table_from_thread()
        if data_frame is None:
            if time is None:
                raise CommandError("No connection to the database.")
            raise CommandError("The data is already up to date")
        utils.update_database(data_frame, time)
