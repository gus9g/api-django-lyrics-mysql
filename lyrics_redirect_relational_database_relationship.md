a tabela Band deve conter os campos
nome texto(200)
genero precisa ter o relacionamento com a tabela MusicalGenre com relacionamento muitos para muitos N:N
fundacao data
finalizacao data
album -> precisa ter o relacionamento com a tabela Album com relacionamento um para muitos 1:N
band_description inteiro -> chave estrangeira para a tabela BandDescription com relacionamento um para um 1:1
timestamp datahora default current_timestamp

a tabela Album deve conter os campos
nome texto(200)
img texto(500)
genero -> precisa ter o relacionamento com a tabela MusicalGenre com relacionamento muitos para muitos N:N
musica -> precisa ter o relacionamento com a tabela Song com relacionamento muitos para muitos N:N
album_description inteiro -> chave estrangeira para a tabela AlbumDescription com relacionamento um para um 1:1
timestamp datahora default current_timestamp

a tabela Song deve conter os campos
nome texto(200)
lancamento data
tempo_musica inteiro
url_musica texto(500)
genre -> precisa ter o relacionamento com a tabela MusicalGenre com relacionamento muitos para muitos N:N
timestamp datahora default current_timestamp

a tabela MusicalGenre deve conter os campos
nome texto(200)
timestamp datahora default current_timestamp

a tabela BandDescription deve conter os campos
descricao texto(1000)

a tabela AlbumDescription deve conter os campos
descricao texto(1000)

Relacionamentos entre as tabelas: 
|Tabela A	| Tipo	 |Tabela B        | 
|-|-|-|
|Band	    | 1:N	 |Album           | 
|Band	    | N:N	 |MusicalGenre    | 
|Band	    | 1:1	 |BandDescription | 
|Album	    | N:N	 |MusicalGenre    | 
|Album	    | N:N	 |Song            | 
|Album	    | 1:1	 |AlbumDescription| 
|Song	    | N:N	 |MusicalGenre    | 


após atualizar é necessario executar os comandos abaixo
python manage.py makemigrations
python manage.py migrate