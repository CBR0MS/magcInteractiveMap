from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Point, Map, Tag, Info, Tour, TourLocation
from django.forms.models import model_to_dict
from django.core import serializers

def index(request):
    try:
        mp = Map.objects.get() # get first map object
        tagObjects = Tag.objects.all().values() # get all tag objects
        queryTagsSelected = []
        queryTags = []
        showDemo = False
        showGuide = False
        locations = None
        tourText = None
        

        # determine if we should show the demo
        demo = request.GET.get('demo', '')

        if demo.lower() == 'true':
            showDemo = True

        # get last closed page 
        last = request.GET.get('last', '')

        # determine if we should show the question tour
        guide = request.GET.get('question-guide', '')

        if guide.lower() == 'true':
            showGuide = True
            tour = Tour.objects.filter(name="Question Guide")[0]
            tourLocations = TourLocation.objects.filter(tour=tour)
            # should probably do this some other way so we don't have
            # to pass so much data when all we need is the slugs
            locations = serializers.serialize('json', tour.get_locations())
            tourText = serializers.serialize('json', tourLocations)


        for tag in tagObjects:
            # add tag to list of tags to be passed to template
            queryTags.append(tag)
            slug = tag['slug']
            query = request.GET.get(slug)
            # if tag name is set to false in url
            if query: 
                # add tag to disabled tag list 
                queryTagsSelected.append(tag['name'])

        pointObjects = Point.objects.all()
        pts = []
        colors = {}
        # if there is an id in the url, pass that value to open it by default
        openId = ''

        for point in pointObjects:
            numberOfTags = point.tags.count()
            numberOfDisabledTags = 0
            badTags = []
            colors[point.slug] = []

            query = request.GET.get(point.slug)
            if query:
                openId = point.slug

            for tag in queryTagsSelected:
                # if the point has a disabled tag, 
                if point.tags.filter(name=tag).exists():
                    numberOfDisabledTags += 1
                    badTags.append(point.tags.filter(name=tag).values()[0]['name'])
            # if the point has at least one non-disabled tag, 
            if numberOfTags > numberOfDisabledTags:
                # add the point to the list to send to template
                pts.append(Point.objects.filter(slug=point.slug).values()[0])

                for tag in point.tags.all():
                    # if the tag is not disabled
                    if tag.name not in badTags:
                        colors[point.slug].append(tag.color) 
        showIFrames = True 
        if request.user_agent.is_mobile or request.user_agent.is_tablet:
            showIFrames = False

    except Map.DoesNotExist:
        # if there is no map, display a service notice
        # TODO: get rid of this 404 and replace with an actual page
        raise Http404("Website under maintenance, check back later")
    return render(request, 'map.html', {'map': mp, 
                                        'selections': queryTagsSelected,
                                        'tags': queryTags, 
                                        'points': pts, 
                                        'pointColors': colors, 
                                        'open': openId,
                                        'demo': showDemo,
                                        'guide': showGuide,
                                        'locations': locations,
                                        'locationsText': tourText,
                                        'iOS': request.user_agent.browser.family == 'Mobile Safari',
                                        'last': last})

def details(request, id):
    pt = get_object_or_404(Point, slug=id)
    images = pt.number_of_images()
    caption = []
    showGuide = False


    # determine if we should show the continue button for guide
    guide = request.GET.get('guide', '')

    if guide.lower() == 'true':
        showGuide = True

    # captions 
    caption.append(pt.additional_caption1)
    caption.append(pt.additional_caption2)
    caption.append(pt.additional_caption3)
    caption.append(pt.additional_caption4)
    caption.append(pt.additional_caption5)

    backArrow = False
    ogMap = False
    # if there is a sender param in url, display back arrow on details page
    sender = request.GET.get('sender')
    # if sender in url
    if sender: 
        backArrow = True
     # if there is a redirected param in url, make "Back to map" go to clean map url (no params)
    redir = request.GET.get('redirected')
    # if sender in url
    if redir: 
        ogMap = True
           
    return render(request, 'detail.html', {'point': pt,
                                           'images': images,
                                           'imgNum': len(images),
                                           'captions': caption, 
                                           'back': backArrow,
                                           'redirected': ogMap,
                                           'iterator': zip(images, caption),
                                           'guide': showGuide })

def about_credits(request):

    info = get_object_or_404(Info, pk=1)

    backArrow = False
    ogMap = False
    # if there is a sender param in url, display back arrow on details page
    sender = request.GET.get('sender')
    # if sender in url
    if sender: 
        backArrow = True
    # if there is a redirected param in url, make "Back to map" go to clean map url (no params)
    redir = request.GET.get('redirected')
    # if sender in url
    if redir: 
        ogMap = True

    return render(request, 'about.html', {'back': backArrow,
                                          'redirected': ogMap,
                                          'info': info, })
