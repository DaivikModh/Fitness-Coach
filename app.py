from flask import Flask, request, render_template, redirect, url_for, jsonify,flash,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = "hello"
db = SQLAlchemy(app)

# Define the User model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

#Define the Profile model
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), db.ForeignKey('users.username'), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    height = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    weight_category = db.Column(db.String(20))
    fitness_level = db.Column(db.String(50), nullable=True)

class WorkoutSelection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), db.ForeignKey('users.username'), nullable=False)
    workout_area = db.Column(db.Text, nullable=False)
    user = db.relationship('Users', backref=db.backref('workout_selections', lazy=True))

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10))
    category = db.Column(db.String(20))
    weight_category = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    exercise_name = db.Column(db.String(100))
    sets = db.Column(db.Integer)
    reps = db.Column(db.String(50))

    def as_dict(self):
        return {
            "id": self.id,
            "day": self.day,
            "category": self.category,
            "weight_category": self.weight_category,
            "gender": self.gender,
            "exercise_name": self.exercise_name,
            "sets": self.sets,
            "reps": self.reps
        }
with app.app_context():
    db.create_all()

def setup_database():
    with app.app_context():
        # Create the exercises table
        db.create_all()
        # Clear existing data (optional)
        db.session.query(Exercise).delete()

        # Insert initial data
        exercises = [
            # Upper Body
            # Men
            Exercise(day='Monday', category='upper-body', weight_category='light', gender='Male', exercise_name='Push-ups', sets=3, reps='10-15'),
            Exercise(day='Monday', category='upper-body', weight_category='light', gender='Male', exercise_name='Incline Push-ups', sets=3, reps='10-15'),
            Exercise(day='Monday', category='upper-body', weight_category='moderate', gender='Male', exercise_name='Decline Push-ups', sets=4, reps='8-12'),
            Exercise(day='Monday', category='upper-body', weight_category='heavy', gender='Male', exercise_name='Diamond Push-ups', sets=4, reps='6-10'),
            # Women
            Exercise(day='Monday', category='upper-body', weight_category='light', gender='Female', exercise_name='Knee Push-ups', sets=3, reps='8-12'),
            Exercise(day='Monday', category='upper-body', weight_category='moderate', gender='Female', exercise_name='Wall Push-ups', sets=3, reps='10-15'),

            # Lower Body
            # Men
            Exercise(day='Tuesday', category='lower-body', weight_category='light', gender='Male', exercise_name='Bodyweight Squats', sets=3, reps='10-15'),
            Exercise(day='Tuesday', category='lower-body', weight_category='moderate', gender='Male', exercise_name='Lunges', sets=3, reps='10-12 per leg'),
            Exercise(day='Tuesday', category='lower-body', weight_category='heavy', gender='Male', exercise_name='Jump Squats', sets=3, reps='10-15'),
            # Women
            Exercise(day='Tuesday', category='lower-body', weight_category='light', gender='Female', exercise_name='Bodyweight Squats', sets=3, reps='10-15'),
            Exercise(day='Tuesday', category='lower-body', weight_category='moderate', gender='Female', exercise_name='Reverse Lunges', sets=3, reps='10-12 per leg'),

            # Cardio
            # Both Genders
            Exercise(day='Wednesday', category='cardio', weight_category='light', gender='Both', exercise_name='Brisk Walking', sets=1, reps='20-30 minutes'),
            Exercise(day='Wednesday', category='cardio', weight_category='moderate', gender='Both', exercise_name='High Knees', sets=3, reps='30 seconds'),
            Exercise(day='Wednesday', category='cardio', weight_category='heavy', gender='Both', exercise_name='Burpees', sets=3, reps='8-12'),

            # Core
            # Men
            Exercise(day='Thursday', category='core', weight_category='light', gender='Male', exercise_name='Plank', sets=3, reps='20-30 seconds'),
            Exercise(day='Thursday', category='core', weight_category='moderate', gender='Male', exercise_name='Bicycle Crunches', sets=3, reps='15 per side'),
            Exercise(day='Thursday', category='core', weight_category='heavy', gender='Male', exercise_name='Mountain Climbers', sets=3, reps='30 seconds'),
            # Women
            Exercise(day='Thursday', category='core', weight_category='light', gender='Female', exercise_name='Plank', sets=3, reps='20-30 seconds'),
            Exercise(day='Thursday', category='core', weight_category='moderate', gender='Female', exercise_name='Side Plank', sets=3, reps='15 seconds per side'),
            Exercise(day='Thursday', category='core', weight_category='heavy', gender='Female', exercise_name='Leg Raises', sets=3, reps='10-15'),

            # Flexibility
            Exercise(day='Friday', category='flexibility', weight_category='light', gender='Both', exercise_name='Gentle Stretching', sets=1, reps='10-15 minutes'),
            Exercise(day='Friday', category='flexibility', weight_category='moderate', gender='Both', exercise_name='Yoga Routine', sets=1, reps='30 minutes'),
            Exercise(day='Friday', category='flexibility', weight_category='heavy', gender='Both', exercise_name='Dynamic Stretching', sets=1, reps='20 minutes'),

            # Full Body
            Exercise(day='Saturday', category='full body', weight_category='light', gender='Both', exercise_name='Bodyweight Circuit (5 exercises)', sets=2, reps='5-10 per exercise'),
            Exercise(day='Saturday', category='full body', weight_category='moderate', gender='Both', exercise_name='Animal Flow', sets=2, reps='15 minutes'),
            Exercise(day='Saturday', category='full body', weight_category='heavy', gender='Both', exercise_name='Burpees', sets=4, reps='8-10'),

            # Active Recovery
            Exercise(day='Sunday', category='Active Recovery', weight_category='light', gender='Both', exercise_name='Walking or Light Yoga', sets=1, reps='30-60 minutes'),
        ]

        db.session.bulk_save_objects(exercises)
        db.session.commit()

