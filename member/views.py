from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from .models import Member, UserLog


def index(request):
    """메인 페이지"""
    context = {
        "m_id": request.session.get("m_id", ""),
        "m_name": request.session.get("m_name", ""),
    }
    return render(request, "member/index.html", context)


@csrf_exempt
def member_reg(request):
    """회원가입 기능"""
    if request.method == "GET":
        return render(request, "member/member_reg.html")

    elif request.method == "POST":
        member_id = request.POST.get("member_id")
        passwd = request.POST.get("passwd")
        name = request.POST.get("name")
        email = request.POST.get("email")

        # 회원가입 중복 체크
        if Member.objects.filter(member_id=member_id).exists():
            return render(request, "member/member_reg.html", {"message": f"{member_id}는 이미 존재하는 아이디입니다."})

        # 회원 정보 저장
        member = Member.objects.create(
            member_id=member_id,
            passwd=passwd,
            name=name,
            email=email
        )

        # 회원가입 로그 기록
        UserLog.objects.create(member=member, action="signup")

        # 회원가입 완료 후 로그인 페이지로 리디렉션
        context = {
            "message": f"{member_id}로 회원가입이 완료되었습니다. 로그인 해주세요."
        }
        return render(request, "member/login.html", context)


def member_login(request):
    """로그인 기능"""
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

        if rs is not None:
            # 로그인 성공
            request.session['m_id'] = member_id
            request.session['m_name'] = rs.name

            context['m_id'] = member_id
            context['m_name'] = rs.name
            context['message'] = rs.name + "님이 로그인하셨습니다."
            
            # 로그인 후 낙상방지 시스템 페이지로 이동
            return render(request, "member/fall_prevention.html", context)

        else:
            context['message'] = "로그인 정보가 맞지않습니다.\\n\\n확인하신 후 다시 시도해 주십시오."
            return render(request, 'member/login.html', context)


def member_logout(request):
    """로그아웃 기능"""
    request.session.flush()
    return redirect('/member/')


def fall_prevention(request):
    """낙상방지 시스템 페이지"""
    return render(request, "member/fall_prevention.html")
