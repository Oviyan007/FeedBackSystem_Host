
from django.shortcuts import render,redirect,HttpResponse
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *

from .models import *
from django.db.models import Count,Q,Avg







def Home(request):
    return render(request,'home/index.html')

def Register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create the user
           
            user = form.save()

            # Additional fields specific to UserProfile
            name = form.cleaned_data.get('name')

            # Check if 'name' is not empty before creating the UserProfile
            if name:
                # Create UserProfile instance
                user_profile = UserProfile(user=user, name=name, designation=form.cleaned_data['designation'])
                user_profile.save()
            else:
                # Handle the case where 'name' is empty (provide appropriate error handling or redirect)
                print("Error: 'name' cannot be empty")

            messages.success(request,"Account has been created")

            # Log the user in
        

            # Redirect to a success page or home page
            return redirect('Login')
        else:
            # Form is not valid, handle errors or log them for debugging
            print(form.errors)
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
            return redirect('Home')  # Redirect to homepage or desired page after login
        else:
            messages.error(request, 'Invalid username or password')  

    return render(request, 'home/login.html',)

def Logoutview(request):
    logout(request)
    return redirect('Home')     



@login_required
def profile(request):
     user = request.user
     if user.is_authenticated:
        return render(request, 'home/profile.html', {'user': user})
     else:
        # Handle the case when the user is not authenticated
        return render(request, 'home/profile.html')

   
    
# @login_required
# def feedback_view(request):
    
#     obj2 = Batch.objects.all()
#     obj1 = Batch.objects.values('Batchyear').distinct()
    
#     subjects = None
#     labs = None
#     if request.session.get('has_submitted', False):
#         return render(request, 'home/Thankyou.html')  # Display a thank you page if already submitted
#     if request.method == 'POST':
#         selected_batch_year = request.POST.get('year')
#         selected_department = request.POST.get('department')

#         subjects = Subject_detail.objects.filter(
#             Batch__Batchyear=selected_batch_year, 
#             Batch__department=selected_department, 
#             sub_type='SUBJECT'
#         )
#         labs = Subject_detail.objects.filter(
#             Batch__Batchyear=selected_batch_year,
#             Batch__department=selected_department,
#             sub_type='LABORATORY'
#         )

#         response_submitted = False

#         for key, value in request.POST.items():
#             if key.startswith('response_'):  # Check if the key corresponds to a feedback response
#                 response_submitted = True
#                 qno = key.split('_')[1]  # Extract the question number from the key
#                 response = value  # Get the selected response value
#                 subject_id = request.POST.get(f'subject_{qno}')
#                 subject = Subject_detail.objects.get(id=subject_id)

#                 # Create and save a Feedback object
#                 feedback = FeedbackRes(
#                     department=selected_department,
#                     Response=int(response),
#                     Qno=int(qno),
#                     subject_detail=subject,
#                     batch_year=selected_batch_year
#                 )
#                 feedback.save()

#     form = OptionForm()

#     return render(request, 'home/fformnew.html', {
#         'Batches': obj1,
#         'depart': obj2,
#         'subjects': subjects, 
#         'labs': labs, 
#         'form': form
#     })

# new code for the after submission handling
# @login_required
# def feedback_view(request):
   
#     if FeedbackRes.objects.filter(user=request.user).exists():
#         return render(request, 'home/Thankyou.html') 

#     obj2 = Batch.objects.all()
#     obj1 = Batch.objects.values('Batchyear').distinct()
    
#     subjects = None
#     labs = None

#     if request.method == 'POST':
#         selected_batch_year = request.POST.get('year')
#         selected_department = request.POST.get('department')

#         subjects = Subject_detail.objects.filter(
#             Batch__Batchyear=selected_batch_year, 
#             Batch__department=selected_department, 
#             sub_type='SUBJECT'
#         )
#         labs = Subject_detail.objects.filter(
#             Batch__Batchyear=selected_batch_year,
#             Batch__department=selected_department,
#             sub_type='LABORATORY'
#         )

#         response_submitted = False

#         for key, value in request.POST.items():
#             if key.startswith('response_'):  # Check if the key corresponds to a feedback response
#                 response_submitted = True
#                 qno = key.split('_')[1]  # Extract the question number from the key
#                 response = value  # Get the selected response value
#                 subject_id = request.POST.get(f'subject_{qno}')
#                 subject = Subject_detail.objects.get(id=subject_id)

