# conftest.py
import pytest

# тестовый клиент
from django.test.client import Client

from news.models import News, Comment


# объект новости в БД
@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок пробной новости',
        text='Просто текст',
    )
    return news

# пользователь-автор


@pytest.fixture
def author(django_user_model):
    # Используем встроенную фикстуру для модели пользователей django_user_model.
    return django_user_model.objects.create(username='Автор')


# пользователь - не автор
@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Мимокрокодил')


# клиент автора
@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)  # Логиним автора в клиенте.
    return client


# клиент неавтора
@pytest.fixture
def not_author_client(not_author):  # Вызываем фикстуру автора.
    client = Client()
    client.force_login(not_author)  # Логиним автора в клиенте.
    return client


# комментарий автора к новости
@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='кг/ам'
    )
    return comment


'''
# фикстура
@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Автор2')





@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)  # Логиним неавтора-пользователя в клиенте.
    return client




@pytest.fixture
# Фикстура запрашивает другую фикстуру создания заметки.
def slug_for_args(note):
    # И возвращает кортеж, который содержит slug заметки.
    # На то, что это кортеж, указывает запятая в конце выражения.
    return (note.slug,)


@pytest.fixture
def form_data():
    return {
        'title': 'Это новая заметка',
        'text': 'С другим текстом',
        'slug': 'new-slug'
    }
'''
