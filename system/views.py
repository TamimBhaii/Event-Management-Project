from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.utils import timezone
from .models import Event, Category, Participant
from .forms import EventForm, CategoryForm, ParticipantForm
from django.core.paginator import Paginator

def index(request):
    return redirect('system:dashboard')

# Updated event_list function
def event_list(request):
    q = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    filter_type = request.GET.get('filter', 'all')  # 'past' / 'upcoming' / 'all'

    events = Event.objects.select_related('category').prefetch_related('participants').annotate(participant_count=Count('participants'))

    # Search & category filter
    if q:
        events = events.filter(Q(name__icontains=q) | Q(location__icontains=q))
    if category_id:
        events = events.filter(category__id=category_id)
    if start_date:
        events = events.filter(date__gte=start_date)
    if end_date:
        events = events.filter(date__lte=end_date)

    # Past / Upcoming filter
    today = timezone.localdate()
    if filter_type == 'past':
        events = events.filter(date__lt=today)
    elif filter_type == 'upcoming':
        events = events.filter(date__gte=today)

    # Ordering
    events = events.order_by('-date', '-time')

    # Pagination
    paginator = Paginator(events, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    # Categories for filter dropdown
    categories = Category.objects.all()

    # Event count per date (optional summary)
    events_per_date = (
        events.values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    context = {
        'events': page_obj,
        'categories': categories,
        'q': q,
        'selected_category': category_id,
        'start_date': start_date,
        'end_date': end_date,
        'filter_type': filter_type,
        'events_per_date': events_per_date,
        'today': today,
    }

    return render(request, 'event_list.html', context)

def event_detail(request, pk):
    event = get_object_or_404(Event.objects.select_related('category').prefetch_related('participants'), pk=pk)
    participants = event.participants.all()
    return render(request,'event_detail.html',{'event': event, 'participants': participants})

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('system:event_list')
    else:
        form = EventForm()
    return render(request,'event_form.html',{'form': form, 'title': 'Create Event'})

def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('system:event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request,'event_form.html',{'form': form, 'title': 'Update Event'})

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('system:event_list')
    return render(request,'confirm_delete.html',{'object': event, 'type': 'Event'})

# Category views
def category_list(request):
    categories = Category.objects.all()
    return render(request,'category_list.html',{'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('system:category_list')
    else:
        form = CategoryForm()
    return render(request,'category_form.html',{'form': form, 'title': 'Create Category'})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('system:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request,'category_form.html',{'form': form, 'title': 'Update Category'})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('system:category_list')
    return render(request,'confirm_delete.html',{'object': category, 'type': 'Category'})

# Participant views
def participant_list(request):
    q = request.GET.get('q','')
    participants = Participant.objects.prefetch_related('events').all()
    if q:
        participants = participants.filter(Q(name__icontains=q) | Q(email__icontains=q))
    paginator = Paginator(participants.order_by('name'), 15)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request,'participant_list.html',{'participants': page_obj, 'q': q})

def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('system:participant_list')
    else:
        form = ParticipantForm()
    return render(request,'participant_form.html',{'form': form, 'title': 'Create Participant'})

def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, request.FILES, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('system:participant_list')
    else:
        form = ParticipantForm(instance=participant)
    return render(request,'participant_form.html',{'form': form, 'title': 'Update Participant'})

def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant.delete()
        return redirect('system:participant_list')
    return render(request,'confirm_delete.html',{'object': participant, 'type': 'Participant'})

# Dashboard
def dashboard(request):
    today = timezone.localdate()

    # Counts
    total_participants = Participant.objects.count()
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gt=today).count()
    past_events = Event.objects.filter(date__lt=today).count()
    todays_events = Event.objects.filter(date=today).select_related('category').prefetch_related('participants')

    # Filter for table
    f = request.GET.get('filter','all')
    if f == 'upcoming':
        events_filtered = Event.objects.filter(date__gte=today)
    elif f == 'past':
        events_filtered = Event.objects.filter(date__lt=today)
    else:
        events_filtered = Event.objects.all()

    # Annotate participant count and select related
    events_filtered = events_filtered.select_related('category') \
                                     .prefetch_related('participants') \
                                     .annotate(participant_count=Count('participants')) \
                                     .order_by('-date', '-time')[:30]

    context = {
        'total_participants': total_participants,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'todays_events': todays_events,
        'events_filtered': events_filtered,
        'filter': f,
    }

    return render(request, 'dashboard.html', context)

