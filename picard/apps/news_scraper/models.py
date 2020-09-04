from django.db import models

class Source(models.Model):
    title = models.CharField(max_length=100,null=False,blank=False)
    slug = models.CharField(max_length=100,null=False,blank=False)
    url = models.URLField(max_length=200,null=False,blank=False)
    description = models.TextField()
    category = models.CharField(max_length=100,null=False,blank=False)
    language = models.CharField(max_length=5,null=False,blank=False)
    
    TYPE_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    status = models.CharField(max_length=10, choices=TYPE_CHOICES, default='inactive')

    def __str__(self):
        return self.title

class Company(models.Model):
    title = models.CharField(max_length=200,null=False,blank=False)
    query = models.CharField(max_length=200,null=False,blank=False)
    sources = models.ManyToManyField(Source)

    TYPE_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    status = models.CharField(max_length=10, choices=TYPE_CHOICES, default='inactive')

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name_plural = "Companies"


class Article(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    author = models.CharField(max_length=100,null=True,blank=True)
    title = models.TextField(null=False,blank=False)
    content = models.TextField(null=True,blank=True)
    url = models.URLField(max_length=500,null=False,blank=False)
    images = models.TextField(null=True,blank=True)
    hyperlinks = models.TextField(null=True,blank=True)

    published_at = models.DateTimeField(null=True,blank=True)

    TYPE_CHOICES = [('incomplete', 'Incomplete'), ('completed', 'Completed'), ('failed', 'Failed')]
    status = models.CharField(max_length=10, choices=TYPE_CHOICES, default='incomplete')


