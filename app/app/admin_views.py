from app import app

@app.route('/admin')
def admin_page():
    return "Admin Page"
