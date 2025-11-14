from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count, Q, Avg, Max, Min
from django.http import JsonResponse, HttpResponseForbidden
from .models import Service, Branch, Appointment, News, Category, ServiceStatistic
from django.utils import timezone
from datetime import timedelta
from .forms import ServiceForm


def home(request):
    # Популярные услуги (по количеству записей)
    popular_services = Service.objects.annotate(
        appointment_count=Count('appointment')
    ).order_by('-appointment_count')[:5]

    nearest_branches = Branch.objects.all()[:8]

    branch_stats = {
        'total_branches': Branch.objects.count(),
        'total_services': Service.objects.count(),
        'total_appointments': Appointment.objects.count()
    }

    latest_news = News.objects.all().order_by('-created_at')[:3]

    # Категории услуг
    categories = Category.objects.annotate(
        service_count=Count('service')
    ).filter(service_count__gt=0)

    context = {
        'popular_services': popular_services,
        'nearest_branches': nearest_branches,
        'branch_stats': branch_stats,
        'latest_news': latest_news,
        'categories': categories,
    }
    return render(request, 'home.html', context)


def search_services(request):
    query = request.GET.get('q', '')
    if query:
        results = Service.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).exclude(
            state_duty__gt=5000
        ).distinct().order_by('name')
    else:
        results = Service.objects.none()


    popular_services = Service.objects.annotate(
        appointment_count=Count('appointment')
    ).order_by('-appointment_count')[:3] #добавление популярных если результатов нет

    return render(request, 'search_results.html', {
        'results': results,
        'query': query,
        'popular_services': popular_services
    })


def service_detail(request, service_id):
    service = get_object_or_404(Service, service_id=service_id)

    recent_appointments = Appointment.objects.filter(
        service=service,
        desired_date__gte=timezone.now().date() - timedelta(days=30)
    )

    busy_days = recent_appointments.extra({
        'day': "EXTRACT(dow FROM desired_date)"
    }).values('day').annotate(count=Count('appointment_id'))

    stat, created = ServiceStatistic.objects.get_or_create(service=service)
    stat.view_count += 1
    stat.save()

    return render(request, 'service_detail.html', {
        'service': service,
        'busy_days': busy_days,
        'stat': stat
    })


def service_list(request):
    """Страница со списком всех услуг для управления"""
    services = Service.objects.all().select_related('category').order_by('service_id')
    return render(request, 'service_list.html', {'services': services})


def service_add(request):
    """Добавление новой услуги"""
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save()
            # Создаем статистику для новой услуги
            ServiceStatistic.objects.create(service=service)
            messages.success(request, f'Услуга "{service.name}" успешно добавлена!')
            return redirect('service_detail', service_id=service.service_id) #вот тут я поменял ссылку, была сыылка на сдругую страницу
    else:
        form = ServiceForm()

    return render(request, 'service_form.html', {
        'form': form,
        'title': 'Добавление новой услуги',
        'submit_text': 'Добавить услугу'
    })


def service_edit(request, service_id):
    service = get_object_or_404(Service, service_id=service_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            updated_service = form.save()
            messages.success(request, f'Услуга "{updated_service.name}" успешно обновлена!')
            return redirect('service_detail', service_id=updated_service.service_id) #здесь происходит перенаправление на service_detail
    else:
        form = ServiceForm(instance=service)

    return render(request, 'service_form.html', {
        'form': form,
        'title': f'Редактирование услуги: {service.name}',
        'submit_text': 'Сохранить изменения'
    })


def service_delete(request, service_id):
    """Удаление услуги"""
    if request.method == 'POST':
        service = get_object_or_404(Service, service_id=service_id)
        service_name = service.name

        # Удаляем связанную статистику
        ServiceStatistic.objects.filter(service=service).delete()
        # Удаляем саму услугу
        service.delete()

        messages.success(request, f'Услуга "{service_name}" успешно удалена!')
        return redirect('service_list')
    else:
        return HttpResponseForbidden("Метод не разрешен")
