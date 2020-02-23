from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from short_post.factory import PostContentFactory
from account.factory import UserFactory
from short_post.models import PostContent
import datetime
from short_post.factory import FavoriteFactory
from short_post.factory import FollowFactory
from short_post.models import Follow

User = get_user_model()


class HomeViewTest(TestCase):
    """
    HomeViewのテストクラス
    """
    def setUp(self):
        UserFactory(username='testUser')
        login_user = User.objects.get(username='testUser')
        test_date_joined = datetime.datetime(2019, 1, 1)
        for i in range(100):
            test_content = i + 1
            test_date_joined = test_date_joined + datetime.timedelta(days=i)
            PostContentFactory(content=test_content,
                               user=login_user, date_joined=test_date_joined)
            test_username = 'testUser' + str(i + 1)
            UserFactory(username=test_username)
            test_user = User.objects.get(username=test_username)
            if i <= 2:
                test_post_content = PostContent\
                    .objects.get(user=login_user, content=test_content)
                FavoriteFactory(post_content=test_post_content,
                                user=login_user, date_joined=test_date_joined)
            if (i + 1) % 2 != 0:
                FollowFactory(follow_user=login_user,
                              followed_user=test_user,
                              date_joined=test_date_joined)
            if (i + 1) % 2 == 0:
                FollowFactory(follow_user=test_user,
                              followed_user=login_user,
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
        follow_count = res.context['follow_count']
        follower_count = res.context['follower_count']
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
            # 初期表示フォロー数確認
            self.assertEqual(follow_count, 50)
            # 初期表示フォロワー数確認
            self.assertEqual(follower_count, 50)

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


class TimeLineViewTest(TestCase):
    """
    TimeLineViewのテストクラス
    """
    def setUp(self):
        UserFactory(username='testUser')
        UserFactory(username='testUser2')
        UserFactory(username='testUser3')
        login_user = User.objects.get(username='testUser')
        test_user2 = User.objects.get(username='testUser2')
        test_user3 = User.objects.get(username='testUser3')
        FollowFactory(follow_user=login_user, followed_user=test_user2)
        test_date_joined = datetime.datetime(2019, 1, 1)
        for i in range(100):
            test_content = i + 1
            test_date_joined = test_date_joined + datetime.timedelta(days=i)

            if test_content % 2 != 0:
                PostContentFactory(content=test_content,
                                   user=login_user,
                                   date_joined=test_date_joined)
            elif test_content % 2 == 0 and test_content % 10 != 0:
                PostContentFactory(content=test_content,
                                   user=test_user2,
                                   date_joined=test_date_joined)
            else:
                PostContentFactory(content=test_content,
                                   user=test_user3,
                                   date_joined=test_date_joined)

        for i in range(10, 110):
            test_username = 'testUser' + str(i + 1)
            UserFactory(username=test_username)
            test_user = User.objects.get(username=test_username)
            if (i + 1) % 2 != 0:
                FollowFactory(follow_user=login_user,
                              followed_user=test_user,
                              date_joined=test_date_joined)
            if (i + 1) % 2 == 0:
                FollowFactory(follow_user=test_user,
                              followed_user=login_user,
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
        follow_post_list = res.context['follow_post_list']
        follow_count = res.context['follow_count']
        follower_count = res.context['follower_count']

        # 確認用リスト作成：すべてのユーザー
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

        # 確認用リスト作成：フォロー中のユーザー
        follow_post_content_list = list()
        follow_user_list = list()
        for i in reversed(range(76, 99)):
            if i % 2 == 0 and i % 10 != 0:
                follow_post_content_list.append(str(i))
                follow_user_list.append('testUser2')

        count = 0
        for post in all_post_list:
            # 初期表示 すべてのユーザーの投稿内容一覧確認
            self.assertEqual(post.content, post_content_list[count])
            self.assertEqual(post.user.username, user_list[count])
            count += 1

        count = 0
        for post in follow_post_list:
            # 初期表示 フォロー中のユーザーの投稿内容一覧確認
            self.assertEqual(post.content, follow_post_content_list[count])
            self.assertEqual(post.user.username, follow_user_list[count])
            count += 1

        # 初期表示フォロー数確認
        self.assertEqual(follow_count, 51)
        # 初期表示フォロワー数確認
        self.assertEqual(follower_count, 50)

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


class OtherUserViewTest(TestCase):
    """
    OtherUserViewのテストクラス
    """
    def setUp(self):
        UserFactory(username='testUser')
        UserFactory(username='testUser2')
        UserFactory(username='testUser3')
        login_user = User.objects.get(username='testUser')
        test_user2 = User.objects.get(username='testUser2')
        test_user3 = User.objects.get(username='testUser3')
        FollowFactory(follow_user=login_user, followed_user=test_user2)
        test_date_joined = datetime.datetime(2019, 1, 1)
        for i in range(100):
            test_content = i + 1
            test_date_joined = test_date_joined + datetime.timedelta(days=i)

            if test_content % 2 != 0:
                PostContentFactory(content=test_content,
                                   user=login_user,
                                   date_joined=test_date_joined)

                if test_content % 3 == 0:
                    test_post_content = PostContent\
                        .objects.get(user=login_user, content=test_content)
                    FavoriteFactory(
                        post_content=test_post_content, user=test_user2,
                        date_joined=test_date_joined)

            elif test_content % 2 == 0 and test_content % 10 != 0:
                PostContentFactory(content=test_content,
                                   user=test_user2,
                                   date_joined=test_date_joined)

            else:
                PostContentFactory(content=test_content,
                                   user=test_user3,
                                   date_joined=test_date_joined)

                if test_content == 100:
                    test_post_content = PostContent\
                        .objects.get(user=test_user3, content=test_content)
                    FavoriteFactory(
                        post_content=test_post_content, user=test_user2,
                        date_joined=test_date_joined)

        for i in range(10, 110):
            test_username = 'testUser' + str(i + 1)
            UserFactory(username=test_username)
            test_user = User.objects.get(username=test_username)
            if (i + 1) % 2 != 0:
                FollowFactory(follow_user=test_user2,
                              followed_user=test_user,
                              date_joined=test_date_joined)
            if (i + 1) % 2 == 0:
                FollowFactory(follow_user=test_user,
                              followed_user=test_user2,
                              date_joined=test_date_joined)

    def login(self):
        """
        共通ログイン処理
        """
        self.client.login(username='testUser', password='sampleapp')

    def test_get_success(self):
        """
        その他ユーザー画面遷移テスト(成功時)
        """
        url = reverse('short_post:other_user') + '?username=testUser2'
        self.login()
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_get_not_login(self):
        """
        その他ユーザー画面遷移テスト(未ログイン時)
        """
        url = reverse('short_post:other_user') + '?username=testUser2'
        redirect_url = reverse('account:login')
        res = self.client.get(url, follow=True)
        self.assertRedirects(res, redirect_url)

    def test_get_not_exist(self):
        """
        その他ユーザー画面遷移テスト(存在しないユーザー)
        """
        url = reverse('short_post:other_user') + '?username=notExistUser'
        self.login()
        redirect_url = reverse('sample_app:error')
        res = self.client.get(url, follow=True)
        self.assertRedirects(res, redirect_url)

    def test_get_failure(self):
        """
        その他ユーザー画面遷移テスト(パラメータ「username」なし)
        """
        url = reverse('short_post:other_user')
        self.login()
        redirect_url = reverse('sample_app:error')
        res = self.client.get(url, follow=True)
        self.assertRedirects(res, redirect_url)

    def test_get_context_data(self):
        """
        初期表示投稿内容一覧確認テスト
        """
        url = reverse('short_post:other_user') + '?username=testUser2'
        self.login()
        res = self.client.get(url)
        user_post_list = res.context['user_post_list']
        user_favorite_list = res.context['user_favorite_list']
        other_user = res.context['other_user']
        follow_flg = res.context['follow_flg']
        follow_count = res.context['follow_count']
        follower_count = res.context['follower_count']

        # 確認用リスト作成：投稿内容一覧
        post_content_list = list()
        user_list = list()
        for i in reversed(range(76, 99)):
            if i % 2 == 0 and i % 10 != 0:
                post_content_list.append(str(i))
                user_list.append('testUser2')

        # 確認用リスト作成：お気に入り一覧
        fav_content_list = list()
        fav_user_list = list()
        for i in reversed(range(51, 101)):
            if i % 2 != 0 and i % 3 == 0:
                fav_content_list.append(str(i))
                fav_user_list.append('testUser')
            if i == 100:
                fav_content_list.append(str(i))
                fav_user_list.append('testUser3')

        count = 0
        for post in user_post_list:
            # 初期表示 投稿内容一覧確認
            self.assertEqual(post.content, post_content_list[count])
            self.assertEqual(post.user.username, user_list[count])
            count += 1

        count = 0
        for post in user_favorite_list:
            # 初期表示 お気に入り一覧確認
            self.assertEqual(
                post.post_content.content, fav_content_list[count])
            self.assertEqual(
                post.post_content.user.username, fav_user_list[count])
            count += 1

        self.assertEqual(other_user, User.objects.get(username='testUser2'))
        self.assertEqual(follow_flg, 1)
        # 初期表示フォロー数確認
        self.assertEqual(follow_count, 50)
        # 初期表示フォロワー数確認
        self.assertEqual(follower_count, 51)

    def test_form_valid_add(self):
        """
        フォロー登録テスト

        """
        user = User.objects.get(username='testUser3')
        url = reverse('short_post:other_user') + '?username=testUser3'
        success_url = '?username=testUser3'
        self.login()
        self.client.get(url)
        res = self.client.post(url, {'followed_user': user.uuid}, follow=True)
        # リダイレクト先確認
        self.assertRedirects(res, success_url)
        # フォロー登録確認
        self.assertEqual(Follow.objects.filter
                         (follow_user=User.objects.get(username='testUser'),
                          followed_user=User.objects.get(username='testUser3')
                          ).count(), 1)

    def test_form_valid_delete(self):
        """

        フォロー削除テスト
        """
        user = User.objects.get(username='testUser2')
        url = reverse('short_post:other_user') + '?username=testUser2'
        success_url = '?username=testUser2'
        self.login()
        self.client.get(url)
        res = self.client.post(url,  {'followed_user': user.uuid}, follow=True)
        # リダイレクト先確認
        self.assertRedirects(res, success_url)
        # フォロー削除確認
        self.assertEqual(Follow.objects.filter
                         (follow_user=User.objects.get(username='testUser'),
                          followed_user=User.objects.get(username='testUser2')
                          ).count(), 0)


class FollowFollowerViewTest(TestCase):
    """
    FollowFollowerViewのテストクラス
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

    def test_get_success(self):
        """
        フォロー中・フォロワー一覧画面遷移テスト(成功時)
        """
        url = reverse('short_post:follow_follower') + '?username=testUser2'
        self.login()
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_get_not_login(self):
        """
        フォロー中・フォロワー一覧画面遷移テスト(未ログイン時)
        """
        url = reverse('short_post:follow_follower') + '?username=testUser2'
        redirect_url = reverse('account:login')
        res = self.client.get(url, follow=True)
        self.assertRedirects(res, redirect_url)

    def test_get_not_exist(self):
        """
        フォロー中・フォロワー一覧画面遷移テスト(存在しないユーザー)
        """
        url = reverse('short_post:follow_follower') + '?username=notExistUser'
        self.login()
        redirect_url = reverse('sample_app:error')
        res = self.client.get(url, follow=True)
        self.assertRedirects(res, redirect_url)

    def test_get_failure(self):
        """
        フォロー中・フォロワー一覧画面遷移テスト(パラメータ「username」なし)
        """
        url = reverse('short_post:follow_follower')
        self.login()
        redirect_url = reverse('sample_app:error')
        res = self.client.get(url, follow=True)
        self.assertRedirects(res, redirect_url)

    def test_get_context_data(self):
        """
        初期表示フォロー中・フォロワー一覧確認テスト
        """
        url = reverse('short_post:follow_follower') + '?username=testUser2'
        self.login()
        res = self.client.get(url)
        follow_list = res.context['follow_list']
        follower_list = res.context['follower_list']
        follower_flg = res.context['follower_flg']
        follow_count = res.context['follow_count']
        follower_count = res.context['follower_count']
        request_user = res.context['request_user']

        # 確認用リスト作成：フォロー一覧
        follow_user_list = list()
        followed_user_list = list()
        for i in reversed(range(81, 100)):
            if i % 2 != 0:
                follower_user = 'testUser' + str(i)
                follow_user_list.append('testUser2')
                followed_user_list.append(follower_user)

        count = 0
        for follow in follow_list:
            # 初期表示 フォロー一覧確認
            self.assertEqual(follow.follow_user.username,
                             follow_user_list[count])
            self.assertEqual(follow.followed_user.username,
                             followed_user_list[count])
            count += 1

        # 確認用リスト作成：フォロワー一覧
        follow_user_list = list()
        followed_user_list = list()
        for i in reversed(range(72, 101)):
            if i % 2 == 0 and i != 2:
                follow_user = 'testUser' + str(i)
                follow_user_list.append(follow_user)
                followed_user_list.append('testUser2')

        count = 0
        for follower in follower_list:
            # 初期表示 フォロワー一覧確認
            self.assertEqual(follower.follow_user.username,
                             follow_user_list[count])
            self.assertEqual(follower.followed_user.username,
                             followed_user_list[count])
            count += 1
        # 初期表示 フォロワーフラグ確認
        self.assertEqual(follower_flg, False)
        # 初期表示 フォロー数確認
        self.assertEqual(follow_count, 50)
        # 初期表示 フォロワー数確認
        self.assertEqual(follower_count, 49)
        # 初期表示 リクエストユーザー確認
        self.assertEqual(request_user, User.objects.get(username='testUser2'))
