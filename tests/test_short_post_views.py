from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from short_post.factory import PostContentFactory
from account.factory import UserFactory
from short_post.models import PostContent
import datetime
import json
from short_post.factory import FavoriteFactory
from short_post.models import Favorite

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
            PostContentFactory(content=test_content,
                               user=test_user, date_joined=test_date_joined)
            if i <= 2:
                test_post_content = PostContent\
                    .objects.get(user=test_user, content=test_content)
                FavoriteFactory(post_content=test_post_content, user=test_user,
                                date_joined=test_date_joined)

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
        res = self.client.get(url, follow=True)
        self.assertRedirects(res, redirect_url)

    def test_get_context_data(self):
        """
        初期表示投稿内容一覧確認テスト
        """
        url = reverse('short_post:home')
        self.login()
        res = self.client.get(url)
        user_post_list = res.context['user_post_list']
        user_favorite_list = res.context['user_favorite_list']
        post_content_list = list()
        fav_content_list = list()
        for i in reversed(range(91, 101)):
            post_content_list.append(str(i))

        for i in reversed(range(1, 4)):
            fav_content_list.append(str(i))

        count = 0
        for post in user_post_list:
            # 初期表示投稿内容一覧確認
            self.assertEqual(post.content, post_content_list[count])
            count += 1

        count = 0
        for fav in user_favorite_list:
            # 初期表示お気に入り一覧確認
            self.assertEqual(fav.post_content.content, fav_content_list[count])
            count += 1

    def test_form_valid(self):
        """
        投稿成功時のテスト

        """
        params = dict(
            content='テスト投稿内容',
        )
        url = reverse('short_post:home')
        success_url = reverse('short_post:home')
        self.login()
        res = self.client.post(url, params, follow=True)
        # リダイレクト先確認
        self.assertRedirects(res, success_url)
        # 投稿内容登録確認
        self.assertEqual(PostContent.objects.filter
                         (user=User.objects.get(username='testUser'),
                          content='テスト投稿内容').count(), 1)

    def test_form_invalid(self):
        """
        投稿失敗時のテスト
        """
        # 文字数超過している投稿内容

        test_content = 'テスト投稿内容あああああああああああああああああああああ' + \
            'あああああああああああああああああああああああああああああああああああああ' + \
            'あああああああああああああああああああああああああああああああああああああ' + \
            'あああああああああああああああああああああああああああああああああああああ' + \
            'ああああああああああああああああああああああああああああああああああ'
        params = dict(content=test_content,)
        url = reverse('short_post:home')
        self.login()
        res = self.client.post(url, params, follow=True)
        # リダイレクトしていないことを確認
        self.assertEqual(res.status_code, 200)
        # 投稿内容登録確認
        self.assertEqual(PostContent.objects.filter
                         (user=User.objects.get(username='testUser'),
                          content=test_content).count(), 0)


class TimeLineView(TestCase):
    """
    TimeLineViewのテストクラス
    """
    def setUp(self):
        UserFactory(username='testUser')
        UserFactory(username='testUser2')
        UserFactory(username='testUser3')
        test_user = User.objects.get(username='testUser')
        test_user2 = User.objects.get(username='testUser2')
        test_user3 = User.objects.get(username='testUser3')
        test_date_joined = datetime.datetime(2019, 1, 1)
        for i in range(100):
            test_content = i + 1
            test_date_joined = test_date_joined + datetime.timedelta(days=i)

            if test_content % 2 != 0:
                PostContentFactory(content=test_content,
                                   user=test_user,
                                   date_joined=test_date_joined)
            elif test_content % 2 == 0 and test_content % 10 != 0:
                PostContentFactory(content=test_content,
                                   user=test_user2,
                                   date_joined=test_date_joined)
            else:
                PostContentFactory(content=test_content,
                                   user=test_user3,
                                   date_joined=test_date_joined)

    def login(self):
        """
        共通ログイン処理
        """
        self.client.login(username='testUser', password='sampleapp')

    def test_get_success(self):
        """
        タイムライン画面遷移テスト(成功時)
        """
        url = reverse('short_post:timeline')
        self.login()
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_get_failure(self):
        """
        タイムライン画面遷移テスト(失敗時)
        """
        url = reverse('short_post:timeline')
        redirect_url = reverse('account:login')
        res = self.client.get(url, follow=True)
        self.assertRedirects(res, redirect_url)

    def test_get_context_data(self):
        """
        初期表示投稿内容一覧確認テスト
        """
        url = reverse('short_post:timeline')
        self.login()
        res = self.client.get(url)
        all_post_list = res.context['all_post_list']
        post_content_list = list()
        user_list = list()
        for i in reversed(range(91, 101)):
            post_content_list.append(str(i))
            if i % 2 != 0:
                user_list.append('testUser')
            elif i % 2 == 0 and i % 10 != 0:
                user_list.append('testUser2')
            else:
                user_list.append('testUser3')

        count = 0
        for post in all_post_list:
            # 初期表示投稿内容一覧確認
            self.assertEqual(post.content, post_content_list[count])
            self.assertEqual(post.user.username, user_list[count])
            count += 1

    def test_form_valid(self):
        """
        投稿成功時のテスト

        """
        params = dict(
            content='テスト投稿内容',
        )
        url = reverse('short_post:timeline')
        success_url = reverse('short_post:timeline')
        self.login()
        res = self.client.post(url, params, follow=True)
        # リダイレクト先確認
        self.assertRedirects(res, success_url)
        # 投稿内容登録確認
        self.assertEqual(PostContent.objects.filter
                         (user=User.objects.get(username='testUser'),
                          content='テスト投稿内容').count(), 1)

    def test_form_invalid(self):
        """
        投稿失敗時のテスト
        """
        # 文字数超過している投稿内容

        test_content = 'テスト投稿内容あああああああああああああああああああああ' + \
            'あああああああああああああああああああああああああああああああああああああ' + \
            'あああああああああああああああああああああああああああああああああああああ' + \
            'あああああああああああああああああああああああああああああああああああああ' + \
            'ああああああああああああああああああああああああああああああああああ'
        params = dict(content=test_content,)
        url = reverse('short_post:timeline')
        self.login()
        res = self.client.post(url, params, follow=True)
        # リダイレクトしていないことを確認
        self.assertEqual(res.status_code, 200)
        # 投稿内容登録確認
        self.assertEqual(PostContent.objects.filter
                         (user=User.objects.get(username='testUser'),
                          content=test_content).count(), 0)


