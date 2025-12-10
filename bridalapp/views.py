from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Board, BoardItem, Profile, CATEGORY_CHOICES, SavedImage
from .forms import BoardForm, BoardItemForm, ProfileUpdateForm, UserUpdateForm
import os
from django.core.files import File
from django.conf import settings
from django.http import HttpResponse
# Create your views here.
def auth_landing(request):
    return render(request, 'auth_landing.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        next_url = request.POST.get('next')  # Read NEXT from form

        if user:
            login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('auth_landing')  # Correct redirect

    else:
        # GET request
        next_url = request.GET.get('next', '')
        return render(request, "auth_landing.html", {'next': next_url})

def register_user(request):
    if request.method == "POST":
        full_name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            print("Passwords do not match")
            return redirect('auth_landing')  # or show a message

        if User.objects.filter(username=username).exists():
            print("Username already exists")
            return redirect('auth_landing')  # or show a message

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
        )
        print("User created:", user.username)
        return redirect('login')  

    return redirect('auth_landing')

@login_required(login_url='login')
def dashboard(request):
    # Get the category from the query string
    category = request.GET.get('category')

    # Start with all boards owned by the user
    boards = Board.objects.filter(owner=request.user).prefetch_related('items')

    # Filter only if category is valid
    valid_categories = [choice[0] for choice in CATEGORY_CHOICES]
    if category in valid_categories:
        boards = boards.filter(category=category)
    else:
        category = None  # Reset if invalid

    context = {
        "boards": boards,
        "selected_category": category
    }
    return render(request, 'dashboard.html', context)

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('auth_landing')

@login_required
def create_board(request): 
    if request.method == 'POST': 
        name = request.POST.get('name') 
        category = request.POST.get('category') 
        Board.objects.create( 
            owner=request.user, 
            name=name, 
            category=category 
        ) 
        return redirect('dashboard') # redirect to boards page after creation 
    return redirect('boards')

@login_required
def board_detail(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    saved_images = board.saved_images.all()
    return render(request, 'board_detail.html', {'board': board, 'saved_images': saved_images})

def rename_board(request, board_id):
    if request.method == "POST":
        new_name = request.POST.get("name")

        board = get_object_or_404(Board, id=board_id, owner=request.user)

        board.name = new_name
        board.save()

        return redirect("dashboard")

    return redirect("dashboard")

def delete_board(request, board_id):
    board = get_object_or_404(Board, id=board_id, owner=request.user)

    if request.method == "POST":
        board.delete()
        return redirect("dashboard")

    return redirect("dashboard")

def view_board(request, board_id):
    board = Board.objects.get(id=board_id, user=request.user)
    items = board.items.all()
    return render(request, 'view_board.html', {'board': board, 'items': items})

@login_required
def profile(request):
    # Ensure profile exists
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('dashboard')  # Redirect after saving
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile
    }
    return render(request, 'profile.html', context)

def home(request):
    boards = Board.objects.filter(owner=request.user) if request.user.is_authenticated else Board.objects.none()
    print(f"DEBUG home: User authenticated: {request.user.is_authenticated}")
    print(f"DEBUG home: User: {request.user}")
    print(f"DEBUG home: Boards count: {boards.count()}")
    return render(request, "home.html", {"boards": boards})

@login_required
def save_image(request):
    if request.method == 'POST':
        print("✅ save_image view triggered!")  # check if view runs
        print("POST data:", request.POST)

        image_path = request.POST.get('image')  # e.g., /media/board_items/wedding1.jpg
        board_id = request.POST.get('board_id')

        print("🔍 POST data received:")
        print("   Image:", image_path)
        print("   Board ID:", board_id)
        print("   User:", request.user.username)

        if not image_path or not board_id:
            print("❌ Missing data!")
            messages.error(request, "Missing image or board selection")
            return redirect('home')

        try:
            board = Board.objects.get(id=board_id, owner=request.user)
            print("✅ Board found:", board.name)

            # Get relative path to MEDIA_ROOT
            # Strip /media/ from the front if present
            if image_path.startswith('/media/'):
                relative_path = image_path.replace('/media/', '', 1)
            else:
                relative_path = image_path

            # Check if image already saved
            existing = SavedImage.objects.filter(
                board=board,
                image=relative_path
            ).first()

            if existing:
                print("⚠️ Image already saved to this board")
                messages.info(request, "Image already saved to this board")
            else:
                # Open file from media and save properly
                full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
                with open(full_path, 'rb') as f:
                    saved_image = SavedImage(board=board)
                    saved_image.image.save(os.path.basename(relative_path), File(f), save=True)
                print("✅ Image saved! ID:", saved_image.id)
                messages.success(request, "Image saved successfully!")

            return redirect('dashboard')

        except Board.DoesNotExist:
            print("❌ Board not found")
            messages.error(request, "Board not found")
            return redirect('home')

        except Exception as e:
            print("❌ Error saving image:", e)
            messages.error(request, f"Error saving image: {e}")
            return redirect('home')

    print("❌ Not a POST request")
    return redirect('home')

def vendors(request):
    return render(request, 'vendors.html')

def inspiration_view(request):
    return render(request, 'inspiration.html')

def color_palettes(request):
    return render(request, 'color_palettes.html')

def blog_tips(request):
    return render(request, 'blog_tips.html')

def bride_view(request):
    return render(request, 'bride.html')

def groom_view(request):
    return render(request, 'groom.html')

def honor(request):
    return render(request, 'honor.html')

def maid(request):
    return render(request, 'maid.html')

def men(request):
    return render(request, 'men.html')

def girls(request):
    return render(request, 'girls.html')

def boys(request):
    return render(request, 'boys.html')
def create_board(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')

        board = Board.objects.create(
            owner=request.user,
            name=name,
            category=category
        )

        # Set default based on category
        default_images = {
            'Bridal': 'gown1.jpg',
            'Groom': 'groom1.jpg',
            'Decor': 'blushdecor.jpg',
            'Accessories': 'ring4.jpg',
        }


        return redirect('dashboard')