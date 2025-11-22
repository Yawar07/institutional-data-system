from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os

app = Flask(__name__)
app.config['DATA_FOLDER'] = 'data'
app.secret_key = 'your_secret_key_here_change_this'  # Required for flash messages

# Ensure data folder exists
os.makedirs(app.config['DATA_FOLDER'], exist_ok=True)

def read_csv(filename):
    filepath = os.path.join(app.config['DATA_FOLDER'], filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_csv(filename, data, fieldnames):
    filepath = os.path.join(app.config['DATA_FOLDER'], filename)
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def append_csv(filename, data, fieldnames):
    filepath = os.path.join(app.config['DATA_FOLDER'], filename)
    file_exists = os.path.exists(filepath)
    with open(filepath, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def delete_record(filename, index, fieldnames):
    records = read_csv(filename)
    if 0 <= index < len(records):
        records.pop(index)
        write_csv(filename, records, fieldnames)
        return True
    return False

def update_record(filename, index, new_data, fieldnames):
    records = read_csv(filename)
    if 0 <= index < len(records):
        records[index] = new_data
        write_csv(filename, records, fieldnames)
        return True
    return False

@app.route('/')
def index():
    return render_template('index.html')

# NSS Enrollment Routes
@app.route('/nss_enrollment', methods=['GET', 'POST'])
def nss_enrollment():
    fieldnames = ['male', 'female', 'total']
    
    if request.method == 'POST':
        action = request.form.get('action', 'add')
        
        if action == 'add':
            data = {
                'male': request.form['male'],
                'female': request.form['female'],
                'total': request.form['total']
            }
            append_csv('nss_enrollment.csv', data, fieldnames)
            flash('Record added successfully!', 'success')
        
        elif action == 'edit':
            index = int(request.form['index'])
            data = {
                'male': request.form['male'],
                'female': request.form['female'],
                'total': request.form['total']
            }
            update_record('nss_enrollment.csv', index, data, fieldnames)
            flash('Record updated successfully!', 'success')
        
        elif action == 'delete':
            index = int(request.form['index'])
            delete_record('nss_enrollment.csv', index, fieldnames)
            flash('Record deleted successfully!', 'success')
        
        return redirect(url_for('nss_enrollment'))
    
    records = read_csv('nss_enrollment.csv')
    return render_template('nss_enrollment.html', records=records)

# Hostels Routes
@app.route('/hostels', methods=['GET', 'POST'])
def hostels():
    fieldnames = ['sno', 'name', 'type', 'capacity', 'students_residing']
    
    if request.method == 'POST':
        action = request.form.get('action', 'add')
        
        if action == 'add':
            data = {
                'sno': request.form['sno'],
                'name': request.form['name'],
                'type': request.form['type'],
                'capacity': request.form['capacity'],
                'students_residing': request.form['students_residing']
            }
            append_csv('hostels.csv', data, fieldnames)
            flash('Hostel added successfully!', 'success')
        
        elif action == 'edit':
            index = int(request.form['index'])
            data = {
                'sno': request.form['sno'],
                'name': request.form['name'],
                'type': request.form['type'],
                'capacity': request.form['capacity'],
                'students_residing': request.form['students_residing']
            }
            update_record('hostels.csv', index, data, fieldnames)
            flash('Hostel updated successfully!', 'success')
        
        elif action == 'delete':
            index = int(request.form['index'])
            delete_record('hostels.csv', index, fieldnames)
            flash('Hostel deleted successfully!', 'success')
        
        return redirect(url_for('hostels'))
    
    records = read_csv('hostels.csv')
    return render_template('hostels.html', records=records)

# Departments Routes
@app.route('/departments', methods=['GET', 'POST'])
def departments():
    fieldnames = ['sno', 'department_name']
    
    if request.method == 'POST':
        action = request.form.get('action', 'add')
        
        if action == 'add':
            data = {
                'sno': request.form['sno'],
                'department_name': request.form['department_name']
            }
            append_csv('departments.csv', data, fieldnames)
            flash('Department added successfully!', 'success')
        
        elif action == 'edit':
            index = int(request.form['index'])
            data = {
                'sno': request.form['sno'],
                'department_name': request.form['department_name']
            }
            update_record('departments.csv', index, data, fieldnames)
            flash('Department updated successfully!', 'success')
        
        elif action == 'delete':
            index = int(request.form['index'])
            delete_record('departments.csv', index, fieldnames)
            flash('Department deleted successfully!', 'success')
        
        return redirect(url_for('departments'))
    
    records = read_csv('departments.csv')
    return render_template('departments.html', records=records)

# Programmes Routes
@app.route('/programmes', methods=['GET', 'POST'])
def programmes():
    fieldnames = ['sno', 'level', 'program_name', 'year_of_start', 'course_duration', 
                  'entry_qualification', 'medium_instruction', 'sanctioned_intake',
                  'approved_intake_ews', 'approved_intake_sc', 'approved_intake_st', 
                  'approved_intake_obc', 'approved_intake_general', 'approved_intake_total']
    
    if request.method == 'POST':
        action = request.form.get('action', 'add')
        
        data = {
            'sno': request.form['sno'],
            'level': request.form['level'],
            'program_name': request.form['program_name'],
            'year_of_start': request.form['year_of_start'],
            'course_duration': request.form['course_duration'],
            'entry_qualification': request.form['entry_qualification'],
            'medium_instruction': request.form['medium_instruction'],
            'sanctioned_intake': request.form['sanctioned_intake'],
            'approved_intake_ews': request.form['approved_intake_ews'],
            'approved_intake_sc': request.form['approved_intake_sc'],
            'approved_intake_st': request.form['approved_intake_st'],
            'approved_intake_obc': request.form['approved_intake_obc'],
            'approved_intake_general': request.form['approved_intake_general'],
            'approved_intake_total': request.form['approved_intake_total']
        }
        
        if action == 'add':
            append_csv('programmes.csv', data, fieldnames)
            flash('Programme added successfully!', 'success')
        elif action == 'edit':
            index = int(request.form['index'])
            update_record('programmes.csv', index, data, fieldnames)
            flash('Programme updated successfully!', 'success')
        elif action == 'delete':
            index = int(request.form['index'])
            delete_record('programmes.csv', index, fieldnames)
            flash('Programme deleted successfully!', 'success')
        
        return redirect(url_for('programmes'))
    
    records = read_csv('programmes.csv')
    return render_template('programmes.html', records=records)

# Student Enrollment Routes
@app.route('/student_enrollment', methods=['GET', 'POST'])
def student_enrollment():
    fieldnames = ['sno', 'category', 'general_male', 'general_female', 'general_transgender',
                  'ews_male', 'ews_female', 'ews_transgender', 'sc_male', 'sc_female', 'sc_transgender',
                  'st_male', 'st_female', 'st_transgender', 'obc_male', 'obc_female', 'obc_transgender',
                  'total_male', 'total_female', 'total_transgender']
    
    if request.method == 'POST':
        action = request.form.get('action', 'add')
        
        data = {
            'sno': request.form['sno'],
            'category': request.form['category'],
            'general_male': request.form['general_male'],
            'general_female': request.form['general_female'],
            'general_transgender': request.form['general_transgender'],
            'ews_male': request.form['ews_male'],
            'ews_female': request.form['ews_female'],
            'ews_transgender': request.form['ews_transgender'],
            'sc_male': request.form['sc_male'],
            'sc_female': request.form['sc_female'],
            'sc_transgender': request.form['sc_transgender'],
            'st_male': request.form['st_male'],
            'st_female': request.form['st_female'],
            'st_transgender': request.form['st_transgender'],
            'obc_male': request.form['obc_male'],
            'obc_female': request.form['obc_female'],
            'obc_transgender': request.form['obc_transgender'],
            'total_male': request.form['total_male'],
            'total_female': request.form['total_female'],
            'total_transgender': request.form['total_transgender']
        }
        
        if action == 'add':
            append_csv('student_enrollment.csv', data, fieldnames)
            flash('Enrollment record added successfully!', 'success')
        elif action == 'edit':
            index = int(request.form['index'])
            update_record('student_enrollment.csv', index, data, fieldnames)
            flash('Enrollment record updated successfully!', 'success')
        elif action == 'delete':
            index = int(request.form['index'])
            delete_record('student_enrollment.csv', index, fieldnames)
            flash('Enrollment record deleted successfully!', 'success')
        
        return redirect(url_for('student_enrollment'))
    
    records = read_csv('student_enrollment.csv')
    return render_template('student_enrollment.html', records=records)

# Examination Results Routes
@app.route('/examination_results', methods=['GET', 'POST'])
def examination_results():
    fieldnames = ['sno', 'prog', 'year', 'month', 'category', 
                  'general_male', 'general_female', 'general_transgender',
                  'ews_male', 'ews_female', 'ews_transgender',
                  'sc_male', 'sc_female', 'sc_transgender',
                  'st_male', 'st_female', 'st_transgender',
                  'obc_male', 'obc_female', 'obc_transgender',
                  'total_male', 'total_female', 'total_transgender']
    
    if request.method == 'POST':
        action = request.form.get('action', 'add')
        
        data = {
            'sno': request.form['sno'],
            'prog': request.form['prog'],
            'year': request.form['year'],
            'month': request.form['month'],
            'category': request.form['category'],
            'general_male': request.form['general_male'],
            'general_female': request.form['general_female'],
            'general_transgender': request.form['general_transgender'],
            'ews_male': request.form['ews_male'],
            'ews_female': request.form['ews_female'],
            'ews_transgender': request.form['ews_transgender'],
            'sc_male': request.form['sc_male'],
            'sc_female': request.form['sc_female'],
            'sc_transgender': request.form['sc_transgender'],
            'st_male': request.form['st_male'],
            'st_female': request.form['st_female'],
            'st_transgender': request.form['st_transgender'],
            'obc_male': request.form['obc_male'],
            'obc_female': request.form['obc_female'],
            'obc_transgender': request.form['obc_transgender'],
            'total_male': request.form['total_male'],
            'total_female': request.form['total_female'],
            'total_transgender': request.form['total_transgender']
        }
        
        if action == 'add':
            append_csv('examination_results.csv', data, fieldnames)
            flash('Result record added successfully!', 'success')
        elif action == 'edit':
            index = int(request.form['index'])
            update_record('examination_results.csv', index, data, fieldnames)
            flash('Result record updated successfully!', 'success')
        elif action == 'delete':
            index = int(request.form['index'])
            delete_record('examination_results.csv', index, fieldnames)
            flash('Result record deleted successfully!', 'success')
        
        return redirect(url_for('examination_results'))
    
    records = read_csv('examination_results.csv')
    return render_template('examination_results.html', records=records)

# Placement Routes
@app.route('/placement', methods=['GET', 'POST'])
def placement():
    fieldnames = ['male_placed', 'female_placed', 'total_placed', 'median_salary']
    
    if request.method == 'POST':
        action = request.form.get('action', 'add')
        
        data = {
            'male_placed': request.form['male_placed'],
            'female_placed': request.form['female_placed'],
            'total_placed': request.form['total_placed'],
            'median_salary': request.form['median_salary']
        }
        
        if action == 'add':
            append_csv('placement.csv', data, fieldnames)
            flash('Placement record added successfully!', 'success')
        elif action == 'edit':
            index = int(request.form['index'])
            update_record('placement.csv', index, data, fieldnames)
            flash('Placement record updated successfully!', 'success')
        elif action == 'delete':
            index = int(request.form['index'])
            delete_record('placement.csv', index, fieldnames)
            flash('Placement record deleted successfully!', 'success')
        
        return redirect(url_for('placement'))
    
    records = read_csv('placement.csv')
    return render_template('placement.html', records=records)

# Staff Information Routes
@app.route('/staff_info', methods=['GET', 'POST'])
def staff_info():
    fieldnames = ['staff_type', 'category', 'subcategory',
                  'general_male', 'general_female', 'general_transgender',
                  'ews_male', 'ews_female', 'ews_transgender',
                  'sc_male', 'sc_female', 'sc_transgender',
                  'st_male', 'st_female', 'st_transgender',
                  'obc_male', 'obc_female', 'obc_transgender',
                  'total_male', 'total_female', 'total_transgender']
    
    if request.method == 'POST':
        action = request.form.get('action', 'add')
        
        data = {
            'staff_type': request.form['staff_type'],
            'category': request.form['category'],
            'subcategory': request.form['subcategory'],
            'general_male': request.form['general_male'],
            'general_female': request.form['general_female'],
            'general_transgender': request.form['general_transgender'],
            'ews_male': request.form['ews_male'],
            'ews_female': request.form['ews_female'],
            'ews_transgender': request.form['ews_transgender'],
            'sc_male': request.form['sc_male'],
            'sc_female': request.form['sc_female'],
            'sc_transgender': request.form['sc_transgender'],
            'st_male': request.form['st_male'],
            'st_female': request.form['st_female'],
            'st_transgender': request.form['st_transgender'],
            'obc_male': request.form['obc_male'],
            'obc_female': request.form['obc_female'],
            'obc_transgender': request.form['obc_transgender'],
            'total_male': request.form['total_male'],
            'total_female': request.form['total_female'],
            'total_transgender': request.form['total_transgender']
        }
        
        if action == 'add':
            append_csv('staff_info.csv', data, fieldnames)
            flash('Staff record added successfully!', 'success')
        elif action == 'edit':
            index = int(request.form['index'])
            update_record('staff_info.csv', index, data, fieldnames)
            flash('Staff record updated successfully!', 'success')
        elif action == 'delete':
            index = int(request.form['index'])
            delete_record('staff_info.csv', index, fieldnames)
            flash('Staff record deleted successfully!', 'success')
        
        return redirect(url_for('staff_info'))
    
    records = read_csv('staff_info.csv')
    return render_template('staff_info.html', records=records)

# Scholarships Routes
@app.route('/scholarships', methods=['GET', 'POST'])
def scholarships():
    fieldnames = ['scholarship_scheme', 'category',
                  'general_male', 'general_female', 'general_transgender',
                  'ews_male', 'ews_female', 'ews_transgender',
                  'sc_male', 'sc_female', 'sc_transgender',
                  'st_male', 'st_female', 'st_transgender',
                  'obc_male', 'obc_female', 'obc_transgender',
                  'total_male', 'total_female', 'total_transgender']
    
    if request.method == 'POST':
        action = request.form.get('action', 'add')
        
        data = {
            'scholarship_scheme': request.form['scholarship_scheme'],
            'category': request.form['category'],
            'general_male': request.form['general_male'],
            'general_female': request.form['general_female'],
            'general_transgender': request.form['general_transgender'],
            'ews_male': request.form['ews_male'],
            'ews_female': request.form['ews_female'],
            'ews_transgender': request.form['ews_transgender'],
            'sc_male': request.form['sc_male'],
            'sc_female': request.form['sc_female'],
            'sc_transgender': request.form['sc_transgender'],
            'st_male': request.form['st_male'],
            'st_female': request.form['st_female'],
            'st_transgender': request.form['st_transgender'],
            'obc_male': request.form['obc_male'],
            'obc_female': request.form['obc_female'],
            'obc_transgender': request.form['obc_transgender'],
            'total_male': request.form['total_male'],
            'total_female': request.form['total_female'],
            'total_transgender': request.form['total_transgender']
        }
        
        if action == 'add':
            append_csv('scholarships.csv', data, fieldnames)
            flash('Scholarship record added successfully!', 'success')
        elif action == 'edit':
            index = int(request.form['index'])
            update_record('scholarships.csv', index, data, fieldnames)
            flash('Scholarship record updated successfully!', 'success')
        elif action == 'delete':
            index = int(request.form['index'])
            delete_record('scholarships.csv', index, fieldnames)
            flash('Scholarship record deleted successfully!', 'success')
        
        return redirect(url_for('scholarships'))
    
    records = read_csv('scholarships.csv')
    return render_template('scholarships.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)