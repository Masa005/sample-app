from account.forms import LoginForm
from account.forms import CreateUserForm
from django.contrib.auth import get_user_model
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from account.forms import UpdateUserForm
from account.forms import MyPasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.db import transaction
from short_post.models import PostContent
from short_post.models import Favorite
from short_post.models import Follow
from django.core.exceptions import ValidationError


User = get_user_model()


class LoginView(LoginView):
    """
    ログイン画面用View
    """
    template_name = "account/login.html"
    form_class = LoginForm


class SignupView(generic.CreateView):
    """
    新規登録画面用View
    """
    template_name = 'account/signup.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('account:signup_done')

    def form_valid(self, form):
        """
        仮登録と本登録用メールの発行
        """
        user = form.save(commit=False)
        # ユーザーを仮登録
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(str(user.pk)),
            'user': user,
        }
        subject = render_to_string('account/mail_template/subject.txt')
        message = render_to_string('account/mail_template/message.txt',
                                   context)
        user.email_user(subject, message)
        return super().form_valid(form)

    def form_invalid(self, form):
        form.add_error(None, '入力項目に誤りがあります')
        return super().form_invalid(form)


class SignupDoneView(generic.TemplateView):

    """
    仮登録完了画面用View
    """
    template_name = 'account/signup_done.html'


class SignupCompleteView(generic.TemplateView):

    """
    本登録完了画面用View
    """
    template_name = 'account/signup_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS')

    def get(self, request, **kwargs):
        """
        本登録処理
        """
        User = get_user_model()
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            messages.add_message(self.request, messages.ERROR,
                                 'URLの有効期限が切れています。再度画面から会員登録を行ってください')
            return redirect('sample_app:error')

        # tokenが間違っている
        except BadSignature:
            messages.add_message(self.request, messages.ERROR,
                                 '不正なアクセスです')
            return redirect('sample_app:error')

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                messages.add_message(self.request, messages.ERROR,
                                     'ユーザーが見つかりません。再度画面から会員登録を行ってください')
                return redirect('sample_app:error')
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)
            messages.add_message(self.request, messages.ERROR,
                                 'このユーザーはすでに登録済みです')
            return redirect('sample_app:error')


class OptionView(LoginRequiredMixin, generic.TemplateView):
    """
    設定画面用View
    """
    template_name = 'account/option.html'

    @transaction.atomic
    def post(self, request):
        try:
            # ユーザーの削除を実行
            User.objects.filter(username=request.user.username).delete()
            # ユーザーのお気に入り削除を実行
            Favorite.objects.filter(
                user=request.user).delete()
            # ユーザーの投稿に対して登録されたお気に入りの削除を実行
            Favorite.objects.filter(
                post_content__user=request.user).delete()
            # ユーザーの投稿削除を実行
            PostContent.objects.filter(
                user=request.user).delete()
            # フォロー削除を実行
            Follow.objects.filter(
                follow_user=request.user).delete()
            # フォロワー削除を実行
            Follow.objects.filter(
                followed_user=request.user).delete()
        except ValidationError:
            messages.add_message(
                self.request, messages.ERROR, 'ユーザー削除処理に失敗しました')
            return redirect('sample_app:error')
            raise ValidationError
        return redirect('account:user_deleted')


class PasswordUpdateView(LoginRequiredMixin, PasswordChangeView):
    """
    パスワード変更画面用View
    """
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('account:option')
    template_name = 'account/password_update.html'

    def form_valid(self, form):
        messages.success(self.request, 'パスワードを変更しました')
        return super().form_valid(form)

    def form_invalid(self, form):
        form.add_error(None, '入力項目に誤りがあります')
        return super().form_invalid(form)


class UserUpdateView(LoginRequiredMixin, generic.FormView):
    """
    プロフィール編集画面用View

    """
    form_class = UpdateUserForm
    success_url = reverse_lazy('account:option')
    template_name = 'account/user_update.html'

    # form初期値設定
    def get_initial(self):
        initial = super().get_initial()
        initial['username'] = self.request.user.username
        initial['name'] = self.request.user.name
        initial['birthday'] = self.request.user.birthday
        initial['email'] = self.request.user.email
        initial['one_word'] = self.request.user.one_word
        return initial

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(instance=self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'プロフィールを変更しました')
        return super().form_valid(form)

    def form_invalid(self, form):
        form.add_error(None, '入力項目に誤りがあります')
        return super().form_invalid(form)


class UserDeletedView(generic.TemplateView):

    """
    退会完了画面用View
    """
    template_name = 'account/user_deleted.html'
