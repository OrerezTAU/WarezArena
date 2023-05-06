from django.db import models
from django.urls import reverse


class Store(models.Model):
    """Model representing a virtual game store."""
    name = models.CharField(max_length=200, help_text='Enter a store name (e.g. Steam)')
    url = models.URLField(max_length=200, help_text='Enter the store URL (e.g. https://store.steampowered.com/)'
                          , blank=True, null=True)
    description = models.TextField(max_length=1000, help_text='Enter a brief description of the store.', null=True,
                                   blank=True)
    games = models.ManyToManyField('Game', help_text='Select a game for this store')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this store."""
        return reverse('store-detail', args=[str(self.id)])


class WarezGroup(models.Model):
    """Model representing a Warez group that is cracking  games."""
    name = models.CharField(max_length=200, help_text='Enter a group name (e.g. SKIDROW)')
    description = models.TextField(max_length=1000, help_text='Enter a brief description of the group.',
                                   null=True, blank=True)
    year_founded = models.DateField(null=True, blank=True, help_text='Enter the year the group was founded.', )
    games_cracked = models.ManyToManyField('Game', help_text='Select a game for this group')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this group."""
        return reverse('warez-group-detail', args=[str(self.id)])


class Game(models.Model):
    """Model representing a game."""
    name = models.CharField(max_length=200, help_text='Enter a game name (e.g. Cyberpunk 2077)')
    cracking_group = models.ForeignKey('WarezGroup', on_delete=models.SET_NULL, null=True)
    crack_date = models.DateField(null=True, blank=True)
    available_on_stores = models.ManyToManyField(Store, help_text='Select stores for this game')
    score = models.DecimalField(max_digits=3, decimal_places=0, null=True, blank=True)
    num_reviews = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['crack_date', 'num_reviews', 'score']

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this game."""
        return reverse('game-detail', args=[str(self.id)])

# Create your models here.
