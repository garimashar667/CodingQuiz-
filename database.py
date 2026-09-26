# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS questions')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_code TEXT,
            language TEXT,
            level TEXT,
            code TEXT,
            op1 TEXT, op2 TEXT, op3 TEXT, op4 TEXT,
            correct TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_code TEXT,
            player_name TEXT,
            score INTEGER
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM questions WHERE room_code = 'SYSTEM'")
    if cursor.fetchone() == 0:
        ultimate_unique_quiz = [
            # PYTHON: REVERSE COMPILER & BUG HUNTING
            ("SYSTEM", "Python", "Easy", "# REVERSE TRACE CHALLENGE\n# Target Terminal Output is: [0, 2, 4]\n# Which option replacing '??' will generate this?", "print([x for x in range(5) if x % 2 == 0])", "print([x*2 for x in range(3)])", "print([x for x in range(6) if x % 2 == 0])", "print(list(range(0, 5, 2)))", "print([x*2 for x in range(3)])"),
            ("SYSTEM", "Python", "Medium", "# BUG HUNTING ARENA\n# Why will this syntax crash on execution?\ndef add_user(name, internal_list=[]):\n    internal_list.append(name)\n    return internal_list", "It creates a Mutable Default Argument memory leak glitch", "It throws an immediate IdentationError on line 2", "Tuple conversion error dynamically triggered", "It throws a TypeError for missing arguments", "It creates a Mutable Default Argument memory leak glitch"),
            ("SYSTEM", "Python", "Hard", "# REVERSE TRACE CHALLENGE\n# Target Terminal Output is: False True\n# Identify the correct logical condition for '??'", "print(all([]), any([]))", "print(any([]), all([]))", "print(bool(None), bool(''))", "print(0.1 + 0.2 == 0.3, bool([]))", "print(all([]), any([]))"),
            
            # JAVASCRIPT: REVERSE COMPILER & TRICKS
            ("SYSTEM", "JavaScript", "Easy", "// REVERSE TRACE CHALLENGE\n// Target Console Output is: 'number'\n// Which code snippet returns this state type?", "console.log(typeof NaN);", "console.log(typeof null);", "console.log(typeof undefined);", "console.log(typeof []);", "console.log(typeof NaN);"),
            ("SYSTEM", "JavaScript", "Medium", "// BUG HUNTING ARENA\n// What will be the final mutated output of this logical paradox?\nconsole.log(true + false + '1');", "'11'", "'101'", "'2'", "NaN", "'11'"),
            ("SYSTEM", "JavaScript", "Hard", "// REVERSE TRACE CHALLENGE\n// Target Console Output is: false\n// Identify the exact strict equivalence glitch condition:", "console.log(0.1 + 0.2 === 0.3);", "console.log([] == ![]);", "console.log(typeof NaN === 'number');", "console.log(null == undefined);", "console.log(0.1 + 0.2 === 0.3);")
        ]
        cursor.executemany("INSERT INTO questions (room_code, language, level, code, op1, op2, op3, op4, correct) VALUES (?,?,?,?,?,?,?,?,?)", ultimate_unique_quiz)
        
    conn.commit()
    conn.close()

def save_custom_question(room_code, language, level, code, op1, op2, op3, op4, correct):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO questions (room_code, language, level, code, op1, op2, op3, op4, correct) VALUES (?,?,?,?,?,?,?,?,?)", 
                   (room_code, language, level, code, op1, op2, op3, op4, correct))
    conn.commit()
    conn.close()

def get_room_questions(room_code, selected_lang):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT level, code, op1, op2, op3, op4, correct FROM questions WHERE room_code = ? AND language = ?", (room_code, selected_lang))
    rows = cursor.fetchall()
    
    if not rows:
        cursor.execute("SELECT level, code, op1, op2, op3, op4, correct FROM questions WHERE room_code = 'SYSTEM' AND language = ?", (selected_lang,))
        rows = cursor.fetchall()
        
    conn.close()
    
    questions = []
    for r in rows:
        questions.append({
            "level": r[0], "code": r[1],
            "options": [r[2], r[3], r[4], r[5]], "correct": r[6]
        })
    return questions

def save_score(room, name, score):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO leaderboard (room_code, player_name, score) VALUES (?, ?, ?)", (room, name, score))
    conn.commit()
    conn.close()

def get_leaderboard(room):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT player_name, score FROM leaderboard WHERE room_code = ? ORDER BY score DESC", (room,))
    data = cursor.fetchall()
    conn.close()
    return data