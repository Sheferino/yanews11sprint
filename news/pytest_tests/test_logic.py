from django.urls import reverse
from pytest_django.asserts import assertFormError
import pytest

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


# аноним не может отправить комментарий
@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(news, client, comment_form_data):
    url = reverse('news:detail', args=(news.pk,))
    # Через анонимный клиент пытаемся создать заметку:
    response = client.post(url, data=comment_form_data)
    # убеждаемся, что новый комментарий не создан
    assert Comment.objects.count() == 0


# авторизованный пользователь может создать комментарий
@pytest.mark.django_db
def test_user_can_create_comment(author_client, news, comment_form_data):
    url = reverse('news:detail', args=(news.pk,))
    # В POST-запросе отправляем данные, полученные из фикстуры form_data:
    response = author_client.post(url, data=comment_form_data)
    # убеждаемся, что комментарий попал в БД
    assert Comment.objects.count() == 1
    # Чтобы проверить значения полей заметки -
    # получаем её из базы при помощи метода get():
    new_comment = Comment.objects.get()
    # Сверяем атрибуты объекта с ожидаемыми.
    assert new_comment.news == comment_form_data['news']
    assert new_comment.text == comment_form_data['text']
    assert new_comment.author == comment_form_data['author']
    # но если хоть одна из этих проверок провалится -
    # весь тест можно признать провалившимся, остальное проверять бессмысленно


# форма не пропускает запрещённые слова в комментарии
@pytest.mark.django_db
def test_user_cant_use_bad_words(news, author_client, comment_form_data):
    url = reverse('news:detail', args=(news.pk,))
    # Формируем данные для отправки формы;
    # тест проверяет первое же плохое слово
    comment_form_data['text'] = f'Плохая музыка, {BAD_WORDS[0]}, очень'
    # Отправляем запрос через авторизованный клиент.
    response = author_client.post(url, data=comment_form_data)
    # Проверяем, есть ли в ответе ошибка формы.
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    # Дополнительно убедимся, что комментарий не был создан.
    assert Comment.objects.count() == 0


@pytest.mark.parametrize(
    'parametrized_client, edition_success',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('not_author_client'), False),
    )
)
# автор может редактировать комментарий
def test_can_edit_comment(parametrized_client,
                          edition_success,
                          comment):
    comment_edited_text = comment.text + '_edited'
    url = reverse('news:edit', args=(comment.pk,))
    # Выполняем запрос на редактирование
    response = parametrized_client.post(
        url, data={'text': comment_edited_text})
    # Обновляем объект комментария.
    comment.refresh_from_db()
    # Проверяем, что текст комментария соответствует обновленному (или нет)
    assert (comment.text == comment_edited_text) == edition_success


@pytest.mark.parametrize(
    'parametrized_client, deletion_success',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('not_author_client'), False),
    )
)
# автор может удалить комментарий
def test_can_delete_comment(parametrized_client,
                            deletion_success,
                            comment):
    url = reverse('news:delete', args=(comment.pk,))
    # убеждаемся, что комментарий в БД есть
    assert Comment.objects.count() == 1
    # Выполняем запрос на удаление
    response = parametrized_client.post(url)
    # убеждаемся, что комент удалён (или нет)
    assert (Comment.objects.count() == 0) == deletion_success
