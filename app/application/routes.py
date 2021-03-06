from app import db
from config import basedir
from flask import render_template, url_for, flash, redirect, request , send_from_directory
from app.application.forms import ApplicationForm
from flask_login import current_user, login_required
from app.models import Application,Course, Message
from werkzeug.utils import secure_filename
from app.application import application
import os

UPLOAD_FOLDER = os.path.join(basedir,'app\static\\academic_records')

@application.route('/applicaton-form/<course_code>' , methods=['POST','GET'])
@login_required
def application_form(course_code):
    form = ApplicationForm()
    course = Course.query.filter_by(course_code=course_code).first_or_404()
    if course in current_user.tutor.get_all_application_courses():
        flash(f"You have already applied for this course {course_code} ")
        return redirect(url_for('courses.apply'))
    if form.validate_on_submit():
        file = form.academic_record.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER,filename))
        application = Application(motivation=form.motivation.data,academic_record=filename,
                        status='Pending',courses=course , tutors=current_user.tutor)
        message = Message(body=f"{current_user.firstname} has applied to tutor {course_code}",
                        author=current_user , recipient=course.lecturer.user)
        db.session.add(application)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('courses.apply'))
    return render_template('application/application_form.html', 
                        title='Application form' , form=form , course_code=course_code)

@application.route('/my-applications')
@login_required
def my_applications():
    return render_template('application/my_applications.html', title='My applications')

@application.route('/view-applications/<course_code>')
@login_required
def view_applications(course_code):
    course = Course.query.filter_by(course_code=course_code).first_or_404()
    return render_template('application/view_applications.html', title='View applicatins' , course=course)

@application.route('/application-details/<int:app_id>')
@login_required
def application_details(app_id):
    application = Application.query.filter_by(applicaton_id=app_id).first_or_404()
    return render_template('application/application_details.html',
                        title='Application Details', application=application)

@application.route('/academic_record/<filename>')
@login_required
def academic_record(filename):
    return send_from_directory(UPLOAD_FOLDER,filename)

@application.route('/application-response/<int:app_id>/<response>')
@login_required
def application_response(app_id,response):
    application = Application.query.filter_by(applicaton_id=app_id).first_or_404()
    application.status = response
    if response == 'Accepted':
        message = Message(body=f"Congratulations {application.tutors.user.firstname} Your application had for {application.courses.course_code} has been accepted the lecturer will contact you regarding enrollment details",
                            author=current_user , recipient=application.tutors.user)
    else:
        message = Message(body=f'Unfortunatly your application for {application.courses.course_code} did not meet the requirements, try applying for a different course, good luck!',
                            author=current_user , recipient=application.tutors.user)
    db.session.add(application)
    db.session.add(message)
    db.session.commit()

    return redirect(url_for('application.application_details',app_id=app_id))

