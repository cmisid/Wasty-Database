from django.db import models


class Person(models.Model):

    class Meta:
        db_table = 'persons'
        verbose_name_plural = 'Persons'
        ordering = ('join_date',)

    first_name = models.CharField(verbose_name='First name', max_length=50)
    last_name = models.CharField(verbose_name='Last name', max_length=100)
    birth_date = models.DateField(verbose_name='Date of birth')
    join_date = models.DateField(verbose_name='Date of birth', auto_now_add=True)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Item(models.Model):

    class Meta:
        db_table = 'items'
        verbose_name_plural = 'Items'
        ordering = ('pub_date',)

    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    pub_date = models.DateTimeField('Date published', auto_now_add=True)
    pub_person = models.ForeignKey(Person, on_delete=models.CASCADE)
