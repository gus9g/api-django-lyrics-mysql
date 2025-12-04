from django.db import models


# ======================
#   Gênero Musical
# ======================
class MusicalGenre(models.Model):
    nome = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


# ======================
#   Descrição da Banda
# ======================
class BandDescription(models.Model):
    descricao = models.TextField(max_length=1000)

    def __str__(self):
        return self.descricao[:50]


# ======================
#   Descrição do Álbum
# ======================
class AlbumDescription(models.Model):
    descricao = models.TextField(max_length=1000)

    def __str__(self):
        return self.descricao[:50]


# ======================
#   Música
# ======================
class Song(models.Model):
    nome = models.CharField(max_length=200)
    lancamento = models.DateField(null=True, blank=True)
    tempo_musica = models.IntegerField()   # tempo em segundos
    url_musica = models.TextField(max_length=500)
    genre = models.ManyToManyField(MusicalGenre)  # N:N

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


# ======================
#   Banda
# ======================
class Band(models.Model):
    nome = models.CharField(max_length=200)
    genero = models.ManyToManyField(MusicalGenre)  # N:N

    fundacao = models.DateField(null=True, blank=True)
    finalizacao = models.DateField(null=True, blank=True)

    band_description = models.OneToOneField(
        BandDescription,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


# ======================
#   Álbum
# ======================
class Album(models.Model):
    nome = models.CharField(max_length=200)
    img = models.TextField(max_length=500)

    genero = models.ManyToManyField(MusicalGenre)  # N:N
    musica = models.ManyToManyField(Song)          # N:N

    # 🔥 AQUI está o relacionamento correto (1 banda → vários álbuns)
    band = models.ForeignKey(
        Band,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='albums'
    )

    album_description = models.OneToOneField(
        AlbumDescription,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
