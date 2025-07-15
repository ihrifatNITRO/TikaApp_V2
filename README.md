<h1 align="center">TikaApp - Vaccination Management System</h1>

<p align="center">
<img src="https://img.shields.io/badge/Django-4.2-blue.svg" alt="Django Version">
<img src="https://img.shields.io/badge/Python-3.11-blue.svg" alt="Python Version">
<img src="https://img.shields.io/badge/Celery-5.2-brightgreen.svg" alt="Celery">
<img src="https://img.shields.io/badge/Redis-7.0-red.svg" alt="Redis">
</p>

<p>TikaApp is a web application built with Django designed to help manage vaccination records for children. It provides a robust system for user registration, separate dashboards for regular users and administrators, and an automated email reminder system for upcoming vaccine appointments.</p>

<p>The superuser (admin) has a dedicated dashboard to view all registered users, manage their profiles, add and update children's vaccination records, and delete users.</p>

Table of Contents
<ol>
<li><a href="#features">Features</a></li>
<li><a href="#project-structure">Project Structure</a></li>
<li><a href="#setup-and-installation">Setup and Installation</a></li>
<li><a href="#running-the-application">Running the Application</a></li>
<li><a href="#future-improvements">Future Improvements</a></li>
</ol>

<a id="features"></a>Features
<ul>
<li><strong>User Registration:</strong> Secure user registration with required email verification. New accounts are inactive until the user clicks a unique link sent to their email.</li>
<li><strong>Unique Field Validation:</strong> Prevents duplicate registrations based on email, ID card number, and phone number.</li>
<li><strong>Separate User & Admin Authentication:</strong>
<ul>
<li>A standard login for regular users.</li>
<li>A separate, secure login page (<code>/super/login/</code>) for superusers.</li>
</ul>
</li>
<li><strong>Superuser Admin Dashboard:</strong>
<ul>
<li>A protected dashboard accessible only to superusers.</li>
<li>View a list of all non-admin users.</li>
<li>Search for users by their name, email, or phone number.</li>
<li>Click on any user to view their detailed profile.</li>
</ul>
</li>
<li><strong>User & Child Management (Admin):</strong>
<ul>
<li>View detailed user profiles, including ID card, phone number, and account status.</li>
<li>Add one or more children to a user's profile via a pop-up modal form.</li>
<li>Update a child's information (name, DOB, vaccine details) using a pop-up modal.</li>
<li>Delete a user and all of their associated records.</li>
</ul>
</li>
<li><strong>Automated Email Reminders:</strong>
<ul>
<li>Uses Celery and Redis to run a background task.</li>
<li>Automatically sends email reminders to parents 3 days and 1 day before a child's next scheduled vaccine date.</li>
</ul>
</li>
</ul>

<a id="project-structure"></a>Project Structure
<p>The project is organized into several Django apps, each with a specific responsibility:</p>
<ul>
<li><strong><code>homepage</code></strong>: Displays the public-facing landing page.</li>
<li><strong><code>register</code></strong>: Handles the new user registration process and email verification.</li>
<li><strong><code>login</code></strong>: Manages the login/logout functionality for regular users.</li>
<li><strong><code>dashboard</code></strong>: A placeholder app for the future regular user dashboard.</li>
<li><strong><code>super</code></strong>: Contains all logic and templates for the superuser admin dashboard, including user management and child record administration.</li>
</ul>

<a id="setup-and-installation"></a>Setup and Installation
<p>Follow these steps to set up and run the project locally.</p>

Prerequisites
<ul>
<li><a href="https://www.python.org/downloads/">Python 3.8+</a></li>
<li><code>pip</code> (Python package installer)</li>
<li><a href="https://redis.io/docs/getting-started/installation/">Redis</a> (for Celery message broker)</li>
</ul>

Installation Steps
<ol>
<li><strong>Clone the repository:</strong>
<pre><code>git clone https://github.com/your-username/TikaApp.git
cd TikaApp</code></pre>
</li>
<li><strong>Create and activate a virtual environment:</strong>
<pre><code># For Windows
python -m venv venv
.\venv\Scripts\activate

For macOS/Linux
python3 -m venv venv
source venv/bin/activate</code></pre>

</li>
<li><strong>Create a <code>requirements.txt</code> file:</strong>
<p>Create a file named <code>requirements.txt</code> in the root of your project and add the following lines:</p>
<pre><code>Django
celery
redis</code></pre>
</li>
<li><strong>Install dependencies:</strong>
<pre><code>pip install -r requirements.txt</code></pre>
</li>
<li><strong>Apply database migrations:</strong>
<p>This will create the necessary tables in your database.</p>
<pre><code>python manage.py migrate</code></pre>
</li>
<li><strong>Create a superuser:</strong>
<p>This account is needed to access the admin dashboard. Follow the prompts to create your admin account.</p>
<pre><code>python manage.py createsuperuser</code></pre>
<p><strong>Important:</strong> When prompted for a <strong>Username</strong>, enter your email address (e.g., <code>admin@example.com</code>) to ensure it works with the custom login system.</p>
</li>
</ol>

<a id="running-the-application"></a>Running the Application
<p>This project uses Celery for background tasks, which requires running multiple processes simultaneously. You will need to open <strong>three separate terminals</strong>.</p>

Terminal 1: Start the Django Server
<pre><code>python manage.py runserver</code></pre>

<p>Your website will be available at <code>http://127.0.0.1:8000/</code>.</p>

Terminal 2: Start the Celery Worker
<p>This process listens for and executes background tasks, like sending emails. The <code>-P eventlet</code> flag is necessary for running on Windows.</p>
<pre><code># For Windows
celery -A TikaApp worker -l info -P eventlet

For macOS/Linux
celery -A TikaApp worker -l info</code></pre>

Terminal 3: Start the Celery Beat Scheduler
<p>This process triggers the scheduled tasks at their specified time (e.g., checking for vaccine reminders every day).</p>
<pre><code>celery -A TikaApp beat -l info</code></pre>
<p>With all three terminals running, the application will be fully functional, including the automated email reminders.</p>

<a id="future-improvements"></a>Future Improvements
<ul>
<li><strong>User-Facing Dashboard:</strong> A dashboard for regular, logged-in users to view and manage their own children's records.</li>
<li><strong>User Profile Editing:</strong> Allow users to update their own profile information (name, password, etc.).</li>
<li><strong>Detailed Vaccine Records:</strong> Expand the <code>Child</code> model to include more details for each vaccine, such as manufacturer, lot number, and the administrator's name.</li>
<li><strong>Calendar View:</strong> Implement a calendar on the user dashboard to visualize upcoming vaccine appointments.</li>
<li><strong>SMS Notifications:</strong> Integrate a service like Twilio to send SMS reminders in addition to emails.</li>
</ul>
