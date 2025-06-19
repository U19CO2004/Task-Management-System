from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'secret-key'  # Needed for flash messages

# Dummy user data
users = [
    {'id': 1, 'full_name': 'Elias', 'username': 'elias', 'role': 'employee'},
    {'id': 2, 'full_name': 'TEST', 'username': 'test', 'role': 'employee'}
]

next_id = 3

@app.route('/')
@app.route('/manage-users')
def manage_users():
    return render_template('manage_users.html', users=users)

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    global next_id
    if request.method == 'POST':
        new_user = {
            'id': next_id,
            'full_name': request.form['full_name'],
            'username': request.form['username'],
            'role': request.form['role']
        }
        users.append(new_user)
        next_id += 1
        flash('User added successfully!', 'success')
        return redirect(url_for('manage_users'))
    return render_template('add_user.html')

@app.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('manage_users'))

    if request.method == 'POST':
        user['full_name'] = request.form['full_name']
        user['username'] = request.form['username']
        user['role'] = request.form['role']
        flash('User updated successfully!', 'success')
        return redirect(url_for('manage_users'))

    return render_template('edit_user.html', user=user)

@app.route('/delete-user/<int:user_id>')
def delete_user(user_id):
    global users
    users = [u for u in users if u['id'] != user_id]
    flash('User deleted successfully!', 'warning')
    return redirect(url_for('manage_users'))

if __name__ == '__main__':
    app.run(debug=True)
