## Code Tracker

> A modern developer productivity web application designed to help developers track their coding journeys, stay consistent, and visualize progress across multiple programming languages through structured roadmaps.

---

### Overview

**Code Tracker** is a full-stack web application built to solve the fragmentation of self-directed learning. By combining predefined learning paths with gamified consistency tracking, it provides developers and students with a centralized hub to monitor milestones, manage daily streaks, and maintain long-term momentum.

---

### Key Features

* **Structured Roadmap System:** Guided, milestone-based learning paths taking users seamlessly from beginner concepts to advanced paradigms.
* **Granular Progress Tracking:** Persistent saving and retrieval of completed topics tailored to individual user accounts.
* **Dynamic Analytics UI:** Real-time circular progress indicators that visually reflect completion percentages instantly.
* **Consistency Streak Engine:** Built-in tracking system designed to encourage daily engagement and combat procrastination.
* **Multi-Language Support:** Out-of-the-box support for popular languages including **Python, Java, C++, and JavaScript**.
* **Secure Authentication:** Basic user credential management separating progress data securely by account.

---

### Technology Stack

| Layer | Technology | Purpose |
| --- | --- | --- |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+) | Responsive UI, dynamic DOM manipulation, and interactive progress widgets |
| **Backend** | Python, Flask, Flask-CORS | Lightweight RESTful routing, middleware management, and request handling |
| **Database** | SQLite | Local relational data persistence for user profiles, roadmaps, and streak logs |

---

### Getting Started & Setup Instructions

To run a local copy of Code Tracker, follow these steps in your terminal:

#### 1. Clone the Repository

```bash
git clone https://github.com/subhranildebnath118-star/CODE-TRACKER.git
cd CODE-TRACKER

```

#### 2. Install Dependencies

Ensure you have Python installed, then install the required backend packages:

```bash
pip install flask flask-cors

```

#### 3. Run the Application

Start the Flask development server:

```bash
python3 app.py

```

#### 4. Access the Platform

Open your browser and navigate to:

```text
http://127.0.0.1:5000

```

---

### Future Roadmap & Enhancements

* **Cloud Deployment:** Migration to production infrastructure using platforms like Render or Railway.
* **Advanced Authentication:** Implementation of industry-standard JWT (JSON Web Tokens) or OAuth2 protocols.
* **Comprehensive Analytics Dashboard:** Weekly/monthly code-time graphs, heatmap calendars, and productivity metrics.
* **AI-Driven Personalization:** Smart roadmap generation and topic recommendations powered by machine learning.
* **Database Scaling:** Transitioning from SQLite to PostgreSQL or MongoDB for high-availability production workloads.

---

### Contributing

Contributions, bug reports, and feature requests are welcome. To contribute:

1. **Fork** the repository.
2. **Create** your feature branch (`git checkout -b feature/AmazingFeature`).
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`).
4. **Push** to the branch (`git push origin feature/AmazingFeature`).
5. Open a **Pull Request**.

---

### License & Acknowledgments

Distributed under the **MIT License**. See `LICENSE` for more information.

* **Author:** Subhranil Debnath
* **Vision:** To make learning programming structured, trackable, and consistent for every student and aspiring developer.
