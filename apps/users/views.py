from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from rest_framework.authtoken.models import Token

from utils.jwt_token import JWTokenTool
from .forms import UserRegisterForm, LoginForm, PasswordChangeForm, ForgetPasswordForm
from .models import Email

#获取用户模型
User = get_user_model()

# Create your views here.

def register_user(request):
    '''
    用户注册函数视图
    '''
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        #表单数据验证通过
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = cleaned_data.get('user', None)
            email = username = cleaned_data.get('username', '')
            password = cleaned_data.get('password', '')

            if not user:
                user.email = email
                user.set_password(password)
                user.save()

                # 创建非激活状态新用户并保存
                user = User.objects.create_user(username=username, password=password, email=email, is_active=False)

            logout(request)#登出用户（确保当前没有用户登陆）

            # 向邮箱发送激活连接
            if send_active_url_email(request, user.email, user):
                return render(request, 'message.html', context={'message': '用户注册成功，请登录邮箱访问收到的连接以激活用户'})

            form.add_error(None, '邮件发送失败，请检查邮箱输入是否有误')
    else:
        form = UserRegisterForm()

    content = {}
    content['form_title'] = '用户注册'
    content['submit_text'] = '注册'
    content['action_url'] = reverse('users:register')
    content['form'] = form
    return render(request, 'form.html', content)


def login_user(request):
    '''
    用户登陆函数视图
    '''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            #登陆用户
            login(request, user)
            next = request.session.get('next', reverse('buckets:bucket_view'))
            return redirect(to=next)
    else:
        #保存登陆后跳转地址，如果存在的话
        next = request.GET.get('next', None)
        if next:
            request.session['next'] = next
        form = LoginForm()

    content = {}
    content['form_title'] = '用户登录'
    content['submit_text'] = '登录'
    content['action_url'] = reverse('users:login')
    content['form'] = form
    return render(request, 'login.html', content)


@login_required
def logout_user(request):
    '''
    注销用户
    '''
    logout(request)
    return redirect(to=request.GET.get('next', reverse('buckets:bucket_view')))


@login_required
def change_password(request):
    '''
    修改密码函数视图
    '''
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST, user=request.user)
        if form.is_valid():
            #修改密码
            new_password = form.cleaned_data['new_password']
            user = request.user
            user.set_password(new_password)
            user.save()

            #注销当前用户，重新登陆
            logout(request)
            return redirect(to=reverse('users:login'))
    else:
        form = PasswordChangeForm()

    content = {}
    content['form_title'] = '修改密码'
    content['submit_text'] = '修改'
    content['action_url'] = reverse('users:change_password')
    content['form'] = form
    return render(request, 'form.html', content)

def forget_password(request):
    '''
    忘记密码视图
    '''
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            urls = []
            try:
                urls.append({'url': reverse('users:login'), 'name': '登录'})
            except:
                pass

            user = form.cleaned_data['user']
            email = form.cleaned_data['username']
            new_password = form.cleaned_data.get('new_password')
            user.email = new_password # 用于email字段暂存要重置的密码
            # 是否是未激活的用户
            if not user.is_active:
                if send_active_url_email(request, email, user):
                    return render(request, 'message.html', context={'message': '用户未激活，请先登录邮箱访问收到的链接以激活用户', 'urls': urls})
                form.add_error(None, '邮件发送失败，请检查用户名输入是否有误，稍后重试')
            else:
                if send_forget_password_email(request, email, user):
                    return render(request, 'message.html', context={'message': '重置密码确认邮件已发送，请尽快登录邮箱访问收到的链接以完成密码重置，以防链接过期无效'})
                form.add_error(None, '邮件发送失败，请检查用户名输入是否有误，稍后重试')

    else:
        form = ForgetPasswordForm()

    content = {}
    content['form_title'] = '找回密码'
    content['submit_text'] = '提交'
    content['form'] = form
    return render(request, 'form.html', content)

def forget_password_confirm(request):
    '''
    忘记密码链接确认，完成密码修改
    :param request:
    :return:
    '''
    urls = []
    try:
        urls.append({'url': reverse('users:login'), 'name': '登录'})
        urls.append({'url': reverse('users:register'), 'name': '注册'})
    except:
        pass

    jwt = JWTokenTool()
    try:
        ret = jwt.authenticate(request)
    except:
        ret = None

    if not ret:
        return render(request, 'message.html', context={'message': 'jwt无效，用户重置密码失败', 'urls': urls})

    user = ret[0]
    password = ret[1]
    user.set_password(password)
    user.save()
    return render(request, 'message.html', context={'message': '用户重置密码成功，请尝试登录', 'urls': urls})

