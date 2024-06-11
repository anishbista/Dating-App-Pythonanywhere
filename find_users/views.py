from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from user_profile.models import BlockedUser, UserProfile
from find_users.filters import UserFilter
from .utilities import calculate_distance
from django.db.models import Exists


def FilterUser(request):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
    blocked_users = [x.user for x in request.user.profile.blocked_users.users.all()]

    if is_ajax:
        if request.method == "POST":
            f = UserFilter(
                request.POST,
                queryset=UserProfile.objects.exclude(user=request.user)
                .exclude(user__in=blocked_users)
                .order_by("-created_on"),
            )
            return render(request, "filter_users_list.html", {"filter": f})
        else:
            return JsonResponse({"status": "Invalid Request"}, status=400)
    else:
        f = UserFilter(
            request.GET,
            queryset=UserProfile.objects.exclude(user=request.user)
            .exclude(user__in=blocked_users)
            .order_by("-created_on"),
        )
        return render(request, "filter_users.html", {"filter": f, "title": "Filter"})


def get_users_by_raduis(request):
    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    if is_ajax:
        if request.method == "GET":
            range = request.GET.get("range")
            print(request.user.profile.description.looking_for)
            querylist = [
                x
                for x in UserProfile.objects.exclude(user=request.user)
                if calculate_distance(request.user, x.lat, x.long) <= int(range)
                and x.gender == request.user.profile.description.looking_for
            ]
            return render(
                request, "swipe_users_ajax.html", {"userprofile_list": querylist}
            )
        else:
            return JsonResponse({"status": "Invalid Request"}, status=400)
    else:
        return HttpResponseBadRequest("Invalid Request")
