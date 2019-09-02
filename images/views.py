from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ImageCreateForm
from django.contrib import messages
from .models import Image
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action
from django.conf import settings
import redis

#connect to the redis database.
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

@login_required
def image_create(request):
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            create_action(request.user, 'bookmarked image', new_image)
            messages.success(request, "Image added successfully")

            return redirect(new_image.get_absolute_url())  # goto thw image detail page

    else:
        form = ImageCreateForm(data=request.GET)

    return render(request,
            'images/image/create.html',
            {'form':form,
            'section':'images'})

@login_required
def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # notation: object-type:id:field
    total_views = r.incr('image:{}:views'.format(image.id))
    # increment image ranking by one.
    r.zincrby('image_ranking', image.id, 1)
    return render(request,
                'images/image/detail.html',
                {'image':image,
                'section':'images',
                'total_views':total_views})

@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    image_action = request.POST.get('action')
    if image_id and image_action:
        try:
            image = Image.objects.get(id=image_id)  #retrieve image
            if image_action == 'like':
                image.users_like.add(request.user)  # remove the user
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)  # add the user
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})

@login_required
def image_list(request):
    objects_list = Image.objects.all()  
    paginator = Paginator(objects_list, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')  # return an empty page
        images = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        images = paginator.page(1)

    if request.is_ajax():
        return render(request,
                'images/image/list_ajax.html',
                {'section':'images',
                'images':images})

    return render(request,
                'images/image/list.html',   
                {'section':'images',
                'images':images})

@login_required
def image_ranking(request):
    # obtain sorted set of image ranking
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    # obtain ids of the images
    image_ranking_ids = [int(id) for id in image_ranking]
    # obtain images
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    # sort images by their index of appearance in the image ranking
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id)) 

    return render(request,
            'images/image/ranking.html',
            {'most_viewed':most_viewed,
            'section':'images'})