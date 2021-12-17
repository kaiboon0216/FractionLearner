from django.shortcuts import render,redirect,get_object_or_404,reverse
from .models import Tutorial,FilesAdmin,Comment,Qcomment
from django.contrib.auth.models import User
from django.views.generic import ListView,TemplateView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import DocumentForm,CommentForm,QcommentForm
from django.contrib import messages

# Create your views here.

def home(request):
    context={
        
        }
    return render(request,'tutorial/homepage.html',context)

def addquestion(request):
    context={
        'file' : FilesAdmin.objects.all()
        }
    return render(request,'tutorial/addquestion.html',context)


class TutorialCreateView(CreateView):
    model = Tutorial 
    fields = ['title','content','image'] 

    def form_valid(self,form):
        form.instance.author = self.request.user 
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['file'] = FilesAdmin.objects.all()
        return context

class TutorialDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tutorial 
    success_url ='/tutorial/' 

    def test_func(self): 
        post = self.get_object() 
        if self.request.user == post.author: 
            return True
        return False

class TutorialListView(ListView):
    model = Tutorial
    template_name = 'tutorial/home.html'
    context_object_name = 'Tutorial' 
    ordering = ['-date_published'] 
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['file'] = FilesAdmin.objects.all()
        return context


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = '/tutorial/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Comment
    fields = ['comment']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)\

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class QcommentUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Qcomment
    fields = ['qcomment']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)\

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class QcommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Qcomment
    success_url = '/tutorial/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class TutorialDetailView(DetailView): 
    model = Tutorial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['file'] = FilesAdmin.objects.all()
        return context

class TutorialUpdateView(UpdateView):
    model = Tutorial 
    fields = ['title','content','image'] 
    
    def form_valid(self,form): 
        form.instance.author = self.request.user 
        return super().form_valid(form)

@login_required
def search(request):
    error = False # Initially no error
    if 'search' in request.GET: # To check there is ‘search’ exist in request.GET/Verify that there is non-empty value  
        search = request.GET['search'] # To Define that search is in the request.GET
        if not search: # If submit empty value
            error = True # It will display error messages
        else:
            users = User.objects.filter(username__icontains=search)
            tutorials = Tutorial.objects.filter(title__icontains=search) # It will show/filter questions based on the keyword
            context = {
                'tutorials': tutorials,
                'users' :users,
                 'query': search,
                'file' : FilesAdmin.objects.all()
            }
            return render(request, 'tutorial/search_results.html', context)
    context = {
        'error': error,
        'file' : FilesAdmin.objects.all()
    }
    return render(request, 'tutorial/search_results.html', context) 

@login_required
def download(request,path):
	file_path=os.path.join(settings.MEDIA_ROOT,path)
	if os.path.exists(file_path):
		with open(file_path,'rb')as fh:
			response=HttpResponse(fh.read(),content_type="application/adminupload")
			response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
			return response
	raise Http404

def upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = request.FILES.get('files')
            FilesAdmin(file=newdoc)
            form.save()
            return redirect('tutorial')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page

    # Render list page with the documents and the form
    context = {'file' : FilesAdmin.objects.all(), 'form': form}
    return render(request, 'tutorial/notes_upload.html', context)

def tutorial_like(request,pk):
    post = get_object_or_404(Tutorial,pk=pk) 
    if request.method == 'POST': 
        if post.liked_by.filter(id=request.user.id).exists():
            post.liked_by.remove(request.user) 
            post.like -= 1 
        else:
            post.liked_by.add(request.user)
            post.like += 1 
            post.save() 
        return redirect((reverse('tutorial-detail', kwargs={'pk':post.pk}))) 
    return render(request,'tutorial/tutoriallike_form.html')

def comment_like(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post = comment.post.pk  
    if request.method == 'POST': 
        if comment.liked_by.filter(id=request.user.id).exists():
            comment.liked_by.remove(request.user) 
            comment.like -= 1 
        else:
            comment.liked_by.add(request.user)
            comment.like += 1 
            comment.save() 
        return redirect((reverse('tutorial-detail', kwargs={'pk':post}))) 
    return render(request,'tutorial/commentlike_form.html')

def add_comment(request,pk):
    post = get_object_or_404(Tutorial,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request,f'You have successfully posted your comment!')
        return redirect((reverse('tutorial-detail', kwargs={'pk':post.pk}))) 

    else:
        form = CommentForm()
    context ={
        'form':form
    }

    return render(request,'tutorial/comment_form.html',context)
    

def qcomment_like(request,pk):
    comment = get_object_or_404(Qcomment,pk=pk)
    post = comment.comment.post.pk 
    if request.method == 'POST': 
        if comment.liked_by.filter(id=request.user.id).exists():
            comment.liked_by.remove(request.user) 
            comment.like -= 1 
        else:
            comment.liked_by.add(request.user)
            comment.like += 1 
            comment.save() 
        return redirect((reverse('tutorial-detail', kwargs={'pk':post}))) 
    return render(request,'tutorial/qcommentlike_form.html')

def add_qcomment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    pk = comment.post.pk
    if request.method == 'POST':
        form = QcommentForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            qcomment = form.save(commit=False)
            qcomment.comment = comment
            qcomment.save()
            messages.success(request,f'You have successfully posted your comment!')
        return redirect((reverse('tutorial-detail', kwargs={'pk':pk})))    
    else:
        form = QcommentForm()
    context ={
        'form':form
    }
    return render(request,'tutorial/qcomment_form.html',context)  

def SolutionView(request,pk):
    post = get_object_or_404(Qcomment,pk=pk)
    comment = post.comment.post.pk 
    if request.method =='POST': 
        if post.r_token == False: 
            post.r_token = True 
            post.save() 
        else:
            post.r_token = False 
            post.save()
        return  redirect((reverse('tutorial-detail', kwargs={'pk':comment}))) 
    return render(request,'tutorial/solution_form.html')

