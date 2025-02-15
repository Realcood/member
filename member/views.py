from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from .models import Member


def index(request):
    context = {}
    # context['m_id'] = request.session['m_id']
    # context['m_name'] = request.session['m_name']

    # m_id 세션변수 값이 없다면 '' 을 넣어라
    context['m_id'] = request.session.get('m_id', '')
    context['m_name'] = request.session.get('m_name', '')

    return render(request, 'member/index.html', context)

def member_reg(request):
    if request.method == "GET":
        return render(request, 'member/member_reg.html')
    
    elif request.method == "POST":
        member_id = request.POST.get("member_id")
        passwd = request.POST.get("passwd")
        name = request.POST.get("name")
        email = request.POST.get("email")

        # 회원가입 중복 체크
        if Member.objects.filter(member_id=member_id).exists():
            return render(request, 'member/member_reg.html', {"message": f"{member_id}가 중복됩니다."})
        
        # 회원 생성
        Member.objects.create(member_id=member_id, passwd=passwd, name=name, email=email)

        return redirect('index')  # 회원가입 후 메인 페이지로 이동

def member_login(request):
    if request.method == "GET":
        return render(request, 'member/login.html')
    elif request.method == "POST":
        context = {}

        member_id = request.POST.get('member_id')
        passwd = request.POST.get('passwd')

        # 로그인 체크하기
        rs = Member.objects.filter(member_id=member_id, passwd=passwd).first()
        print(member_id + '/' + passwd)
        print(rs)

        #if rs.exists():
        if rs is not None:

            # OK - 로그인
            request.session['m_id'] = member_id
            request.session['m_name'] = rs.name

            context['m_id'] = member_id
            context['m_name'] = rs.name
            context['message'] = rs.name + "님이 로그인하셨습니다."
            return render(request, 'member/index.html', context)

        else:

            context['message'] = "로그인 정보가 맞지않습니다.\\n\\n확인하신 후 다시 시도해 주십시오."
            return render(request, 'member/login.html', context)


def member_logout(request):
    request.session.flush()
    return redirect('/member/')