from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from short_post.factory import PostContentFactory
from account.factory import UserFactory
from short_post.models import PostContent
import datetime
import json

User = get_user_model()

class HomeViewTest(TestCase):
    """
    HomeViewのテストクラス
    """
    def setUp(self):
        UserFactory(username='testUser')
        test_user = User.objects.get(username='testUser')
        test_date_joined = datetime.datetime(2019, 1, 1)
        for i in range(100):
            test_content = i + 1
            test_date_joined = test_date_joined + datetime.timedelta(days=i)
            PostContentFactory(content=test_content,user=test_user,date_joined=test_date_joined)

    def login(self):
        """
        共通ログイン処理
        """
        self.client.login(username='testUser', password='sampleapp')

    def test_get_success(self):
        """
        ホーム画面遷移テスト(成功時)
        """
        url = reverse('short_post:home')
        self.login()
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_get_failure(self):
        """
        ホーム画面遷移テスト(失敗時)
        """
        url = reverse('short_post:home')
        redirect_url = reverse('account:login')
        res = self.client.get(url,follow=True)
        self.assertRedirects(res, redirect_url)

    def test_get_context_data(self):
        """
        初期表示投稿内容一覧確認テスト
        """
        url = reverse('short_post:home')
        self.login()
        res = self.client.get(url)
        user_post_list = res.context['user_post_list']
        count = 0
        test_content_list = list()
        for i in reversed(range(91,101)):
            test_content_list.append(str(i))

        for post in user_post_list:
            #初期表示投稿内容一覧確認
            self.assertEqual(post.content,test_content_list[count])
            count+=1

    def test_post_load_api_succes(self):
        """
        投稿一覧取得APIテスト
        存在するページのリクエスト時
        """
        url = reverse('short_post:post_load') + '?page=5'
        self.login()
        res = self.client.get(url)
        res_content = json.loads(res.content)
        user_post_list = res_content['user_post_list']
        count = 0
        test_content_list = list()
        for i in reversed(range(51,61)):
            test_content_list.append(str(i))

        for post in user_post_list:
            #投稿内容一覧確認
            self.assertEqual(post['content'],test_content_list[count])
            count+=1

    def test_post_load_api_not_exist(self):
        """
        投稿一覧取得APIテスト
        存在しないページのリクエスト時
        """
        url = reverse('short_post:post_load') + '?page=11'
        self.login()
        res = self.client.get(url)
        self.assertEqual(res.status_code, 204)

    def test_post_load_api_empty(self):
        """
        投稿一覧取得APIテスト
        空のリクエスト時
        """
        url = reverse('short_post:post_load')
        self.login()
        res = self.client.get(url)
        self.assertEqual(res.status_code, 204)

    def test_form_valid(self):
        """
        投稿成功時のテスト

        """
        params = dict(
            content ='テスト投稿内容',
        )
        url = reverse('short_post:home')
        success_url = reverse('short_post:home')
        self.login()
        res = self.client.post(url,params,follow=True)
        #リダイレクト先確認
        self.assertRedirects(res, success_url)
        #投稿内容登録確認
        self.assertEqual(PostContent.objects.filter(user = User.objects.get(username='testUser')
                                                    ,content='テスト投稿内容').count(),1)

    def test_form_invalid(self):
        """
        投稿失敗時のテスト
        """
        #文字数超過している投稿内容

        test_content = 'テスト投稿内容あああああああああああああああああああああ' + \
            'あああああああああああああああああああああああああああああああああああああ' + \
            'あああああああああああああああああああああああああああああああああああああ' + \
            'あああああああああああああああああああああああああああああああああああああ' + \
            'ああああああああああああああああああああああああああああああああああ'
        params = dict(content = test_content,)
        url = reverse('short_post:home')
        self.login()
        res = self.client.post(url,params,follow=True)
        #リダイレクトしていないことを確認
        self.assertEqual(res.status_code, 200)
        #投稿内容登録確認
        self.assertEqual(PostContent.objects.filter(user = User.objects.get(username='testUser')
                                                    ,content=test_content).count(),0)
