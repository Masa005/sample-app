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
from short_post.factory import FollowFactory

User = get_user_model()


class PostLoadApiTest(TestCase):
    """
    post_load_apiのテストクラス
    """
    def setUp(self):
        UserFactory(username='testUser')
        UserFactory(username='testUser2')
        UserFactory(username='testUser3')
        test_user = User.objects.get(username='testUser')
        test_user2 = User.objects.get(username='testUser2')
        test_user3 = User.objects.get(username='testUser3')
        test_date_joined = datetime.datetime(2019, 1, 1)
        FollowFactory(follow_user=test_user, followed_user=test_user3)
        for i in range(100):
            test_content = i + 1
            test_date_joined = test_date_joined + datetime.timedelta(days=i)

            if test_content % 2 != 0:
                PostContentFactory(
                    content=test_content, user=test_user,
                    date_joined=test_date_joined)

            elif test_content % 2 == 0 and test_content % 10 != 0:
                PostContentFactory(
                    content=test_content, user=test_user2,
                    date_joined=test_date_joined)

            else:
                PostContentFactory(
                    content=test_content, user=test_user3,
                    date_joined=test_date_joined)

    def login(self):
        """
        共通ログイン処理
        """
        self.client.login(username='testUser', password='sampleapp')

    def test_post_load_api_login(self):
        """
        投稿一覧取得APIテスト
        ログインユーザー投稿内容一覧確認
        """
        url = reverse('short_post:post_load') + '?page=2&username=testUser'
        self.login()
        res = self.client.get(url)
        res_content = json.loads(res.content)
        user_post_list = res_content['user_post_list']

        login_content_list = list()
        loginuser_list = list()
        # 確認用リスト作成：ログインユーザー投稿内容一覧
        for i in reversed(range(61, 80)):
            if i % 2 != 0:
                login_content_list.append(str(i))
                loginuser_list.append('testUser')

        count = 0
        for post in user_post_list:
            # ログインユーザー投稿内容一覧確認
            self.assertEqual(post['content'], login_content_list[count])
            self.assertEqual(post['user']['username'], loginuser_list[count])
            count += 1

    def test_post_load_api_other(self):
        """
        投稿一覧取得APIテスト
        その他ユーザー投稿内容一覧確認
        """
        url = reverse(
            'short_post:post_load') + '?page=2&username=testUser2&other=true'
        self.login()
        res = self.client.get(url)
        res_content = json.loads(res.content)
        user_post_list = res_content['user_post_list']

        login_content_list = list()
        loginuser_list = list()
        # 確認用リスト作成：その他ユーザー投稿内容一覧
        for i in reversed(range(52, 75)):
            if i % 2 == 0 and i % 10 != 0:
                login_content_list.append(str(i))
                loginuser_list.append('testUser2')

        count = 0
        for post in user_post_list:
            # その他ユーザー投稿内容一覧確認
            self.assertEqual(post['content'], login_content_list[count])
            self.assertEqual(post['user']['username'], loginuser_list[count])
            count += 1

    def test_post_load_api_follow(self):
        """
        投稿一覧取得APIテスト
        フォローユーザー投稿内容一覧確認
        """
        url = reverse(
            'short_post:post_load') + '?page=1&username=testUser&follow=true'
        self.login()
        res = self.client.get(url)
        res_content = json.loads(res.content)
        user_post_list = res_content['user_post_list']

        login_content_list = list()
        loginuser_list = list()
        # 確認用リスト作成：フォローユーザー投稿内容一覧
        for i in reversed(range(10, 101)):
            if i % 10 == 0:
                login_content_list.append(str(i))
                loginuser_list.append('testUser3')

        count = 0
        for post in user_post_list:
            # フォローユーザー投稿内容一覧確認
            self.assertEqual(post['content'], login_content_list[count])
            self.assertEqual(post['user']['username'], loginuser_list[count])
            count += 1

    def test_post_load_api_all(self):
        """
        投稿一覧取得APIテスト
        すべてのユーザー投稿内容一覧確認
        """
        url = reverse(
            'short_post:post_load') + '?page=2&username=all'
        self.login()
        res = self.client.get(url)
        res_content = json.loads(res.content)
        user_post_list = res_content['user_post_list']

        login_content_list = list()
        loginuser_list = list()
        # 確認用リスト作成：すべてのユーザー投稿内容一覧
        for i in reversed(range(81, 91)):
            if i % 2 != 0:
                login_content_list.append(str(i))
                loginuser_list.append('testUser')

            elif i % 2 == 0 and i % 10 != 0:
                login_content_list.append(str(i))
                loginuser_list.append('testUser2')

            else:
                login_content_list.append(str(i))
                loginuser_list.append('testUser3')

        count = 0
        for post in user_post_list:
            # すべてのユーザー投稿内容一覧確認
            self.assertEqual(post['content'], login_content_list[count])
            self.assertEqual(post['user']['username'], loginuser_list[count])
            count += 1

    def test_post_load_api_not_exist(self):
        """
        投稿一覧取得APIテスト
        存在しないページのリクエスト時
        """
        url = reverse('short_post:post_load') + '?page=11&username=testUser'
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
        UserFactory(username='testUser2')
        test_user2 = User.objects.get(username='testUser2')
        UserFactory(username='testUser3')
        test_user3 = User.objects.get(username='testUser3')
        test_date_joined = datetime.datetime(2019, 1, 1)
        for i in range(100):
            test_content = i + 1
            test_date_joined = test_date_joined + datetime.timedelta(days=i)

            if test_content % 2 != 0:
                PostContentFactory(content=test_content,
                                   user=test_user2,
                                   date_joined=test_date_joined)
                test_post_content = PostContent\
                    .objects.get(user=test_user2, content=test_content)
                FavoriteFactory(post_content=test_post_content, user=test_user,
                                date_joined=test_date_joined)
            elif test_content % 2 == 0 and test_content % 10 != 0:
                PostContentFactory(content=test_content,
                                   user=test_user,
                                   date_joined=test_date_joined)
                test_post_content = PostContent\
                    .objects.get(user=test_user, content=test_content)
                FavoriteFactory(
                    post_content=test_post_content, user=test_user2,
                    date_joined=test_date_joined)
            else:
                PostContentFactory(content=test_content,
                                   user=test_user3,
                                   date_joined=test_date_joined)
                test_post_content = PostContent\
                    .objects.get(user=test_user3, content=test_content)
                FavoriteFactory(
                    post_content=test_post_content, user=test_user2,
                    date_joined=test_date_joined)
                if test_content == 80:
                    FavoriteFactory(
                        post_content=test_post_content, user=test_user,
                        date_joined=test_date_joined)

    def login(self):
        """
        共通ログイン処理
        """
        self.client.login(username='testUser', password='sampleapp')

    def test_fav_load_login(self):
        """
        お気に入り一覧取得APIテスト
        ログインユーザーお気に入り一覧確認
        """
        url = reverse('short_post:fav_load') + '?page=2&username=testUser'
        self.login()
        res = self.client.get(url)
        res_content = json.loads(res.content)
        user_favorite_list = res_content['user_favorite_list']
        test_content_list = list()
        user_list = list()
        for i in reversed(range(63, 81)):
            if i % 2 != 0:
                test_content_list.append(str(i))
                user_list.append('testUser2')
            if i == 80:
                test_content_list.append(str(i))
                user_list.append('testUser3')

        count = 0
        for fav in user_favorite_list:
            # お気に入り一覧確認
            self.assertEqual(fav['post_content']['content'],
                             test_content_list[count])
            self.assertEqual(fav['post_content']['user']['username'],
                             user_list[count])
            count += 1

    def test_fav_load_other(self):
        """
        お気に入り一覧取得APIテスト
        その他ユーザーお気に入り一覧確認
        """
        url = reverse(
            'short_post:fav_load') + '?page=2&username=testUser2&other=true'
        self.login()
        res = self.client.get(url)
        res_content = json.loads(res.content)
        user_favorite_list = res_content['user_favorite_list']
        login_user_favorite_list = res_content['login_user_favorite_list']
        user_list = list()
        test_content_list = list()
        # 確認用リスト作成：その他のユーザーお気に入り一覧
        for i in reversed(range(60, 81)):
            if i % 2 == 0 and i % 10 != 0:
                test_content_list.append(str(i))
                user_list.append('testUser')
            elif i % 10 == 0:
                test_content_list.append(str(i))
                user_list.append('testUser3')

        count = 0
        for fav in user_favorite_list:
            # その他ユーザーお気に入り一覧確認
            self.assertEqual(fav['post_content']['content'],
                             test_content_list[count])
            self.assertEqual(fav['post_content']['user']['username'],
                             user_list[count])
            count += 1

        # 確認用リスト作成：ログインユーザーお気に入り一覧
        for i in reversed(range(60, 81)):
            if i == 80:
                test_content_list.append(str(i))
                user_list.append('testUser3')

        count = 0
        for fav in login_user_favorite_list:
            if fav:
                # ログインユーザーお気に入り一覧確認
                self.assertEqual(fav['post_content']['content'],
                                 test_content_list[count])
                self.assertEqual(fav['post_content']['user']['username'],
                                 user_list[count])
                count += 1

    def test_fav_load_not_exist(self):
        """
        お気に入り一覧取得APIテスト
        存在しないページのリクエスト時
        """
        url = reverse('short_post:post_load') + '?page=11&username=testUser'
        self.login()
        res = self.client.get(url)
        self.assertEqual(res.status_code, 204)

    def test_fav_load_empty(self):
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

    def test_favorite_add_succes(self):
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

    def test_favorite_add_exist(self):
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

    def test_favorite_add_value_error(self):
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

    def test_favorite_delete_succes(self):
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

    def test_favorite_delete_value_error(self):
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


