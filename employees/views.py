from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Employee, Department, Position
from .forms import EmployeeForm, DepartmentForm, PositionForm

def employee_list(request):
    employees = Employee.objects.filter(is_active=True)
    departments = Department.objects.all()
    search_query = request.GET.get('q', '')
    department_id = request.GET.get('department', '')
    
    if search_query:
        employees = employees.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(position__name__icontains=search_query)
        )
    
    if department_id:
        employees = employees.filter(department_id=department_id)
    
    context = {
        'employees': employees,
        'departments': departments,
        'search_query': search_query,
        'current_department': department_id
    }
    return render(request, 'employees/employee_list.html', context)

def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})

@login_required
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.user != employee.user and not request.user.is_staff:
        messages.error(request, 'У вас нет прав для редактирования этого профиля')
        return redirect('employee_detail', pk=pk)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен')
            return redirect('employee_detail', pk=pk)
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
