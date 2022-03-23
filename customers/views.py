from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Address, Passport
from .serializers import AddressSerializer, UserSerializer


# Create your views here.
def register(request):
    '''show the register page'''
    return render(request, 'user/register.html')

def register_handle(request):
    '''handle registration'''
    # 接收数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')

    # 进行数据校验
    if not all([username, password, email]):
        # 有数据为空
        return render(request, 'user/register.html', {'errmsg': 'parameter can not be null!'})

    # 判断邮箱是否合法
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        # 邮箱不合法
        return render(request, 'users/register.html', {'errmsg': 'email not legal!'})

    # 进行业务处理:注册，向账户系统中添加账户
    # Passport.objects.create(username=username, password=password, email=email)
    try:
        passport = User.objects.add_passport(username=username, password=get_hash(password), email=email,gender=gender)
    except Exception as e:
        print("e: ", e) # 把异常打印出来
        return render(request, 'user/register.html', {'errmsg': '用户名已存在！'})

    serializer = Serializer(settings.SECRET_KEY, 3600)
    token = serializer.dumps({'confirm':passport.id}) # 返回bytes
    token = token.decode()

    #send_mail('尚硅谷书城用户激活', '', settings.EMAIL_FROM, [email], html_message='<a href="http://127.0.0.1:8000/user/active/%s/">http://127.0.0.1:8000/user/active/</a>' % token)
    #send_active_email.delay(token, username, email)

    # 注册完，还是返回注册页。
    return redirect(reverse('goods:index'))

def login(request):
    '''显示登录页面'''
    if request.COOKIES.get("username"):
        username = request.COOKIES.get("username")
        checked = 'checked'
    else:
        username = ''
        checked = ''
    context = {
        'username': username,
        'checked': checked,
    }

    return render(request, 'users/login.html', context)

@api_view()
def address_list(request):
    queryset = Address.objects.all()
    serializer = AddressSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view()
def user_list(request):
    queryset = User.objects.all()
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)
