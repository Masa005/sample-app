from django.test import TestCase
from account.factory import UserFactory
from account.forms import CreateUserForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateUserFormTest(TestCase):
    """
    CreateUserFormのテストクラス
    """

    def setUp(self):
        """
        仮登録状態のユーザーと本登録済みのユーザーを用意
        """
        UserFactory(username='notActiveUser',
                    email='notActive@example.com', is_active=False)
        UserFactory(username='activeUser',
                    email='active@example.com', is_active=True)

    def test_clean_email_exist(self):
        """
        clean_emailメソッドのテスト
        同じメールアドレスで仮登録段階のアカウントが存在した場合
        """
        params = dict(
            username='testuser',
            name='テストユーザー',
            email='notActive@example.com',
            birthday='1999-9-9',
            password1='sampleapp',
            password2='sampleapp'
        )
        form = CreateUserForm(params)
        form.is_valid()
        form.clean_email()
        # notActiveUserのアカウントが削除されていればOK
        self.assertEqual(User.objects.filter(username='notActiveUser')
                         .count(), 0)
        # ActiveUserのアカウントが存在していればOK
        self.assertEqual(User.objects.filter(username='activeUser').count(), 1)

    def test_clean_email_not_exist(self):
        """
        clean_emailメソッドのテスト
        同じメールアドレスで仮登録段階のアカウントが存在しない場合
        """
        params = dict(
            username='testuser',
            name='テストユーザー',
            email='test@example.com',
            birthday='1999-9-9',
            password1='sampleapp',
            password2='sampleapp'
        )
        form = CreateUserForm(params)
        form.is_valid()
        form.clean_email()
        # notActiveUser,ActiveUserのアカウントが存在していればOK
        self.assertEqual(User.objects.filter(username='notActiveUser')
                         .count(), 1)
        self.assertEqual(User.objects.filter(username='activeUser').count(), 1)
