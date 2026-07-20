from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3

quiz = Blueprint("quiz", __name__)


# ==========================
# Database Connection
# ==========================
def get_connection():
    conn = sqlite3.connect("quiz.db")
    conn.row_factory = sqlite3.Row
    return conn


# ==========================
# Create Quiz
# ==========================
@quiz.route("/create_quiz", methods=["GET", "POST"])
def create_quiz():

    if "user" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO quizzes
            (title, description, created_by)
            VALUES (?, ?, ?)
            """,
            (title, description, session["user"])
        )

        conn.commit()
        conn.close()

        return redirect(url_for("quiz.quiz_list"))

    return render_template("create_quiz.html")


# ==========================
# Quiz List
# ==========================
@quiz.route("/quiz_list")
def quiz_list():

    if "user" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM quizzes
        WHERE created_by=?
        ORDER BY id DESC
        """,
        (session["user"],)
    )

    quizzes = cur.fetchall()

    conn.close()

    return render_template(
        "quiz_list.html",
        quizzes=quizzes
    )


# ==========================
# Delete Quiz
# ==========================
@quiz.route("/delete_quiz/<int:quiz_id>")
def delete_quiz(quiz_id):

    if "user" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM questions WHERE quiz_id=?",
        (quiz_id,)
    )

    cur.execute(
        "DELETE FROM quizzes WHERE id=?",
        (quiz_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("quiz.quiz_list"))


# ==========================
# Edit Quiz
# ==========================
@quiz.route("/edit_quiz/<int:quiz_id>", methods=["GET", "POST"])
def edit_quiz(quiz_id):

    if "user" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]

        cur.execute(
            """
            UPDATE quizzes
            SET title=?, description=?
            WHERE id=?
            """,
            (title, description, quiz_id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("quiz.quiz_list"))

    cur.execute(
        "SELECT * FROM quizzes WHERE id=?",
        (quiz_id,)
    )

    quiz_data = cur.fetchone()

    conn.close()

    return render_template(
        "edit_quiz.html",
        quiz=quiz_data
    )
    # ==========================
# Add Question
# ==========================
@quiz.route("/add_question/<int:quiz_id>", methods=["GET", "POST"])
def add_question(quiz_id):

    if "user" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":

        question = request.form["question"]
        option_a = request.form["option_a"]
        option_b = request.form["option_b"]
        option_c = request.form["option_c"]
        option_d = request.form["option_d"]
        correct_answer = request.form["correct_answer"].upper()

        cur.execute(
            """
            INSERT INTO questions
            (
                quiz_id,
                question,
                option_a,
                option_b,
                option_c,
                option_d,
                correct_answer
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                quiz_id,
                question,
                option_a,
                option_b,
                option_c,
                option_d,
                correct_answer
            )
        )

        conn.commit()

        return redirect(url_for("quiz.view_questions", quiz_id=quiz_id))

    conn.close()

    return render_template(
        "add_question.html",
        quiz_id=quiz_id
    )


# ==========================
# View Questions
# ==========================
@quiz.route("/view_questions/<int:quiz_id>")
def view_questions(quiz_id):

    if "user" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM questions
        WHERE quiz_id=?
        ORDER BY id
        """,
        (quiz_id,)
    )

    questions = cur.fetchall()

    conn.close()

    return render_template(
        "view_questions.html",
        questions=questions,
        quiz_id=quiz_id
    )


# ==========================
# Edit Question
# ==========================
@quiz.route("/edit_question/<int:question_id>", methods=["GET", "POST"])
def edit_question(question_id):

    if "user" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":

        question = request.form["question"]
        option_a = request.form["option_a"]
        option_b = request.form["option_b"]
        option_c = request.form["option_c"]
        option_d = request.form["option_d"]
        correct_answer = request.form["correct_answer"].upper()

        cur.execute(
            """
            UPDATE questions
            SET
                question=?,
                option_a=?,
                option_b=?,
                option_c=?,
                option_d=?,
                correct_answer=?
            WHERE id=?
            """,
            (
                question,
                option_a,
                option_b,
                option_c,
                option_d,
                correct_answer,
                question_id
            )
        )

        conn.commit()

        cur.execute(
            "SELECT quiz_id FROM questions WHERE id=?",
            (question_id,)
        )

        quiz_id = cur.fetchone()["quiz_id"]

        conn.close()

        return redirect(
            url_for("quiz.view_questions", quiz_id=quiz_id)
        )

    cur.execute(
        "SELECT * FROM questions WHERE id=?",
        (question_id,)
    )

    question = cur.fetchone()

    conn.close()

    return render_template(
        "edit_question.html",
        question=question
    )


# ==========================
# Delete Question
# ==========================
@quiz.route("/delete_question/<int:question_id>")
def delete_question(question_id):

    if "user" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT quiz_id FROM questions WHERE id=?",
        (question_id,)
    )

    quiz_id = cur.fetchone()["quiz_id"]

    cur.execute(
        "DELETE FROM questions WHERE id=?",
        (question_id,)
    )

    conn.commit()
    conn.close()

    return redirect(
        url_for("quiz.view_questions", quiz_id=quiz_id)
    )
    # ==========================
# Take Quiz (Show All Quizzes)
# ==========================
@quiz.route("/take_quiz")
def take_quiz():

    if "user" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM quizzes
        ORDER BY id DESC
    """)

    quizzes = cur.fetchall()

    conn.close()

    return render_template(
        "take_quiz.html",
        quizzes=quizzes
    )


# ==========================
# Start Quiz
# ==========================
@quiz.route("/start_quiz/<int:quiz_id>")
def start_quiz(quiz_id):

    if "user" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM quizzes WHERE id=?",
        (quiz_id,)
    )
    quiz_data = cur.fetchone()

    cur.execute(
        """
        SELECT *
        FROM questions
        WHERE quiz_id=?
        ORDER BY id
        """,
        (quiz_id,)
    )

    questions = cur.fetchall()

    conn.close()

    if not questions:
        return "<h2>No questions added to this quiz yet.</h2>"

    return render_template(
        "start_quiz.html",
        quiz=quiz_data,
        questions=questions
    )


# ==========================
# Submit Quiz
# ==========================
@quiz.route("/submit_quiz/<int:quiz_id>", methods=["POST"])
def submit_quiz(quiz_id):

    if "user" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM questions
        WHERE quiz_id=?
        ORDER BY id
        """,
        (quiz_id,)
    )

    questions = cur.fetchall()

    score = 0
    review = []

    for q in questions:

        user_answer = request.form.get(f"q{q['id']}")
        correct_answer = q["correct_answer"]

        if user_answer == correct_answer:
            score += 1

        review.append({
            "question": q["question"],
            "your_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": user_answer == correct_answer
        })

    conn.close()

    total = len(questions)

    percentage = 0

    if total > 0:
        percentage = round((score / total) * 100)

    if percentage >= 90:
        performance = "🏆 Excellent"

    elif percentage >= 75:
        performance = "🌟 Very Good"

    elif percentage >= 60:
        performance = "👍 Good"

    elif percentage >= 40:
        performance = "🙂 Average"

    else:
        performance = "📚 Poor"

    return render_template(
        "result.html",
        score=score,
        total=total,
        percentage=percentage,
        performance=performance,
        review=review
    )