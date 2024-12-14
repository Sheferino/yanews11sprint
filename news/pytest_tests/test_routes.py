from http import HTTPStatus
from django.urls import reverse

import pytest
from pytest_django.asserts import assertRedirects


# проверки доступности для анонимов
@pytest.mark.parametrize(
    'name',  # Имя параметра функции.
    # Значения, которые будут передаваться в name.
    ('news:home', 'users:login', 'users:logout', 'users:signup')
)
@pytest.mark.django_db
def test_availability_for_anonymous_user(client, name):
    # используем встроенную фикстуру client из плагина pytest-django
    url = reverse(name)  # Получаем ссылку на нужный адрес.
    response = client.get(url)  # Выполняем запрос.
    assert response.status_code == HTTPStatus.OK


# доступность новости для анонимов
@pytest.mark.django_db
def test_availability_news(client, news):
    url = reverse('news:detail', args=(news.pk,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


# доступ к работе с комментарием для автора
@pytest.mark.parametrize(
    'urlname',  # Имя параметра функции.
    # Значения, которые будут передаваться в name.
    ('news:edit', 'news:delete')
)
@pytest.mark.django_db
def test_comment_author(comment, author_client, urlname):
    url = reverse(urlname, args=(comment.pk,))
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


# доступ к работе с комментарием для неавтора
@pytest.mark.parametrize(
    'urlname',  # Имя параметра функции.
    # Значения, которые будут передаваться в name.
    ('news:edit', 'news:delete')
)
@pytest.mark.django_db
def test_comment_notauthor(comment, not_author_client, urlname):
    url = reverse(urlname, args=(comment.pk,))
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


# доступ к работе с комментарием для анонима
@pytest.mark.parametrize(
    'urlname',  # Имя параметра функции.
    # Значения, которые будут передаваться в name.
    ('news:edit', 'news:delete')
)
@pytest.mark.django_db
def test_comment_anonymous(comment, client, urlname):
    url = reverse(urlname, args=(comment.pk,))
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