class FollowFollowerLoadApiTest(TestCase):
    """
    follow_follower_load_apiのテストクラス
    """
    def setUp(self):
        UserFactory(username='testUser')
        UserFactory(username='testUser2')
        request_user = User.objects.get(username='testUser2')
        test_date_joined = datetime.datetime(2019, 1, 1)
        for i in range(100):
            test_date_joined = test_date_joined + datetime.timedelta(days=i)
            test_username = 'testUser' + str(i + 1)
            if i + 1 != 2:
                UserFactory(username=test_username)
                test_user = User.objects.get(username=test_username)
            if (i + 1) % 2 != 0:
                FollowFactory(follow_user=request_user,
                              followed_user=test_user,
                              date_joined=test_date_joined)
            if (i + 1) % 2 == 0 and i + 1 != 2:
                FollowFactory(follow_user=test_user,
                              followed_user=request_user,
                              date_joined=test_date_joined)

    def login(self):
        """
        共通ログイン処理
        """
        self.client.login(username='testUser', password='sampleapp')

    def test_follow_load(self):
        """
        フォロー中・フォロワー一覧取得APIテスト
        フォロー中一覧確認
        """
        url = reverse(
            'short_post:follow_follower_load') + '?page=2&username=testUser2'
        self.login()
        res = self.client.get(url)
        res_content = json.loads(res.content)
        follow_follower_list = res_content['follow_follower_list']

        # 確認用リスト作成：フォロー一覧
        follow_user_list = list()
        followed_user_list = list()
        for i in reversed(range(61, 80)):
            if i % 2 != 0:
                follower_user = 'testUser' + str(i)
                follow_user_list.append('testUser2')
                followed_user_list.append(follower_user)

        count = 0
        for follow in follow_follower_list:
            # 初期表示 フォロー一覧確認
            self.assertEqual(follow['follow_user']['username'],
                             follow_user_list[count])
            self.assertEqual(follow['followed_user']['username'],
                             followed_user_list[count])
            count += 1

    def test_follower_load(self):
        """
        フォロー中・フォロワー一覧取得APIテスト
        フォロワー一覧確認
        """
        url = reverse(
            'short_post:follow_follower_load'
            ) + '?page=2&username=testUser2&follower=True'
        self.login()
        res = self.client.get(url)
        res_content = json.loads(res.content)
        follow_follower_list = res_content['follow_follower_list']

        # 確認用リスト作成：フォロワー一覧
        follow_user_list = list()
        followed_user_list = list()
        for i in reversed(range(62, 81)):
            if i % 2 == 0 and i != 2:
                follow_user = 'testUser' + str(i)
                follow_user_list.append(follow_user)
                followed_user_list.append('testUser2')

        count = 0
        for follower in follow_follower_list:
            # 初期表示 フォロー一覧確認
            self.assertEqual(follower['follow_user']['username'],
                             follow_user_list[count])
            self.assertEqual(follower['followed_user']['username'],
                             followed_user_list[count])
            count += 1

    def test_follow_follower_load_not_exist(self):
        """
        フォロー中・フォロワー一覧取得APIテスト
        存在しないページのリクエスト時
        """
        url = reverse(
            'short_post:follow_follower_load') + '?page=11&username=testUser2'
        self.login()
        res = self.client.get(url)
        self.assertEqual(res.status_code, 204)

    def test_follow_follower_load_api_empty(self):
        """
        フォロー中・フォロワー一覧取得APIテスト
        空のリクエスト時
        """
        url = reverse('short_post:follow_follower_load')
        self.login()
        res = self.client.get(url)
        self.assertEqual(res.status_code, 204)


