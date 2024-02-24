from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import login,logout, authenticate
from django.shortcuts import redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from datetime import datetime

from website.helper import renderhelper,is_ajax
from website.models import CustomUser
from website.decorators import admin_required,student_required

# Login View
class LoginPageView(View):
    context = {}

    def get(self, request):
        return renderhelper(request,'layout', 'login', self.context)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        # try:
        #     validate_password(password)
        # except ValidationError as e:
        #     messages.error(request, ', '.join(e.messages))
        #     return renderhelper(request, 'layout','login', self.context)

        # username = CustomUser.objects.get(email=email.lower()).username
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            if user.is_admin:
                return redirect('website:AdminList')
            else:
                return redirect('website:student-dashboard')
        else:
            messages.error(request, 'Username or Password is Incorrect')
            return renderhelper(request,'layout', 'login', self.context)

# Logout View  
class Logout(LoginRequiredMixin,View):
    context={}
    def get(self, request):
        request.session.flush()
        logout(request)
        return redirect('website:login')

# Student Registration   
class StudentRegistrationPageView(View):
    context = {}

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, 'Sign out the current user and register a new user')
            return redirect('website:login')
        else:
            return renderhelper(request,'student', 'student_registration', self.context)

    def post(self, request):
        data = CustomUser()
            
        image = request.FILES.get('image')
        name = request.POST['name']
        email = request.POST['email']
        dob = request.POST['dob']
        phone = request.POST['phone']
        password = request.POST['password']
        username = request.POST['username']

        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, ', '.join(e.messages))
            return renderhelper(request,'student', 'student_registration', self.context)
        
        try:
            data.name=name
            data.image=image
            if dob:
                dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
                data.birth_date = dob_date
            data.phone=phone
            data.email=email
            data.username=username
            data.set_password(password)
            data.password_text=password
            data.is_student=True   
            data.save()
            login(request,data)
            messages.info(request, 'Account Created Successfully')
            return redirect('website:student-dashboard')
        except:
            messages.info(request, 'Something Went Wrong')
            return renderhelper(request,'student', 'student_registration', self.context)

# Student Dashboard
@method_decorator(student_required, name='dispatch')
class StudentDashboard(View):
    def get(self, request):
        context={}
        path="dashboard"
        user=request.user
        context['data']=user
        context['path']=path
        return renderhelper(request,'student','student_dashboard',context)
    

# Student Profile Edit  
@method_decorator(student_required, name='dispatch')
class StudentProfileEditView(View):
    def get(self, request):
        context={}
        data=request.user
        context['data']=data
        return renderhelper(request,'student', 'student_registration', context)

    def post(self, request):

        data = CustomUser.objects.get(id=request.user.id)

            
        image = request.FILES.get('image')
        name = request.POST['name']
        email = request.POST['email']
        dob = request.POST['dob']
        phone = request.POST['phone']
        password = request.POST['password']
        username = request.POST['username']

        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, ', '.join(e.messages))
            return renderhelper(request,'student', 'student_registration', self.context)
        
        try:
            data.name=name
            data.image=image
            if dob:
                dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
                data.birth_date = dob_date
            data.phone=phone
            data.email=email
            data.username=username
            data.set_password(password)
            data.password_text=password
            data.is_student=True   
            data.save()
            login(request,data)
            messages.info(request, 'Successfully Updated')

        except:
            messages.info(request, 'Something Went Wrong')
        return redirect('website:student-dashboard')


# Admin Registration   
class AdminRegistrationPageView(View):
    context = {}

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, 'Sign out the current user and register a new user')
            return redirect('website:login')
        else:
            return renderhelper(request,'admin', 'admin_registration', self.context)

    def post(self, request):
        data = CustomUser()
            
        image = request.FILES.get('image')
        name = request.POST['name']
        email = request.POST['email']
        dob = request.POST['dob']
        phone = request.POST['phone']
        password = request.POST['password']
        username = request.POST['username']

        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, ', '.join(e.messages))
            return renderhelper(request,'admin', 'admin_registration', self.context)
        
        try:
            data.name=name
            data.image=image
            if dob:
                dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
                data.birth_date = dob_date
            data.phone=phone
            data.email=email
            data.username=username
            data.set_password(password)
            data.password_text=password
            data.is_admin=True   
            data.save()
            login(request,data)
            messages.info(request, 'Admin Created Successfully')
            return redirect('website:AdminList')
        except:
            messages.info(request, 'Something Went Wrong')
            return renderhelper(request,'admin', 'admin_registration', self.context)

# Admin Dashboard   
@method_decorator(admin_required, name='dispatch')    
class AdminDashboard(LoginRequiredMixin,View):
    def get(self, request):
        context = {}
        path="dashboard"
        conditions = Q()
        if is_ajax(request):
            page = request.GET.get('page', 1)
            context['page'] = page
            searchkey = request.GET.get('searchkey')
            status = request.GET.get('status')
            mark = request.GET.get('mark')

            type = request.GET.get('type')
            if type == '1':
                id = request.GET.get('id')
                vl = request.GET.get('vl')
                cat = CustomUser.objects.get(id=id)
                if vl == '2':
                    cat.is_active = False
                else:
                    cat.is_active = True
                cat.save()
                messages.info(request, 'Successfully Updated')

            if searchkey:
                conditions |= Q(name__icontains=searchkey)
            if status:
                conditions &= Q(is_active=status)
            if mark:
                id = request.GET.get('id')
                print(id)
                print("mark",mark)
                CustomUser.objects.filter(id=id).update(marks=mark)
                messages.info(request, 'Mark Updated Successfully')

            data_list = CustomUser.objects.filter(conditions,is_student=True).order_by('-id')
            paginator = Paginator(data_list, 15)

            try:
                datas = paginator.page(page)
            except PageNotAnInteger:
                datas = paginator.page(1)
            except EmptyPage:
                datas = paginator.page(paginator.num_pages)
            context['datas'] = datas
            template = loader.get_template('website/admin/admin_table.html')
            html_content = template.render(context, request)

            return JsonResponse({'status': True, 'template': html_content})


        data = CustomUser.objects.filter(is_student=True).order_by('-id')

        p = Paginator(data, 15)
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        context["path"]=path
        context['datas'] = page
        context['page'] = page_num
        return renderhelper(request, 'admin', 'admin_view',context)