class PostLoadApiTest(TestCase):
    """
    post_load_apiのテストクラス
    """
    def setUp(self):
        UserFactory(username='testUser')
        test_user = User.objects.get(username='testUser')
        test_date_joined = datetime.datetime(2019, 1, 1)
        for i in range(100):
            test_content = i + 1
            test_date_joined = test_date_joined + datetime.timedelta(days=i)
            PostContentFactory(content=test_content,
                               user=test_user, date_joined=test_date_joined)

    def login(self):
        """
        共通ログイン処理
        """
        self.client.login(username='testUser', password='sampleapp')

    def test_post_load_api_succes(self):
        """
        投稿一覧取得APIテスト
        存在するページのリクエスト時
        """
        url = reverse('short_post:post_load') + '?page=5&user-name=testUser'
        self.login()
        res = self.client.get(url)
        res_content = json.loads(res.content)
        user_post_list = res_content['user_post_list']
        count = 0
        test_content_list = list()
        for i in reversed(range(51, 61)):
            test_content_list.append(str(i))

        for post in user_post_list:
            # 投稿内容一覧確認
            self.assertEqual(post['content'], test_content_list[count])
            count += 1

    def test_post_load_api_not_exist(self):
        """
        投稿一覧取得APIテスト
        存在しないページのリクエスト時
        """
        url = reverse('short_post:post_load') + '?page=11&user-name=testUser'
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


class FavLoadApiTest(TestCase):
    """
    fav_load_apiのテストクラス
    """
    def setUp(self):
        UserFactory(username='testUser')
        test_user = User.objects.get(username='testUser')
        test_date_joined = datetime.datetime(2019, 1, 1)
        for i in range(100):
            test_content = i + 1
            test_date_joined = test_date_joined + datetime.timedelta(days=i)
            PostContentFactory(content=test_content,
                               user=test_user, date_joined=test_date_joined)

            if i >= 24 and i <= 34:
                test_post_content = PostContent\
                    .objects.get(user=test_user, content=test_content)
                FavoriteFactory(post_content=test_post_content, user=test_user,
                                date_joined=test_date_joined)

    def login(self):
        """
        共通ログイン処理
        """
        self.client.login(username='testUser', password='sampleapp')

    def test_fav_load_api_succes(self):
        """
        お気に入り一覧取得APIテスト
        存在するページのリクエスト時
        """
        url = reverse('short_post:fav_load') + '?page=1&user-name=testUser'
        self.login()
        res = self.client.get(url)
        res_content = json.loads(res.content)
        user_favorite_list = res_content['user_favorite_list']
        count = 0
        test_content_list = list()
        for i in reversed(range(25, 36)):
            test_content_list.append(str(i))

        for fav in user_favorite_list:
            # お気に入り一覧確認
            self.assertEqual(fav['post_content']['content'],
                             test_content_list[count])
            count += 1

    def test_fav_load_api_not_exist(self):
        """
        お気に入り一覧取得APIテスト
        存在しないページのリクエスト時
        """
        url = reverse('short_post:post_load') + '?page=11&user-name=testUser'
        self.login()
        res = self.client.get(url)
        self.assertEqual(res.status_code, 204)

    def test_fav_load_api_empty(self):
        """
        お気に入り一覧取得APIテスト
        空のリクエスト時
        """
        url = reverse('short_post:post_load')
        self.login()
        res = self.client.get(url)
        self.assertEqual(res.status_code, 204)


