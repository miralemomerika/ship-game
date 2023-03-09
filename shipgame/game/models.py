from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import random


SHIP_SIZES = {
    'SMALL': {'hit_probability': 30, 'critical_hit_probability': 30},
    'MEDIUM': {'hit_probability': 40, 'critical_hit_probability': 20},
    'LARGE': {'hit_probability': 50, 'critical_hit_probability': 10}
}


class Captain(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    rank = models.CharField(max_length=100, null=False, blank=False)
    ship = models.OneToOneField('Ship', on_delete=models.CASCADE, related_name='captain')


class Game(models.Model):
    id = models.BigAutoField(primary_key=True, )
    created_at = models.DateTimeField(auto_now_add=True)
    game_ended = models.BooleanField(default=False)
    
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
    
    @property
    def critical_hit_probability(self):
        return SHIP_SIZES[self.size]['critical_hit_probability']
    
    def attack(self, target_ship):
        hit_probability = target_ship.hit_probability
        damage = 0
        if random.randint(1, 100) <= hit_probability:
            damage = random.randint(10, 30)
        
        target_ship.defend(damage)

    
    def defend(self, attack_damage):
        critical_hit_probability = self.critical_hit_probability
        damage_taken = attack_damage
        
        if random.randint(1, 100) <= critical_hit_probability:
            damage_taken = int(attack_damage * 2)
        
        if (self.health - damage_taken) <= 0:
            self.health = 0
        else:
            self.health -= damage_taken
            
        self.save()
