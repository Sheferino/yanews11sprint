import pytest

from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm


# проверка доступности формы отправки комментария
@pytest.mark.parametrize(
    'parametrized_client, form_on_page',
    (
        # Передаём фикстуры в параметры при помощи "ленивых фикстур":
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('client'), False),
    )
)
@pytest.mark.django_db
def test_pages_contains_form(parametrized_client, form_on_page, news):
    # Формируем URL.
    url = reverse('news:detail', args=(news.pk,))
    # Запрашиваем нужную страницу:
    response = parametrized_client.get(url)
    # Проверяем, есть ли объект формы в словаре контекста:
    assert ('form' in response.context) == form_on_page
    if form_on_page:
        # Проверяем, что объект формы (если есть) относится к нужному классу.
        assert isinstance(response.context['form'], CommentForm)


@pytest.mark.django_db
@pytest.mark.usefixtures('generate_news')
def test_news_count(client):
    # загружаем главную. Код ответа проверяется в тестах маршрутов
    url = reverse('news:home')
    response = client.get(url)
    # список объектов из словаря контекста
    object_list = response.context['object_list']
    # определяем количество записей
    news_count = object_list.count()
    assert (news_count == settings.NEWS_COUNT_ON_HOME_PAGE)


@pytest.mark.django_db
@pytest.mark.usefixtures('generate_news')
def test_news_order(client):
    # загружаем главную. Код ответа проверяется в тестах маршрутов
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    # Получаем даты новостей в том порядке, как они выведены на странице.
    all_dates = [news.date for news in object_list]
    # Сортируем полученный список по убыванию.
    sorted_dates = sorted(all_dates, reverse=True)
    # Проверяем, что исходный список был отсортирован правильно.
    assert all_dates == sorted_dates


@pytest.mark.django_db
@pytest.mark.usefixtures('generate_comments')
def test_comments_order(client, news):
    url = reverse('news:detail', args=(news.pk,))
    response = client.get(url)
    # Получаем объект новости по названию модели
    news = response.context['news']
    # Получаем все комментарии к новости из атрибута comment_set.
    # Создаётся автоматически при ForeignKey
    all_comments = news.comment_set.all()
    # Собираем временные метки всех комментариев.
    all_timestamps = [comment.created for comment in all_comments]
    # Сортируем временные метки, менять порядок сортировки не надо.
    sorted_timestamps = sorted(all_timestamps)
    # Проверяем, что временные метки отсортированы правильно.
    assert all_timestamps == sorted_timestamps
