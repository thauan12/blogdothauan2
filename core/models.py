from django.contrib.auth.models import User
from django.db import models
from stdimage import StdImageField


class PublicadosManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='publicado')


class Post(models.Model):
    objects = models.Manager()
    publicados = PublicadosManager()
    STATUS_CHOICES = (
        ('rascunho', 'Rascunho'),
        ('publicado', 'Publicado'),
    )
    titulo = models.CharField(max_length=70)
    slug = models.SlugField(max_length=70)
    corpo = models.TextField()
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='rascunho')
    criado = models.DateTimeField(auto_now_add=True)
    publicado = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts_autor')
    imagem = StdImageField('Imagem', upload_to='posts',
                           variations={'thumb': {
                                                    'width': 438,
                                                    'height': 438,
                                                    'crop':True
                                                }
                                       },
                           blank=True, null=True
                           )

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('-publicado',)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='comentarios')
    nome = models.CharField('Nome', max_length=50)
    email = models.EmailField('E-mail')
    texto = models.TextField('Comentário')
    criado = models.DateTimeField('Criado em', auto_now_add=True)
    status = models.BooleanField('Ativo', default=False)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'

    def __str__(self):
        return f'Comentário de {self.nome} em {self.criado}'
