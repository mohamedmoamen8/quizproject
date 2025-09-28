# 🎯 Quiz Project

A simple **Quiz Web Application** built with **Flask (Python)** for the backend and **HTML, CSS, JavaScript** for the frontend.  
The app supports **multiple quiz categories**, keeps track of scores, and includes a **leaderboard and ranking system**.
focus in backend and flask (leaderboard- and save the results)
---

## 🚀 Features
- Multiple quiz categories (Science, History, Sports, Movies & TV, General Knowledge, etc.).
- Leaderboard with ranking system.
- Score tracking per user/session.
- Simple and clean UI.
- Flask backend with templates and static files.

---

## 🛠️ Tech Stack
- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (default) – easy to switch to MySQL/PostgreSQL
- **Version Control:** Git & GitHub

---

## 📂 Project Structure

│── instance/ # Configurations & DB files
│── static/ # CSS, JS, images
│── templates/ # HTML templates
│── app.py # Main Flask app
│── requirements.txt # Python dependencies
│── README.md # Project documentation
1. **Clone the repository**
   ```bash
   git clone https://github.com/mohamedmoamen8/quizproject.git
   cd quizproject
Create & activate a virtual environment (recommended)

bash
Copy code
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
Install dependencies

bash
Copy code
pip install -r requirements.txt
Run the app

bash
Copy code
python app.py
Open in browser

cpp
Copy code
http://127.0.0.1:5000 
before log in no leaderboard and see my result
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/80a59d42-4b3d-447c-86c2-826c7a9f1be5" />
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/7d63cc1d-8082-4a9c-8a25-7586c75173e8" />
after
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/316a5786-1ece-442d-8236-b6cce77c665e" />
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/d08a77c3-c322-4d1a-9e88-74250bd90b61" />
<img width="1366" height="768" alt="Screenshot 2025-09-28 160854" src="https://github.com/user-attachments/assets/8cbc4f79-6692-41fb-9a73-4c55020e17dc" />

<img width="1366" height="768" alt="Screenshot 2025-09-28 160907" src="https://github.com/user-attachments/assets/0256e33b-5202-406f-9f65-1c2110352cdc" />


<img width="1366" height="768" alt="Screenshot 2025-09-28 160919" src="https://github.com/user-attachments/assets/e9b59c5a-c83e-4a8c-8f5c-686c8c2b1f40" />
<img width="1366" height="768" alt="Screenshot 2025-09-28 160926" src="https://github.com/user-attachments/assets/8b3b6632-8f37-4f48-9f08-de54df692a65" />

🔮 Future Improvements
improve User authentication (login/signup).

Admin panel to add/manage questions.

Timer per question.

More question types (True/False, Multiple answers, etc.).

REST API for mobile app integration.

 Better UI/UX design( by using react for front e)
