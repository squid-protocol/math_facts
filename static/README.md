# Math Facts Tracker: UI Templates

This directory contains the user interface templates for the Math Facts Tracker application. The front-end relies on **Jinja2** templating via Flask to inject dynamic data (like math problems, usernames, and progress metrics) into the HTML structure.

The interface is intentionally minimalist. It eschews distracting animations or "gamified" avatars in favor of rapid, frictionless data entry and clean, interactive data visualization using Plotly.js.

## Template Overview

### Core Structure
* **`layout.html`:** The foundational template. It handles the inclusion of CSS (`style.css`), Google Fonts (Poppins and Roboto Mono), and the CDN link for `Plotly.js` (v2.32.0). It also manages the display of flashed error/success messages. All other templates extend this file.
* **`index.html`:** The landing page. It dynamically generates a selection button for each student defined in the backend `STUDENTS_CONFIG`.

### The Testing Interface
* **`practice.html`:** The engine of the application. This page is built for speed.
    * **Zero-Wait Design:** It uses a hidden form submission and an on-screen keypad to allow children to punch in answers instantly.
    * **Conditional Layouts:** It dynamically changes the layout based on the student's needs.
        * **Rosalyn's Layout (Addition):** Displays questions vertically (traditional stacked format) and includes a visual "Hundreds Number Chart" as a learning aid.
        * **Lola's Layout (Multiplication):** Displays questions horizontally in a standard equation format.
    * *Note: This interface intentionally prevents standard keyboard input (using `readonly onfocus="this.blur()"`) on mobile/tablets to stop native virtual keyboards from popping up and obstructing the custom keypad.*

### The Progress Dashboards
The application utilizes separate dashboards to handle the unique metrics tracked for different mathematical operations.

* **`addition_progress.html` (Rosalyn's Dashboard):** Focuses on accuracy, streaks, and "bottom number" analysis.
    * **Heatmaps:** Uses Plotly to render a heatmap showing the total correct answers across different numerical categories (e.g., adding a single digit to a number in the 20s, 30s, etc.).
    * **Summary Charts:** Displays two separate heatmaps visualizing overall accuracy percentage and trimmed average speed grouped by the bottom number, helping identify specific trouble spots (e.g., "struggles when adding 8").
* **`multiplication_progress.html` (Lola's Dashboard):** Focuses on highly granular speed tracking across a traditional times table grid.
    * **The Detail Grid:** A massive interactive heatmap where the X and Y axes represent the factors (0-12). The color intensity of each cell represents the *fastest* time achieved for that specific problem.
    * **Interactive Line Graph:** When a user hovers over a cell in the heatmap (e.g., 7x8), Plotly dynamically renders a line graph to the right, plotting the history of their attempt times for that specific problem, providing a visual narrative of their improvement.

### Legacy/Utility Templates
* **`progress.html`:** An older, combined progress template that attempted to handle both heatmap logic and standard table views. This is largely superseded by the specialized operation dashboards.
* **`start.html`:** A legacy template originally used to initiate 5-minute timed sessions. The application has since transitioned to a continuous, zero-friction testing model, making this template inactive but retained for architectural history.