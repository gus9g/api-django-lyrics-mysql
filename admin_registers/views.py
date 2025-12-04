from django.shortcuts import render, redirect
from lyrics_redirect_django.models import Band, Album, BandDescription, MusicalGenre, Song
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse, JsonResponse

def index(request):
    return render(request, 'registers/index.html')

# -----------------------------
# -- Musical Genre ------------ 
# -----------------------------

# Listar gêneros
def musicalGenre(request):
    genres_qs = MusicalGenre.objects.order_by('nome').values('id', 'nome')
    genres_list = list(genres_qs)
    return JsonResponse({"generos": genres_list}, status=200)

# Adicionar gênero
@csrf_exempt
def musicalGenreAdd(request, **kwargs):
    if request.method != 'POST':
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    nome = data.get('nome')
    if not nome:
        return JsonResponse({"error": "Campo 'nome' é obrigatório"}, status=400)

    genre = MusicalGenre.objects.create(nome=nome)
    return JsonResponse({"message": "Gênero criado com sucesso", "id": genre.id}, status=201)

# Alterar gênero
@csrf_exempt
def musicalGenreAlter(request, **kwargs):
    if request.method != 'POST':
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    genre_id = data.get('id')
    if not genre_id:
        return JsonResponse({"error": "Campo 'id' é obrigatório"}, status=400)

    genre = MusicalGenre.objects.filter(id=genre_id).first()
    if not genre:
        return JsonResponse({"error": "Gênero não encontrado"}, status=404)

    nome = data.get('nome')
    if nome:
        genre.nome = nome
        genre.save(update_fields=['nome'])

    return JsonResponse({"message": "Gênero alterado com sucesso"}, status=200)

# Remover gênero
@csrf_exempt
def musicalGenreRemove(request, **kwargs):
    if request.method != 'POST':
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    genre_id = data.get('id')
    if not genre_id:
        return JsonResponse({"error": "Campo 'id' é obrigatório"}, status=400)

    genre = MusicalGenre.objects.filter(id=genre_id).first()
    if not genre:
        return JsonResponse({"error": "Gênero não encontrado"}, status=404)

    genre.delete()
    return JsonResponse({"message": "Gênero excluído com sucesso"}, status=200)


# -----------------------------
# -- Band --------------------- 
# -----------------------------

def band(request):
    bands_qs = Band.objects.order_by('nome')
    bands_list = []

    for band in bands_qs:
        bands_list.append({
            "id": band.id,
            "nome": band.nome,
            "fundacao": band.fundacao,
            "finalizacao": band.finalizacao,
            # ManyToMany -> lista de ids ou nomes
            "generos": list(band.genero.values("id", "nome")),
            # OneToOne -> descrição se existir
            "descricao": band.band_description.descricao if band.band_description else None
        })
    return JsonResponse({"bands": bands_list}, status=200)


@csrf_exempt
def bandAdd(request, **kwargs):
    if request.method == 'POST':
        data = json.loads(request.body)  # <-- pega o JSON do POST

        nome = data.get('nome')
        fundacao = data.get('fundacao') or None
        finalizacao = data.get('finalizacao') or None
        generos = data.get('generos', [])
        desc = data.get('band_description')

        if not nome:
            return HttpResponse("Campo 'nome' é obrigatório", status=400)

        band = Band.objects.create(
            nome=nome,
            fundacao=fundacao,
            finalizacao=finalizacao
        )

        band.genero.add(*generos)

        if desc:
            bd = BandDescription.objects.create(descricao=desc)
            band.band_description = bd
            band.save(update_fields=['band_description'])

        return JsonResponse({"message":"Banda criada com sucesso"}, status=201)
    return JsonResponse({"message":"Método não permitido"}, status=405)

@csrf_exempt
def bandAlter(request, **kwargs):
    if request.method != 'POST':
        return JsonResponse({"message","Método não permitido"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"message":"JSON inválido"}, status=400)

    band_id = data.get('id')
    if not band_id:
        return JsonResponse({"message": "Campo 'id' é obrigatório"}, status=400)

    band = Band.objects.filter(id=band_id).first()
    if not band:
        return JsonResponse({"message":"Banda não encontrada"}, status=404)

    # Atualiza campos simples
    nome = data.get('nome')
    fundacao = data.get('fundacao') or None
    finalizacao = data.get('finalizacao') or None
    if nome:
        band.nome = nome
    band.fundacao = fundacao
    band.finalizacao = finalizacao
    band.save(update_fields=['nome', 'fundacao', 'finalizacao'])

    # Atualiza gêneros (ManyToMany)
    generos = data.get('generos')
    if generos is not None:  # aceita lista vazia
        band.genero.set(generos)

    # Atualiza descrição (OneToOne)
    desc = data.get('band_description')
    if desc:
        if band.band_description:
            band.band_description.descricao = desc
            band.band_description.save()
        else:
            bd = BandDescription.objects.create(descricao=desc)
            band.band_description = bd
            band.save(update_fields=['band_description'])

    return JsonResponse({"message": "Banda alterada com sucesso"}, status=200)

@csrf_exempt
def bandRemove(request, **kwargs):
    if request.method != 'POST':
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    band_id = data.get('id')
    if not band_id:
        return JsonResponse({"error": "Campo 'id' é obrigatório"}, status=400)

    band = Band.objects.filter(id=band_id).first()
    if not band:
        return JsonResponse({"error": "Banda não encontrada"}, status=404)

    band.delete()
    return JsonResponse({"message": "Banda excluída com sucesso"}, status=200)


