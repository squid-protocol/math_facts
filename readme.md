# FastMathFacts Engine

FastMathFacts is a gamified math practice engine designed to reward both mastery and gritty determination. 

Currently migrating from a legacy Django multi-page application to a decoupled, reactive Single Page Application (SPA).

## Core Architecture

* **Frontend:** Vue 3 (Composition API/Options API) + Tailwind CSS via CDN.
* **State Management:** Reactive local state coupled with `localStorage` for offline persistence.
* **Rendering:** Hardware-accelerated CSS animations (`transform`, `opacity`, `filter`) to maintain 60fps during intense gamification loops.

## Gamification Systems

The engine mathematically separates natural talent from hard work using two distinct scoring mechanisms:

### 1. Mastery Score (Perfection)
An exponentially scaling score that rewards students for achieving blisteringly fast response times on specific math facts. 
* Uses a High-Watermark system: once a time tier is achieved, it is permanently locked in.
* Tiers progress from ROYGBIV colors into Precious Metals (Bronze, Silver, Gold, Platinum).
* Platinum squares (< 0.25s) yield 1,000x more points than Red squares (> 8s).

### 2. Determination Score (Grit)
A dynamically scaling experience pool that rewards effort over raw intelligence.
* **The "Easy" Penalty:** Answering a previously mastered question yields 0 points.
* **The Grind Bonus:** Actively practicing historical weak spots grants bonus points.
* **The Breakthrough Multiplier:** Shaving fractions of a second off a personal best average yields massive point injections.

## Game Modes

* **Campaign (Infinite):** Dynamically scales the grid as the student proves mastery. Automatically stretches the rolling average evaluation window to prevent score tanking as the grid grows.
* **Weak Spots:** An algorithmic mode that specifically targets coordinate pairs where the student's historical speed or accuracy falls below the target threshold.
* **Total Test:** A true random test across the entire currently unlocked grid.

## Anti-Cheat & Analytics

* **Idle Catcher:** If the user abandons a problem for more than 15 seconds, the engine automatically pauses and drops the current timer to protect their rolling average from contamination.
* **Reactive Feedback:** The engine physically prevents the CSS animations from caching, ensuring visual dopamine hits (Arcade shifts, massive glows) fire flawlessly on every successful interaction.

## Next Steps / Roadmap

1. **Backend Integration:** Wire up a Django API to sync the `localStorage` state to a PostgreSQL/SQLite database to allow cross-device progression.
2. **Profile Management:** Implement multi-user selection to isolate sibling progression on shared devices.
3. **Build Pipeline:** Migrate the monolithic `index.html` into a Vite-powered Vue build pipeline for better componentization.