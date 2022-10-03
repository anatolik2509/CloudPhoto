import boto_client_config


index_template = '''
<!doctype html>
<html>
    <head>
        <title>Фотоархив</title>
    </head>
<body>
    <h1>Фотоархив</h1>
    <ul>
        {album_list}
    </ul>
</body>
'''


error_template = '''
<!doctype html>
<html>
    <head>
        <title>Фотоархив</title>
    </head>
<body>
    <h1>Ошибка</h1>
    <p>Ошибка при доступе к фотоархиву. Вернитесь на <a href="index.html">главную страницу</a> фотоархива.</p>
</body>
</html>
'''

album_template = '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/galleria/1.6.1/themes/classic/galleria.classic.min.css" />
        <style>
            .galleria{{ width: 960px; height: 540px; background: #000 }}
        </style>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/galleria/1.6.1/galleria.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/galleria/1.6.1/themes/classic/galleria.classic.min.js"></script>
    </head>
    <body>
        <div class="galleria">
            {photo_list}
        </div>
        <p>Вернуться на <a href="index.html">главную страницу</a> фотоархива</p>
        <script>
            (function() {{
                Galleria.run('.galleria');
            }}());
        </script>
    </body>
</html>
'''

album_list_e = '''
<li><a href="album{n}.html">{name}</a></li>
'''

photo_list_e = '''
<img src="{url}" data-title="{name}">
'''


def make_site():
    s3_res = boto_client_config.get_resource()
    s3_client = boto_client_config.get_client()
    objects = s3_res.Bucket(boto_client_config.get_bucket()).objects.all()
    objects = [obj for obj in objects]
    objects = set(map(lambda name: name[0], filter(lambda arr: len(arr) > 1, map(lambda o: o.key.split('/'), objects))))
    make_index_page(objects, s3_client)
    make_error_page(s3_client)
    make_album_pages(objects, s3_client, s3_res)
    open_site(s3_client, s3_res)


def make_error_page(client):
    client.put_object(Bucket=boto_client_config.get_bucket(), Key='error.html', Body=error_template)


def make_index_page(albums, client):
    res_str = ''
    for i, a in enumerate(albums):
        res_str += album_list_e.format(n=i, name=a)
    index = index_template.format(album_list=res_str)
    client.put_object(Bucket=boto_client_config.get_bucket(), Key='index.html', Body=index)


def make_album_pages(albums, client, res):
    for i, album in enumerate(albums):
        photos = res.Bucket(boto_client_config.get_bucket()).objects.filter(Prefix=album + '/')
        photos = list(photos)
        photo_list = ''
        for photo in photos:
            photo_list += photo_list_e.format(url=photo.key, name=photo.key)
        album_page = album_template.format(photo_list=photo_list)
        client.put_object(Bucket=boto_client_config.get_bucket(), Key=f'album{i}.html', Body=album_page)


def open_site(client, res):
    website_configuration = {
        'ErrorDocument': {'Key': 'error.html'},
        'IndexDocument': {'Suffix': 'index.html'},
    }
    client.put_bucket_website(Bucket=boto_client_config.get_bucket(),
                              WebsiteConfiguration=website_configuration)
    res.BucketAcl(boto_client_config.get_bucket()).put(ACL='public-read')
    print(f'https://{boto_client_config.get_bucket()}.website.yandexcloud.net/')
