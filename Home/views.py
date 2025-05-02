from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, OptionForm, ProfileEditForm
from .models import UserProfile, FeedbackRes, Subject_detail, Batch, BatchSection,Faculty
from django.db.models import Count, Avg, Q, F


def Home(request):
    return render(request, 'home/index.html')


# def Register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             # Save the user and create UserProfile at the same time
#             user = form.save(commit=False)
#             user.save()

#             # Optionally, create the UserProfile explicitly if not done in the form
#             UserProfile.objects.create(
#                 user=user,
#                 name=form.cleaned_data['name'],
#                 email=user.email,
#                 designation=form.cleaned_data['designation']
#             )

#             messages.success(request, "Account has been created successfully.")
#             return redirect('Login')
#         else:
#             print(form.errors)
#     else:
#         form = RegistrationForm()
    
#     return render(request, 'home/register.html', {'form': form})
def Register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            designation = form.cleaned_data['designation']
            faculty_code = form.cleaned_data.get('faculty_code', '').strip()

            if designation == 'faculty':
                # Check if the faculty code is valid
                if not Faculty.objects.filter(faculty_code=faculty_code).exists():
                    messages.error(request, "Invalid faculty code. Please contact admin.")
                    return render(request, 'home/register.html', {'form': form})

            # Save user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Ensure password is hashed

            # Set the role based on the designation
            user.role = 'FACULTY' if designation == 'faculty' else 'STUDENT'

            user.save()

            # Create a UserProfile and set designation
            UserProfile.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                email=user.email,
                designation=designation  # Ensure designation is set here
            )

            messages.success(request, "Account has been created successfully.")
            return redirect('Login')
        else:
            # In case of invalid form, print errors and re-render the form
            print(form.errors)
            return render(request, 'home/register.html', {'form': form})

    else:
        form = RegistrationForm()
        return render(request, 'home/register.html', {'form': form})




