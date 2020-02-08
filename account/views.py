from account.forms import LoginForm, CreateUserForm
from django.contrib.auth import get_user_model
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin


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
    template_name = "account/option.html"
