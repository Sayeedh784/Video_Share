from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import View
from hitcount.views import HitCountDetailView
# Create your views here.
def home(request):
  all_video= PostVideo.objects.all()
  return render(request,'app/home.html',{'all':all_video})

def search_list(request):
  if request.method == 'POST':
    q = request.POST['q']
    videos = PostVideo.objects.filter(caption__icontains=q)
    
    
  context = { 'q': q, 'videos':videos}
  return render(request,'app/search_list.html',context)

class UserUpdateView(LoginRequiredMixin,UpdateView):
  model = User
  fields = ('name','image','location')
  template_name = 'app/user_profile.html'
  login_url = 'login'

  def dispatch(self,request,*args,**kwargs):
    obj= self.get_object()
    if obj.id != self.request.user.id:
      raise PermissionDenied
    return super().dispatch(request,*args,**kwargs)

def user_signup(request):
  if request.method == "POST":
    form = UserSignupForm(request.POST)
    if form.is_valid():
      form.save()
      email = form.cleaned_data.get('email')
      messages.success(request, "Congratulations!!! Registered successfully")
      form = UserSignupForm()
      return redirect('login')
  else:
    form = UserSignupForm()
  context = {
      'form': form
  }
  return render(request, 'app/signup.html', context)

def profile(request,id):
  user = User.objects.get(id=request.user.id)
  myupload = PostVideo.objects.filter(user = request.user.id)

  return render(request, 'app/profile.html',{'user':user,'myupload':myupload})

def seeprofile(request,pk):
  profileid = User.objects.get(pk=pk)
  return render(request,'app/profile.html',{'profileid':profileid})

class VideoPostCreateView(LoginRequiredMixin,CreateView):
  model = PostVideo
  template_name = 'app/videoupload.html'
  fields = ("caption","description","video")
  login_url = 'login'

  def form_valid(self, form):
    form.instance.user = User.objects.get(id=self.request.user.id)
    return super().form_valid(form)


class VideoDetailView(HitCountDetailView):
  model = PostVideo
  template_name = 'app/video_detail.html'
  count_hit = True

class VideoUpdateView(LoginRequiredMixin,UpdateView):
  model = PostVideo
  fields = ("caption","description","video")
  template_name = 'app/video_update.html'
  login_url = 'login'

  def dispatch(self,request,*args,**kwargs):
    obj= self.get_object()
    if obj.user != self.request.user:
      raise PermissionDenied
    return super().dispatch(request,*args,**kwargs)

class VideoDeleteView(LoginRequiredMixin,DeleteView):
  model = PostVideo
  template_name = 'app/video_delete.html'
  success_url = reverse_lazy('home')
  login_url = 'login'


  def dispatch(self,request,*args,**kwargs):
    obj= self.get_object()
    if obj.user != self.request.user:
      raise PermissionDenied
    return super().dispatch(request,*args,**kwargs)

class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
      post = PostVideo.objects.get(pk=pk)

      is_dislike = False

      for dislike in post.dislikes.all():
          if dislike == request.user:
              is_dislike = True
              break

      if is_dislike:
          post.dislikes.remove(request.user)

      is_like = False

      for like in post.likes.all():
          if like == request.user:
              is_like = True
              break

      if not is_like:
          post.likes.add(request.user)

      if is_like:
          post.likes.remove(request.user)

      next = request.POST.get('next', '/')
      return HttpResponseRedirect(next)

class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
      post = PostVideo.objects.get(pk=pk)

      is_like = False

      for like in post.likes.all():
          if like == request.user:
              is_like = True
              break

      if is_like:
          post.likes.remove(request.user)

      is_dislike = False

      for dislike in post.dislikes.all():
          if dislike == request.user:
              is_dislike = True
              break

      if not is_dislike:
          post.dislikes.add(request.user)

      if is_dislike:
          post.dislikes.remove(request.user)

      next = request.POST.get('next', '/')
      return HttpResponseRedirect(next)


  
 