#                 # Create and save a Feedback object
#                 feedback = FeedbackRes(
#                     user=request.user,  # Save user with feedback to track submission
#                     department=selected_department,
#                     Response=int(response),
#                     Qno=int(qno),
#                     subject_detail=subject,
#                     batch_year=selected_batch_year
#                 )
#                 feedback.save()
                
#         # Set a flag in the session to track feedback submission if not using the model
#         request.session['has_submitted'] = True  
        
#         # Redirect to thank-you page after submission
#         return render(request, 'home/Thankyou.html')

#     form = OptionForm()

#     return render(request, 'home/fformnew.html', {
#         'Batches': obj1,
#         'depart': obj2,
#         'subjects': subjects, 
#         'labs': labs, 
#         'form': form
#     })
    
#newcode after debugging 
# @login_required
# def feedback_view(request):
#     # Redirect to thank-you page if user has already submitted feedback
#     if FeedbackRes.objects.filter(user=request.user).exists():
#         return render(request, 'home/Thankyou.html') 

#     obj2 = Batch.objects.all()
#     obj1 = Batch.objects.values('Batchyear').distinct()
    
#     subjects = None
#     labs = None

#     if request.method == 'POST':
#         selected_batch_year = request.POST.get('year')
#         selected_department = request.POST.get('department')

#         subjects = Subject_detail.objects.filter(
#             Batch__Batchyear=selected_batch_year, 
#             Batch__department=selected_department, 
#             sub_type='SUBJECT'
#         )
#         labs = Subject_detail.objects.filter(
#             Batch__Batchyear=selected_batch_year,
#             Batch__department=selected_department,
#             sub_type='LABORATORY'
#         )

#         # Process feedback responses
#         responses_saved = []
#         for key, value in request.POST.items():
#             if key.startswith('response_'):  # Check if the key corresponds to a feedback response
#                 qno = key.split('_')[1]  # Extract the question number from the key
#                 response = value  # Get the selected response value
#                 subject_id = request.POST.get(f'subject_{qno}')
#                 try:
#                     subject = Subject_detail.objects.get(id=subject_id)
                    
#                     # Check if the user already submitted feedback for this subject and question
#                     if FeedbackRes.objects.filter(
#                         user=request.user, 
#                         Qno=int(qno), 
#                         subject_detail=subject
#                     ).exists():
#                         messages.error(request, f"Feedback for question {qno} already submitted.")
#                         continue

#                     # Save the feedback
#                     feedback = FeedbackRes.objects.create(
#                         user=request.user,  # Save user with feedback to track submission
#                         department=selected_department,
#                         Response=int(response),
#                         Qno=int(qno),
#                         subject_detail=subject,
#                         batch_year=selected_batch_year
#                     )
#                     responses_saved.append(feedback)
#                 except Subject_detail.DoesNotExist:
#                     messages.error(request, f"Subject with ID {subject_id} does not exist.")
#                 except Exception as e:
#                     messages.error(request, f"An error occurred: {str(e)}")

#         # Check if any responses were saved successfully
#         if responses_saved:
#             request.session['has_submitted'] = True  
#             return render(request, 'home/Thankyou.html', {"responses": responses_saved})
#         else:
#             messages.error(request, "No feedback responses were saved. Please try again.")
    
#     form = OptionForm()

#     return render(request, 'home/fformnew.html', {
#         'Batches': obj1,
#         'depart': obj2,
#         'subjects': subjects, 
#         'labs': labs, 
#         'form': form
#     })
 #coutning the response


def calculate_feedback_score():
    # Count responses
    average_count = FeedbackRes.objects.filter(Response=2).count()
    good_count = FeedbackRes.objects.filter(Response=3).count()
    very_good_count = FeedbackRes.objects.filter(Response=4).count()
    excellent_count = FeedbackRes.objects.filter(Response=5).count()

    # Calculate the weighted average using the given formula
    if (average_count + good_count + very_good_count + excellent_count) == 0:
        return 0  # Avoid division by zero

    score = round((((average_count*2) + (good_count*3) + (very_good_count*4) + (excellent_count*5)) / 
                ((average_count + good_count + very_good_count + excellent_count)*5)) * 5, 2)

    return score
@login_required
def feedback_score_view(request):
    score = calculate_feedback_score()
    return render(request, 'home/score.html', {'score': score})