class FavoriteAddApiTest(TestCase):
    """
    favorite_add_apiのテストクラス
    """
    def setUp(self):
        UserFactory(username='testUser')
        test_user = User.objects.get(username='testUser')
        test_date_joined = datetime.datetime(2019, 1, 1)
        PostContentFactory(post_id='624d138851cf4474bf2e18be8be50a1e',
                           content='test',
                           user=test_user,
                           date_joined=test_date_joined)
        FavoriteFactory(post_content__post_id='9758ebaa3fa34110'
                        'aa3dbde31eaf40c8',
                        post_content__content='test_favlite',
                        user=test_user)

    def login(self):
        """
        共通ログイン処理
        """
        self.client.login(username='testUser', password='sampleapp')

    def test_favorite_add_api_succes(self):
        """
        お気に入り登録APIテスト
        登録成功時
        """
        url = reverse('short_post:favorite_add')
        self.login()
        test_post_id = '624d138851cf4474bf2e18be8be50a1e'
        params = dict(post_id=test_post_id,)
        res = self.client.post(url, params)
        res_content = json.loads(res.content)
        status = res_content['status']
        # APIの応答ステータスを確認
        self.assertEqual(status, '200')
        # お気に入り登録されていることを確認
        self.assertEqual(Favorite.objects.filter(
            post_content__post_id='624d138851cf4474bf2e18be8be50a1e'
            ).count(), 1)

    def test_favorite_add_api_exist(self):
        """
        お気に入り登録APIテスト
        すでにお気に入り登録されている場合
        """
        url = reverse('short_post:favorite_add')
        self.login()
        test_post_id = '9758ebaa3fa34110aa3dbde31eaf40c8'
        params = dict(post_id=test_post_id,)
        res = self.client.post(url, params)
        res_content = json.loads(res.content)
        status = res_content['status']
        # APIの応答ステータスを確認
        self.assertEqual(status, '204')
        # お気に入り登録されていないことを確認
        self.assertEqual(Favorite.objects.filter(
            post_content__post_id='9758ebaa3fa34110aa3dbde31eaf40c8',
            user__username='testUser').count(), 1)

    def test_favorite_add_api_value_error(self):
        """
        お気に入り登録APIテスト
        不正なリクエスト時
        """
        url = reverse('short_post:favorite_add')
        self.login()
        test_post_id = '不正なリクエスト'
        params = dict(post_id=test_post_id,)
        res = self.client.post(url, params)
        res_content = json.loads(res.content)
        status = res_content['status']
        # APIの応答ステータスを確認
        self.assertEqual(status, '204')


class FavoriteDeleteApiTest(TestCase):
    """
    favorite_delete_apiのテストクラス
    """
    def setUp(self):
        UserFactory(username='testUser')
        test_user = User.objects.get(username='testUser')
        FavoriteFactory(post_content__post_id='9758ebaa3fa34110'
                        'aa3dbde31eaf40c8',
                        post_content__content='test_favlite',
                        user=test_user)

    def login(self):
        """
        共通ログイン処理
        """
        self.client.login(username='testUser', password='sampleapp')

    def test_favorite_delete_api_succes(self):
        """
        お気に入り削除APIテスト
        削除成功時
        """
        url = reverse('short_post:favorite_delete')
        self.login()
        test_post_id = '9758ebaa3fa34110aa3dbde31eaf40c8'
        params = dict(post_id=test_post_id,)
        res = self.client.post(url, params)
        res_content = json.loads(res.content)
        status = res_content['status']
        # APIの応答ステータスを確認
        self.assertEqual(status, '200')
        # お気に入り削除されていることを確認
        self.assertEqual(Favorite.objects.filter(
            post_content__post_id='9758ebaa3fa34110aa3dbde31eaf40c8'
            ).count(), 0)

    def test_favorite_delete_api_value_error(self):
        """
        お気に入り削除APIテスト
        不正なリクエスト時
        """
        url = reverse('short_post:favorite_delete')
        self.login()
        test_post_id = '不正なリクエスト'
        params = dict(post_id=test_post_id,)
        res = self.client.post(url, params)
        res_content = json.loads(res.content)
        status = res_content['status']
        # APIの応答ステータスを確認
        self.assertEqual(status, '204')
