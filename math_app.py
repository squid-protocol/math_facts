import sqlite3
import random
import time
from flask import Flask, render_template, request, redirect, url_for, flash, json
from collections import defaultdict, Counter
import os
import math

# --- Configuration ---
STUDENTS_CONFIG = {
    "Lola": {
        "operation": "multiplication",
        "symbol": "×",
        "range1": (0, 12),
        "range2": (0, 12)
    },
    "Rosalyn": {
        "operation": "addition",
        "symbol": "+",
        "range1": (10, 99),
        "range2": (0, 20)
    }
}
STUDENT_NAMES = list(STUDENTS_CONFIG.keys())

# --- Database Path ---
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_FILE = os.path.join(basedir, 'math_facts.db')
# --- End Configuration ---


# --- Flask App Initialization ---
app = Flask(__name__)
app.secret_key = 'a_very_secret_key_for_sessions' 

# --- Database Setup ---
def init_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL)')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL,
            num1 INTEGER NOT NULL, num2 INTEGER NOT NULL,
            answer_time_ms INTEGER NOT NULL, is_correct BOOLEAN NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    for name in STUDENT_NAMES:
        cursor.execute("INSERT OR IGNORE INTO users (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

# --- Helper Functions ---
def get_user_id(name):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE name = ?", (name,))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

def get_level_for_time(time_s):
    if time_s is None: return 0
    if time_s < 1: return 6
    if time_s < 2: return 5
    if time_s < 3: return 4
    if time_s < 4: return 3
    if time_s < 5: return 2
    return 1

def get_level_for_count(count):
    if count is None or count == 0: return 0
    if count >= 20: return 5
    if count >= 15: return 4
    if count >= 10: return 3
    if count >= 5: return 2
    return 1

def get_user_progress(user_id, username):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT num1, num2, answer_time_ms, is_correct FROM results WHERE user_id = ? ORDER BY timestamp ASC", (user_id,))
    records = cursor.fetchall()
    conn.close()
    if not records: return None

    operation = STUDENTS_CONFIG[username]['operation']

    if operation == 'multiplication':
        # ... (Lola's logic remains the same)
        lola_config = STUDENTS_CONFIG['Lola']
        min_x, max_x = lola_config['range1']
        min_y, max_y = lola_config['range2']
        x_labels = [str(i) for i in range(min_x, max_x + 1)]
        y_labels = [str(i) for i in range(min_y, max_y + 1)]
        detail_z = [[None for _ in x_labels] for _ in y_labels]
        detail_hover_texts = [[f"{x} × {y}<br>Not yet tested" for x in x_labels] for y in y_labels]
        history_for_js, all_correct_times_ms, fastest_times = {}, [], {}
        history_by_question = defaultdict(list)
        for num1, num2, time_ms, is_correct in records:
            if is_correct:
                history_by_question[(num1, num2)].append(time_ms)
                all_correct_times_ms.append(time_ms)
        for (n1, n2), history in history_by_question.items():
            if history and (str(n1) in x_labels and str(n2) in y_labels):
                fastest_time_ms = min(history)
                fastest_times[(n1, n2)] = fastest_time_ms
                fastest_time_s = round(fastest_time_ms / 1000, 2)
                avg_time_s = round(sum(history) / len(history) / 1000, 2)
                row_idx, col_idx = y_labels.index(str(n2)), x_labels.index(str(n1))
                detail_z[row_idx][col_idx] = fastest_time_s
                detail_hover_texts[row_idx][col_idx] = (f"<b>{n1} × {n2} = {n1*n2}</b><br><br>"
                                                        f"Fastest Time: {fastest_time_s}s<br>"
                                                        f"Average Time: {avg_time_s}s<br>"
                                                        f"Attempts: {len(history)}")
                history_for_js[f"{n1}x{n2}"] = [round(t / 1000, 2) for t in history]
        total_level = 0
        num_facts = len(x_labels) * len(y_labels)
        max_possible_level = num_facts * 6
        for x in x_labels:
            for y in y_labels:
                fastest_time_ms = fastest_times.get((int(x), int(y)))
                fastest_time_s = round(fastest_time_ms / 1000, 2) if fastest_time_ms else None
                total_level += get_level_for_time(fastest_time_s)
        level_percentage = (total_level / max_possible_level) * 100 if max_possible_level > 0 else 0
        if all_correct_times_ms:
            all_correct_times_ms.sort()
            max_y_range = math.ceil(all_correct_times_ms[min(int(len(all_correct_times_ms)*0.95), len(all_correct_times_ms)-1)] / 1000)
        else:
            max_y_range = 10
        return {'type': 'multiplication', 'data': {'detail_heatmap': {'z': detail_z, 'x': x_labels, 'y': y_labels, 'hover_texts': detail_hover_texts}, 'history_data': history_for_js, 'max_y_range': max_y_range, 'level_info': { 'total_level': total_level, 'percentage': level_percentage }}}

    elif operation == 'addition':
        rosalyn_config = STUDENTS_CONFIG['Rosalyn']
        # CORRECTED: Define axes based on the new orientation
        x_labels_main = [str(i) for i in range(rosalyn_config['range2'][0], rosalyn_config['range2'][1] + 1)]
        y_labels_main = [f"{i*10}s" for i in range(rosalyn_config['range1'][0]//10, rosalyn_config['range1'][1]//10 + 1)]
        
        correct_counts_by_category = defaultdict(int)
        for num1, num2, _, is_correct in records:
            if is_correct:
                decade = (num1 // 10) * 10
                category_key = (str(num2), f"{decade}s") # (x_val, y_val)
                correct_counts_by_category[category_key] += 1
        
        count_z = [[None for _ in x_labels_main] for _ in y_labels_main]
        total_level, max_possible_level = 0, 0
        for r_idx, y_label in enumerate(y_labels_main):
            for c_idx, x_label in enumerate(x_labels_main):
                count = correct_counts_by_category.get((x_label, y_label))
                if count is not None:
                    count_z[r_idx][c_idx] = count
                    total_level += get_level_for_count(count)
                max_possible_level += 5
        level_percentage = (total_level / max_possible_level) * 100 if max_possible_level > 0 else 0

        streaks, current_streak = [], 0
        for _, _, _, is_correct in records:
            if is_correct: current_streak += 1
            else:
                if current_streak > 0: streaks.append(current_streak)
                current_streak = 0
        if current_streak > 0: streaks.append(current_streak)
        longest_streak, last_streak = max(streaks) if streaks else 0, streaks[-1] if streaks else 0

        # --- NEW: Calculations for summary graphs ---
        attempts_by_bottom_num = defaultdict(list)
        for _, num2, time_ms, is_correct in records:
            attempts_by_bottom_num[num2].append({'correct': is_correct, 'time': time_ms})

        summary_x_labels = [str(i) for i in range(rosalyn_config['range2'][0], rosalyn_config['range2'][1] + 1)]
        time_summary_z, accuracy_summary_z = [], []
        time_summary_hover, accuracy_summary_hover = [], []
        
        for i in range(rosalyn_config['range2'][0], rosalyn_config['range2'][1] + 1):
            attempts = attempts_by_bottom_num.get(i)
            if not attempts:
                time_summary_z.append(None)
                accuracy_summary_z.append(None)
                time_summary_hover.append(f"Problems like ... + {i}<br>Not yet tested")
                accuracy_summary_hover.append(f"Problems like ... + {i}<br>Not yet tested")
                continue
            
            correct_count = sum(a['correct'] for a in attempts)
            total_attempts = len(attempts)
            accuracy = (correct_count / total_attempts) * 100
            accuracy_summary_z.append(round(accuracy, 1))
            accuracy_summary_hover.append(f"<b>... + {i}</b><br>Accuracy: {round(accuracy, 1)}%<br>({correct_count}/{total_attempts} correct)")

            correct_times = [a['time'] for a in attempts if a['correct']]
            if len(correct_times) > 3:
                correct_times.sort()
                q1, q3 = correct_times[int(len(correct_times)*0.25)], correct_times[int(len(correct_times)*0.75)]
                upper_bound = q3 + 1.5 * (q3 - q1)
                non_outliers = [t for t in correct_times if t <= upper_bound]
                avg_s = round(sum(non_outliers) / len(non_outliers) / 1000, 2) if non_outliers else None
                time_summary_z.append(avg_s)
                time_summary_hover.append(f"<b>... + {i}</b><br>Avg Speed: {avg_s}s")
            elif correct_times:
                avg_s = round(sum(correct_times) / len(correct_times) / 1000, 2)
                time_summary_z.append(avg_s)
                time_summary_hover.append(f"<b>... + {i}</b><br>Avg Speed: {avg_s}s")
            else:
                time_summary_z.append(None)
                time_summary_hover.append(f"<b>... + {i}</b><br>No correct answers yet")

        return {
            'type': 'addition', 
            'data': {
                'count_heatmap': {'z': count_z, 'x': x_labels_main, 'y': y_labels_main},
                'streak_info': {'longest': longest_streak, 'last': last_streak}, 
                'level_info': {'total_level': total_level, 'percentage': level_percentage},
                'time_summary': {'z': [time_summary_z], 'x': summary_x_labels, 'hover_texts': [time_summary_hover]},
                'accuracy_summary': {'z': [accuracy_summary_z], 'x': summary_x_labels, 'hover_texts': [accuracy_summary_hover]}
            }
        }

    return None

@app.route("/")
def index():
    return render_template('index.html', students=STUDENT_NAMES)

@app.route("/practice/<username>")
def practice(username):
    if username not in STUDENTS_CONFIG: return "User not found", 404
    config = STUDENTS_CONFIG[username]
    num1, num2 = random.randint(*config['range1']), random.randint(*config['range2'])
    start_time_ms = int(time.time() * 1000)
    user_id = get_user_id(username)
    total_answered, total_correct = 0, 0
    if user_id:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT is_correct FROM results WHERE user_id = ?", (user_id,))
        records = cursor.fetchall()
        conn.close()
        if records:
            total_answered, total_correct = len(records), sum(1 for r in records if r[0])
    return render_template('practice.html', username=username, num1=num1, num2=num2, start_time=start_time_ms, operator=config['symbol'], total_answered=total_answered, total_correct=total_correct)

@app.route("/submit_answer/<username>", methods=["POST"])
def submit_answer(username):
    if username not in STUDENTS_CONFIG: return "User not found", 404
    config = STUDENTS_CONFIG[username]
    end_time_ms = int(time.time() * 1000)
    form = request.form
    num1, num2, start_time_ms = int(form['num1']), int(form['num2']), int(form['start_time'])
    user_answer = int(form.get('answer', '0')) if form.get('answer', '0').isdigit() else 0
    correct_answer = num1 * num2 if config['operation'] == 'multiplication' else num1 + num2
    is_correct = (user_answer == correct_answer)
    answer_time_ms = end_time_ms - start_time_ms
    user_id = get_user_id(username)
    if user_id:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO results (user_id, num1, num2, answer_time_ms, is_correct) VALUES (?, ?, ?, ?, ?)", (user_id, num1, num2, answer_time_ms, is_correct))
        conn.commit()
        conn.close()
    if is_correct: flash('Correct! Good job!', 'success')
    else: flash(f'Not quite. The correct answer for {num1} {config["symbol"]} {num2} was {correct_answer}. You can do it!', 'error')
    return redirect(url_for('practice', username=username))

@app.route("/progress/<username>")
def progress(username):
    if username not in STUDENTS_CONFIG: return "User not found", 404
    user_id = get_user_id(username)
    progress_data = get_user_progress(user_id, username)
    
    if progress_data and progress_data['type'] == 'multiplication':
        return render_template('multiplication_progress.html', username=username, progress_data=progress_data)
    elif progress_data and progress_data['type'] == 'addition':
        return render_template('addition_progress.html', username=username, progress_data=progress_data)
    
    return render_template('addition_progress.html', username=username, progress_data=None)


# --- Main Execution ---
if __name__ == "__main__":
    if not os.path.exists(DATABASE_FILE):
        print(f"Database not found at {DATABASE_FILE}, creating a new one...")
        init_database()
    
    print(f"Using database at: {DATABASE_FILE}")
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
