from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Employee, Department, Position
from .forms import EmployeeForm, DepartmentForm, PositionForm
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.conf import settings

User = get_user_model()

def employee_list(request):

    search_query = request.GET.get('q', '').strip()
    department_id = request.GET.get('department', '')
    position_id = request.GET.get('position', '')
    page = request.GET.get('page', 1)


    employees = User.objects.filter(is_active=True).select_related(
        'employee_profile',
        'employee_profile__department',
        'employee_profile__position'
    )

    if search_query:
        employees = employees.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(employee_profile__position__name__icontains=search_query) |
            Q(email__icontains=search_query)
        ).distinct()

    if department_id:
        employees = employees.filter(employee_profile__department_id=department_id)

    if position_id:
        employees = employees.filter(employee_profile__position_id=position_id)


    departments = cache.get('departments_list')
    if departments is None:
        departments = Department.objects.all()
        cache.set('departments_list', departments, 60 * 60)  # кэшируем на 1 час

    positions = cache.get('positions_list')
    if positions is None:
        positions = Position.objects.all()
        cache.set('positions_list', positions, 60 * 60) 


    employees = employees.order_by('last_name', 'first_name')

    paginator = Paginator(employees, 12)  
    employees_page = paginator.get_page(page)

    context = {
        'employees': employees_page,
        'departments': departments,
        'positions': positions,
        'search_query': search_query,
        'current_department': department_id,
        'current_position': position_id,
    }

    return render(request, 'employees/employee_list.html', context)

def employee_detail(request, pk):
    user = get_object_or_404(User, pk=pk, is_active=True)
    try:
        employee = user.employee_profile
    except Employee.DoesNotExist:
        employee = None
    
    context = {
        'employee': employee,
        'user': user,
    }
    
    return render(request, 'employees/employee_detail.html', context)

@login_required
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.user != employee.user and not request.user.is_staff:
        messages.error(request, 'У вас нет прав для редактирования этого профиля')
        return redirect('employees:employee_detail', pk=employee.user.pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен')
            return redirect('employees:employee_detail', pk=employee.user.pk)
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form, 'employee': employee})

@login_required
def department_list(request):
    if not request.user.is_staff:
        messages.error(request, 'У вас нет прав для просмотра этой страницы')
        return redirect('home')
    
    departments = Department.objects.all()
    return render(request, 'employees/department_list.html', {'departments': departments})

@login_required
def department_create(request):
    if not request.user.is_staff:
        messages.error(request, 'У вас нет прав для создания отделов')
        return redirect('home')
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Отдел успешно создан')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    
    return render(request, 'employees/department_form.html', {'form': form})

@login_required
def position_list(request):
    if not request.user.is_staff:
        messages.error(request, 'У вас нет прав для просмотра этой страницы')
        return redirect('home')
    
    positions = Position.objects.all()
    return render(request, 'employees/position_list.html', {'positions': positions})

@login_required
def position_create(request):
    if not request.user.is_staff:
        messages.error(request, 'У вас нет прав для создания должностей')
        return redirect('home')
    
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Должность успешно создана')
            return redirect('position_list')
    else:
        form = PositionForm()
    
    return render(request, 'employees/position_form.html', {'form': form})

@login_required
def employee_create(request, pk):
    user = get_object_or_404(User, pk=pk, is_active=True)
    
   
    if hasattr(user, 'employee_profile'):
        messages.warning(request, 'Профиль уже существует')
        return redirect('employees:employee_detail', pk=pk)
    

    if request.user != user and not request.user.is_staff:
        messages.error(request, 'У вас нет прав для создания этого профиля')
        return redirect('employees:employee_list')
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.user = user
            employee.save()
            messages.success(request, 'Профиль успешно создан')
            return redirect('employees:employee_detail', pk=pk)
    else:
        form = EmployeeForm()
    
    return render(request, 'employees/employee_form.html', {
        'form': form,
        'user': user,
        'is_create': True
    })
