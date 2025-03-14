from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid
import pytz  # Thư viện pytz để xử lý múi giờ

# Khởi tạo ứng dụng Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'daotiensang123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Tạo thư mục uploads nếu chưa tồn tại
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Khởi tạo cơ sở dữ liệu
db = SQLAlchemy(app)

# Đặt múi giờ Việt Nam (UTC+7)
vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')

# Các mô hình (Models)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    avatar = db.Column(db.String(200), nullable=True, default='default-avatar.png')
    is_admin = db.Column(db.Boolean, default=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    tasks = db.relationship('Task', backref='category', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='Chưa hoàn thành')
    created = db.Column(db.DateTime, default=lambda: datetime.now(vietnam_tz))  # Lưu thời gian theo múi giờ Việt Nam
    finished = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

# Hàm hỗ trợ
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_avatar(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        return unique_filename
    return None

# Các tuyến đường (Routes)
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        avatar_file = request.files.get('avatar')
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Tên người dùng đã tồn tại!', 'danger')
            return redirect(url_for('register'))
        
        avatar_filename = save_avatar(avatar_file) if avatar_file else 'default-avatar.png'
        
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            avatar=avatar_filename
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Tên người dùng hoặc mật khẩu không chính xác!', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Đã đăng xuất thành công!', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if session.get('is_admin'):
        tasks = Task.query.all()
        categories = Category.query.all()
        users = User.query.all()
    else:
        tasks = Task.query.filter_by(user_id=user_id).all()
        categories = Category.query.all()
        users = None
    
    return render_template('dashboard.html', tasks=tasks, categories=categories, users=users, user=user)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if request.method == 'POST':
        avatar_file = request.files.get('avatar')
        
        if avatar_file:
            avatar_filename = save_avatar(avatar_file)
            if avatar_filename:
                user.avatar = avatar_filename
                db.session.commit()
                flash('Cập nhật avatar thành công!', 'success')
        
        return redirect(url_for('profile'))
    
    return render_template('profile.html', user=user)

@app.route('/task/new', methods=['GET', 'POST'])
def new_task():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category_id = request.form.get('category_id')
        
        new_task = Task(
            title=title,
            description=description,
            user_id=session['user_id'],
            category_id=category_id if category_id else None
        )
        
        db.session.add(new_task)
        db.session.commit()
        
        flash('Công việc mới đã được tạo!', 'success')
        return redirect(url_for('dashboard'))
    
    categories = Category.query.all()
    return render_template('new_task.html', categories=categories)

@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != session['user_id'] and not session.get('is_admin'):
        flash('Bạn không có quyền chỉnh sửa công việc này!', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.category_id = request.form.get('category_id')
        
        db.session.commit()
        
        flash('Công việc đã được cập nhật!', 'success')
        return redirect(url_for('dashboard'))
    
    categories = Category.query.all()
    return render_template('edit_task.html', task=task, categories=categories)

@app.route('/task/<int:task_id>/delete')
def delete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != session['user_id'] and not session.get('is_admin'):
        flash('Bạn không có quyền xóa công việc này!', 'danger')
        return redirect(url_for('dashboard'))
    
    db.session.delete(task)
    db.session.commit()
    
    flash('Công việc đã được xóa!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/task/<int:task_id>/complete')
def complete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    task = Task.query.get_or_404(task_id)
    
    if task.user_id != session['user_id'] and not session.get('is_admin'):
        flash('Bạn không có quyền cập nhật trạng thái công việc này!', 'danger')
        return redirect(url_for('dashboard'))
    
    task.status = 'Hoàn thành'
    task.finished = datetime.now(vietnam_tz)  # Lưu thời gian hoàn thành theo múi giờ Việt Nam
    db.session.commit()
    
    flash('Công việc đã được đánh dấu là hoàn thành!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/category/new', methods=['GET', 'POST'])
def new_category():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        new_category = Category(
            name=name,
            description=description
        )
        
        db.session.add(new_category)
        db.session.commit()
        
        flash('Danh mục mới đã được tạo!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('new_category.html')

@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def edit_category(category_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    category = Category.query.get_or_404(category_id)
    
    if request.method == 'POST':
        category.name = request.form['name']
        category.description = request.form['description']
        
        db.session.commit()
        
        flash('Danh mục đã được cập nhật!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_category.html', category=category)

@app.route('/category/<int:category_id>/delete')
def delete_category(category_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    category = Category.query.get_or_404(category_id)
    
    if category.tasks:
        flash('Không thể xóa danh mục đang chứa công việc!', 'danger')
        return redirect(url_for('dashboard'))
    
    db.session.delete(category)
    db.session.commit()
    
    flash('Danh mục đã được xóa!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/users')
def admin_users():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/toggle_admin/<int:user_id>')
def toggle_admin(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(user_id)
    
    if user.id != session['user_id']:
        user.is_admin = not user.is_admin
        db.session.commit()
        
        flash(f'Quyền admin của người dùng {user.username} đã được thay đổi!', 'success')
    else:
        flash('Bạn không thể thay đổi quyền admin của chính mình!', 'danger')
    
    return redirect(url_for('admin_users'))

# Hàm khởi tạo cơ sở dữ liệu
def init_db():
    with app.app_context():  # Đảm bảo có ngữ cảnh ứng dụng
        db.create_all()

        # Tạo tài khoản admin nếu chưa tồn tại
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)

            # Tạo các danh mục mặc định
            categories = [
                Category(name='Công việc', description='Các công việc liên quan đến công ty'),
                Category(name='Cá nhân', description='Các công việc cá nhân'),
                Category(name='Học tập', description='Các công việc liên quan đến học tập')
            ]

            for category in categories:
                db.session.add(category)

            # Tạo người dùng thử nghiệm
            test_user = User(
                username='test',
                password=generate_password_hash('test123'),
                is_admin=False
            )
            db.session.add(test_user)

            db.session.commit()

            # Tạo các công việc mẫu
            tasks = [
                Task(
                    title='Hoàn thành báo cáo',
                    description='Hoàn thành báo cáo kế hoạch quý 2',
                    status='Chưa hoàn thành',
                    user_id=test_user.id,
                    category_id=1
                ),
                Task(
                    title='Mua sắm',
                    description='Mua sắm đồ dùng cá nhân',
                    status='Hoàn thành',
                    user_id=test_user.id,
                    category_id=2,
                    finished=datetime.now(vietnam_tz)  # Lưu thời gian hoàn thành theo múi giờ Việt Nam
                ),
                Task(
                    title='Học lập trình Flask',
                    description='Hoàn thành khóa học Flask trên Udemy',
                    status='Đang thực hiện',
                    user_id=test_user.id,
                    category_id=3
                ),
                Task(
                    title='Kiểm tra dữ liệu',
                    description='Kiểm tra dữ liệu báo cáo quý 1',
                    status='Chưa hoàn thành',
                    user_id=admin.id,
                    category_id=1
                )
            ]

            for task in tasks:
                db.session.add(task)

            db.session.commit()

if __name__ == '__main__':
    init_db() 
    app.run(debug=True)