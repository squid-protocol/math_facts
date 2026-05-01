# Math Facts Tracker

A fast-paced, data-driven web application designed to help children master addition and multiplication facts through rapid testing and gamified metrics. 

## The Problem
Many existing math fact applications suffer from slow transitions, unnecessary animations, and rigid testing structures that frustrate learners. Furthermore, their progress tracking is often binary (pass/fail) or lacks the granularity needed to show incremental improvement. 

## The Solution
This application was built to eliminate wait times and provide instant, summative feedback. It treats math fluency like a video game—rewarding speed and accuracy with a granular "Mastery Level" system. No matter where a student is in their learning journey, the system highlights micro-progress to keep them motivated, while showing high performers exactly where they can shave off milliseconds.

## Key Features

* **Zero-Friction Practice:** The interface is designed for rapid-fire input. There are no "loading" screens between questions; the moment an answer is submitted, the next question appears. 
* **Student-Specific Profiles:** The application uses a configuration dictionary to tailor the experience to individual learners.
    * **Lola (Multiplication):** Tests factors 0-12. Features an interactive heatmap visualizing the fastest time for every single coordinate pair (e.g., 7x8), allowing students to hover and see a line graph of their speed improvements over time.
    * **Rosalyn (Addition):** Tests double-digit plus single-digit addition. Features a visual hundreds chart and tracks streaks, accuracy percentages, and average speeds grouped by the "bottom number" to identify specific stumbling blocks.
* **Gamified Micro-Leveling:** Instead of standard grades, the system converts response times and correct answers into "Experience Points." This fills a visual thermometer, translating raw data into a "Level" that rewards any progress, no matter how small. 
* **SQLite Database:** All attempts, including the exact millisecond duration of the answer, are logged locally for robust data analysis. 
* **Data Visualization:** Built with Plotly.js, the progress dashboards provide interactive heatmaps, line charts, and histograms to visualize accuracy and speed.

## Project Structure
```text
.
├── math_app.py                      # Main Flask application and database logic
├── math_facts.db                    # SQLite database (generated on first run)
├── static/
│   ├── css/
│   │   └── style.css                # Application styling
│   └── images/
│       └── hundreds-number-chart.jpg # Helper image for addition practice
└── templates/
    ├── addition_progress.html       # Rosalyn's specific dashboard
    ├── index.html                   # Student selection screen
    ├── layout.html                  # Base HTML template with Plotly.js integration
    ├── multiplication_progress.html # Lola's specific dashboard
    ├── practice.html                # Rapid-fire testing interface
    ├── progress.html                # Legacy combined progress template
    └── start.html                   # Session initiation screen
```

## Setup & Installation

1.  **Prerequisites:** Ensure you have Python 3 installed.
2.  **Dependencies:** Install Flask.
    ```bash
    pip install Flask
    ```
3.  **Run the Application:**
    ```bash
    python math_app.py
    ```
4.  **Access:** Open a web browser and navigate to `http://localhost:5000`. The SQLite database (`math_facts.db`) will be created automatically upon the first run. 

## Configuration
To add a new student or change parameters, edit the `STUDENTS_CONFIG` dictionary at the top of `math_app.py`. 
```python
STUDENTS_CONFIG = {
    "StudentName": {
        "operation": "multiplication", # or "addition"
        "symbol": "×", 
        "range1": (0, 12),             # Range for the top number
        "range2": (0, 12)              # Range for the bottom number
    }
}
```