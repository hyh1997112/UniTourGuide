from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, UploadImageFormID, UploadImageFormUni, ReviewForm, UploadImageFormPhoto
from .models import Guide, School, Manager, Tour, GuideApplication
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.dateformat import DateFormat
from django.utils.timezone import datetime
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

# The home page


def index(request):
    schools = School.objects.filter(recommand=True)
    return render(request, 'unitourguide/index.html', {"schools": schools})

# The sign in page


def signin(request):
    if request.user.is_authenticated:
        errormessage = "You have already logged in, please log out first to change the user"
        return render(request, 'unitourguide/signin.html', {"errormessage":  errormessage})
    errormessage = ""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            errormessage = "User do not exist or password wrong"
            return render(request, 'unitourguide/signin.html', {"errormessage":  errormessage})
    return render(request, 'unitourguide/signin.html')

# The sigh up page


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data['username']
            first = form.cleaned_data['firstname']
            last = form.cleaned_data['lastname']
            passcode = form.cleaned_data['password']
            user = User.objects.create_user(
                username=account, password=passcode)
            user.first_name = first
            user.last_name = last
            user.save()
            # user.groups.add(Group.objects.get(name='customer'))
            login(request, user)
            return redirect("/")
    else:
        form = SignupForm()
    return render(request, 'unitourguide/signup.html', {'form': form})


def find_uni(request):
    schools = School.objects.filter(display=True)
    errorMessage = ""
    if request.method == "GET":
        if ("search_by_name" in request.GET) and (len(request.GET["search_name"]) > 0):
            search_name = request.GET["search_name"]
            schools = School.objects.filter(name=search_name)
            if len(schools) == 0:
                errorMessage = "Sorry. We don't have any guides at " + search_name
                return render(request, 'unitourguide/find_uni.html', {"schools": schools, "errorMessage": errorMessage})
        if "filter_by_place" in request.GET:
            if "city_select" in request.GET:
                city = request.GET["city_select"]
                if city is not None:
                    schools = School.objects.filter(city=city)
                    return render(request, 'unitourguide/find_uni.html', {"schools": schools, })
            if "state_select" in request.GET:
                state = request.GET["state_select"]
                if state is not None:
                    schools = School.objects.filter(state=state)
                    return render(request, 'unitourguide/find_uni.html', {"schools": schools, })
    return render(request, 'unitourguide/find_uni.html', {"schools": schools, })


def find_guide(request, school_id):
    school = School.objects.get(id=school_id)
    guides = Guide.objects.filter(school=school).exclude(price=None)
    tours = Tour.objects.filter(school=school)
    message = "Here are all guides at %s." % school.name
    order = False
    date = None
    if request.method == 'GET':
        if "date" in request.GET and len(request.GET["date"]) > 0:
            date = request.GET["date"]
            tours2 = Tour.objects.filter(condition="accepted")
            if tours2 is not None:
                tours2 = tours2.filter(date=date)
                guides_to_exclude = [tour2.guide.id for tour2 in tours2]
                guides = guides.exclude(id__in=guides_to_exclude)
                if len(guides) > 0:
                    message = "Here are the available guides for date %s at %s." % (
                        date, school.name)
                else:
                    message = "Sorry. No available guides for date %s at %s." % (
                        date, school.name)
    if request.method == "POST" and "choose_guide" in request.POST and "guide_id" in request.POST:
        if not request.user.is_authenticated:
            return redirect(signin)
        guide_id = request.POST["guide_id"]
        guide = Guide.objects.get(id=guide_id)
        customer = request.user
        condition = "pending"
        if "hidden_date" in request.POST:
            date = request.POST["hidden_date"]
        if date == "None":
            date = datetime.today()
        tour = Tour(date=date, school=school, guide=guide,
                    customer=customer, condition=condition)
        tour.save()
        order = True
        message = "Thank you! Your order is on the way!"
    return render(request, 'unitourguide/find_guide.html', {"guides": guides, "school": school, "tours": tours, "message": message, "order": order, "hidden_date": date})


@login_required
def my_tour(request):
    current_user = request.user
    current_status = ['pending', 'accepted']
    past_status = ['completed', 'cancelled', 'declined']
    current_tours = Tour.objects.filter(
        customer=current_user).filter(condition__in=current_status)
    past_tours = Tour.objects.filter(
        customer=current_user).filter(condition__in=past_status)
    if request.method == 'POST' and "cancel" in request.POST:
        cancel_tour = Tour.objects.get(id=int(request.POST["cancel"]))
        cancel_tour.condition = "cancelled"
        cancel_tour.save()

    return render(request, 'unitourguide/my_tour.html', {"current_tours": current_tours, "past_tours": past_tours})


@login_required
def write_review(request, tour_id):
    tour = Tour.objects.get(id=tour_id)
    form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['feedback']
            tour.feedback = feedback
            rating = form.cleaned_data['rating']
            tour.rating = rating
            tour.save()
            # update the guide's mean rating
            guide = tour.guide
            if not guide.rating:
                guide.rating = rating
            else:
                # get all tours of the guide
                tours = Tour.objects.filter(guide=guide)
                all_ratings = []
                for tour in tours:
                    if tour.rating:
                        all_ratings.append(tour.rating)
                guide.rating = round(sum(all_ratings)/len(all_ratings), 1)
            guide.save()
            return redirect("/")
    return render(request, 'unitourguide/write_review.html', {"form": form})


