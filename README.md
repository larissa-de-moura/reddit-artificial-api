# Reddit Hot Posts API

Este projeto tem a ideia de disponibilizar os posts que estão *hot* dentro do subreddit */r/artificial*.
A base de dados que a API consulta já vai carregada com alguns registros (~1k).

A API possui 3 endpoints:
- /hot_posts 
- /hot_posts/{dt_ini}/{dt_fin}/{sort_by}
- /hot_posts/{sort_by}

<br />

## Instrucoes

Após clonar o repositório localmente, entre no diretório principal e rode:
```
docker build -t reddit-api:latest .
```
Depois:
```
docker run -p 80:80 reddit-api
```
<br />

## Endpoints


### **/hot_posts**

Os métodos aceitos são: [POST, PUT]. Este endpoint espera um payload no formato abaixo:
```
{
      "title": string,
       "author": string,
       "ts_creation": string,
       "num_ups": integer,
       "num_comments": integer
}
```

Onde "title" e "author" são os campos de título e autor, "ts_creation" é a string date da criação do post (também aceita epoch), e "num_ups" e "num_comments" são a quantidade de ups e comentários, respectivamente.
*Retorna:*
> {
>      "title": string,
>       "author": string,
>       "ts_creation": string,
>       "num_ups": integer,
>       "num_comments": integer
>    }

<br />

<br />

### **/hot_posts/{sort_by}**

Os métodos aceitos são: [GET]. Este endpoint espera uma url com os parâmetros [ sort_by]. 
Os sortings possíveis são:
> [ups, comments]

<br />

Esse endpoint retorna uma lista de usuários ordenados pelo sorting passado, junto com a quantidade daquele sorting (ex.: qtd de Ups)

```
/hot_posts/comments
```
*Retorna:*
> list[100] = [{
>      "title": string,
>       "{sort_by}": int
>    }, ... {99}
>]

<br />

<br />

### **/hot_posts/{dt_ini}/{dt_fin}/{sort_by}**
Os métodos aceitos são: [GET]. Este endpoint espera uma url com os parâmetros [dt_ini, dt_fin, sort_by]. 
Os sortings possíveis são:
> [ups, comments]

<br />

As datas devem obedecer a especificação:
```
YYYY-MM-DD['T'hh:mm[:ss][:ms]]
```

Os parâmetros de hora, minuto, segundo e milissegundo são **opcionais**.

A data de início (dt_ini) deve ser maior que a final, ambas devem ter o mesmo formato, e respeitar a ISO8601.
Exemplo:
```
/hot_posts/2021-01-05T00:00:00/2021-01-19T07:30:00/comments
```
*Retorna:*
> list[100] = [{
>      "title": string,
>       "author": string,
>       "ts_creation": string,
>       "num_ups": integer,
>       "num_comments": integer
>    }, ... {99}
>]

