from flask import Flask, request, render_template_string
import csv
import os

app = Flask(__name__)

# In-Memory-Benutzerdaten
users = []

# HTML-Template mit Formular und Anzeige
html_template = """
<!doctype html>
<html>
<head>
    <title>Benutzer hinzufügen</title>
</head>
<body>
    <h1>Benutzer hinzufügen</h1>
    <form method="post">
        Name: <input type="text" name="name" required><br>
        E-Mail: <input type="email" name="email" required><br>
        <input type="submit" value="Hinzufügen">
    </form>

    <h2>Benutzerliste:</h2>
    <ul>
        {% for user in users %}
            <li>{{ user.name }} ({{ user.email }})</li>
        {% else %}
            <li>Keine Benutzer vorhanden.</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

# Funktion zum Speichern der Benutzerdaten in eine CSV-Datei mit Debug-Ausgabe
def save_users_to_csv():
    file_path = os.path.join(os.getcwd(), "benutzer.csv")
    print(f"Versuche, die CSV-Datei in folgendem Verzeichnis zu speichern: {file_path}")
    try:
        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["name", "email"])
            writer.writeheader()
            writer.writerows(users)
        print("CSV-Datei wurde erfolgreich geschrieben.")
    except Exception as e:
        print("Fehler beim Schreiben der CSV-Datei:", e)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        if name and email:
            users.append({"name": name, "email": email})
            print("Neuer Benutzer hinzugefügt:", name, email)
            save_users_to_csv()  # CSV-Speichern nach jedem Eintrag
    return render_template_string(html_template, users=users)

if __name__ == "__main__":
    print("Aktuelles Arbeitsverzeichnis:", os.getcwd())
    app.run(debug=False)
