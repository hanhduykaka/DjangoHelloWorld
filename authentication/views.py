from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


# def index(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return render(request, 'officematter/index.html')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'authentication/index.html', {'form': form})

def user_login(request):
    return render(request,"authentication/index.html")

def index(request):
     if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password = password)
        if user:
             return render(request, "officematter/index.html")
            # if user.is_active:
            #     login(request, user)
            #     result = "Chào bạn " + username
            #     return render(request, "officematter/index.html", context={'result':result})
            # else:
            #     print("Không đăng nhập được")
            #     print("Username: {} and password: {}".format(username, password))
            #     login_result = "Username và password không hợp lệ"
            #     return render(request, "authentication/index.html",context={'login_result': login_result})
     else:
         form = AuthenticationForm()
         return render(request, 'authentication/index.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    result = "Bạn đã đăng xuất. Vui lòng chọn 'Đăng nhập'"
    return render(request, "officematter/index.html", {"result":result})