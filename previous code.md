Navbar \previous code 

{% extends 'home/layout.html'%}
{% include 'home/header.html' %}

{% block body %}
<nav class="navbar navbar-expand-lg bg-body-tertiary py-3 text-uppercase border-bottom border-light-subtle sticky-top">
  <div class="container">
    <a class="navbar-brand" href="#">DSEC</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav ms-auto mb-2 mb-lg-0 gap-4">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="{% url 'Home' %}">Home</a>
        </li>
        
        {% if user.is_authenticated %}
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="{% url 'Profile' %}">Profile</a>
          </li>

          <form id="logoutForm" method="POST" action="{% url 'Logout' %}">
            {% csrf_token %}
            <button type="submit" class="btn btn-danger">Logout</button>
          </form>

          <!-- Check if the user is faculty, disable the feedback button -->
          {% if user.role == 'FACULTY' %}
            <li class="nav-item">
              <!-- Make the 'Give Feedback' link inactive for faculty -->
              <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Give Feedback</a>
            </li>
          {% else %}
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="{% url 'FeedBack' %}">Give Feedback</a>
            </li>
          {% endif %}

          {% if user.role == 'FACULTY' %}
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="{% url 'Report' %}">View Report</a>
            </li>
          {% endif %}
        {% else %}
          <li class="nav-item">
            <a class="nav-link active" href="{% url 'Login' %}">Login</a>
          </li>
          <li class="nav-item">
            <a class="nav-link active" href="{% url 'Register' %}">Register</a>
          </li>
        {% endif %}
      </ul>
    </div>
  </div>
</nav>
{% endblock %}





code report 



<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Feedback Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/0.4.1/html2canvas.min.js"></script>
    <style>
        /* Flexbox for responsive layout */
        .card-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px; /* Space between cards */
        }

        /* Card styles */
        .card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px; /* Maximum width for each card */
            margin: 10px;
            background-color: white;
        }

        .card h4 {
            font-size: 1.2rem;
            text-align: center;
        }

        /* Responsive canvas */
        .feedbackChart {
            width: 100%;
            height: auto;
            max-height: 400px;
        }

        /* Responsive typography */
        h2 {
            text-align: center;
        }

        /* table css  */
        table,th,td{
            border: 1px solid #000;
            border-collapse: collapse;
        }
        table {
            width: 100%;
            margin: 20px 0;
            
            
        }

        th, td {
            padding: 10px;
            text-align: center;
           
        }

        th {
            background-color: #f4f4f4;
        }

        /* Make the table responsive */
        @media (max-width: 768px) {
            table {
                display: block;
                overflow-x: auto;
                white-space: nowrap;
            }
        }

        /* Styling for mobile view */
        @media (max-width: 576px) {
            th, td {
                padding: 8px;
                font-size: 14px;
            }
        }

        /* Add some hover effect */
        tr:hover {
            background-color: #f1f1f1;
        }
         /* Print-specific styles */
    @media print {
        /* Hide the select box and the filter button during printing */
        #batchDepartmentForm, 
        #BatchButton,
        #downloadPDF {
            display: none;
        }
    @media print {
    nav.navbar {
      display: none !important;
    }
  }
        /* Ensure the table is properly displayed during printing */
        table {
            width: 100%;
            page-break-inside: avoid;
        }
        
    }
    </style>
