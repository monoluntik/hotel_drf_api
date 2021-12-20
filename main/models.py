from django.db import models

from account.models import MyUser

COUNTRIES = (
        ('Азербайджанская Республика', 'Азербайджанская Республика'), 
        ('Республика Армения', 'Республика Армения'), 
        ('Республика Беларусь', 'Республика Беларусь'), 
        ('Республика Казахстан', 'Республика Казахстан'), 
        ('Кыргызская Республика', 'Кыргызская Республика'), 
        ('Республика Молдова', 'Республика Молдова'), 
        ('Российская Федерация', 'Российская Федерация'), 
        ('Республика Таджикистан', 'Республика Таджикистан'), 
        ('Туркменистан', 'Туркменистан'), 
        ('Республика Узбекистан', 'Республика Узбекистан'), 
        ('Украина', 'Украина')
    )


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    country = models.CharField(choices=COUNTRIES, max_length=255)
    address = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return f'{self.name} {self.country} {self.address}'


class HotelImage(models.Model):
    image = models.ImageField(upload_to='images')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')


class Apartment(models.Model):
    rooms = models.IntegerField(choices=((i,i) for i in range(1,10)))
    description = models.TextField()
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='apartments')

    def __str__(self) -> str:
        return f'{self.hotel} {self.id}'

class ApartmentImage(models.Model):
    image = models.ImageField(upload_to='images')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.author}:{self.body}'


class Likes(models.Model):
    likes = models.BooleanField(default=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='likes')


    def __str__(self):
        return str(self.likes)


class Rating(models.Model):
    rating = models.IntegerField(default=0)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rating')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='rating')

    def __str__(self):
        return str(self.rating)


class Favorite(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='favourites')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favourites')
    favorite = models.BooleanField(default=True)
