from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import reverse, redirect
from . import forms
from . import models
from django.utils.text import slugify


class Group(LoginRequiredMixin, DetailView):
    template_name = 'snippets/group.html'
    model = models.Group


class CreateGroup(LoginRequiredMixin, CreateView):
    model = models.Group
    fields = ('name', 'description', 'type', 'logo')
    template_name = 'snippets/create_group.html'

    def form_valid(self, form):
        self.object = form.save(False)
        self.object.creator = self.request.user
        self.object.slug = slugify(self.object.name, True)
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('snippets:group', kwargs={'pk': self.object.id, 'slug': self.object.slug})


class CreateSnippet(LoginRequiredMixin, CreateView):
    form_class = forms.Snippet
    template_name = 'snippets/create_snippet.html'

    def get_success_url(self):
        return reverse('snippets:snippet', kwargs={'pk': self.object.id})

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


class Snippet(DetailView):
    model = models.Snippet
    template_name = 'snippets/snippet.html'

    def get_context_data(self, **kwargs):
        self.extra_context = {'screenshots': self.object.screenshot_snippet.all()}
        return super().get_context_data(**kwargs)


@login_required
def join_group(request, invite_id):
    invite = get_object_or_404(models.InviteLink, invite_id=invite_id)
    member, created = models.Member.objects.get_or_create(user=request.user, group=invite.group)
    if created:
        invite.users_joined += 1
        invite.save()
    return redirect('snippets:group', invite.group.id)
