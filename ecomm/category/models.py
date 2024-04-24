from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True,null=True)
    description = models.TextField(blank=True)
    categorey_image = models.ImageField(blank=True,null=True,upload_to='categories')
    def save(self,*args,**kwargs):
        self.slug = slugify(self.category_name)
        super(Category,self).save(*args,**kwargs)

    def __str__(self) -> str:
        return self.category_name

    def get_url(self):
        return reverse('products_by_category',args=[self.slug])

    