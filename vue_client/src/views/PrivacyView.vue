<template>
    <div class="max-w-4xl mx-auto my-12 px-4 font-sans text-slate-800">
        <h1 class="text-4xl font-black tracking-tight text-slate-900 mb-2">Privacy Policy</h1>
        <p class="text-lg font-bold text-indigo-600 mb-8">
            Privacy by Default. Local Isolation. No personal data ever leaves your device unless you ask it to.
        </p>

        <hr class="border-slate-200 my-6">

        <div class="space-y-8">
            <section>
                <h2 class="text-2xl font-black tracking-tight text-slate-900 mb-3">1. Local Isolation (How Your Data is Stored)</h2>
                <p class="text-slate-600 leading-relaxed mb-3">
                    FastMathFacts is built using a "Thick Client" architecture. This means the entire math engine runs directly inside your web browser. 
                </p>
                <p class="text-slate-600 leading-relaxed">
                    By default, <strong>all of your training records, speed profiles, determination scores, and progression levels are saved locally on your device</strong> using standard HTML5 Local Storage. Under normal operation, your practice data never communicates with our servers, and we have zero visibility into your individual progress.
                </p>
            </section>

            <section>
                <h2 class="text-2xl font-black tracking-tight text-slate-900 mb-3">2. Educational Compliance (COPPA, FERPA & GDPR)</h2>
                <p class="text-slate-600 leading-relaxed mb-3">
                    Because of our local-first architecture, FastMathFacts is inherently compliant with strict international and educational data standards, including the <strong>General Data Protection Regulation (GDPR)</strong>, the <strong>Children's Online Privacy Protection Act (COPPA)</strong>, and the <strong>Family Educational Rights and Privacy Act (FERPA)</strong>.
                </p>
                <ul class="list-disc list-inside space-y-2 font-medium text-slate-700 pl-2">
                    <li>We do not require user accounts, passwords, or email addresses to use the practice engine.</li>
                    <li>We do not collect or store Personally Identifiable Information (PII).</li>
                    <li>We do not use third-party advertising trackers or sell data to data brokers.</li>
                </ul>
            </section>

            <section>
                <h2 class="text-2xl font-black tracking-tight text-slate-900 mb-3">3. The Global Leaderboard (100% Opt-In)</h2>
                <p class="text-slate-600 leading-relaxed mb-3">
                    Submitting your scores to the Global Leaderboard is <strong>strictly optional</strong>. If you choose to benchmark your progress against the world, we ask that you use a custom username, nickname, or initials to maintain total identity protection.
                </p>
                <p class="text-slate-600 leading-relaxed">
                    When you submit a score to the dashboard, we transmit the following anonymized payload to our server:
                </p>
                <ul class="list-disc list-inside space-y-2 font-medium text-slate-700 pl-2 mt-3">
                    <li>Your chosen username/initials.</li>
                    <li>Your broad demographic selections (Age Bracket and Geographic Region), if provided.</li>
                    <li>Your current math scores (Mastery, Determination, Level, and Session Accuracy).</li>
                    <li>An anonymized, randomly-generated Device ID (only if you check the "Remember this device" box, allowing you to track your own growth across multiple sessions).</li>
                </ul>
            </section>

            <section>
                <h2 class="text-2xl font-black tracking-tight text-slate-900 mb-3">4. Telemetry and Educational Efficacy</h2>
                <p class="text-slate-600 leading-relaxed">
                    We periodically analyze macro-level, anonymized system benchmarks from our leaderboard (e.g., identifying which math facts take generalized age groups the longest to master). This high-level telemetry data contains no individual profile tracking and serves entirely to boost the educational value of the engine and refine our teaching algorithms over time.
                </p>
            </section>
        </div>

        <div class="mt-12 p-6 bg-slate-50 border border-slate-200 rounded-2xl">
            <p class="text-sm text-slate-500 font-bold text-center">
                Last Updated: June 2026. For terms of use, please review our <router-link to="/terms/" class="text-indigo-500 hover:text-indigo-600 underline">Terms of Service</router-link>.
            </p>
        </div>
    </div>
</template>

<script>
export default {
    name: 'PrivacyView'
}
</script>