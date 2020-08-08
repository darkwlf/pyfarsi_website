from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import reverse, redirect
from . import forms
from . import models
from .functions import close_snippet
from django.utils.text import slugify


class Group(LoginRequiredMixin, DetailView):
    template_name = 'snippets/group.html'
    model = models.Group

    def get_context_data(self, **kwargs):
        try:
            self.extra_context = {'member': models.Member.objects.get(user=request.user, group=self.object)}
        except models.Member.DoesNotExists:
            pass
        return super().get_context_data()


class CreateGroup(LoginRequiredMixin, CreateView):
    model = models.Group
    fields = ('name', 'description', 'type', 'logo')
    template_name = 'snippets/create_group.html'

    def form_valid(self, form):
        self.object = form.save(False)
        self.object.slug = slugify(self.object.name, True)
        self.object.save()
        models.Member.objects.create(
            user=self.request.user, group=self.object, rank=models.Member.Rank.owner, status=models.Member.Rank.member
            )
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('snippets:group', kwargs={'pk': self.object.id, 'slug': self.object.slug})


class CreateSnippet(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = forms.Snippet
    template_name = 'snippets/create_snippet.html'
    redirect_field_name = None

    def get_success_url(self):
        return reverse('snippets:snippet', kwargs={'pk': self.object.id})

    def test_func(self):
        group = models.Group.objects.get(id=self.kwargs['group_id'])
        try:
            return models.Member.objects.get(user=self.request.user, group=group)
        except models.Member.DoesNotExists:
            return group.type == models.Group.Type.public

    def form_valid(self, form):
        self.object = form.save(False)
        self.object.user = self.request.user
        self.object.group = get_object_or_404(
            models.Member, user=self.request.user, group__id=self.kwargs['group_id']
        ).group
        self.object.slug = slugify(self.object.name, True)
        self.object.save()
        for screenshot in self.request.FILES.getlist('screenshots'):
            models.ScreenShot.objects.create(snippet=self.object, file=screenshot)
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        self.extra_context = {'group_id': self.kwargs['group_id']}
        return super().get_context_data(**kwargs)


class Snippet(UserPassesTestMixin, DetailView):
    model = models.Snippet
    template_name = 'snippets/snippet.html'
    redirect_field_name = None

    def test_func(self):
        try:
            return models.Member.objects.get(user=self.request.user, group=self.object.group)
        except models.Member.DoesNotExists:
            return self.object.group.type == models.Group.Type.public

    def get_context_data(self, **kwargs):
        self.extra_context = {'screenshots': self.object.screenshot_snippet.all()}
        return super().get_context_data(**kwargs)


@login_required
def join_group_with_link(request, invite_id):
    invite = get_object_or_404(models.InviteLink, invite_id=invite_id)
    member, created = models.Member.objects.get_or_create(
        user=request.user, group=invite.group, defaults={'status': models.Member.Status.member}
        )
    if created:
        invite.users_joined += 1
        invite.save()
    return redirect('snippets:group', pk=invite.group.id)


@login_required
def join_group(request, group_id):
    group = get_object_or_404(models.Group, id=group_id)
    models.Member.objects.get_or_create(
        user=request.user, group=group, defaults={'status': models.Member.Status.pending}
        )
    return redirect('snippets:group', pk=group.id)


@login_required
def close_snippet(request, snippet_id):
    snippet = get_object_or_404(models.Snippet, id=snippet_id)
    if snippet.user != request.user:
        try:
            models.Member.objects.get(
                user=request.user,
                rank__in=(models.Member.Rank.admin, models.Member.Rank.owner),
                group=snippet.group
                )
        except models.Member.DoesNotExists:
            pass
        else:
            close_snippet(snippet)
    else:
        close_snippet(snippet)
    return redirect('snippets:snippet', pk=snippet_id)
