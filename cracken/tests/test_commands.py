from io import StringIO
from django.core.management import call_command

from django.test import TestCase

from cracken.models import Store, Game, WarezGroup

from cracken import utils


class UpdateCommandTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create objects that aren't going to be modified or changed in any of the test methods.
        call_command("update_data")

    def setUp(self):
        # called before every test function to set up any objects that may be modified by the test
        # (every test function will get a "fresh" version of these objects).
        pass
    def test_num_of_games(self):
        dataframe = utils.extract_table_from_thread()
        num = dataframe.shape[0]
        self.assertEqual(Game.objects.count(), num)

    def test_num_of_stores(self):
        dataframe = utils.extract_table_from_thread()
        group_names = dataframe['Group'].explode().unique()
        self.assertEqual(WarezGroup.objects.count(), len(group_names))

    def test_num_of_groups(self):
        dataframe = utils.extract_table_from_thread()
        store_names = dataframe['Store'].explode().unique()
        self.assertEqual(Store.objects.count(), len(store_names))

