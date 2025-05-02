from django.db import models

# Create your models here.
class FlavorPreference(models.Model):
    """db Model for FlavorPreferences"""
    flavor_Name = models.CharField(max_length=100)

    def __str__(self):
        """String for representing the Model object."""
        return self.flavor_Name

class Ingredients(models.Model):
    """ db Model for Ingredients"""
    Ingredients_Name = models.CharField(max_length=100)

    flavor=models.ForeignKey(FlavorPreference,on_delete=models.CASCADE)

    def __str__(self):
        """String for representing the Model object."""
        return self.Ingredients_Name

class Product(models.Model):
    """db Model for Products"""
    Product_Name = models.CharField(max_length=100)
    Description= models.CharField(max_length=200)
    Price= models.FloatField()
    Available= models.BooleanField()
    ProductIngredients = models.ManyToManyField(Ingredients, related_name='Products')
    ProductImage = models.ImageField(default='fallback.png', blank=True)
    ###many to many that pulls from Ingredients models
    def __str__(self):
        """String for representing the Model object."""
        return self.Product_Name