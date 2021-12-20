from django.contrib import admin
from .models import Apartment, Hotel, ApartmentImage, HotelImage, Comment
# Register your models here.
# admin.site.register(Hotel)
# admin.site.register(Apartment)
  

class ApartmentImageInLine(admin.TabularInline):
    model = ApartmentImage
    max_num = 50
    min_num = 1


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    inlines = [ApartmentImageInLine,]


class HotelImageInLine(admin.TabularInline):
    model = HotelImage
    max_num = 50
    min_num = 1


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelImageInLine,]

admin.site.register(Comment)