# report generating
@login_required
def feedback_report_view(request):
    obj2 = Batch.objects.all()
    obj1 = Batch.objects.values('Batchyear').distinct()
    
  
    selected_batch = request.POST.get('batch_year', None)
    selected_department = request.POST.get('department', None)

    feedback_query = FeedbackRes.objects.all()

    if selected_batch:
        feedback_query = feedback_query.filter(batch_year=selected_batch)
    
    if selected_department:
        feedback_query = feedback_query.filter(department=selected_department)
        

    subject_feedback = feedback_query.values('subject_detail__sub_name','subject_detail__sub_code',).annotate(
        average_count=Count('Response', filter=models.Q(Response=2)),
        good_count=Count('Response', filter=models.Q(Response=3)),
        very_good_count=Count('Response', filter=models.Q(Response=4)),
        excellent_count=Count('Response', filter=models.Q(Response=5)),
        average_score=Avg('Response'),
       
    )
    #code for faculty name...
    # For each subject, find the related staff using the ManyToMany relationship
    for feedback in subject_feedback:
        subject = Subject_detail.objects.get(sub_code=feedback['subject_detail__sub_code'])
        feedback['staff_names'] = ', '.join([staff.name for staff in subject.staff_handling.all()])

    context = {
        'subject_feedback': subject_feedback,
        'Batches': obj1,
        'depart': obj2,
        'selected_batch': selected_batch,
        'selected_department': selected_department,
        
    }
    
    return render(request, 'home/report.html', context)



   
def submit(request):
    return render(request,'home/test.html')

# testing with semester 
@login_required
def feedback_view(request):

    # Redirect to thank-you page if user has already submitted feedback
    if FeedbackRes.objects.filter(user=request.user).exists():
        return render(request, 'home/Thankyou.html')

    obj2 = Batch.objects.all()
    obj1 = Batch.objects.values('Batchyear').distinct()
    semesters = range(1, 9)  # Assuming semesters 1-8
    

    # Initialize default values
    selected_batch_year = None
    selected_department = None
    selected_semester = None

    subjects = None
    labs = None

    if request.method == 'POST':
        selected_batch_year = request.POST.get('year')
        selected_department = request.POST.get('department')
        selected_semester = request.POST.get('semester')  # Get selected semester
        print(selected_semester)

        # Filter subjects and labs by batch, department, and semester
        subjects = Subject_detail.objects.filter(
            Batch__Batchyear=selected_batch_year, 
            Batch__department=selected_department,
            orensemester=selected_semester,  # Add semester filter
            sub_type='SUBJECT'
        )
        labs = Subject_detail.objects.filter(
            Batch__Batchyear=selected_batch_year,
            Batch__department=selected_department,
            orensemester=selected_semester,  # Add semester filter
            sub_type='LABORATORY'
        )

        # Process feedback responses
        responses_saved = []
        for key, value in request.POST.items():
            if key.startswith('response_'):  # Check if the key corresponds to a feedback response
                qno = key.split('_')[1]  # Extract the question number from the key
                response = value  # Get the selected response value
                subject_id = request.POST.get(f'subject_{qno}')
                try:
                    subject = Subject_detail.objects.get(id=subject_id)
                    
                    # Check if the user already submitted feedback for this subject and question
                    if FeedbackRes.objects.filter(
                        user=request.user, 
                        Qno=int(qno), 
                        subject_detail=subject
                    ).exists():
                        messages.error(request, f"Feedback for question {qno} already submitted.")
                        continue

                    # Save the feedback
                    feedback = FeedbackRes.objects.create(
                        user=request.user,  # Save user with feedback to track submission
                        department=selected_department,
                        Response=int(response),
                        Qno=int(qno),
                        subject_detail=subject,
                        batch_year=selected_batch_year
                    )
                    responses_saved.append(feedback)
                except Subject_detail.DoesNotExist:
                    messages.error(request, f"Subject with ID {subject_id} does not exist.")
                except Exception as e:
                    messages.error(request, f"An error occurred: {str(e)}")

        # Check if any responses were saved successfully
        if responses_saved:
            request.session['has_submitted'] = True
            return render(request, 'home/Thankyou.html', {"responses": responses_saved})
        else:
            messages.error(request, "No feedback responses were saved. Please try again.")

    form = OptionForm()

    # Get all available departments for the selected batch year if provided
    departments = (
        Subject_detail.objects.filter(Batch__Batchyear=selected_batch_year)
        .values('department')
        .distinct() if selected_batch_year else None
    )

    return render(request, 'home/fformnew.html', {
        'Batches': obj1,
        'depart': obj2,
        'semesters': semesters,  # Pass the semesters to the template
        'subjects': subjects, 
        'labs': labs, 
        'form': form,
        'departments': departments,  # Pass departments based on batch year
    })