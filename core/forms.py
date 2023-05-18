from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from core.models import Comentario


class EmailForm(forms.Form):
    nome = forms.CharField(max_length=100)
    email = forms.EmailField()
    destino = forms.EmailField()
    coments = forms.CharField(required=False,
                              widget=forms.Textarea)

    def enviar_email(self, meupost):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        destino = self.cleaned_data['destino']
        coments = self.cleaned_data['coments']

        conteudo = f'Leia o post: {meupost.titulo}\n' \
                   f'Comentários: {coments}'
        mail = EmailMessage(
            subject=f'{nome} recomenda ler o Post{meupost.titulo}',
            body=conteudo,
            from_email=email,
            to=[destino],
            headers={'Reply-To': email}
        )
        mail.send()


class ComentModelForm(forms.ModelForm):

    class Meta:
        model = Comentario
        fields = ['nome', 'email', 'texto']

    def salvarComentario(self, post):
        novo_coment = self.save(commit=False)
        novo_coment.post = post
        novo_coment.nome = self.cleaned_data['nome']
        novo_coment.email = self.cleaned_data['email']
        novo_coment.texto = self.cleaned_data['texto']
        return novo_coment.save()


class CadUsuarioForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']