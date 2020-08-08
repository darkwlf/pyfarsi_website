from django.views.generic import CreateView, ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import reverse, redirect
from . import forms, models, actions
from .functions import take_action
from django.utils.text import slugify
from django.db.models import Q


class Group(DetailView):
    template_name = 'snippets/group.html'
    model = models.Group

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            try:
                self.extra_context = {'member': models.Member.objects.get(user=request.user, group=self.object)}
            except models.Member.DoesNotExists:
                pass
        return super().get_context_data()


class Snippets(ListView):
    paginate_by = 15
    template_name = 'snippets/snippets.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            memberships = self.request.user.member_user.select_related('group').filter(
                status=models.Member.Status.member, group__type=models.Group.Type.private
                )
            groups = [group_tuple[0] for membership_groups in memberships.values_list(
                'group__id'
                ) for group_tuple in membership_groups]
        else:
            groups = []
        keyword = self.request.GET.get('q', '')
        result = models.Snippet.objects.filter((
            Q(group__type=models.Group.Type.public) | Q(group__id__in=groups)
            ) & (Q(name__icontains=keyword) | Q(description__icontains=keyword)))
        if self.request.GET['groups']:
            groups = self.request.GET['groups'].split(', ')
            return result.filter(group__id__in=groups)
        return result


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
def snippet_actions(request, snippet_id:int, action: str):
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
            take_action(snippet, action)
    else:
        take_action(snippet, action)
    if action is actions.close:
        return redirect('snippets:snippet', pk=snippet_id)
    return redirect('snippets:snippets', groups=snippet.group.id)