# -----------------------------
# -- Albuns-------------------- 
# -----------------------------
# Listar álbuns
def album(request):
    albums_qs = Album.objects.order_by('nome')
    albums_list = []

    for album in albums_qs:
        albums_list.append({
            "id": album.id,
            "nome": album.nome,
            "img": album.img,
            "generos": list(album.genero.values("id", "nome")),
            "musicas": list(album.musica.values("id", "nome")),
            "descricao": album.album_description.descricao if album.album_description else None,
            "band_id": album.band.id if album.band else None,
            "band_nome": album.band.nome if album.band else None,
        })

    return JsonResponse({"albums": albums_list}, status=200)

# Adicionar álbum
@csrf_exempt
def albumAdd(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    nome = data.get('nome')
    img = data.get('img')
    band_id = data.get('band_id')
    generos_ids = data.get('generos', [])
    musicas_ids = data.get('musicas', [])
    descricao_text = data.get('descricao')

    if not nome:
        return JsonResponse({"error": "Campo 'nome' é obrigatório"}, status=400)

    album = Album.objects.create(
        nome=nome,
        img=img,
        band_id=band_id if band_id else None
    )

    if generos_ids:
        album.genero.add(*generos_ids)

    if musicas_ids:
        album.musica.add(*musicas_ids)

    if descricao_text:
        desc = AlbumDescription.objects.create(descricao=descricao_text)
        album.album_description = desc
        album.save(update_fields=['album_description'])

    return JsonResponse({"message": "Álbum criado com sucesso", "id": album.id}, status=201)

# Alterar álbum
@csrf_exempt
def albumAlter(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    album_id = data.get('id')
    if not album_id:
        return JsonResponse({"error": "Campo 'id' é obrigatório"}, status=400)

    album = Album.objects.filter(id=album_id).first()
    if not album:
        return JsonResponse({"error": "Álbum não encontrado"}, status=404)

    nome = data.get('nome')
    img = data.get('img')
    band_id = data.get('band_id')
    generos_ids = data.get('generos', [])
    musicas_ids = data.get('musicas', [])
    descricao_text = data.get('descricao')

    if nome:
        album.nome = nome
    if img:
        album.img = img
    if band_id is not None:
        album.band_id = band_id
    album.save()

    if generos_ids is not None:
        album.genero.set(generos_ids)
    if musicas_ids is not None:
        album.musica.set(musicas_ids)
    if descricao_text is not None:
        if album.album_description:
            album.album_description.descricao = descricao_text
            album.album_description.save()
        else:
            desc = AlbumDescription.objects.create(descricao=descricao_text)
            album.album_description = desc
            album.save(update_fields=['album_description'])

    return JsonResponse({"message": "Álbum alterado com sucesso"}, status=200)

# Remover álbum
@csrf_exempt
def albumRemove(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    album_id = data.get('id')
    if not album_id:
        return JsonResponse({"error": "Campo 'id' é obrigatório"}, status=400)

    album = Album.objects.filter(id=album_id).first()
    if not album:
        return JsonResponse({"error": "Álbum não encontrado"}, status=404)

    album.delete()
    return JsonResponse({"message": "Álbum excluído com sucesso"}, status=200)


# -----------------------------
# -- Song --------------------- 
# -----------------------------

# Listar músicas
def song(request):
    songs_qs = Song.objects.order_by('nome')
    songs_list = []

    for song in songs_qs:
        songs_list.append({
            "id": song.id,
            "nome": song.nome,
            "lancamento": song.lancamento,
            "tempo_musica": song.tempo_musica,
            "url_musica": song.url_musica,
            "generos": list(song.genre.values("id", "nome"))
        })

    return JsonResponse({"songs": songs_list}, status=200)

# Adicionar música
@csrf_exempt
def songAdd(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    nome = data.get('nome')
    lancamento = data.get('lancamento')
    tempo_musica = data.get('tempo_musica')
    url_musica = data.get('url_musica')
    generos_ids = data.get('generos', [])

    if not nome:
        return JsonResponse({"error": "Campo 'nome' é obrigatório"}, status=400)

    song = Song.objects.create(
        nome=nome,
        lancamento=lancamento if lancamento else None,
        tempo_musica=tempo_musica if tempo_musica else None,
        url_musica=url_musica if url_musica else None
    )

    if generos_ids:
        song.genre.add(*generos_ids)

    return JsonResponse({"message": "Música criada com sucesso", "id": song.id}, status=201)

# Alterar música
@csrf_exempt
def songAlter(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    song_id = data.get('id')
    if not song_id:
        return JsonResponse({"error": "Campo 'id' é obrigatório"}, status=400)

    song = Song.objects.filter(id=song_id).first()
    if not song:
        return JsonResponse({"error": "Música não encontrada"}, status=404)

    nome = data.get('nome')
    lancamento = data.get('lancamento')
    tempo_musica = data.get('tempo_musica')
    url_musica = data.get('url_musica')
    generos_ids = data.get('generos')

    if nome:
        song.nome = nome
    if lancamento is not None:
        song.lancamento = lancamento
    if tempo_musica is not None:
        song.tempo_musica = tempo_musica
    if url_musica is not None:
        song.url_musica = url_musica
    song.save()

    if generos_ids is not None:
        song.genre.set(generos_ids)

    return JsonResponse({"message": "Música alterada com sucesso"}, status=200)

# Remover música
@csrf_exempt
def songRemove(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    song_id = data.get('id')
    if not song_id:
        return JsonResponse({"error": "Campo 'id' é obrigatório"}, status=400)

    song = Song.objects.filter(id=song_id).first()
    if not song:
        return JsonResponse({"error": "Música não encontrada"}, status=404)

    song.delete()
    return JsonResponse({"message": "Música excluída com sucesso"}, status=200)

