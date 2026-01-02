from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import UserRegisterForm, SessionBookForm, ReservationForm
from .models import LibrarySession, Resource, Reservation, User
from django.shortcuts import render
from .models import Book

def book_list_view(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def dashboard(request):
    # [cite: 40] Real-time tracking of library activities
    active_sessions = LibrarySession.objects.filter(is_active=True, user=request.user)
    
    # Staff view sees all sessions
    if request.user.role == 'STAFF':
        all_active = LibrarySession.objects.filter(is_active=True)
        return render(request, 'staff_dashboard.html', {'sessions': all_active})

    return render(request, 'dashboard.html', {'active_sessions': active_sessions})

@login_required
def book_session(request):
    # [cite: 41] Allocates time in session
    if request.method == 'POST':
        form = SessionBookForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            
            # Lock the resource [cite: 111]
            resource = session.resource
            resource.is_available = False
            resource.save()
            
            session.save()
            
            # [cite: 41] Notification logic (Simulated via Flash Message)
            messages.success(request, f"Session started! Ends at {session.end_time.strftime('%H:%M')}")
            return redirect('dashboard')
    else:
        form = SessionBookForm()
    return render(request, 'book_session.html', {'form': form})

@login_required
def end_session(request, session_id):
    # Logic to free up resource
    session = LibrarySession.objects.get(id=session_id,user=request.user)
    if request.user == session.user or request.user.role == 'STAFF':
        session.is_active = False
        session.save()
        
        # Make resource available again
        resource = session.resource
        resource.is_available = True
        resource.save()
        
        messages.info(request, "Session ended successfully.")
    return redirect('dashboard')

@login_required
def reports(request):
    # [cite: 44] Reports and analytics
    if request.user.role != 'STAFF':
        return redirect('dashboard')
        
    total_users = User.objects.count()
    total_sessions = LibrarySession.objects.count()
    active_now = LibrarySession.objects.filter(is_active=True).count()
    
    context = {
        'total_users': total_users,
        'total_sessions': total_sessions,
        'active_now': active_now
    }
    return render(request, 'reports.html', context)

@login_required
def reports(request):
    all_sessions =LibrarySession.objects.all()
    total_resources =Resource.objects.count()
    return render(request,'reports.html',{'sessions':all_sessions,'total_resources':total_resources })
