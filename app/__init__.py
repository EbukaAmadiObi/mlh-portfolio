import os
import logging
import json
import datetime
from flask import Flask, render_template, request, jsonify, url_for, redirect
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password = os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )
    print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

work_experiences = [
    {
        "job_title": "Production Engineering Fellow",
        "company": "Major League Hacking",
        "dates": "Jun 2025 - Present",
        "description": "You know the deal."
    },
    {
        "job_title": "Software Engineering Intern",
        "company": "Arista Networks",
        "dates": "May 2024 - Aug 2024",
        "description": "Working on the Arista CloudVision Platform, a web-based portal that shows\
                        it’s users the status of their network, lets them update it’s configuration, \
                        and provides notifications to its users when something goes wrong. Focused on \
                        network automation and visibility through dashboard metrics and alerts on \
                        service level indicators. • Assisted in implementing a new feature in Go \
                        to display the configuration of server hardware, implemented automated \
                        testing and optimized performance to improve the user experience. \
                        • Collaborated with the engineering team to ensure seamless integration \
                        and deployment of network management solutions using Git and Jenkins."
    },
    {
        "job_title": "Team Lead",
        "company": "Google Developer Student Club",
        "dates": "Jul 2023 - Jun 2024",
        "description": "Partnered with Google to organise workshops, projects, and events \
                        for students at my university. Managed a core team of 4 students to help create \
                        a successful student organisation. Helped to increased club membership \
                        by 370% over 3 months."
    },
    {
        "job_title": "Apparel Designer",
        "company": "Redbubble & Teepublic",
        "dates": "Oct 2019 - Jun 2024",
        "description": "Independent apparel designer at Redbubble and Teepublic \n\n \
                        • Designed over 160 artworks to be sold on t-shirts, stickers, mugs and other products\n\
                        • Researched current and popular niches to create impactful and trendy designs\n\
                        • Sold over 9500 units total"
    },
    {
        "job_title": "Assistant Lab Technician",
        "company": "IGSL Ltd.",
        "dates": "Jul 2021 - Aug 2021",
        "description": "I performed detailed and methodical testing and analysis of soils, \
                        rocks, concrete, and their properties as well as collaborated with \
                        other technicians to gain a complete picture of the characteristics, \
                        nature, and integrity of soil in sites before clearing them to begin \
                        construction projects like the construction of a new Lidl location."
    },
    {
        "job_title": "Freelance Graphic Designer",
        "company": "myself",
        "dates": "Feb 2020 - May 2021",
        "description": "Designed logos and posters and other stuff for people in my community back in Kildare"
    }
    
]

education_history = [
    {
        "degree": "Bachelor of Engineering in Electronic Engineering",
        "institution": "University College Dublin",
        "years": "Sept 2021 - Sept 2025"
    }
]

hobbies_data = [
    {
        "name": "Engineering Projects",
        "image": 'img/IMG_4431.JPG',
        "description": "What kind of engineer would I be without them? Pictured above is a 3D LED matrix I built in 3rd year, led a small team of students to (almost) finish..."
    },
    {
        "name": "Social Events",
        "image": 'img/IMG_7187.jpg',
        "description": "Love attending mixers and networking events, also organised a lot of them during uni, looking for a way to keep that going..."
    },
    {
        "name": "Partying",
        "image": 'img/IMG_4206.jpg',
        "description": "What can I say"
    }
]

NAV_PAGES = [
    {'endpoint': 'index', 'name': 'Home'},
    {'endpoint': 'about', 'name': 'About'},
    {'endpoint': 'work', 'name': 'Work'},
    {'endpoint': 'education', 'name': 'Education'},
    {'endpoint': 'hobbies', 'name': 'Hobbies'},
    {'endpoint': 'travel', 'name': 'Travel'},
    {'endpoint': 'timeline', 'name': 'Timeline'},
]

@app.context_processor
def inject_nav_pages():
    return dict(nav_pages=NAV_PAGES)

@app.route('/')
def index():
    return render_template('index.html', title="Ebuka's Portfolio", url=os.getenv("URL"))

@app.route('/about')
def about():
    return render_template('about.html', title="About Me", url=os.getenv("URL"))

@app.route('/save_about', methods=['POST'])
def save_about():
    global about_me
    about_me = request.form['about_me']
    return redirect(url_for('about'))

@app.route('/work')
def work():
    return render_template('work.html', title="Work Experience", url=os.getenv("URL"), work_experiences=work_experiences)

