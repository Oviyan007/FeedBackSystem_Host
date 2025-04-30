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