</head>
<body>
    {% block body %}
    {% include 'home/navbar.html' %}

    <h2>Feedback Report</h2>
    <div class="container">
        <div class="row mt-4">
            <form method="post" action="" id="batchDepartmentForm">
                {% csrf_token %}
                <select name="batch_year" id="batchSelect" required>
                    <option value="">Select the batch</option>
                    {% for ans in Batches %}
                        <option value="{{ ans.Batchyear }}" {% if selected_batch == ans.Batchyear %}selected{% endif %}>
                            {{ ans.Batchyear }}
                        </option>
                    {% endfor %}
                </select>
                <select name="department" id="departmentSelect" required>
                    <option value="">Select the department</option>
                    {% for ans in depart %}
                        <option value="{{ ans.department }}" {% if selected_department == ans.department %}selected{% endif %}>
                            {{ ans.department }}
                        </option>
                    {% endfor %}
                </select>
                <button type="submit" class="btn btn-primary" id="BatchButton">Filter</button>
            </form>
        </div>

        <!-- Card container for responsive layout -->
        <div class="container" id="contentContainer" style="display: none;"> <!-- Hidden by default -->
            <div class="card-container">
                {% for subject in subject_feedback %}
                <div class="card">
                    <div class="card-body">
                        <h4 class="card-title">{{ subject.subject_detail__sub_name }}</h4>
                        <canvas id="feedbackChart-{{ forloop.counter }}" class="feedbackChart"></canvas>
                    </div>

                    <script>
                        var ctx = document.getElementById('feedbackChart-{{ forloop.counter }}').getContext('2d');
                        var feedbackChart = new Chart(ctx, {
                            type: 'bar',
                            data: {
                                labels: ['Average', 'Good', 'Very Good', 'Excellent'],
                                datasets: [{
                                    label: 'Feedback for {{ subject.subject_detail__sub_name }}',
                                    data: [
                                        {{ subject.average_count|default:0 }},
                                        {{ subject.good_count|default:0 }},
                                        {{ subject.very_good_count|default:0 }},
                                        {{ subject.excellent_count|default:0 }}
                                    ],
                                    backgroundColor: [
                                        'rgba(255, 99, 132, 0.2)',
                                        'rgba(54, 162, 235, 0.2)',
                                        'rgba(75, 192, 192, 0.2)',
                                        'rgba(153, 102, 255, 0.2)'
                                    ],
                                    borderColor: [
                                        'rgba(255, 99, 132, 1)',
                                        'rgba(54, 162, 235, 1)',
                                        'rgba(75, 192, 192, 1)',
                                        'rgba(153, 102, 255, 1)'
                                    ],
                                    borderWidth: 1
                                }]
                            },
                            options: {
                                scales: {
                                    y: {
                                        beginAtZero: true
                                    }
                                }
                            }
                        });
                    </script>
                </div>
                {% endfor %}
            </div>

            <h2 style="text-align: center;">Subject-Wise Feedback Report</h2>
            <table>
                <thead>
                    <tr>
                        <th>S.No</th>
                        <th>Subject</th>
                        <th>Faculty Name</th>
                        <th>Average (2)</th>
                        <th>Good (3)</th>
                        <th>Very Good (4)</th>
                        <th>Excellent (5)</th>
                        <th>Average Score</th> <!-- New column for average score -->
                    </tr>
                </thead>
                <tbody>
                    {% for subject in subject_feedback %}
                        <tr>
                            <td>{{ forloop.counter }}</td>
                            <td>{{ subject.subject_detail__sub_name }}/{{ subject.subject_detail__sub_code }}</td>
                            <td>{{ subject.staff_names }}</td>
                            <td>{{ subject.average_count | stringformat:'.2f'}}</td>
                            <td>{{ subject.good_count|default:0 }}</td>
                            <td>{{ subject.very_good_count|default:0 }}</td>
                            <td>{{ subject.excellent_count|default:0 }}</td>
                            <td>{{ subject.average_score|default:"N/A" }}</td> 
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
            <button id="downloadPDF" class="btn btn-secondary">Download as PDF</button>
        </div>
    </div>
    {% endblock %}
    
    <script>  
        // JavaScript to toggle content visibility based on batch and department selection
        window.addEventListener('load', function () {
            var batchSelect = document.getElementById('batchSelect');
            var departmentSelect = document.getElementById('departmentSelect');
            var contentContainer = document.getElementById('contentContainer');
            var batchForm = document.getElementById('batchDepartmentForm');
    
            // Check if both batch and department are selected on page load
            toggleContentVisibility();
    
            // Add event listener for form submission
            batchForm.addEventListener('submit', function(event) {
                toggleContentVisibility();
            });
    
            function toggleContentVisibility() {
                // Check if both batch and department are selected
                if (batchSelect.value !== '' && departmentSelect.value !== '') {
                    contentContainer.style.display = 'block';
                } else {
                    contentContainer.style.display = 'none';
                }
            }
        });
         
    
        document.getElementById('downloadPDF').addEventListener('click', function () {
    // Hide certain elements for printing
    document.getElementById('downloadPDF').style.display = 'none';
    document.getElementById('batchDepartmentForm').style.display = 'none';
    document.getElementById('BatchButton').style.display = 'none';
    document.getElementById('footercontainer').style.display = 'none';
    document.querySelector('nav.navbar').style.display = 'none';

    

    // Trigger the print
    window.print();

    // Optionally: After printing, restore the visibility of hidden elements (if necessary)
    setTimeout(function () {
        document.getElementById('downloadPDF').style.display = 'block';
        document.getElementById('batchDepartmentForm').style.display = 'block';
        document.getElementById('BatchButton').style.display = 'block';
        document.querySelector('nav.navbar').style.display = 'block';

    }, 100);
});
    
    </script>
