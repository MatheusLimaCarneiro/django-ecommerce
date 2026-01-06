from django.db import models

class Category(models.Model):
    name = models.CharField("Nome",max_length=255)
    description = models.TextField("Descrição",blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

    def __str__(self):
        return self.name
