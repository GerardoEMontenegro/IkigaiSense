# forms.py
from django import forms
from apps.post.models import Post, Comment, PostImage

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'allow_comments']
        labels = {
            'title': 'Título',
            'category': 'Categoría',
            'content': 'Contenido',
            'allow_comments': 'Permitir comentarios',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#6D9773]'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#6D9773]',
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'rows': 8,
                'placeholder': 'Escribe el contenido del post...'
            }),
            'allow_comments': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 text-[#6D9773] rounded focus:ring-[#6D9773]',
            }),
        }


class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage  
        fields = ['image']  
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg',
                'accept': 'image/*'  
            })
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError("La imagen no puede superar los 5MB.")
            return image
        raise forms.ValidationError("Debes subir una imagen.")


ImageFormSet = forms.inlineformset_factory(
    Post,           
    PostImage,      
    form=PostImageForm,  
    extra=3,        
    can_delete=True,
    max_num=5,
    validate_max=True,
    min_num=0,
    validate_min=False,
)


class PostFilterForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        label='Buscar',
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar por título o contenido...',
            'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#6D9773]'
        })
    )
    order_by = forms.ChoiceField(
        required=False,
        label='Ordenar por',
        choices=[
            ('-created_at', 'Más recientes'),
            ('created_at', 'Más antiguos'),
            ('-amount_comments', 'Más comentados'),
            ('-average_rating', 'Mejor puntuados'),
        ],
        widget=forms.Select(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#6D9773]'
        })
    )