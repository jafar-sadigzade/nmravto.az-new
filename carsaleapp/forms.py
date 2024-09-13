from django import forms
from carsaleapp.models import Comment, CarDetail, CarSpecification, CarPricing, CarImage


class NewComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"


class CarDetailForm(forms.ModelForm):
    # Fields from CarSpecification
    gearbox = forms.CharField(max_length=20, required=False)
    mileage = forms.IntegerField(required=False)
    distanceunit = forms.CharField(max_length=5, required=False)
    volume = forms.IntegerField(required=False)
    power = forms.IntegerField(required=False)
    condition = forms.CharField(widget=forms.Textarea, required=False)

    # Fields from CarPricing
    price = forms.IntegerField(required=False)
    priceunit = forms.CharField(max_length=8, required=False)

    # Fields from CarImage
    front = forms.ImageField(required=False)
    side = forms.ImageField(required=False)
    interior = forms.ImageField(required=False)

    class Meta:
        model = CarDetail
        fields = [
            'usage', 'brand', 'model', 'ban', 'color', 'fuel',
            'year', 'market', 'seats', 'credit', 'swap', 'is_comment', 'addinfo',
            'gearbox', 'mileage', 'distanceunit', 'price', 'priceunit', 'volume',
            'power', 'condition', 'front', 'side', 'interior'
        ]
        widgets = {
            'condition': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'addinfo': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    def save(self, commit=True):
        car_detail = super().save(commit=False)

        if commit:
            car_detail.save()

        # Save or update CarSpecification instance
        car_specification, created = CarSpecification.objects.update_or_create(
            car=car_detail,
            defaults={
                'gearbox': self.cleaned_data['gearbox'],
                'mileage': self.cleaned_data['mileage'],
                'distanceunit': self.cleaned_data['distanceunit'],
                'volume': self.cleaned_data['volume'],
                'power': self.cleaned_data['power'],
                'condition': self.cleaned_data['condition'],
            }
        )

        # Save or update CarPricing instance
        car_pricing, created = CarPricing.objects.update_or_create(
            car=car_detail,
            defaults={
                'price': self.cleaned_data['price'],
                'priceunit': self.cleaned_data['priceunit'],
            }
        )

        # Save or update CarImage instance
        car_image, created = CarImage.objects.update_or_create(
            car=car_detail,
            defaults={
                'front': self.cleaned_data['front'],
                'side': self.cleaned_data['side'],
                'interior': self.cleaned_data['interior'],
            }
        )

        return car_detail
