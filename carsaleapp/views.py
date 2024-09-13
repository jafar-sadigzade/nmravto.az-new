from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from carsaleapp.forms import *
from carsaleapp.models import CarDetail


def cars_request(request):
    cars = CarDetail.objects.select_related('specifications', 'pricing', 'images').prefetch_related('multiple_images',
                                                                                                    'favorites').all()

    paginator = Paginator(cars, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'cars.html', {'cars': page_obj})


def car_detailed_views(request, id):
    car = get_object_or_404(Caradd, id=id)
    context = {"car": car}

    # car comments view
    comments = car.comments.all()
    if request.method == 'POST':
        comment_form = NewComment(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.car = car
            user_comment.save()
            return HttpResponseRedirect('/car_details/' + str(car.id), context)
    else:
        comment_form = NewComment()
    return render(request, "car-details.html", {
        'comments': comments,
        'comments_form': comment_form,
        "car": car,
        "carimages": CarMultipleImages.objects.filter(carid=car.id)
    })


@csrf_exempt
@login_required(login_url="login")
def caradd(request):
    if request.method == 'POST':
        form = CarAddForms(request.POST, request.FILES)
        if form.is_valid():
            new_car = form.save(commit=False)
            new_car.user = request.user
            new_car.save()
            form.save_m2m()  # Save many-to-many relationships

            return render(request, "caradd.html", {"success": "Elanınız uğurla dərc edildi! "})
    else:
        form = CarAddForms()

    return render(request, "caradd.html", {"form": form})


@csrf_exempt
def searchcar(request):
    if request.method == 'POST':
        brand = request.POST.get("brand")
        model = request.POST.get("model")
        pricemin = request.POST.get("minPrice")
        pricemax = request.POST.get("maxPrice")
        yearmin = request.POST.get("minYear")
        yearmax = request.POST.get("maxYear")

        cars = Caradd.objects.all()

        # Add filters based on provided parameters
        if brand:
            cars = cars.filter(brand__icontains=brand)
        if model:
            cars = cars.filter(model__icontains=model)
        if pricemin:
            cars = cars.filter(price__gte=pricemin)
        if pricemax:
            cars = cars.filter(price__lte=pricemax)
        if yearmin:
            cars = cars.filter(year__gte=yearmin)
        if yearmax:
            cars = cars.filter(year__lte=yearmax)

        if (
                brand == '' and model == '' and pricemin == '' and pricemax == '' and yearmax == '' and yearmin == '') or not cars.exists():
            warning = 'Axtarışa uyğun heçnə tapılmadı!'

            return render(request, "searchcar.html", {"warning": warning})
        return render(request, "searchcar.html", {'cars': cars})
    return render(request, "searchcar.html")


def favorites_add(request, id):
    car = get_object_or_404(Caradd, id=id)
    if car.favorites.filter(id=request.user.id).exists():
        car.favorites.remove(request.user)
    else:
        car.favorites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required(login_url="login")
def favorites_list(request):
    cars = Caradd.objects.filter(favorites=request.user)
    carpaginator = Paginator(cars, 6)
    page = request.GET.get('page')
    try:
        cars = carpaginator.page(page)
    except PageNotAnInteger:
        cars = carpaginator.page(1)
    except EmptyPage:
        cars = carpaginator.page(carpaginator.num_pages)
    return render(request, "favorites.html", {"cars": cars})


@login_required(login_url='login')
def carads_list(request):
    cars = Caradd.objects.filter(user=request.user)
    carpaginator = Paginator(cars, 6)
    page = request.GET.get('page')
    try:
        cars = carpaginator.page(page)
    except PageNotAnInteger:
        cars = carpaginator.page(1)
    except EmptyPage:
        cars = carpaginator.page(carpaginator.num_pages)
    return render(request, "elanlar.html", {"cars": cars})


@csrf_exempt
def carads_remove(request, id):
    car = get_object_or_404(Caradd, id=id)
    if car.user.id == request.user.id:
        car.delete()
    return redirect("elanlar")


@csrf_exempt
def carcomment_add(request, id):
    car = get_object_or_404(Caradd, id=id)
    if car.user.id == request.user.id:
        if car.iscomment:
            car.iscomment = False
            car.save()
        else:
            car.iscomment = True
            car.save()
    return HttpResponseRedirect('/car_details/' + str(car.id))


@login_required(login_url='login')
def careditviews(request, id):
    car = get_object_or_404(Caradd, id=id)

    if request.method == 'POST':
        usage = request.POST["usage"]
        brand = request.POST["brand"]
        model = request.POST["model"]
        ban = request.POST["ban"]
        color = request.POST["color"]
        fuel = request.POST["fuel"]
        transmitter = request.POST["transmitter"]
        year = request.POST["year"]
        gearbox = request.POST["gearbox"]
        mileage = request.POST["mileage"]
        distanceunit = request.POST["distanceunit"]
        price = request.POST["price"]
        priceunit = request.POST["priceunit"]
        volume = request.POST["volume"]
        power = request.POST["power"]
        market = request.POST["market"]
        condition = request.POST["condition"]
        seats = request.POST["seats"]
        credit = request.POST["credit"]
        swap = request.POST["swap"]
        images = request.FILES.getlist('images')
        addinfo = request.POST["addinfo"]

        for image in images:
            if len(images) > 15:
                return render(request, 'caredit.html', {'car': car,
                                                        'error': f'Siz maksimum 15 şəkil əlavə edə bilərsiniz. Seçdiyiniz şəkil sayı: {len(images)}'})
            else:
                carimages = CarMultipleImages.objects.create(images=image)
                carimages.carid.add(car.id)
                car.onetimeaddimage = True

        car.usage = usage
        car.brand = brand
        car.model = model
        car.ban = ban
        car.color = color
        car.fuel = fuel
        car.transmitter = transmitter
        car.year = year
        car.gearbox = gearbox
        car.mileage = mileage
        car.distanceunit = distanceunit
        car.price = price
        car.priceunit = priceunit
        car.volume = volume
        car.power = power
        car.market = market
        car.condition = condition
        car.seats = seats
        car.credit = credit
        car.swap = swap
        car.addinfo = addinfo
        car.save()
        return render(request, 'caredit.html', {'car': car, 'success': 'Uğurla redakte olundu'})

    return render(request, 'caredit.html', {'car': car})
