from django.shortcuts import render, redirect
from allauth.account import views

from django.views import View #カスタムユーザー
from accounts.models import CustomUser, Post_Inquiry #カスタムユーザー
from accounts.forms import ProfileForm, SignupUserForm, Inquiry #カスタムユーザー
from django.contrib.auth.mixins import LoginRequiredMixin #カスタムユーザー

from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q

import datetime

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator


# パスワードリセット機能
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives


import requests
import os


TMDB_TOKEN = os.environ.get("TMDB_TOKEN")
headers = {
    "accept": "application/json",
    "Authorization": TMDB_TOKEN
}

genresLists = requests.get("https://api.themoviedb.org/3/genre/movie/list?language=ja", headers=headers).json().get("genres")


class LoginView(views.LoginView):
    template_name = 'accounts/login/login.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "password_change"
        context["genresLists"] = genresLists
        return context

class LogoutView(views.LogoutView):
    template_name = 'accounts/login/logout.html'
    
    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('/')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "password_change"
        context["genresLists"] = genresLists
        return context


class SignupView(views.SignupView):
    template_name = 'accounts/register/signup.html'
    form_class = SignupUserForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["genresLists"] = genresLists
        return context

def TermsView(request):
    return render(request, "accounts/register/terms.html")

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        Switch = False

        user_data = CustomUser.objects.get(id=request.user.id)
        return render(request, 'accounts/profile/profile.html', {
            'user_data': user_data,
            'genresLists': genresLists,
            'Switch': Switch
        })



from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from pathlib import Path

class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        form = ProfileForm(
            request.POST or None,
            initial={
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
                'nick_name': user_data.nick_name,
                'user_screen_id': user_data.user_screen_id,
                'year': user_data.year,
                'zipcode': user_data.zipcode,
                'address': user_data.address,
                'buildingname': user_data.buildingname,
                'tel': user_data.tel,
                'job': user_data.job,
                'avatar': user_data.avatar,
            }
        )
        return render(request, 'accounts/profile/profile_edit.html',{
            'form': form,
            'genresLists': genresLists,
        })

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        errors = []
        if form.is_valid():

            def validate_unique(self):
                user_screen_id = self
                SearchResult =  CustomUser.objects.filter(user_screen_id=user_screen_id).exclude(id=request.user.id)
                # print(SearchResult)
                if SearchResult.exists():
                    errors.append(f"{user_screen_id}は既に使われています。別のIDに変更してください")
                return user_screen_id
            
            user_data = CustomUser.objects.get(id=request.user.id)
            user_data.first_name = form.cleaned_data['first_name']
            user_data.last_name = form.cleaned_data['last_name']
            user_data.nick_name = form.cleaned_data['nick_name']
            user_data.user_screen_id = validate_unique(form.cleaned_data['user_screen_id'])
            # user_data.user_screen_id = form.cleaned_data['user_screen_id']
            user_data.year = form.cleaned_data['year']
            user_data.zipcode = form.cleaned_data['zipcode']
            user_data.address = form.cleaned_data['address']
            user_data.buildingname = form.cleaned_data['buildingname']
            user_data.tel = form.cleaned_data['tel']
            user_data.job = form.cleaned_data['job']
            
            image_file_dict = self.request.FILES
            if image_file_dict:
                avatar = request.FILES['avatar']
                
                IMG_SIZE: tuple[int, int] = (600, 600)
                    # メモリ上のデータを読み込む
                mem_img: InMemoryUploadedFile = avatar
                # InMemoryUploadedFileのデータをBytesIOにコピー
                byte_io: BytesIO = BytesIO()
                for chunk in mem_img.chunks():
                    byte_io.write(chunk)
                byte_io.seek(0)

                # BytesIOからPIL Imageを読み込む
                org_img: Image.Image = Image.open(byte_io)
                # 画像の加工
                # tgt_img: Image.Image = org_img.resize(IMG_SIZE)
                w, h = Image.Image.width, Image.Image.height
                print(org_img.format)
                tgt_img: Image.Image = org_img.crop((0, 0, 400, 400))
                image_io: BytesIO = BytesIO()
                tgt_img.save(image_io, format=f"{org_img.format}")
                bmp_path: str = str(Path(mem_img.name).with_suffix(f'.{org_img.format}'))

                # 画像の保存
                uploaded_file = InMemoryUploadedFile(
                    image_io, None, bmp_path, mem_img.content_type,
                    image_io.tell(), None
                )
                user_data.avatar = uploaded_file
                
            print(form.errors.get_json_data())
            values  = form.errors.get_json_data().values()



            if errors:
                return render(request, 'accounts/profile/profile_edit.html',{
                'form': form,
                'genresLists': genresLists,
                'errors': errors
            })

            user_data.save()

            return redirect('profile')
        else:
            user_data = CustomUser.objects.get(id=request.user.id)
            form = ProfileForm(
            request.POST or None,
            initial={
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'nick_name': form.cleaned_data['nick_name'],
                'user_screen_id': user_data.user_screen_id,
                'year': form.cleaned_data['year'],
                'zipcode': form.cleaned_data['zipcode'],
                'address': form.cleaned_data['address'],
                'buildingname': form.cleaned_data['buildingname'],
                'tel': form.cleaned_data['tel'],
                'job': form.cleaned_data['job'],
                'avatar': user_data.avatar,
            }
        )
            
            for value in values:
                for v in value:
                    errors.append(v["message"])

            return render(request, 'accounts/profile/profile_edit.html',{
            'form': form,
            'genresLists': genresLists,
            'errors': errors
        })

