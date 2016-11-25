from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from FamilyConnectionTree.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
# Create your views here.


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })

    return render_to_response(
        'registration/register.html',
        variables,
    )


def register_success(request):
    return render_to_response(
        'success.html',
    )


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def post_list(request):
    try:
        family = Profile.objects.get(userName_id__exact=request.user.id)
    except Exception:
        return profile_edit(request)
    posts = Post.objects.filter(family__exact=family.familyName).order_by('published_date')
    return render(request, 'home.html', {'posts': posts})

def inbox_list(request):
    posts = Message.objects.filter(reciever=request.user)
    return render(request, 'message_inbox.html', {'posts': posts})


def contact(request):
    family = Profile.objects.get(userName_id__exact=request.user.id)
    list_of_families = Profile.objects.filter(familyName__exact=family.familyName)
    return render(request, 'contact.html', {'family_members': list_of_families,'family_name':family.familyName})


def news(request):
    family = Profile.objects.get(userName_id__exact=request.user.id)
    posts = Post.objects.filter(family__exact=family.familyName,post_type__exact=1).order_by('published_date')
    return render(request, 'news.html', {'user': request.user,'posts': posts})


def memories(request):
    family = Profile.objects.get(userName_id__exact=request.user.id)
    posts = Post.objects.filter(family__exact=family.familyName, post_type__exact=2).order_by('published_date')
    return render(request, 'memories.html', {'user': request.user, 'posts': posts})


def facts(request):
    family = Profile.objects.get(userName_id__exact=request.user.id)
    posts = Post.objects.filter(family__exact=family.familyName,post_type__exact=3).order_by('published_date')
    return render(request, 'facts.html', {'user': request.user, 'posts': posts})


def info(request):
    return render(request, 'about.html', {'user': request.user})

def family_info(request):
    family = Profile.objects.get(userName_id__exact=request.user.id)
    membersOfFamily = Profile.objects.filter(familyName__exact=family.familyName)
    famName = Family.objects.get(familyName__exact=family.familyName)
    return render(request, 'family_info.html', {'user': request.user, 'familyInfo':famName , 'FamilyMembers':membersOfFamily})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})


def family_new(request):
    if request.method == "POST":
        form = FamilyForm(request.POST,request.FILES)
        if form.is_valid():
            family = form.save(commit=False)
            family.numberOfMembers = 0
            family.familyPicture=form.cleaned_data['familyPicture']
            family.save()
            return HttpResponseRedirect('/home/')
    else:
        form = FamilyForm()
    return render(request, 'post_edit.html', {'form': form})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            family = Profile.objects.get(userName_id__exact=request.user.id)
            post.family=family.familyName
            post.text = post.text + " ......says  " + family.name
            post.img=form.cleaned_data['img']
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})


def profile_edit(request):
    if request.method == "POST":
        creator_choices = [(c.familyName) for c in Family.objects.all()]
        creator = forms.ChoiceField(required=True, label='Family Name', choices=creator_choices)
        form = ProfileForm(request.POST,request.FILES)
        form.fields['familyName'].choices=creator_choices
        if form.is_valid():
            profile = form.save(commit=False)
            profile.picture = form.cleaned_data['picture']
            profile.userName = request.user
            fam = Family.objects.get(familyName__exact=profile.familyName)
            fam.numberOfMembers = fam.numberOfMembers+1
            profile.save()
            fam.save()
            return render_to_response(
                'home.html',
                {'user': request.user}
            )
    else:
        form = ProfileForm()
    return render(request, 'profile_edit.html', {'form': form})


def message_edit(request):
    if request.method == "POST":
        creator_choices = [(c.username) for c in User.objects.all()]
        creator = forms.ChoiceField(required=True, label='Send To', choices=creator_choices)
        form = MessageForm(request.POST)
        form.fields['reciever'].choices=creator_choices
        if form.is_valid():
            profile = form.save(commit=False)
            profile.sender = request.user
            profile.created_at = timezone.now()
            profile.save()
            return render_to_response(
                'home.html',
                {'user': request.user}
            )
    else:
        form = MessageForm()
    return render(request, 'message_edit.html', {'form': form})