def active_user(request):
    '''
    激活用户
    :param request:
    :return:
    '''
    urls = []
    try:
        urls.append({'url': reverse('users:login'), 'name': '登录'})
        urls.append({'url': reverse('users:register'), 'name': '注册'})
    except:
        pass

    key = request.GET.get('token', None)
    try:
        token = Token.objects.select_related('user').get(key=key)
    except Token.DoesNotExist:
        return render(request, 'message.html', context={'message': '用户激活失败，无待激活账户，或者账户已被激活，请直接尝试登录', 'urls': urls})

    user = token.user
    user.is_active = True
    user.save()

    reflesh_new_token(token)

    return render(request, 'message.html', context={'message': '用户已激活', 'urls': urls})


def get_active_link(request, user):
    '''
    获取账户激活连接

    :param request: 请求对象
    :param user: 用户对象
    :return: 正常: url
            错误：None
    '''
    token = get_or_create_token(user=user)
    if not token:
        return None

    try:
        active_link = reverse('users:active')
    except:
        return None

    active_link = request.build_absolute_uri(active_link)
    active_link += f'?token={token.key}'
    return active_link


def send_active_url_email(request, to_email, user):
    '''
    发送用户激活连接邮件
    
    :param email: 邮箱
    :param user: 用户对象
    :return: True(发送成功)，False(发送失败)
    '''
    active_link = get_active_link(request, user)
    if not active_link:
        return False

    message = f'''
        亲爱的用户：
            欢迎使用EVHarbor,您已使用本邮箱成功注册账号，请访问下面激活连接以激活账户,如非本人操作请忽略此邮件。
            激活连接：{active_link}
        '''
    return send_one_email(subject='EVHarbor账户激活', receiver=to_email, message=message, log_message=active_link)

def send_one_email(receiver, message, subject='EVHarbor', log_message=''):
    '''
    发送一封邮件

    :param receiver: 接收邮箱
    :param message: 邮件内容
    :param log_message: 邮件记录中要保存的邮件内容(邮件内容太多，可以只保存主要信息)
    :return: True(发送成功)，False(发送失败)
    '''
    email = Email()
    email.message = log_message
    ok = email.send_email(subject=subject,receiver=receiver, message=message)
    if ok:
        return True
    return False


def get_or_create_token(user):
    '''
    获取用户或为用户创建一个token，会在数据库表中产生一条token记录

    :param user: 用户对象
    :return: Token对象
    '''
    token, created = Token.objects.get_or_create(user=user)
    if not token:
        return None

    return token

def reflesh_new_token(token):
    '''
    更新用户的token

    :param token: token对象
    :return: 无
    '''
    token.delete()
    token.key = token.generate_key()
    token.save()

def send_forget_password_email(request, to_email, user):
    '''
    发送忘记密码连接邮件

    :param email: 邮箱
    :param user: 用户对象
    :return: True(发送成功)，False(发送失败)
    '''
    link = get_find_password_link(request, user)
    if not link:
        return False

    message = f'''
        亲爱的用户：
            欢迎使用EVHarbor,您正在为以本邮箱注册的账号找回密码，请访问下面连接以完成账户密码修改,如非本人操作请忽略此邮件。
            连接：{link}
        '''
    return send_one_email(subject='EVHarbor账户找回密码', receiver=to_email, message=message, log_message=link)


def get_find_password_link(request, user):
    '''
    获取找回密码连接
    :param request:
    :param user:
    :return: 正常：url; 错误：None
    '''
    jwt = JWTokenTool()
    token = jwt.obtain_one_jwt_token(user=user)
    if not token:
        return None

    try:
        url = reverse('users:forget_confirm')
    except:
        return None

    url = request.build_absolute_uri(url)
    return url + '?jwt=' + token

@login_required
def security(request, *args, **kwargs):
    '''
     安全凭证函数视图
    '''
    user = request.user
    token = get_or_create_token(user=user)
    return render(request, 'security.html', context={'token': token})