class PostDeleteApiTest(TestCase):
    """
    post_delete_apiのテストクラス
    """
    def setUp(self):
        UserFactory(username='testUser')
        UserFactory(username='testUser2')
        test_user = User.objects.get(username='testUser')
        test_user2 = User.objects.get(username='testUser2')
        PostContentFactory(post_id='9758ebaa3fa34110aa3dbde31eaf40c8',
                           content='テストコンテンツ', user=test_user)
        test_post_content = PostContent.objects.get(
            post_id='9758ebaa3fa34110aa3dbde31eaf40c8')
        FavoriteFactory(post_content=test_post_content,
                        user=test_user2)

    def login(self):
        """
        共通ログイン処理
        """
        self.client.login(username='testUser', password='sampleapp')

    def test_post_delete_succes(self):
        """
        投稿削除APIテスト
        削除成功時
        """
        url = reverse('short_post:post_delete')
        self.login()
        test_post_id = '9758ebaa3fa34110aa3dbde31eaf40c8'
        params = dict(post_id=test_post_id,)
        res = self.client.post(url, params)
        res_content = json.loads(res.content)
        status = res_content['status']
        # APIの応答ステータスを確認
        self.assertEqual(status, '200')
        # 投稿が削除されていることを確認
        self.assertEqual(PostContent.objects.filter(
            post_id='9758ebaa3fa34110aa3dbde31eaf40c8'
            ).count(), 0)
        self.assertEqual(Favorite.objects.filter(
            post_content__post_id='9758ebaa3fa34110aa3dbde31eaf40c8'
            ).count(), 0)

    def test_post_delete_value_error(self):
        """
        投稿削除APIテスト
        不正なリクエスト時
        """
        url = reverse('short_post:post_delete')
        self.login()
        test_post_id = '不正なリクエスト'
        params = dict(post_id=test_post_id,)
        res = self.client.post(url, params)
        res_content = json.loads(res.content)
        status = res_content['status']
        # APIの応答ステータスを確認
        self.assertEqual(status, '204')
        # 投稿が削除されていないことを確認
        self.assertEqual(PostContent.objects.filter(
            post_id='9758ebaa3fa34110aa3dbde31eaf40c8'
            ).count(), 1)
        self.assertEqual(Favorite.objects.filter(
            post_content__post_id='9758ebaa3fa34110aa3dbde31eaf40c8'
            ).count(), 1)
