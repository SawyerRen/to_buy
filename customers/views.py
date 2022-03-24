from django.shortcuts import render, redirect, reverse
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
        passport = User.objects.add_user(username=username, password=get_hash(password), email=email,gender=gender)
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

def login_check(request):
    '''进行用户登录校验'''
    # 1.获取数据
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')

    # 2.数据校验
    if not all([username, password, remember]):
        # 有数据为空
        return JsonResponse({'res': 2, 'errmsg': 'data cannot be null'})

    # 3.进行处理:根据用户名和密码查找账户信息
    passport = User.objects.get_user(username=username, password=password)

    if passport:
        next_url = reverse('goods:index')
        jres = JsonResponse({'res': 1, 'next_url': next_url})

        # 判断是否需要记住用户名
        if remember == 'true':
            # 记住用户名
            jres.set_cookie('username', username, max_age=7*24*3600)
        else:
            # 不要记住用户名
            jres.delete_cookie('username')

        # 记住用户的登录状态
        request.session['islogin'] = True
        request.session['username'] = username
        request.session['user_id'] = passport.id
        return jres
    else:
        # 用户名或密码错误
        return JsonResponse({'res': 0, 'errmsg': 'username or password is wrong.'})

def logout(request):
    '''用户退出登录'''
    # 清空用户的session信息
    request.session.flush()
    # 跳转到首页
    return redirect(reverse('goods:index'))


@api_view()
def user(request):
    user = User.objects.get(id=request.session['user_id'])

    goodsList = []
    goods_ids = request.COOKIES.get('goods_ids', '')
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',')
        for goods_id in goods_ids1:
            goodsList.append(GoodsDetail.objects.get(id=int(goods_id)))

    context = {'user_email': user.email,
               'user_name': request.session['user_name'],
               'page_name': 1, # 隐藏购物车
               'user_phone':user.phone_number,
               'goods_list': goodsList}
    return render(request, 'user/user_center_info.html', context)

@api_view()
def address(request):
    '''用户中心-地址页'''
    # 获取登录用户的id
    passport_id = request.session.get('user_id')

    if request.method == 'GET':
        # 显示地址页面
        # 查询用户的默认地址
        addr = Address.objects.get_default_address(user_id=passport_id)
        return render(request, 'user/user_center_site.html', {'addr': addr, 'page': 'address'})
    else:
        # 添加收货地址
        # 1.接收数据
        recipient_first_name = request.POST.get('first_name')
        recipient_second_name= request.POST.get('last_name')
        state = request.POST.get('state')
        county=request.POST.get('county')
        street=request.POST.get('street')
        zip_code = request.POST.get('zip_code')
        recipient_phone = request.POST.get('phone')

        # 2.进行校验
        if not all([recipient_name, recipient_addr, zip_code, recipient_phone]):
            return render(request, 'users/user_center_site.html', {'errmsg': '参数不能为空!'})

        # 3.添加收货地址
        Address.objects.add_one_address(user_id=user_id,
                           recipient_first_name=recipient_first_name,
                           recipient_second_name=recipient_second_name,
                           state=state,
                           county=county,
                           street=street,
                           zip_code=zip_code,
                           recipient_phone=recipient_phone)

        # 4.返回应答
        return redirect(reverse('user:address'))
