# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    
    # Tables tabhi banengi agar pehle se nahi hain (Bina drop kiye data safe rahega)
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
    
    # Sirf SYSTEM questions ko safe reload karne ke liye check
    cursor.execute("SELECT COUNT(*) FROM questions WHERE room_code = 'SYSTEM'")
    if cursor.fetchone()[0] == 0:
        ultimate_unique_quiz = [
            # 🐍 PYTHON TIER (5 Puzzles)
            ("SYSTEM", "Python", "Easy", "# REVERSE TRACE CHALLENGE\n# Target Output is:\n# Which replacement for '??' works?", "print([x for x in range(5) if x % 2 == 0])", "print([x*2 for x in range(3)])", "print([x for x in range(6) if x % 2 == 0])", "print(list(range(0, 5, 2)))", "print([x*2 for x in range(3)])"),
            ("SYSTEM", "Python", "Medium", "# BUG HUNTING ARENA\n# Why does this fail for strings?\ndef calc(x):\n    return x + 5.0", "Unsupported operand type", "IndentationError", "NameError", "Works perfectly", "Unsupported operand type"),
            ("SYSTEM", "Python", "Medium", "# REVERSE TRACE CHALLENGE\n# Target Output is: True\n# Select the correct evaluation configuration:", "print(round(2.5) == round(3.5))", "print(0.1 + 0.2 == 0.3)", "print(bool([]))", "print('A' is 'A')", "print(round(2.5) == round(3.5))"),
            ("SYSTEM", "Python", "Hard", "# BUG HUNTING ARENA\n# Identify the dynamic default mutable storage glitch context:", "def add(n, l=[]): l.append(n); return l", "x = 10; def f(): print(x); x = 5", "a = 256; b = 256; print(a is b)", "print(all([]))", "def add(n, l=[]): l.append(n); return l"),
            ("SYSTEM", "Python", "Extreme", "# REVERSE TRACE CHALLENGE\n# Target Output is: True False\n# Which logic maps this vacuous truth behavior?", "print(all([]), any([]))", "print(any([]), all([]))", "print(10 > 5 > 2, bool(''))", "print(type(type) == object, False)", "print(all([]), any([]))"),
            
            # 💛 JAVASCRIPT TIER (5 Puzzles)
            ("SYSTEM", "JavaScript", "Easy", "// REVERSE TRACE CHALLENGE\n// Target Console Output is: 'number'\n// Which code snippet returns this state type?", "console.log(typeof NaN);", "console.log(typeof null);", "console.log(typeof undefined);", "console.log(typeof []);", "console.log(typeof NaN);"),
            ("SYSTEM", "JavaScript", "Medium", "// BUG HUNTING ARENA\n// What will be the final mutated output of this logical paradox?\nconsole.log(true + false + '1');", "'11'", "'101'", "'2'", "NaN", "'11'"),
            ("SYSTEM", "JavaScript", "Medium", "// REVERSE TRACE CHALLENGE\n// Target Output is: true\n// Select the dynamic loose type equivalence:", "console.log([] == ![]);", "console.log(0.1 + 0.2 === 0.3);", "console.log(null === undefined);", "console.log(NaN === NaN);", "console.log([] == ![]);"),
            ("SYSTEM", "JavaScript", "Hard", "// BUG HUNTING ARENA\n// Why does strict equality return false here?\nconsole.log(0.1 + 0.2 === 0.3);", "Binary Floating-Point IEEE 754 precision anomaly", "V8 Engine parsing constraint", "Scope hoisting restriction", "Garbage collection leak", "Binary Floating-Point IEEE 754 precision anomaly"),
            ("SYSTEM", "JavaScript", "Extreme", "// REVERSE TRACE CHALLENGE\n// Target Output is: undefined\n// Which expression references this implicit block state?", "let a; console.log(a);", "console.log(typeof null);", "console.log(NaN);", "console.log(this);", "let a; console.log(a);"),
            
            # 💙 C++ TIER (5 Puzzles)
            ("SYSTEM", "C++", "Easy", "// REVERSE TRACE CHALLENGE\n// Target Output is: 2\n// Select the operation that rounds down integer division:", "int a = 5, b = 2; cout << a / b;", "float a = 5, b = 2; cout << a / b;", "cout << 5 % 2;", "cout << (5 >> 1);", "int a = 5, b = 2; cout << a / b;"),
            ("SYSTEM", "C++", "Medium", "// COMPILER BINDING TRAP\n// What is the behavior of executing nested mutations on standard streams?\ncout << ++x << ' ' << x++;", "Expression sequence evaluation is Compiler Dependent", "Undefined token memory loop", "Immediate Segmentation Fault", "Syntax structural crash", "Expression sequence evaluation is Compiler Dependent"),
            ("SYSTEM", "C++", "Medium", "// REVERSE TRACE CHALLENGE\n// Target Output is: 1\n// Which condition evaluates logical truth representation?", "cout << (10 > 5 && 3 < 4);", "cout << (5 & 2);", "cout << (sizeof(char) == 4);", "cout << (NULL == 1);", "cout << (10 > 5 && 3 < 4);"),
            ("SYSTEM", "C++", "Hard", "// BUG HUNTING / MEMORY PROFILE\n// Why does 'int* ptr = new int; delete ptr;' trigger a leak allocation?", "Missing bracket structure: delete[] ptr;", "Dangling reference assignment mapping", "Stack frame overflow parameters", "Invalid pointer type declaration syntax", "Missing bracket structure: delete[] ptr;"),
            ("SYSTEM", "C++", "Extreme", "// REVERSE TRACE CHALLENGE\n// Target Output is: 4 (on 32-bit architecture systems)\n// Identify the sizing metric trace:", "cout << sizeof(int*);", "cout << sizeof(double);", "cout << sizeof(std::string);", "cout << sizeof(long long);", "cout << sizeof(int*);"),
            
            # ☕ JAVA TIER (5 Puzzles)
            ("SYSTEM", "Java", "Easy", "// REVERSE TRACE CHALLENGE\n// Target Output is: 30Java\n// Select code snippet generating correct precedence concatenation:", "System.out.println(10 + 20 + \"Java\");", "System.out.println(\"Java\" + 10 + 20);", "System.out.println(\"Java\" + (10 + 20));", "System.out.println(10 + \"Java\" + 20);", "System.out.println(10 + 20 + \"Java\");"),
            ("SYSTEM", "Java", "Medium", "// STRING POOL MEMORY MATRIX\n// What is the comparison outcome value of distinct allocation spaces?\nString s1 = \"Hi\"; String s2 = new String(\"Hi\"); System.out.println(s1 == s2);", "false", "true", "NullPointerException", "Compilation Error", "false"),
            ("SYSTEM", "Java", "Medium", "// REVERSE TRACE CHALLENGE\n// Target Output is: true\n// Select reference matching utilizing value comparison protocols:", "System.out.println(s1.equals(s2));", "System.out.println(s1 == s2);", "System.out.println(s1.identityHashCode());", "System.out.println(s1.compareTo(s2) != 0);", "System.out.println(s1.equals(s2));"),
            ("SYSTEM", "Java", "Hard", "// BUG HUNTING ARENA\n// What exception is thrown by trying to modify an unmodifiable list mapping?", "UnsupportedOperationException", "NullPointerException", "IndexOutOfBoundsException", "ClassCastException", "UnsupportedOperationException"),
            ("SYSTEM", "Java", "Extreme", "// REVERSE TRACE CHALLENGE\n// Target Output is: 0\n// Which default primitive initialization state maps this metric vector?", "int[] arr = new int; System.out.println(arr);", "Integer x = null; System.out.println(x);", "char c; System.out.println(c);", "System.out.println(System.identityHashCode(null));", "int[] arr = new int; System.out.println(arr);")
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