</body>

</html>
{% include 'home/footer.html' %} 


code register 

{% extends 'home/layout.html' %}
{% include 'home/header.html' %} 
{%load crispy_forms_tags %} 
{% block body %}
{% include 'home/navbar.html' %}


    
    <!-- <div class="container-fluid " style="margin-top: 100px;">
        <div class="col-md-offset-4 col-md-10">
            <h2 class="text-primary page-header text-center">User Registration</h2>
        </div>
        <div class=" col-md-offset-6 col-md-4 well bg-light" >
            <form  method="POST" autocomplete="off" >
                {% if messages %}
                    {% for message in messages %}
                        <div class="alert alert-{{message.tags}}">
                            {{message}}
                        </div>
                    {% endfor %}
                {% endif %}

                {% csrf_token %}
                {{ form|crispy }}
                <button type="submit" class="btn btn-primary">Register</button>
            </form>
            <div >
                <a href="{% url 'Login' %}">SignIn Now</a>
             </div>
        </div>
        
    </div> -->
    <div class="container" style="margin-top:70px;min-height:600px;">
        <div class="row">
          <div class="col-12">
            <h4 class="mb-3"> New User Registration</h4>
            <hr style="border-color:#b8bfc2;">
            
          </div>
        </div>
        <section class="py-4" >
          <div class="container">
            <div class="row">
              <div class="col-6">
                <form method="post" action="">
                  {% csrf_token %}
                  <div class="mb-4">
                    <label for="" class="form-label">User Name</label>
                    {{form.username}}
                  </div>
                  <div class="mb-4">
                    <label for="" class="form-label">Full Name / Register Number</label>
                    {{ form.name}}
                  </div>
                  <div class="mb-4">
                    <label for="" class="form-label">User Email</label>
                    {{form.email}}
                  </div>
                  <div class="mb-4">
                    <label for="" class="form-label">Password</label>
                    {{form.password1}}
                  </div>
                  <div class="mb-4">
                    <label for="" class="form-label">Confirm Password</label>
                    {{form.password2}}
                  </div>
                  <div class="mb-4">
                    <label for="designation" class="form-label">Designation</label>
                    {{ form.designation }}
                </div>
                  <button type="submit" class="btn btn-primary">Register</button>
                </form>
                <p class="my-2">Already user ? <a href="{% url 'Login' %}">Login Now</a> </p>
              </div>
              <div class="col-6">
                
                    {% if form.errors.username %}
                      <label class="text-danger d-block">{{ form.errors.username }}</label>
                    {% endif %}
                
                    {% if form.errors.email %}
                    <label class="text-danger d-block">{{ form.errors.email }}</label>
                    {% endif %}
                  
                    {% if form.errors.password1 %}
                    <label class="text-danger d-block">{{ form.errors.password1 }}</label>
                    {% endif %}
                  
                    {% if form.errors.password2 %}
                    <label class="text-danger d-block">{{ form.errors.password2 }}</label>
                    {% endif %}
                  
              </div>
            </div>
          </div>
        </section>
      </div>
    
  

{% endblock %}