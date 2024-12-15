from datetime import datetime, timedelta

import pytest

from django.conf import settings
from django.test.client import Client
from django.utils import timezone

from news.models import News, Comment


COMMENT_FROM_FORM = 'кг/ам' 

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
    # Встроенная фикстура для модели пользователей django_user_model.
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
        text='кг/ам изначальный'
    )
    return comment


# массив новостей
@pytest.fixture
def generate_news():
    today = datetime.today()
    news_list = []
    for idx in range(settings.NEWS_COUNT_ON_HOME_PAGE):
        news_list.append(News(
            title=f'Заголовок пробной новости {idx}',
            text=f'Просто текст {idx} новости',
            date=today - timedelta(days=idx)
        ))
    News.objects.bulk_create(news_list)


# массив комментариев
@pytest.fixture
def generate_comments(news, author):
    # Запоминаем текущее время (с указание часового пояса):
    now = timezone.now()
    # Создаём несколько комментариев с разным временем в цикле.
    for idx in range(5):
        # Создаём объект и записываем его в переменную.
        comment = Comment.objects.create(
            news=news, author=author, text=f'Кг/ам # {idx}',
        )
        # Сразу после создания меняем время создания комментария.
        # изначально его задать нельзя, поскольку при создании объекта это
        # поле заполняется автоматически
        comment.created = now + timedelta(days=idx)
        # И сохраняем эти изменения.
        comment.save()


# заполненная форма комментария
@pytest.fixture
def comment_form_data(news, author):
    return {
        'news': news,
        'author': author,
        'text': 'Комментарий из формы'
    }

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