@app.route('/add_work', methods=['POST'])
def add_work():
    
    date1 = datetime.datetime.strptime(request.form['date1'], "%Y-%m-%d").strftime("%b %Y")
    date2 = datetime.datetime.strptime(request.form['date2'], "%Y-%m-%d").strftime("%b %Y")

    work_experiences.append({
        'job_title': request.form['job_title'],
        'company': request.form['company'],
        'dates': date1 + ' - ' + date2,
        'description': request.form['description']
    })
    return redirect(url_for('work'))

@app.route('/education')
def education():
    return render_template('education.html', title="Education", url=os.getenv("URL"), education_history=education_history)

@app.route('/add_education', methods=['POST'])
def add_education():
    
    year1 = datetime.datetime.strptime(request.form['year1'], "%Y-%m-%d").strftime("%Y")
    year2 = 'Present' if request.form.get('currently_attending') else datetime.datetime.strptime(request.form['year2'], "%Y-%m-%d").strftime("%Y")

    education_history.append({
        'degree': request.form['degree'],
        'institution': request.form['institution'],
        'years': year1 + ' - ' + year2
    })
    return redirect(url_for('education'))

@app.route('/hobbies')
def hobbies():
    # We need to generate the image URLs dynamically
    hobbies_with_urls = []
    for hobby in hobbies_data:
        hobbies_with_urls.append({
            'name': hobby['name'],
            'image': url_for('static', filename=hobby['image']),
            'description': hobby['description']
        })
    return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"), hobbies=hobbies_with_urls)

@app.route('/add_hobby', methods=['POST'])
def add_hobby():
    name = request.form['name']
    image_file = request.files['image']

    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).rstrip().replace(' ', '_')
    filename = f"{safe_name}.jpg"
    upload_folder = os.path.join(app.static_folder, 'img')
    os.makedirs(upload_folder, exist_ok=True)
    save_path = os.path.join(upload_folder, filename)
    image_file.save(save_path)

    hobbies_data.append({
        'name': name,
        'image': f'img/{filename}',
        'description': request.form['description']
    })

    return redirect(url_for('hobbies'))

@app.route('/travel')
def travel():
    try:
        with open('app/markers.json', 'r') as f:
            markers = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        markers = []
    return render_template('travel.html', title="Travel", url=os.getenv("URL"), markers=markers)

@app.route('/add_marker', methods=['POST'])
def add_marker():
    data = request.get_json()
    if not data or 'lat' not in data or 'lng' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    try:
        with open('app/markers.json', 'r') as f:
            markers = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        markers = []

    markers.append({
        'lat': data['lat'],
        'lng': data['lng'],
        'note': data.get('note', '')
    })

    with open('app/markers.json', 'w') as f:
        json.dump(markers, f, indent=4)

    return jsonify({'success': 'Marker added'}), 201


@app.route('/upload', methods=['POST'])
def upload_file():
    app.logger.info("Upload endpoint was hit")
    if 'profile_picture' not in request.files:
        app.logger.error("No 'profile_picture' in request.files")
        return jsonify({'error': 'No file part'}), 400
    file = request.files['profile_picture']
    if file.filename == '':
        app.logger.error("Filename is empty")
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = 'logo.jpg'
        upload_folder = os.path.join(app.static_folder, 'img')
        save_path = os.path.join(upload_folder, filename)
        app.logger.info(f"Attempting to save file to: {save_path}")
        try:
            file.save(save_path)
            app.logger.info(f"Successfully saved file to: {save_path}")
            response = jsonify({'success': 'File uploaded successfully'})
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response, 200
        except Exception as e:
            app.logger.error(f"Failed to save file: {e}")
            return jsonify({'error': str(e)}), 500
        
@app.route('/timeline')
def timeline():
    timeline_posts = []
    for p in TimelinePost.select().order_by(TimelinePost.created_at.desc()):
        post_dict = model_to_dict(p)
        post_dict["formatted_date"] = p.created_at.strftime('%B %d, %Y')
        timeline_posts.append(post_dict)
    return render_template('timeline.html', title="Timeline", url=os.getenv("URL"), timeline_posts=timeline_posts)

@app.route('/timeline_post' , methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    TimelinePost.create(name=name, email=email, content=content)

    return redirect(url_for('timeline'))


@app.route('/api/timeline_post' , methods=['POST'])
def api_post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)


@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts':[
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }