# API FindFood

Essa é uma API desenvolvida em Django restframework que 
tem como objetivo catalogar todas as informações de restaurantes no 
município de Ituiutaba/MG.

## Para configurar o uso

Há um arquivo necessário para a configuração de variáveis de 
ambiente. O `.env`, o template dele é o seguinte:

````dotenv
DB_ENGINE=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

SECRET_KEY=

CLOUD_NAME=
API_KEY=
API_SECRET=
````

Os parâmetros que tem como prefixo DB, são as variáveis referêntes ao
banco de dados. Já as variáveis `CLOUD_NAME`, `API_KEY` e `API_SECRET`, 
são para a configuração do provedor de imagens em núvem `cloudinary`.

### Instalação do cloudinary

No arquivo `settings.py` coloque as seguintes informações.

````python
import cloudinary
import cloudinary.uploader
import cloudinary.api

INSTALLED_APPS = [
    ...,
    'cloudinary',
]

...

cloudinary.config(
    cloud_name='',
    api_key='',
    api_secret=''
)
````

Sinta-se livre para utilizar outro provedor de imagens.

## Para executar

Para executar utilize o comando:

````commandline
python manage.py runserver
````

## Rotas

### Restaurante

`post /restaurant/` entrada:

````json
{
  "name": "nome_do_restaurante",
  "type": "tipo_do_restaurante",
  "img": "url_da_img"
}
````

No caso da url, utilizei o postman no modo de envio de form para 
anexar a imagem. Caso queria adicionar de outra forma procure a documentação
do `cloudinary` ou do provedor que esteja utilizando.

`get /restaurant/` saída:

````json
[
  {
    "id":"id_do_restaurante",
    "name": "nome_do_restaurante",
    "type": "tipo_do_restaurante",
    "restaurant_address": {
      "id": "id_do_address",
      "line1": "linha_1_do_restaurante",
      "line2": "linha_2_do_restaurante",
      "number": "número_do_restaurante",
      "postal_code": "CEP_do_restaurante"
    },
    "opening_days": [
      {
        "id": "id_dos_horários_de_funcionamento",
        "interval_id": {
          "id": "id_do_intervalo_de_funcionamento",
          "day": "dia",
          "open": "hora_que_abre",
          "close": "hora_que_fecha"
        }
      }
    ],
    "socials": [
      {
        "type": "tipo_de_canal_de_contato",
        "information": "url_do_canal_de_contato"
      }
    ],
    "img": "url_da_imagem_do_restaurante",
    "is_open": "se_o_restaurante_está_aberto"
  }
]
````

`get /restaurant/{id}/` saída:

````json
{
"id":"id_do_restaurante",
"name": "nome_do_restaurante",
"type": "tipo_do_restaurante",
"restaurant_address": {
  "id": "id_do_address",
  "line1": "linha_1_do_restaurante",
  "line2": "linha_2_do_restaurante",
  "number": "número_do_restaurante",
  "postal_code": "CEP_do_restaurante"
},
"opening_days": [
  {
    "id": "id_dos_horários_de_funcionamento",
    "interval_id": {
      "id": "id_do_intervalo_de_funcionamento",
      "day": "dia",
      "open": "hora_que_abre",
      "close": "hora_que_fecha"
    }
  }
],
"socials": [
  {
    "type": "tipo_de_canal_de_contato",
    "information": "url_do_canal_de_contato"
  }
],
"img": "url_da_imagem_do_restaurante",
"is_open": "se_o_restaurante_está_aberto"
}
````

`put /restaurant/{id}/ entrada:`

````json
{
  "name": "nome_do_restaurante",
  "type": "tipo_do_restaurante",
  "img": "url_da_img"
}
````

`patch /restaurant/{id}/ entrada:`

````json
{
  "name": "nome_do_restaurante",
  "type": "tipo_do_restaurante",
  "img": "url_da_img"
}
````

`delete /restaurante/{id}/`

### Endereço

`post /address/` entrada:

````json
{
  "line1": "line_1_do_restaurante",
  "line2": "line_2_do_restaurente",
  "number": "número_do_restaurante",
  "postal_code": "CEP_do_restaurante"
}
````

`put /address/{id}/` entrada:

````json
{
  "line1": "line_1_do_restaurante",
  "line2": "line_2_do_restaurente",
  "number": "número_do_restaurante",
  "postal_code": "CEP_do_restaurante"
}
````

`patch /address/{id}/` entrada:

````json
{
  "line1": "line_1_do_restaurante",
  "line2": "line_2_do_restaurente",
  "number": "número_do_restaurante",
  "postal_code": "CEP_do_restaurante"
}
````

`delete /address/{id}/`

### Schedule

`post /schedule/` entrada:

````json
[
  {
    "interval_id": {
      "day": "dia",
      "open": "hora_que_abre",
      "close": "hora_que_fecha"
    },
    "restaurant_id": "id_do_restaurante"
  }
]
````

ou

````json
{
    "interval_id": {
      "day": "dia",
      "open": "hora_que_abre",
      "close": "hora_que_fecha"
    },
    "restaurant_id": "id_do_restaurante"
}
````

`put /schedule/{interval_id__day}` entrada:

````json
{
    "interval_id": {
      "day": "dia",
      "open": "hora_que_abre",
      "close": "hora_que_fecha"
    },
    "restaurant_id": "id_do_restaurante"
}
````

com o `interval_id__day` sendo o dia de 
um dos intervalos escolhidos.

`patch /schedule/{interval_id__day}` entrada:

````json
{
    "interval_id": {
      "day": "dia",
      "open": "hora_que_abre",
      "close": "hora_que_fecha"
    },
    "restaurant_id": "id_do_restaurante"
}
````

com o `interval_id__day` sendo o dia de 
um dos intervalos escolhidos.

`delete /schedule/{interval_id__day}` 
com o `interval_id__day` sendo o dia de 
um dos intervalos escolhidos.

### Contact

`post /contact/`

````json
[
  {
    "type": "tipo_de_canal_de_contato",
    "information": "url_do_canal_de_contato",
    "restaurant_id": "id_do_restaurante"
  }
]
````

ou

````json
{
    "type": "tipo_de_canal_de_contato",
    "information": "url_do_canal_de_contato",
    "restaurant_id": "id_do_restaurante"
}
````

`put /contact/{id}` entrada: 

````json
{
    "type": "tipo_de_canal_de_contato",
    "information": "url_do_canal_de_contato",
    "restaurant_id": "id_do_restaurante"
}
````

`patch /contact/{id}` entrada:

````json
{
    "type": "tipo_de_canal_de_contato",
    "information": "url_do_canal_de_contato",
    "restaurant_id": "id_do_restaurante"
}
````

`delete /contact/{id}`