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
from short_post.serializers import FavoriteSerializer
from django.core.exceptions import ValidationError

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
        return context

    def form_valid(self, form):
        """
        投稿処理
        """
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)


class TimeLineView(LoginRequiredMixin, generic.FormView):
    """
    タイムライン画面用View
    """
    template_name = "short_post/timeline.html"


def post_load_api(request):
    """
    投稿一覧取得API
    """
    request_user_name = request.GET.get('user-name')
    # ユーザーの投稿内容一覧を取得
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
        serializer_post = PostContentSerializer(data=result_post.object_list,
                                                many=True)
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
    request_user_name = request.GET.get('user-name')
    # ユーザーのお気に入り一覧を取得
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
