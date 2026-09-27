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
        python_exhaustive_quiz = [
            # 🟢 EASY LEVEL (1 - 5)
            ("SYSTEM", "Python", "Easy", "# PUZZLE 1: REVERSE TRACE CHALLENGE\n# Target Terminal Output is:\n# Which option replacing '??' will generate this?", "print([x for x in range(5) if x % 2 == 0])", "print([x*2 for x in range(3)])", "print([x for x in range(6) if x % 2 == 0])", "print(list(range(0, 5, 2)))", "print([x*2 for x in range(3)])"),
            ("SYSTEM", "Python", "Easy", "# PUZZLE 2: BUG HUNTING ARENA\n# Why does this operation fail for string concatenation?\nprint('Python' + 3.14)", "TypeError: can only concatenate str to str", "SyntaxError: invalid float literal token", "ValueError: structural casting fault", "Works perfectly by automatically casting", "TypeError: can only concatenate str to str"),
            ("SYSTEM", "Python", "Easy", "# PUZZLE 3: REVERSE TRACE CHALLENGE\n# Target Output is: nohtyP\n# Identify the missing slicing indices sequence mapping:", "text = 'Python'; print(text[::-1])", "text = 'Python'; print(text[-1:0])", "text = 'Python'; print(text[1:5:-1])", "text = 'Python'; print(text.reverse())", "text = 'Python'; print(text[::-1])"),
            ("SYSTEM", "Python", "Easy", "# PUZZLE 4: DATA STRUCTURE TRICK\n# What is the unique collection length metric output?\nprint(len({1, 2, 2, 3, 3, 3}))", "6", "3", "4", "TypeError", "3"),
            ("SYSTEM", "Python", "Easy", "# PUZZLE 5: STRING MUTATION OVERLOAD\n# Predict the compilation character trace behavior:\nprint(3 * 'A' + 'B')", "AAAB", "A3B", "SyntaxError", "AAA B", "AAAB"),
            
            # 🟡 MEDIUM LEVEL (6 - 10)
            ("SYSTEM", "Python", "Medium", "# PUZZLE 6: BUG HUNTING ARENA\n# Why does this fail for string evaluation runtime?\ndef calc(x): return x + 5.0", "Unsupported operand type dynamic validation", "IndentationError caught on line 2", "NameError lookup variable crash", "Works flawlessly via polymorphic parsing", "Unsupported operand type dynamic validation"),
            ("SYSTEM", "Python", "Medium", "# PUZZLE 7: REVERSE TRACE CHALLENGE\n# Target Output is: True\n# Which logic maps Banker's Rounding protocols tracking parity?", "print(round(2.5) == round(3.5))", "print(0.1 + 0.2 == 0.3)", "print(bool([]))", "print('A' is 'A')", "print(round(2.5) == round(3.5))"),
            ("SYSTEM", "Python", "Medium", "# PUZZLE 8: DICTIONARY FALLBACK TRACE\n# Predict the runtime output matrix of target missing key parameters:\nd = {'a': 1, 'b': 2}; print(d.get('c', 404))", "None", "KeyError exception trace", "404", "0", "404"),
            ("SYSTEM", "Python", "Medium", "# PUZZLE 9: BOOLEAN FALSY PARADOX\n# What sequence token string is output by empty state checks?\nprint(bool([]), bool(), bool(''))", "False True False", "False False False", "True True True", "TypeError structural warning", "False False False"),
            ("SYSTEM", "Python", "Medium", "# PUZZLE 10: LIST MUTATION PARADOX\n# Predict the structural update trace value of array items:\nx = []; y = x; y.append(5); print(x)", "[]", "", "None", "AttributeError tracking elements", ""),
            
            # 🟠 HARD LEVEL (11 - 15)
            ("SYSTEM", "Python", "Hard", "# PUZZLE 11: BUG HUNTING ARENA\n# Identify the dynamic default mutable reference leak context loop:", "def add(n, l=[]): l.append(n); return l", "x = 10; def f(): print(x); x = 5", "a = 256; b = 256; print(a is b)", "print(all([]))", "def add(n, l=[]): l.append(n); return l"),
            ("SYSTEM", "Python", "Hard", "# PUZZLE 12: FLOATING POINT REFERENCE ANOMALY\n# What boolean logic matches precision computation offsets?", "print(0.1 + 0.2 == 0.3)", "True", "False", "Machine Dependent allocation", "ValueError validation loop", "False"),
            ("SYSTEM", "Python", "Hard", "# PUZZLE 13: VARIABLE SCOPE RESOLUTION SURVEILLANCE\n# What error runtime flag is triggered by local lookup shadowing?\nx = 5\ndef run():\n    print(x)\n    x = 10\nrun()", "NameError runtime trace", "UnboundLocalError reference conflict", "TypeError mismatch bounds", "Runs perfectly outputting 5", "UnboundLocalError reference conflict"),
            ("SYSTEM", "Python", "Hard", "# PUZZLE 14: INTERNALS MEMORY CACHING PIPELINE\n# Identify the behavior tracking integers bounds outside cache pool:\na = 257; b = 257; print(a is b)", "True", "False", "None structural context", "SegmentationFault dynamic core", "False"),
            ("SYSTEM", "Python", "Hard", "# PUZZLE 15: TRICKY MUTABILITY REFERENCE MATRIX\n# Why can elements inside a tuple update successfully under these parameters?\nt = (1, 2, []); t.append(99); print(t)", "Tuple immutable; inner list allows modification", "TypeError: item assignment crash", "SyntaxError checking tokens layout", "ValueError parameter conversion glitch", "Tuple immutable; inner list allows modification"),
            
            # 🔴 EXTREME LEVEL (16 - 20)
            ("SYSTEM", "Python", "Extreme", "# PUZZLE 16: REVERSE TRACE CHALLENGE\n# Target Output is: True False\n# Which dynamic engine query maps this logical empty iterator paradox?", "print(all([]), any([]))", "print(any([]), all([]))", "print(10 > 5 > 2, bool(''))", "print(type(type) == object, False)", "print(all([]), any([]))"),
            ("SYSTEM", "Python", "Extreme", "# PUZZLE 17: META-OBJECT META-CLASS RESOLUTION\n# Predict the precise execution object class map value:\nprint(type(type))", "<class 'object'>", "<class 'type'>", "<class 'class'>", "TypeError parameter mismatch", "<class 'type'>"),
            ("SYSTEM", "Python", "Extreme", "# PUZZLE 18: OPERATOR PRECEDENCE REVERSE LOGIC\n# What token output string is evaluated by the execution tree?\nx = True; y = False; z = False\nif x or y and z: print('Win')\nelse: print('Lose')", "Win", "Lose", "SyntaxError matching tags", "None feedback loop", "Win"),
            ("SYSTEM", "Python", "Extreme", "# PUZZLE 19: CLOSURE SCOPE LEAK BINDINGS\n# Predict the array token value evaluated under dynamic runtime:\nfuncs = [lambda x: i * x for i in range(3)]", "0", "2", "4", "TypeError evaluation crash", "4"),
            ("SYSTEM", "Python", "Extreme", "# PUZZLE 20: DYNAMIC POINTER IDENTICAL REFERENCING\n# What boolean response maps internal optimization bounds check validation?\na = -5; b = -5; print(a is b)", "True", "False", "SyntaxError compilation flag", "Machine dependent output", "True")
        ]
        cursor.executemany("INSERT INTO questions (room_code, language, level, code, op1, op2, op3, op4, correct) VALUES (?,?,?,?,?,?,?,?,?)", python_exhaustive_quiz)
        
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
    
    # Direct strict room code override to guarantee system backup loading instantly
    if room_code == "SYSTEM":
        cursor.execute("SELECT level, code, op1, op2, op3, op4, correct FROM questions WHERE room_code = 'SYSTEM'")
    else:
        cursor.execute("SELECT level, code, op1, op2, op3, op4, correct FROM questions WHERE room_code = ?", (room_code,))
        
    rows = cursor.fetchall()
    
    if not rows:
        cursor.execute("SELECT level, code, op1, op2, op3, op4, correct FROM questions WHERE room_code = 'SYSTEM'")
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