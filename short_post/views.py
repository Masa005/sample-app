from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from short_post.models import PostContent
from short_post.forms import PostForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from short_post.serializers import PostContentSerializer
from short_post.models import Favorite
from django.db.models import Prefetch
from django.core.exceptions import ValidationError
from short_post.serializers import FavoriteSerializer
from django.contrib import messages
from django.shortcuts import redirect
from short_post.forms import FollowForm
from short_post.models import Follow
from short_post.serializers import FollowSerializer
from django.db import transaction

User = get_user_model()


class HomeView(LoginRequiredMixin, generic.FormView):
    """
    ホーム画面用View
    """
    template_name = 'short_post/home.html'
    form_class = PostForm
    success_url = reverse_lazy('short_post:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ログインユーザーの投稿内容一覧を取得
        user_post_list = PostContent.objects.filter(
            user__username=self.request.user.username
            ).select_related().all().order_by(
                'date_joined').reverse().prefetch_related(
                    Prefetch('favorite_set', queryset=Favorite.objects.filter(
                        user__username=self.request.user.username),
                        to_attr='prefetch_favorite'))
        # ログインユーザーのお気に入り一覧を取得
        user_favorite_list = Favorite.objects.filter(
            user=self.request.user).order_by('date_joined').reverse()

        # ログインユーザーのフォロー数を取得
        follow_count = Follow.objects.filter(
            follow_user__username=self.request.user.username).count()

        # ログインユーザーのフォロワー数を取得
        follower_count = Follow.objects.filter(
            followed_user__username=self.request.user.username).count()

        # 投稿内容一覧を10個ずつ表示
        post_paginator = Paginator(user_post_list, 10)
        # お気に入り一覧を10個ずつ表示
        favorite_paginator = Paginator(user_favorite_list, 10)
        # 1ページ目の投稿内容一覧を設定
        user_post_list = post_paginator.page(1)
        # 1ページ目のお気に入り一覧を設定
        user_favorite_list = favorite_paginator.page(1)
        context['user_post_list'] = user_post_list
        context['user_favorite_list'] = user_favorite_list
        context['follow_count'] = follow_count
        context['follower_count'] = follower_count
        return context

    def form_valid(self, form):
        """
        投稿処理
        """
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        messages.add_message(self.request, messages.INFO,
                             '投稿しました')
        return super().form_valid(form)


class TimeLineView(LoginRequiredMixin, generic.FormView):
    """
    タイムライン画面用View
    """
    template_name = "short_post/timeline.html"
    form_class = PostForm
    success_url = reverse_lazy('short_post:timeline')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # すべてのユーザーの投稿内容一覧を取得
        all_post_list = PostContent.objects.all()\
            .order_by('date_joined').reverse().prefetch_related(
                    Prefetch('favorite_set', queryset=Favorite.objects.filter(
                        user__username=self.request.user.username),
                             to_attr='prefetch_favorite'))

        resultList = Follow.objects.filter(
            follow_user__username=self.request.user.username)
        followedList = list()
        for followed in resultList:
            followedList.append(followed)

        # フォロー中のユーザーの投稿内容一覧を取得
        follow_post_list = PostContent.objects.filter(
            user__followed_user__in=followedList).order_by(
                'date_joined').reverse().prefetch_related(
                    Prefetch('favorite_set', queryset=Favorite.objects.filter(
                        user__username=self.request.user.username),
                             to_attr='prefetch_favorite'))

        # ログインユーザーのフォロー数を取得
        follow_count = Follow.objects.filter(
            follow_user__username=self.request.user.username).count()

        # ログインユーザーのフォロワー数を取得
        follower_count = Follow.objects.filter(
            followed_user__username=self.request.user.username).count()

        # 投稿内容一覧を10個ずつ表示
        post_paginator = Paginator(all_post_list, 10)
        follow_post_paginator = Paginator(follow_post_list, 10)
        # 1ページ目の投稿内容一覧を設定
        all_post_list = post_paginator.page(1)
        follow_post_list = follow_post_paginator.page(1)
        context['all_post_list'] = all_post_list
        context['follow_post_list'] = follow_post_list
        context['follow_count'] = follow_count
        context['follower_count'] = follower_count
        return context

    def form_valid(self, form):
        """
        投稿処理
        """
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        messages.add_message(self.request, messages.INFO,
                             '投稿しました')
        return super().form_valid(form)


class OtherUserView(LoginRequiredMixin, generic.FormView):
    """
    その他ユーザー画面用View
    """
    template_name = "short_post/other_user.html"
    form_class = FollowForm
    request_user_name = ''
    success_url = ''

    def get(self, request):
        if 'username' in self.request.GET:
            try:
                OtherUserView.request_user_name = self.request.GET.get(
                    'username')
                User.objects.get(username=OtherUserView.request_user_name)
            except User.DoesNotExist:
                messages.add_message(self.request, messages.ERROR,
                                     'そのユーザーは存在しません')
                return redirect('sample_app:error')
            return super(OtherUserView, self).get(request)
        else:
            messages.add_message(self.request, messages.ERROR,
                                 '不正なアクセスです')
            return redirect('sample_app:error')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_user = User.objects.get(
            username=OtherUserView.request_user_name)
        # すでにフォローしたユーザーかチェック
        follow_flg = Follow.objects.filter(
            follow_user__username=self.request.user.username,
            followed_user__username=request_user).count()
        # ユーザーの投稿内容一覧を取得
        user_post_list = PostContent.objects.filter(
            user__username=OtherUserView.request_user_name
            ).select_related().all().order_by(
                'date_joined').reverse().prefetch_related(
                    Prefetch('favorite_set', queryset=Favorite.objects.filter(
                        user__username=self.request.user.username),
                        to_attr='prefetch_favorite'))
        # ユーザーのお気に入り一覧を取得
        user_favorite_list = Favorite.objects.filter(
            user=request_user).order_by(
                'date_joined').reverse().prefetch_related(
                    Prefetch('post_content__favorite_set',
                             queryset=Favorite.objects.filter(
                                 user__username=self.request.user.username),
                             to_attr='prefetch_favorite'))

        # ユーザーのフォロー数を取得
        follow_count = Follow.objects.filter(
            follow_user__username=OtherUserView.request_user_name).count()

        # ユーザーのフォロワー数を取得
        follower_count = Follow.objects.filter(
            followed_user__username=OtherUserView.request_user_name).count()

        # 投稿内容一覧を10個ずつ表示
        post_paginator = Paginator(user_post_list, 10)
        # お気に入り一覧を10個ずつ表示
        favorite_paginator = Paginator(user_favorite_list, 10)
        # 1ページ目の投稿内容一覧を設定
        user_post_list = post_paginator.page(1)
        # 1ページ目のお気に入り一覧を設定
        user_favorite_list = favorite_paginator.page(1)
        context['user_post_list'] = user_post_list
        context['user_favorite_list'] = user_favorite_list
        context['other_user'] = request_user
        context['follow_flg'] = follow_flg
        context['follow_count'] = follow_count
        context['follower_count'] = follower_count
        return context

    # form初期値設定
    def get_initial(self):
        initial = super().get_initial()
        try:
            request_user = User.objects.get(
                username=OtherUserView.request_user_name)
        except User.DoesNotExist:
            messages.add_message(self.request, messages.ERROR,
                                 'そのユーザーは存在しません')
            return redirect('sample_app:error')
        initial['followed_user'] = request_user
        return initial

    def form_valid(self, form):
        """
        フォロー処理
        """
        follow_form = form.save(commit=False)
        OtherUserView.success_url = '?username=' + OtherUserView\
            .request_user_name

        # すでにフォローしたユーザーかチェック
        exist_check = Follow.objects.filter(
            follow_user__username=self.request.user.username,
            followed_user=follow_form.
            followed_user).count()
        if exist_check == 0:
            # フォロー登録を行う
            follow_form.follow_user = self.request.user
            follow_form.save()
            messages.add_message(self.request, messages.INFO,
                                 'フォローしました')
            return super().form_valid(form)
        else:
            # フォロー削除を行う
            Follow.objects.filter(
                follow_user__username=self.request.user.username,
                followed_user=follow_form.followed_user).delete()
            messages.add_message(self.request, messages.INFO,
                                 'フォローを解除しました')
            return super().form_valid(form)


class FollowFollowerView(LoginRequiredMixin, generic.TemplateView):
    """
    フォロー中・フォロワー一覧画面用View
    """
    template_name = "short_post/follow_follower.html"

    def get(self, request):
        print(request)
        if 'username' in self.request.GET:
            request_username = self.request.GET.get('username')
            try:
                User.objects.get(
                    username=request_username)
            except User.DoesNotExist:
                messages.add_message(self.request, messages.ERROR,
                                     'そのユーザーは存在しません')
                return redirect('sample_app:error')
            return super(FollowFollowerView, self).get(request)
        else:
            messages.add_message(self.request, messages.ERROR,
                                 '不正なアクセスです')
            return redirect('sample_app:error')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_username = self.request.GET.get('username')
        request_user = User.objects.get(
                    username=request_username)

        follower_flg = False
        if 'follower' in self.request.GET and self.request.GET.get('follower'):
            follower_flg = True
        # ユーザーのフォロー一覧を取得
        follow_list = Follow.objects.filter(
            follow_user__username=request_username).order_by(
                'date_joined').reverse()

        # ユーザーのフォロワー一覧を取得
        follower_list = Follow.objects.filter(
            followed_user__username=request_username).order_by(
                'date_joined').reverse()

        # ユーザーのフォロー数を取得
        follow_count = Follow.objects.filter(
            follow_user__username=request_username).count()

        # ユーザーのフォロワー数を取得
        follower_count = Follow.objects.filter(
            followed_user__username=request_username).count()

        # フォロー一覧を10個ずつ表示
        follow_paginator = Paginator(follow_list, 10)
        # フォロワー一覧を10個ずつ表示
        follower_paginator = Paginator(follower_list, 10)

        # 1ページ目のフォロー一覧を設定
        follow_list = follow_paginator.page(1)
        # 1ページ目のフォロワー一覧を設定
        follower_list = follower_paginator.page(1)

        context['follow_list'] = follow_list
        context['follower_list'] = follower_list
        context['follower_flg'] = follower_flg
        context['follow_count'] = follow_count
        context['follower_count'] = follower_count
        context['request_user'] = request_user
        return context


def post_load_api(request):
    """
    投稿一覧取得API
    """
    request_user_name = request.GET.get('username')
    if 'other' in request.GET and request.GET.get('other'):
        # その他ユーザーの投稿内容を取得
        user_post_list = PostContent.objects.filter(
            user__username=request_user_name
        ).select_related().all().order_by(
            'date_joined').reverse().prefetch_related(
                Prefetch('favorite_set', queryset=Favorite.objects.filter(
                    user__username=request.user.username),
                    to_attr='prefetch_favorite'))

    elif 'follow' in request.GET and request.GET.get('follow'):
        resultList = Follow.objects.filter(
            follow_user__username=request.user.username)
        followedList = list()
        for followed in resultList:
            followedList.append(followed)

        # フォロー中のユーザーの投稿内容一覧を取得
        user_post_list = PostContent.objects.filter(
            user__followed_user__in=followedList).order_by(
                'date_joined').reverse().prefetch_related(
                    Prefetch('favorite_set', queryset=Favorite.objects.filter(
                        user__username=request.user.username),
                             to_attr='prefetch_favorite'))

    elif request_user_name == 'all':
        # すべてのユーザーの投稿内容一覧を取得
        user_post_list = PostContent.objects.all()\
            .order_by('date_joined').reverse().prefetch_related(
                    Prefetch('favorite_set', queryset=Favorite.objects.filter(
                        user__username=request.user.username),
                             to_attr='prefetch_favorite'))

    else:
        # ログインユーザーの投稿内容一覧を取得
        user_post_list = PostContent.objects.filter(
            user__username=request_user_name
            ).select_related().all().order_by(
                'date_joined').reverse().prefetch_related(
                    Prefetch('favorite_set', queryset=Favorite.objects.filter(
                        user__username=request_user_name),
                        to_attr='prefetch_favorite'))
    # 投稿内容一覧を10個ずつ表示
    paginator = Paginator(user_post_list, 10)
    page = request.GET.get('page')
    try:
        # リクエストされたページの投稿内容一覧を設定
        result_post = paginator.page(page)
        serializer_post = PostContentSerializer(
            data=result_post.object_list, many=True)
        serializer_post.is_valid()
        serializer_post.save()
    # 空のリクエストや存在しないページのリクエスト時は何も返さない
    except (PageNotAnInteger, EmptyPage):
        return HttpResponse(status=204)
    return JsonResponse(data={
        'user_post_list': serializer_post.data,
        'page': result_post.number,
        'has_next': result_post.has_next()})


def fav_load_api(request):
    """
    お気に入り一覧取得API
    """
    request_user_name = request.GET.get('username')
    if 'other' in request.GET and request.GET.get('other'):
        # その他ユーザーのお気に入り一覧を取得
        user_favorite_list = Favorite.objects.filter(
            user__username=request_user_name).order_by(
                'date_joined').reverse().prefetch_related(
                    Prefetch('post_content__favorite_set',
                             queryset=Favorite.objects.filter(
                                 user__username=request.user.username),
                             to_attr='prefetch_favorite'))

        # ログインユーザーお気に入り一覧
        login_user_favorite_list = list()
        for login_user_favorite in user_favorite_list:
            if login_user_favorite.post_content.prefetch_favorite:
                login_user_favorite_list.append(
                    login_user_favorite.post_content.prefetch_favorite[0])
            else:
                login_user_favorite_list.append(None)

        # 投稿内容一覧を10個ずつ表示
        other_user_paginator = Paginator(user_favorite_list, 10)
        login_user_paginator = Paginator(login_user_favorite_list, 10)
        page = request.GET.get('page')
        try:
            # リクエストされたページのお気に入り一覧を設定
            other_user_result_fav = other_user_paginator.page(page)
            login_user_result_fav = login_user_paginator.page(page)

            serializer_other_user_fav = FavoriteSerializer(
                data=other_user_result_fav.object_list, many=True)
            serializer_other_user_fav.is_valid()
            serializer_other_user_fav.save()

            serializer_login_user_fav = FavoriteSerializer(
                data=login_user_result_fav.object_list, many=True)
            serializer_login_user_fav.is_valid()
            serializer_login_user_fav.save()

        # 空のリクエストや存在しないページのリクエスト時は何も返さない
        except (PageNotAnInteger, EmptyPage):
            return HttpResponse(status=204)
        return JsonResponse(data={
            'user_favorite_list': serializer_other_user_fav.data,
            'page': other_user_result_fav.number,
            'has_next': other_user_result_fav.has_next(),
            'login_user_favorite_list': serializer_login_user_fav.data})
    else:
        # ログインユーザーのお気に入り一覧を取得
        user_favorite_list = Favorite.objects.filter(
                user__username=request_user_name).order_by(
                    'date_joined').reverse()
    # 投稿内容一覧を10個ずつ表示
    paginator = Paginator(user_favorite_list, 10)
    page = request.GET.get('page')
    try:
        # リクエストされたページのお気に入り一覧を設定
        result_fav = paginator.page(page)
        serializer_fav = FavoriteSerializer(data=result_fav.object_list,
                                            many=True)
        serializer_fav.is_valid()
        serializer_fav.save()

    # 空のリクエストや存在しないページのリクエスト時は何も返さない
    except (PageNotAnInteger, EmptyPage):
        return HttpResponse(status=204)
    return JsonResponse(data={
        'user_favorite_list': serializer_fav.data,
        'page': result_fav.number,
        'has_next': result_fav.has_next()})


def follow_follower_load_api(request):
    """
    フォロー中・フォロワー一覧取得API
    """
    request_username = request.GET.get('username')
    if 'follower' in request.GET and request.GET.get('follower'):
        # ユーザーのフォロワー一覧を取得
        follow_follower_list = Follow.objects.filter(
            followed_user__username=request_username).order_by(
                'date_joined').reverse()

    else:
        # ユーザーのフォロー一覧を取得
        follow_follower_list = Follow.objects.filter(
            follow_user__username=request_username).order_by(
                'date_joined').reverse()

    # 投稿内容一覧を10個ずつ表示
    paginator = Paginator(follow_follower_list, 10)
    page = request.GET.get('page')
    try:
        # リクエストされたページの投稿内容一覧を設定
        result_post = paginator.page(page)
        serializer_follow_follower = FollowSerializer(
            data=result_post.object_list, many=True)
        serializer_follow_follower.is_valid()
        serializer_follow_follower.save()
    # 空のリクエストや存在しないページのリクエスト時は何も返さない
    except (PageNotAnInteger, EmptyPage):
        return HttpResponse(status=204)
    return JsonResponse(data={
        'follow_follower_list': serializer_follow_follower.data,
        'page': result_post.number,
        'has_next': result_post.has_next()})


def favorite_add_api(request):
    """
    お気に入り登録API
    """
    request_post_id = request.POST.get('post_id')
    try:
        reqest_post_content = PostContent(post_id=request_post_id)
        favolite_count = Favorite.objects.filter(
            user=request.user, post_content=reqest_post_content
                                                 ).count()
        favolite = Favorite(user=request.user,
                            post_content=reqest_post_content)
    except ValidationError:
            return JsonResponse(data={'status': '204'})

    # 既にお気に入り登録されている場合は登録しない
    if(favolite_count >= 1):
        return JsonResponse(data={'status': '204'})
    # お気に入り登録を実行
    favolite.save()
    return JsonResponse(data={'status': '200'})


def favorite_delete_api(request):
    """
    お気に入り削除API
    """
    request_post_id = request.POST.get('post_id')
    try:
        reqest_post_content = PostContent(post_id=request_post_id)
        # お気に入り削除を実行
        Favorite.objects.filter(user=request.user,
                                post_content=reqest_post_content).delete()
    except ValidationError:
            return JsonResponse(data={'status': '204'})
    return JsonResponse(data={'status': '200'})


@transaction.atomic
def post_delete_api(request):
    """
    投稿削除API
    """
    request_post_id = request.POST.get('post_id')
    try:
        reqest_post_content = PostContent(post_id=request_post_id)
        # 投稿の削除を実行
        PostContent.objects.filter(post_id=request_post_id).delete()
        # お気に入り削除を実行
        Favorite.objects.filter(post_content=reqest_post_content).delete()
    except ValidationError:
        return JsonResponse(data={'status': '204'})
        raise ValidationError
    messages.add_message(request, messages.INFO,
                         '投稿を削除しました')
    return JsonResponse(data={'status': '200'})
