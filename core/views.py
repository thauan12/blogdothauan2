from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, FormView, CreateView

from core.forms import EmailForm, ComentModelForm, CadUsuarioForm
from core.models import Post, Comentario


class IndexView(TemplateView):
    template_name = "blog/index.html"


class ListarPostsListView(ListView):
    context_object_name = 'posts'
    template_name = 'blog/post/listarposts.html'
    queryset = Post.publicados.all()
    paginate_by = 2


class DetalhePostView(DetailView):
    template_name = "blog/post/detalhepost.html"
    context_object_name = 'post'
    queryset = Post.publicados.all()

    def _get_coments(self, id_post):
        try:
            coments = Comentario.objects.filter(post_id=id_post, status=True)
            # coments = Comentario.objects.get(post_id=id_post)
            return coments
        except Comentario.DoesNotExist:
            return Exception

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['comentarios'] = self._get_coments(self.object.id)
        return contexto



class FormContatoView(FormView):
    template_name = 'blog/post/enviarpost.html'
    form_class = EmailForm
    success_url = reverse_lazy('listar_posts')

    def get_post(self, id_post):
        try:
            return Post.publicados.get(pk=id_post)
        except Post.DoesNotExist:
            messages.error(self.request, 'Post não encontrado!')
            reverse_lazy('listar_posts')

    def get_context_data(self, **kwargs):
        context = super(FormContatoView, self).get_context_data(**kwargs)
        context['post'] = self.get_post(self.kwargs['pk'])
        return context

    def form_valid(self, form):
        meupost = self.get_context_data()['post']
        form.enviar_email(meupost)
        messages.success(self.request, f'Post {meupost.titulo} '
                                       f'enviado com sucesso.')
        return super(FormContatoView, self).form_valid(form)

    def form_invalid(self, form):
        meupost = self.get_context_data()['post']
        messages.error(self.request, f'Post {meupost.titulo} não enviado.')
        return super(FormContatoView, self).form_invalid(form)


class ComentarioCreateView(LoginRequiredMixin, CreateView):
    template_name = 'blog/post/comentarios.html'
    form_class = ComentModelForm
    login_url = 'loginuser'

    def _get_post(self, id_post):
        try:
            post = Post.publicados.get(id=id_post)
            return post
        except Post.DoesNotExist:
            return Exception

    def form_valid(self, form, *args, **kwargs):
        post = self._get_post(self.kwargs['pk'])
        form.salvarComentario(post)
        return redirect('detalhe_post', post.publicado.day, post.publicado.month,
                        post.publicado.year, post.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self._get_post(self.kwargs['pk'])
        return context


class CadUsuarioView(CreateView):
    template_name = 'blog/usuarios/cadusuario.html'
    form_class = CadUsuarioForm
    success_url = reverse_lazy('loginuser')

    def form_valid(self, form):
        form.cleaned_data
        form.save()
        messages.success(self.request, 'Usuario Cadastrado!!!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Usuário não cadastrado!!!')
        return super().form_invalid(form)


class LoginUsuarioView(FormView):
    template_name = 'blog/usuarios/login.html'
    model = User
    form_class = AuthenticationForm
    success_url = reverse_lazy('listar_posts')

    def form_valid(self, form):
        nome = form.cleaned_data['username']
        senha = form.cleaned_data['password']
        usuario = authenticate(self.request,username=nome, password=senha)
        if usuario is not None:
            login(self.request, usuario)
            return redirect('listar_posts')
        messages.error(self.request, 'Usuário inexistente.')
        return redirect('loginuser')

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível logar!')
        return redirect('loginuser')


class LogoutView(LoginRequiredMixin, LogoutView):

    def get(self, request):
        logout(request)
        return redirect('listar_posts')