class ProfileCheckView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/profile/profile_delete.html')
    
    def post(self, request, *args, **kwargs):
        return redirect('profile_delete', 'True')

class ProfileDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            if self.request.user.is_authenticated:
                if self.kwargs['slug'] == "True":
                    CustomUser.objects.get(id=self.request.user.id).delete()
                    self.logout()
            else:
                return redirect('profile')
        except:
            return redirect('profile')
        return redirect('Index')


class ManageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        
        return render(request, 'accounts/manage.html', {
                'genresLists': genresLists,
        })


class InquiryView(View):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            try:
                form = Inquiry(request.POST or None)
                context = {
                    'form': form,
                    'genresLists': genresLists,
                }
                return render(request, 'accounts/inquiry/inquiry.html', context)
            except ObjectDoesNotExist:
                return redirect('management')
        
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                form = Inquiry(request.POST or None)
                if form.is_valid():
                    inquiry_data = Post_Inquiry()
                    inquiry_data.email = form.cleaned_data['email']
                    inquiry_data.first_name = form.cleaned_data['first_name']
                    inquiry_data.last_name = form.cleaned_data['last_name']
                    inquiry_data.title = form.cleaned_data['title']
                    inquiry_data.summary = form.cleaned_data['summary']
                    inquiry_data.read_field = form.cleaned_data['read_field']
                    inquiry_data.save()
                    return redirect('Inquiry_complete')
            except:
                    return redirect('management')
        return redirect('management')

class InquiryCompleteView(View):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            try:
                inquiry_data = Post_Inquiry.objects.filter(email=request.user.email).order_by('-created').all()[0]
                # send_email(inquiry_data)
                return render(request, 'accounts/inquiry/inquiry_send_completely.html', {
                    'genresLists': genresLists,
                })
            except ObjectDoesNotExist:
                return redirect('management')

class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    """パスワード変更ビュー"""
    success_url = reverse_lazy('password_change_done')
    template_name = 'accounts/password/password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "password_change"
        context["genresLists"] = genresLists
        return context

class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'accounts/password/password_change_done.html'

class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'accounts/mail_template/reset/subject.txt'
    email_template_name = 'accounts/mail_template/reset/message.txt'
    template_name = 'accounts/password/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')

class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'accounts/password/password_reset_done.html'

class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'accounts/password/password_reset_confirm.html'

class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'accounts/password/password_reset_complete.html'

