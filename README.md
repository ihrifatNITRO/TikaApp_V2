<h1 align="center">TikaApp - Vaccination Management System</h1>

<p align="center">
<img src="https://img.shields.io/badge/Django-4.2-blue.svg" alt="Django Version">
<img src="https://img.shields.io/badge/Python-3.11-blue.svg" alt="Python Version">
<img src="https://img.shields.io/badge/Celery-5.5-brightgreen.svg" alt="Celery">
<img src="https://img.shields.io/badge/Redis-6.2-red.svg" alt="Redis">
</p>

TikaApp is a full-stack web application built with Django, designed to help manage and track vaccination records for children. It provides a robust system for user registration, separate, fully-featured dashboards for parents and administrators, and an automated email reminder system for upcoming vaccine appointments.

The superuser (admin) has a dedicated, secure dashboard to view all registered users, manage their profiles, add and update children's vaccination records, and delete users. Regular users have a personal, responsive dashboard to view their profile and their children's vaccination status.

<h2>Table of Contents</h2>
<ol>
<li><a href="#features">Features</a></li>
<li><a href="#project-structure">Project Structure</a></li>
<li><a href="#setup-and-installation">Setup and Installation</a></li>
<li><a href="#running-the-application">Running the Application</a></li>
<li><a href="#future-improvements">Future Improvements</a></li>
</ol>

<h2 id="features">✨ Features</h2>

<ul>
<li><strong>Secure User Registration:</strong> New accounts are created with email verification. Accounts remain inactive until the user clicks a unique activation link sent to their email.</li>
<li><strong>Unique Field Validation:</strong> Prevents duplicate registrations based on unique email, ID card number, and phone number.</li>
<li><strong>Dual-Role Authentication:</strong>
<ul>
<li>A stylish, responsive login page for regular users.</li>
<li>A separate, secure login page (<code>/super/login/</code>) exclusively for superusers.</li>
</ul>
</li>
<li><strong>Responsive User Dashboard:</strong>
<ul>
<li>A modern, visually appealing, and fully scalable dashboard for logged-in parents.</li>
<li>Displays the parent's profile and a clean, card-based list of all their children's vaccination records.</li>
</ul>
</li>
<li><strong>Comprehensive Superuser Dashboard:</strong>
<ul>
<li>A protected dashboard accessible only to superusers.</li>
<li>View a list of all non-admin users, with their email and phone number displayed.</li>
<li>Search for users by their name, email, or phone number.</li>
<li>View detailed user profiles, including ID card, phone number, and account status.</li>
</ul>
</li>
<li><strong>Full Child Management (Admin):</strong>
<ul>
<li>Add one or more children to a user's profile via a pop-up modal form.</li>
<li>Update a child's information (name, DOB, vaccine details) using a pop-up modal.</li>
<li>Delete a user, which also removes all of their associated child records.</li>
</ul>
</li>
<li><strong>Automated Email Reminders:</strong>
<ul>
<li>Uses <strong>Celery</strong> and <strong>Redis</strong> to run a background task scheduler.</li>
<li>Automatically sends email reminders to parents 3 days and 1 day before a child's next scheduled vaccine date.</li>
</ul>
</li>
</ul>

<h2 id="project-structure">🏗️ Project Structure</h2>

<p>The project is organized into several Django apps, each with a specific responsibility:</p>
<ul>
<li><strong><code>homepage</code></strong>: Displays the public-facing, responsive landing page.</li>
<li><strong><code>register</code></strong>: Handles the new user registration process, form validation, and email verification.</li>
<li><strong><code>login</code></strong>: Manages the login/logout functionality for regular (non-super) users.</li>
<li><strong><code>dashboard</code></strong>: Provides the personal, responsive dashboard for logged-in parents.</li>
<li><strong><code>super</code></strong>: Contains all logic and templates for the superuser admin dashboard, including the admin login, user management, and child record administration.</li>
</ul>

<h2 id="setup-and-installation">🚀 Setup and Installation</h2>

<p>Follow these steps to set up and run the project locally.</p>

<h3>Prerequisites</h3>
<ul>
<li><a href="https://www.python.org/downloads/">Python 3.8+</a></li>
<li><code>pip</code> (Python package installer)</li>
<li><a href="https://redis.io/docs/getting-started/installation/">Redis</a> (for the Celery message broker)</li>
</ul>

<h3>Installation Steps</h3>
<ol>
<li><strong>Clone the repository:</strong>
<pre><code>git clone https://github.com/your-username/TikaApp.git
cd TikaApp</code></pre>
</li>
<li><strong>Create and activate a virtual environment:</strong>
<pre><code># For Windows
python -m venv zenv
.\zenv\Scripts\activate

For macOS/Linux
python3 -m venv zenv
source zenv/bin/activate</code></pre>
</li>
<li><strong>Install dependencies from <code>requirements.txt</code>:</strong>

<pre><code>pip install -r requirements.txt</code></pre>

</li>
<li><strong>Apply database migrations:</strong>
    <p>This will create the necessary tables in your database.</p>

<pre><code>python manage.py migrate</code></pre>

</li>
<li><strong>Create a superuser:</strong>
    <p>This account is needed to access the admin dashboard. Follow the prompts to create your admin account.</p>

<pre><code>python manage.py createsuperuser</code></pre>

    <p><strong>Important:</strong> When prompted for a <strong>Username</strong>, enter your email address (e.g., <code>admin@example.com</code>) to ensure it works with the custom admin login system.</p>
</li>

</ol>

<h2 id="running-the-application">🏃 Running the Application</h2>

<p>This project uses Celery for background tasks, which requires running multiple processes simultaneously. You will need to open <strong>three separate terminals</strong> (all with the virtual environment activated).</p>

<h3>Terminal 1: Start the Django Server</h3>
<pre><code>python manage.py runserver</code></pre>
<p>Your website will be available at <code>http://127.0.0.1:8000/</code>.</p>

<h3>Terminal 2: Start the Celery Worker</h3>
<p>This process listens for and executes background tasks, like sending emails.</p>
<pre><code># The '-P eventlet' flag is required on Windows
celery -A TikaApp worker -l info -P eventlet</code></pre>

<h3>Terminal 3: Start the Celery Beat Scheduler</h3>
<p>This process triggers the scheduled tasks at their specified time (e.g., checking for vaccine reminders every day).</p>
<pre><code>celery -A TikaApp beat -l info</code></pre>
<p>With all three terminals running, the application will be fully functional, including the automated email reminders.</p>

<h2 id="future-improvements">🔮 Future Improvements</h2>

<ul>
<li><strong>Detailed Vaccine Records:</strong> Expand the <code>Child</code> model to include more details for each vaccine, such as manufacturer and lot number.</li>
<li><strong>Calendar View:</strong> Implement a calendar on the user dashboard to visualize upcoming vaccine appointments.</li>
<li><strong>SMS Notifications:</strong> Integrate a service like Twilio to send SMS reminders in addition to emails.</li>
</ul>
