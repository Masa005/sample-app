from django.test import TestCase
from account.factory import UserFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
import freezegun

User = get_user_model()

class LoginViewTest(TestCase):
    """
    LoginViewのテストクラス
    """
    def setUp(self):
        UserFactory(username='notActiveUser',is_active=False)
        UserFactory(username='activeUser',is_active=True)

    def test_get(self):
        """
        ログイン画面遷移テスト
        """
        url = reverse('account:login')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_post_success(self):
        """
        ログイン成功時テスト
        """
        params = dict(
            username ='activeUser',
            password ='sampleapp'
        )
        url = reverse('account:login')
        success_url = reverse('short_post:home')
        res = self.client.post(url,params,follow=True)
        #ログイン成功後リダイレクト先確認
        self.assertEqual(User.objects.filter(username='activeUser').count(),1)
        self.assertRedirects(res, success_url)

    def test_post_failure(self):
        """
        ログイン失敗時テスト
        """
        params = dict(
            username = 'notActiveUser',
            password = 'sampleapp'
        )
        url = reverse('account:login')
        res = self.client.post(url,params,follow=True)
        #リダイレクトしないことを確認
        self.assertEqual(res.status_code, 200)

class SignupViewTest(TestCase):
    """
    SignupViewのテストクラス
    """
    def test_get(self):
        """
        新規登録画面遷移テスト
        """
        url = reverse('account:signup_init')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_form_valid(self):
        """
        登録成功時のテスト
        """
        params = dict(
            username ='testuser',
            name = 'テストユーザー',
            email = 'test@example.com',
            birthday = '1999-9-9',
            password1 = 'sampleapp',
            password2 = 'sampleapp'
        )
        url = reverse('account:signup_init')
        success_url = reverse('account:signup_done')
        res = self.client.post(url,params,follow=True)
        #リダイレクト先確認
        self.assertRedirects(res, success_url)
        #仮登録確認
        self.assertEqual(User.objects.filter(username='testuser',is_active=False).count(),1)
        #メッセージが１つ送信されたことを確認
        self.assertEqual(len(mail.outbox), 1)
        #メッセージのタイトルが正しいことを確認
        self.assertEqual(mail.outbox[0].subject, 'SampleApp   -   会員登録確認')
        #送信先の確認
        self.assertEqual(mail.outbox[0].to,['test@example.com'])

    def test_form_invalid(self):
        """
        登録失敗時のテスト
        """
        params = dict(
            username ='testuser',
            name = 'テストユーザー',
            email = 'test@example.com',
            birthday = '1999-99-99',
            password1 = 'sampleapp',
            password2 = 'sampleapp'
        )
        url = reverse('account:signup_init')
        res = self.client.post(url,params,follow=True)
        #リダイレクトされないことを確認
        self.assertEqual(res.status_code, 200)
        #仮登録されていないことを確認
        self.assertEqual(User.objects.filter(username='testuser',is_active=False).count(),0)

class SignupCompleteViewTest(TestCase):
    """
    SignupCompleteViewのテストクラス
    """
    def Signup(self):
        """
        共通仮登録処理
        """
        params = dict(
            username ='testuser',
            name = 'テストユーザー',
            email = 'test@example.com',
            birthday = '1999-9-9',
            password1 = 'sampleapp',
            password2 = 'sampleapp'
        )
        url = reverse('account:signup_init')
        res = self.client.post(url,params,follow=True)
        return res

    def test_get_success(self):
        """
        本登録成功時
        """
        self.Signup()
        message = mail.outbox[0].body
        message_list = message.split('\n')
        url = message_list[6]
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        #本登録確認
        self.assertEqual(User.objects.filter(username='testuser',is_active=True).count(),1)

    def test_get_failure_expired(self):
        """
        本登録失敗時(期限切れ)
        """
        self.Signup()
        message = mail.outbox[0].body
        message_list = message.split('\n')
        url = message_list[6]
        error_url = reverse('sample_app:error')
        #現在日時を変更し、期限切れにする
        with freezegun.freeze_time('9999-1-1'):
            res = self.client.get(url)
            #エラー画面にリダイレクトすることを確認
            self.assertRedirects(res, error_url)
            #本登録されていないことを確認
            self.assertEqual(User.objects.filter(username='testuser',is_active=True).count(),0)

    def test_get_failure_bad_token(self):
        """
        本登録失敗時(不正なトークン)
        """
        self.Signup()
        url = 'http://testserver/sample_app/account/signup/complete/qqqqqqqqqqqqqqqqq/'
        error_url = reverse('sample_app:error')
        res = self.client.get(url)
        #エラー画面にリダイレクトすることを確認
        self.assertRedirects(res, error_url)
        #本登録されていないことを確認
        self.assertEqual(User.objects.filter(username='testuser',is_active=True).count(),0)

    def test_get_failure_not_exist(self):
        """
        本登録失敗時(ユーザーが存在しない)
        """
        self.Signup()
        message = mail.outbox[0].body
        message_list = message.split('\n')
        url = message_list[6]
        error_url = reverse('sample_app:error')
        #仮登録したユーザーを削除
        User.objects.filter(username='testuser',is_active=False).delete()
        res = self.client.get(url)
        #エラー画面にリダイレクトすることを確認
        self.assertRedirects(res, error_url)
        #本登録されていないことを確認
        self.assertEqual(User.objects.filter(username='testuser',is_active=True).count(),0)

    def test_get_failure_registered(self):
        """
        本登録失敗時(すでに登録済み)
        """
        self.Signup()
        message = mail.outbox[0].body
        message_list = message.split('\n')
        url = message_list[6]
        error_url = reverse('sample_app:error')
        self.client.get(url)
        #同じURLに2回目のアクセス
        res = self.client.get(url)
        #エラー画面にリダイレクトすることを確認
        self.assertRedirects(res, error_url)
