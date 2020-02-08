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

User = get_user_model()


class HomeView(LoginRequiredMixin, generic.FormView):
    """
    ホーム画面用View
    """
    template_name = "short_post/home.html"
    form_class = PostForm
    success_url = reverse_lazy('short_post:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ログインユーザーの投稿内容一覧を取得
        user_post_list = PostContent.objects.filter(
            user__username=self.request.user.username)\
            .select_related().all().order_by('date_joined').reverse()
        # 投稿内容一覧を10個ずつ表示
        paginator = Paginator(user_post_list, 10)
        # 1ページ目の投稿内容一覧を設定
        user_post_list = paginator.page(1)
        context["user_post_list"] = user_post_list
        return context

    def form_valid(self, form):
        """
        投稿処理
        """
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)


class TimeLineView(LoginRequiredMixin, generic.TemplateView):
    """
    タイムライン画面用View
    """
    template_name = "short_post/timeline.html"


def post_load_api(request):
    """
    投稿一覧取得API
    """
    # ログインユーザーの投稿内容一覧を取得
    user_post_list = PostContent.objects.filter(
        user__username=request.user.username).select_related().all().order_by(
                                                    'date_joined').reverse()
    # 投稿内容一覧を10個ずつ表示
    paginator = Paginator(user_post_list, 10)
    page = request.GET.get('page')
    try:
        # リクエストされたページの投稿内容一覧を設定
        result = paginator.page(page)
        serializer = PostContentSerializer(data=result.object_list, many=True)
        serializer.is_valid()
        serializer.save()
    # 空のリクエストや存在しないページのリクエスト時は何も返さない
    except (PageNotAnInteger, EmptyPage):
        return HttpResponse(status=204)
    return JsonResponse(data={
        'user_post_list': serializer.data,
        'page': result.number,
        'has_next': result.has_next()})


def favorite_add_api(request):
    """
    お気に入り登録API
    """
    print("成功！")
    return JsonResponse(data={'data': 'data'})
