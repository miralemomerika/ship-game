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
    
    def winner(self):
        """
            Method that returns a winner of the game if there is only one ship standing.
            If there aren't any ships there is no winner.
            If there are multiple ships standing method returns appropriate message
            that the game hasn't ended yet
        """
        ships = Ship.objects.select_related('captain').filter(health__gt=0, game=self)
        
        if len(ships) == 1:
            return f'The winner of {self.name} is {ships[0].captain.name} with ship id {ships[0].id}'
        elif len(ships) == 0:
            return f'All ships sunk, there is no winner in {self.name}'
        else:
            return f'{self.name} hasn\'t ended yet'
    
    def has_ended(self):
        """
            Method that return True if the game has ended and False if there is still 
            2 or more ships standing
        """
        ships = Ship.objects.filter(health__gt=0, game=self)
        
        if len(ships) > 1:
            return False
        elif len(ships) <= 1:
            if self.game_ended is False:
                self.game_ended = True
                self.save()
            return True


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
    
    def has_sunk(self):
        return self.health == 0