@login_required
def to_be_guide(request):
    schools = School.objects.all()
    message = ""
    display = True

    if Guide.objects.filter(user=request.user).exists():
        message = "You are already a guide. Don't apply again."
        display = False
        return render(request, 'unitourguide/to_be_guide.html', {"schools": schools, "message": message, "display": display})
    if GuideApplication.objects.filter(user=request.user).exists():
        message = "You already have a pending application. Don't apply again."
        display = False
        return render(request, 'unitourguide/to_be_guide.html', {"schools": schools, "message": message, "display": display})

    if request.method == 'POST':
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        studentID = request.POST["studentid"]
        # state = request.POST["state_select"]
        # city = request.POST["city_select"]
        if not (first_name and last_name and email and studentID):
            message = "You must fill in all of the fields: First Name, Last Name, Email, and Student ID."
            return render(request, 'unitourguide/to_be_guide.html', {"schools": schools, "message": message, "display": display})

        if "school_select" not in request.POST:
            state_new = request.POST["state_name"]
            city_new = request.POST["city_input"]
            school_new_name = request.POST["other_uni"]
            school_description = request.POST["description"]

            if state_new and city_new and school_new_name and school_description:
                new_uni = School(name=school_new_name, state=state_new,
                                 city=city_new, description=school_description)
                uniform = UploadImageFormUni(request.POST, request.FILES)
                if uniform.is_valid():
                    new_uni.picture = uniform.cleaned_data["image_uni"]
                    new_uni.save()
                    school_id = new_uni.id
                else:
                    message = "You must upload a uni image."
                    return render(request, 'unitourguide/to_be_guide.html', {"schools": schools, "message": message, "display": display})
            else:
                message = "You must input state, city, and uni name."
                return render(request, 'unitourguide/to_be_guide.html', {"schools": schools, "message": message, "display": display})
        else:
            school_id = request.POST["school_select"]

        school = School.objects.get(id=school_id)
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        application = GuideApplication(
            user=request.user, email=email, school=school, studentID=studentID)
        idform = UploadImageFormID(request.POST, request.FILES)
        if idform.is_valid():
            application.document = idform.cleaned_data["image_ID"]
            application.condition = "pending"
            application.save()
            message = "Application submitted! Thank you."
            display = False
            return render(request, 'unitourguide/to_be_guide.html', {"schools": schools, "message": message, "display": display})
        else:
            message = "You must upload valid document."
            return render(request, 'unitourguide/to_be_guide.html', {"schools": schools, "message": message, "display": display})

    return render(request, 'unitourguide/to_be_guide.html', {"schools": schools, "message": message, "display": display})


def manage_guide(request):
    applications = GuideApplication.objects.filter(condition="pending")
    guides = Guide.objects.all()
    message=""
    if request.method == "POST":
        if "deny" in request.POST:
            application = GuideApplication.objects.get(id=request.POST["deny"])
            application.delete()

        if "approve" in request.POST:
            application = GuideApplication.objects.get(id=request.POST["approve"])
            uni = application.school
            # check whether it is a new school
            if not uni.display:
                if request.POST["latitude"] and request.POST["longitude"]:
                    uni.latitude = request.POST["latitude"]
                    uni.longitude = request.POST["longitude"]
                    uni.save()
                else:
                    message = "Please enter the latitude and longitude."
            if uni.latitude and uni.longitude:
                application.condition = "approved"
                application.user.is_staff = True
                application.user.save()
                # create guide object
                newguide = Guide(user=application.user,
                                studentID=application.studentID)
                newguide.save()

                # add the new guide to the uni
                uni.guides.add(newguide)
                if uni.display == False:
                    uni.display = True
                    uni.save()
                application.save()

        if "delete_guide" in request.POST:
            guide = Guide.objects.get(id=request.POST["delete_guide"])
            # change the status of his or her application
            application = guide.user.application
            application.delete()
            # delete the guide object
            guide.delete()

    return render(request, 'unitourguide/manage_guide.html', {"applications": applications, "guides": guides, "message": message})


def my_profile(request):
    current_user = request.user
    the_guide = Guide.objects.get(user=current_user)
    current_status = ['pending', 'accepted']
    past_status = ['completed', 'cancelled', 'declined']
    current_tours = Tour.objects.filter(
        guide=the_guide).filter(condition__in=current_status)
    past_tours = Tour.objects.filter(
        guide=the_guide).filter(condition__in=past_status)
    if request.method == 'POST' and "accept" in request.POST:
        cancel_tour = Tour.objects.get(id=int(request.POST["accept"]))
        cancel_tour.condition = "accepted"
        cancel_tour.save()
    if request.method == 'POST' and "deny" in request.POST:
        cancel_tour = Tour.objects.get(id=int(request.POST["deny"]))
        cancel_tour.condition = "declined"
        cancel_tour.save()
    return render(request, 'unitourguide/my_profile.html', {"current_tours": current_tours, "past_tours": past_tours})


def my_info(request):
    current_user = request.user
    the_guide = Guide.objects.get(user=current_user)
    message = ""
    if request.method == 'POST':
        if "updateprice" in request.POST:
            price = request.POST["new_price"]
            if price != "":
                the_guide.price = price
                the_guide.save()
        if "updatedes" in request.POST:
            des = request.POST["new_description"]
            if des != "":
                the_guide.description = des
                the_guide.save()
        if "update_photo" in request.POST:
            photoform = UploadImageFormPhoto(request.POST, request.FILES)
            if photoform.is_valid():
                new_pic = photoform.cleaned_data["image_photo"]
                the_guide.picture = new_pic
                the_guide.save()
                message = "Your photo is uploaded successfully"
                return render(request, 'unitourguide/my_info.html', {"guide": the_guide, "message": message})
            else:
                message = "You must upload valid document."
                return render(request, 'unitourguide/my_info.html', {"guide": the_guide, "message": message})
    return render(request, 'unitourguide/my_info.html', {"guide": the_guide, "message": message})


def logoutpage(request):
    logout(request)
    return render(request, 'unitourguide/logout.html')
