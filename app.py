from flask import Flask, render_template, request, redirect, url_for
import supabase

app = Flask(__name__)
supabase_url = 'https://mhceiasyoevezkxqmtsc.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1oY2VpYXN5b2V2ZXpreHFtdHNjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQ1NTI3MzYsImV4cCI6MjA1MDEyODczNn0.MpnZCoe7ufBXjKMKEatfolrnzUmRsZl9HP8Wx9r6hiE'
client = supabase.Client(supabase_url, supabase_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = {
        'static': request.form['static'],
        'game_name': request.form['game_name'],
        'game_surname': request.form['game_surname'],
        'penalty_type': request.form['penalty_type'],
        'issuer': request.form['issuer'],
        'article': request.form['article'],
        'date': request.form['date'],
        'work_off': 'on' if 'work_off' in request.form else 'off',
        'issued': 'on' if 'issued' in request.form else 'off',
        'warnings_count': request.form.get('warnings_count', ''),
        'reprimands_count': request.form.get('reprimands_count', ''),
        'penalty_worked_off': request.form['penalty_worked_off'],
        'employee_dismissed': request.form['employee_dismissed']
    }

    # Проверяем, существует ли запись с таким же значением static
    response = client.table('penalties').select('*').eq('static', data['static']).execute()
    # if response.error:
    #     return f"Ошибка: {response.error.message}", 500

    if response.data:
        # Запись существует, обновляем её
        update_response = client.table('penalties').update(data).eq('static', data['static']).execute()
        # if update_response.error:
        #     return f"Ошибка: {update_response.error.message}", 500
    else:
        # Записи нет, создаем новую
        insert_response = client.table('penalties').insert(data).execute()
        # if insert_response.error:
        #     return f"Ошибка: {insert_response.error.message}", 500

    return redirect(url_for('index'))

@app.route('/view', methods=['GET', 'POST'])
def view():
    results = []
    static_value = ''
    if request.method == 'POST':
        static_value = request.form['static']
        response = client.table('penalties').select('*').eq('static', static_value).execute()
        # if response.error:
        #     return f"Ошибка: {response.error.message}", 500
        results = response.data

    # Получаем все записи из таблицы penalties
    all_penalties_response = client.table('penalties').select('*').execute()
    # if all_penalties_response.error:
    #     return f"Ошибка: {all_penalties_response.error.message}", 500
    all_penalties = all_penalties_response.data

    return render_template('view.html', results=results, static_value=static_value, all_penalties=all_penalties)

if __name__ == '__main__':
    app.run(debug=True)