@app.route('/')
def landing():
    session['loggedIn'] = False
    return render_template('homepage.html')

@app.route('/contactus')
def contactus():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Here, you can handle the form data (e.g., save it to a database, send an email, etc.)
        # For now, we will just flash a success message.
        flash(f'Thank you, {name}! Your message has been received.')
        
        # Redirect back to the contact page
        return redirect(url_for('contactus'))
    
    # Render the contact page
    return render_template('contactus.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')  # Use get() to avoid KeyError
        password = request.form.get('password')
        
        # Check if the username or password is missing
        if not username or not password:
            return render_template('register.html')

        # Create a new User instance
        new_user = Users(username=username, password=password)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Redirect to the login page after successful registration
        return redirect(url_for('login'))

    # Render the registration page (GET request)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    
        if not username or not password:
            return "The data is missing", 400

        # Retrieve the user from the database
        user = Users.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            session['loggedIn'] = True
            return redirect(url_for('setup_profile', username=username))  # Redirect to a welcome page or dashboard
        else:
            flash("Username or password not found.","error")
            return render_template('login.html')  # Unauthorized

    return render_template('login.html')

@app.route('/setup_profile', methods=['GET', 'POST'])
def setup_profile():
    username = request.args.get('username')
    user = Profile.query.filter_by(user_name=username).first()
    
    if user:
        return redirect(url_for('workout', username=username))
    else:    
        if request.method == 'POST':
            age = request.form.get('age')
            gender = request.form.get('gender')
            height = request.form.get('height')
            weight = request.form.get('weight')
            fitness_level = request.form.get('fitness_level')

            if float(weight) < 60:  # Example threshold for light
                weight_category = 'light'
            elif 60 <= float(weight) <= 90:  # Example threshold for moderate
                weight_category = 'moderate'
            else:  # Above 100
                weight_category = 'heavy'

            new_profile = Profile(user_name=username, age=age, gender=gender,height=height,weight=weight,weight_category=weight_category,fitness_level=fitness_level)

            # Add the user to the database
            db.session.add(new_profile)
            db.session.commit()
            
            return redirect(url_for('workout', username=username))
        
    return render_template('setup_profile.html', username=username)

@app.route('/profile')
def details():
    if session.get('loggedIn') == True:
        # Retrieve data from query parameters
        username = session.get('username')
        user = Profile.query.filter_by(user_name=username).first()
        
        age = user.age
        height = user.height
        weight = user.weight
        gender = user.gender
        fitness_level = user.fitness_level
        return render_template('profile.html', username=username, age=age,height=height,weight=weight,gender=gender,fitness_level=fitness_level)
    else:
        return render_template('login.html')
# @app.route('/workout', methods=['GET', 'POST'])
# def workout():
#     username = request.args.get('username')
    
#     # Check if there are any existing workout selections for the username
#     existing_workouts = WorkoutSelection.query.filter_by(user_name=username).all()
    
#     if existing_workouts:
#         return redirect(url_for('exercise', username=username))
    
#     if request.method == 'POST':
#         selected_areas = request.form.getlist('workout-areas')
        
#         if selected_areas: 
#             # Clear existing selections
#             WorkoutSelection.query.filter_by(user_name=username).delete()
            
#             # Create new WorkoutSelection entries
#             for area in selected_areas:
#                 new_selection = WorkoutSelection(user_name=username, workout_area=area)
#                 db.session.add(new_selection)
            
#             # Commit the changes to the database
#             db.session.commit()
            
#             return redirect(url_for('exercise', username=username))
#         else:
#             return "No workout area selected"
    
#     return render_template('workout.html', username=username)

@app.route('/workout', methods=['GET', 'POST'])
def workout():
    if session.get('loggedIn') == True:
        username = session.get('username')  # Retrieve the username from query parameters
        
        if request.method == 'POST':
            # Get all selected workout areas (multiple values from checkboxes)
            selected_areas = request.form.getlist('workout-areas')
            
            if selected_areas: 
                return redirect(url_for('exercise', username=username, selections=','.join(selected_areas)))
            else:
                return "No workout area selected"
        return render_template('workout.html', username=username)
    else:
        return render_template('login.html')

@app.route('/exercise')
def exercise():
    username = session.get('username')
    selections = request.args.get('selections')
    
    # Parse selected areas into a list if there are any
    selected_areas = selections.split(',') if selections else []
    
    # Fetch the user's profile details (e.g., weight category)
    user_details = Profile.query.filter_by(user_name=username).first()
    
    # Initialize an empty list to store exercises from all selected categories
    exercise_list = []
    
    # Initialize a list to store the names of the selected areas
    selected_area_names = []

    # Iterate over each selected area
    for area in selected_areas:
        # Fetch exercises for each category (area) and the user's weight category
        exercises = Exercise.query.filter_by(category=area, weight_category=user_details.weight_category).all()
        
        # Add the fetched exercises to the exercise_list
        exercise_list.extend(exercises)
        
        # Assuming 'category' (area) is a human-readable name, add it to the list
        selected_area_names.append(area)  # Append the name of the area to the list

    # Render the template with the final exercise list and selected area names
    return render_template('exercise.html',username=username, exercises_today=exercise_list, selected_areas=selected_area_names)



@app.route('/dietPlan')
def dietPlan():
    return render_template('dietPlan.html');

@app.route('/fitnessplan')
def fitnessplan():
    return render_template('fitnessplan.html');

@app.route('/test')
def test():
    return render_template('navbar.html');

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)
