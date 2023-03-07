from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


SHIP_SIZES = {
    'SMALL': {'hit_probability': 30},
    'MEDIUM': {'hit_probability': 40},
    'LARGE': {'hit_probability': 50}
}


class Captain(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    rank = models.CharField(max_length=100, null=False, blank=False)
    ship = models.OneToOneField('Ship', on_delete=models.CASCADE, related_name='captain')


class Game(models.Model):
    id = models.BigAutoField(primary_key=True, )
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def name(self):
        return f'Game {self.id}'


class Ship(models.Model):
    soldiers = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(1), MaxValueValidator(100)])
    health = models.IntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])
    size = models.CharField(max_length=6, choices=[('SMALL', 'Small'), ('MEDIUM', 'Medium'), ('LARGE', 'Large')])
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    
    def set_size(self):
        if self.soldiers <= 32:
            self.size = 'SMALL'
        elif self.soldiers <= 65:
            self.size = 'MEDIUM'
        else:
            self.size = 'LARGE'

    def save(self, *args, **kwargs):
        self.set_size()
        super().save(*args, **kwargs)

    @property
    def hit_probability(self):
        return SHIP_SIZES[self.size]['hit_probability']