def Loginview(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Check if the profile is complete (example check, modify as per your fields)
            try:
                user_profile = UserProfile.objects.get(user=user)
                if not user_profile.name or not user_profile.email:
                    # Redirect to profile update page if required fields are missing
                    return redirect('Profile')
            except UserProfile.DoesNotExist:
                # If profile doesn't exist, create a new one and redirect to profile update page
                UserProfile.objects.create(user=user)
                return redirect('Profile')

            return redirect('Home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'home/login.html')


# def Logoutview(request):
#     logout(request)
#     return redirect('Home')
def Logoutview(request):
    logout(request)              # Logs the user out
    # request.session.flush()      # Clears session data
    return redirect('Home')


@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('Profile')  # Redirect to the same page after saving
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'home/profile.html', {
        'form': form,
        'profile': profile
    })


@login_required
# def feedback_view(request):
#     if request.session.get('has_submitted', False):
#         return render(request, 'home/Thankyou.html')

#     obj2 = Batch.objects.all()
#     obj1 = Batch.objects.values('Batchyear').distinct()
#     semesters = range(1, 9)

#     selected_batch_year = request.POST.get('year')
#     selected_department = request.POST.get('department')
#     selected_semester = request.POST.get('semester')

#     subjects = None
#     labs = None

#     if request.method == 'POST' and selected_batch_year and selected_department and selected_semester:
#         subjects = Subject_detail.objects.filter(
#         Batch__Batchyear=selected_batch_year,
#         Batch__department=selected_department,
#         orensemester=selected_semester,
#         sub_type='SUBJECT'
#     )
#         labs = Subject_detail.objects.filter(
#         Batch__Batchyear=selected_batch_year,
#         Batch__department=selected_department,
#         orensemester=selected_semester,
#         sub_type='LABORATORY'
#     )

#     responses_saved = False

#     for key in request.POST:
#         if key.startswith('response_'):
#             qno = key.split('_')[1]
#             response = request.POST[key]
#             subject_id = request.POST.get(f'subject_{qno}')

#             try:
#                 subject = Subject_detail.objects.get(id=subject_id)
#                 FeedbackRes.objects.create(
#                     department=selected_department,
#                     Response=int(response),
#                     Qno=int(qno),
#                     subject_detail=subject,
#                     batch_year=selected_batch_year
#                 )
#                 responses_saved = True
#             except Subject_detail.DoesNotExist:
#                 print(f"Subject with ID {subject_id} not found")
#             except Exception as e:
#                 print(f"Error saving feedback: {e}")

#     if responses_saved:
#         request.session['has_submitted'] = True
#         return render(request, 'home/Thankyou.html')

#     form = OptionForm()
#     return render(request, 'home/fformnew.html', {
#         'Batches': obj1,
#         'depart': obj2,
#         'semesters': semesters,
#         'subjects': subjects,
#         'labs': labs,
#         'form': form
#     })

#testing feedback view for the section
@login_required
def feedback_view(request):
    if request.session.get('has_submitted', False):
        return render(request, 'home/Thankyou.html')

    obj2 = Batch.objects.all()
    obj1 = Batch.objects.values('Batchyear').distinct()
    semesters = range(1, 9)

    selected_batch_year = request.POST.get('year', '').strip()
    selected_department = request.POST.get('department', '').strip()
    selected_semester = request.POST.get('semester', '').strip()
    selected_section = request.POST.get('section', '')

    print("Selected section:", selected_section)
    sections = None
    has_sections = False
    subjects = None
    labs = None
    responses_saved = False

    # Check if department has sections
    if selected_batch_year and selected_department:
        batch_qs = Batch.objects.filter(Batchyear=selected_batch_year, department=selected_department)
        batch_ids = batch_qs.values_list('id', flat=True)
        batch_section_qs = BatchSection.objects.filter(batch_id__in=batch_ids)

        if batch_section_qs.exists():
            has_sections = True
            sections = batch_section_qs.values_list('section_name', flat=True)
            print("Sections available:", list(sections))  # Debug line to check sections
        else:
            has_sections = False
            print("No sections found for the selected batch/department")

    # Show subjects and labs if everything is selected
    if selected_batch_year and selected_department and selected_semester:
        if not has_sections or (has_sections and selected_section):
            subjects = Subject_detail.objects.filter(
                Batch__Batchyear=selected_batch_year,
                Batch__department=selected_department,
                orensemester=selected_semester,
                sub_type='SUBJECT'
            )
            labs = Subject_detail.objects.filter(
                Batch__Batchyear=selected_batch_year,
                Batch__department=selected_department,
                orensemester=selected_semester,
                sub_type='LABORATORY'
            )

    print("Selected section2:", selected_section)
    # Save responses
    for key in request.POST:
        if key.startswith('response_'):
            qno = key.split('_')[1]
            response = request.POST[key]
            subject_id = request.POST.get(f'subject_{qno}')

            try:
                subject = Subject_detail.objects.get(id=subject_id)

                section_obj = None
                if selected_section:
                    section_obj = BatchSection.objects.filter(
                        batch__Batchyear=selected_batch_year,
                        batch__department=selected_department,
                        section_name=selected_section
                    ).first()

                    # Debugging the section fetching
                    if section_obj:
                        print(f"Found section: {section_obj.section_name}")
                    else:
                        print(f"No matching section found for {selected_batch_year}, {selected_department}, {selected_section}")

                # Save the feedback response
                feedback = FeedbackRes.objects.create(
                    department=selected_department,
                    Response=int(response),
                    Qno=int(qno),
                    subject_detail=subject,
                    batch_year=selected_batch_year,
                    section=selected_section,
                    user=request.user if request.user.is_authenticated else None
                )
                print("Saved feedback entry:", feedback, " | Section saved:", feedback.section)

                responses_saved = True

            except Subject_detail.DoesNotExist:
                print(f"Subject with ID {subject_id} not found")
            except Exception as e:
                print(f"Error saving feedback: {e}")
    # Before rendering the response
    print("Request POST data:", request.POST)
    selected_section = request.POST.get('section', '').strip()
    print("Selected section after POST:", selected_section)

    if responses_saved:
        request.session['has_submitted'] = True
        return render(request, 'home/Thankyou.html')

    form = OptionForm()
    return render(request, 'home/fformnew.html', {
        'Batches': obj1,
        'depart': obj2,
        'semesters': semesters,
        'subjects': subjects,
        'labs': labs,
        'form': form,
        'sections': sections,
        'selected_year': selected_batch_year,
        'selected_department': selected_department,
        'selected_semester': selected_semester,
        'selected_section': selected_section,
    })


def calculate_feedback_score():
    average_count = FeedbackRes.objects.filter(Response=2).count()
    good_count = FeedbackRes.objects.filter(Response=3).count()
    very_good_count = FeedbackRes.objects.filter(Response=4).count()
    excellent_count = FeedbackRes.objects.filter(Response=5).count()

    total = average_count + good_count + very_good_count + excellent_count
    if total == 0:
        return 0

    score = round((((average_count * 2) + (good_count * 3) +
                   (very_good_count * 4) + (excellent_count * 5)) /
                  (total * 5)) * 5, 2)
    return score


@login_required
def feedback_score_view(request):
    score = calculate_feedback_score()
    return render(request, 'home/score.html', {'score': score})


@login_required
def feedback_report_view(request):
    batches = Batch.objects.all()
    departments = Batch.objects.values_list('department', flat=True).distinct()
    semesters = [1, 2, 3, 4, 5, 6, 7, 8]
    sections = BatchSection.objects.values_list('section_name', flat=True).distinct()

    selected_batch = selected_department = selected_semester = selected_section = None
    subject_feedback = []

    if request.method == 'POST':
        selected_batch = request.POST.get('batch_year')
        selected_department = request.POST.get('department')
        selected_semester = request.POST.get('semester')
        selected_section = request.POST.get('section')
        print("Selected batch:", selected_batch)
        print("Selected department:", selected_department)
        print("Selected semester:", selected_semester)
        print("Selected section:", selected_section)
        

        if selected_batch and selected_department and selected_semester and selected_section:
            feedback_qs = FeedbackRes.objects.filter(
            batch_year=selected_batch,
            department=selected_department,
            section=selected_section,
            subject_detail__orensemester=selected_semester
        )
            print("Number of feedback results:", feedback_qs.count())
            subject_feedback = (
                feedback_qs
                .values('subject_detail__sub_code', 'subject_detail__sub_name')
                .annotate(
                    average_score=Avg('Response'),
                    average_count=Count('id', filter=Q(Response__lte=2)),
                    good_count=Count('id', filter=Q(Response__gt=2, Response__lte=3)),
                    very_good_count=Count('id', filter=Q(Response__gt=3, Response__lte=4)),
                    excellent_count=Count('id', filter=Q(Response__gt=4)),
                    staff_names=F('subject_detail__staff_handling__name')
                )
                .order_by('subject_detail__sub_code')
            )
        else:
            subject_feedback = []
    
    total_response_count = FeedbackRes.objects.values('user').distinct().count() 
    return render(request, 'home/report.html', {
        'Batches': batches,
        'depart': departments,
        'semesters': semesters,
        'sections': sections,
        'selected_batch': selected_batch,
        'selected_department': selected_department,
        'selected_semester': selected_semester,
        'selected_section': selected_section,
        'subject_feedback': subject_feedback,
        'total_response_count': total_response_count
    })



def submit(request):
    return render(request, 'home/test.html')
