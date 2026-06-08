<template>
    <div class="max-w-4xl mx-auto my-12 px-4 font-sans text-slate-800">
        <h1 class="text-4xl font-black tracking-tight text-slate-900 mb-2">Terms of Service</h1>
        <p class="text-lg font-bold text-indigo-600 mb-8">
            By using the FastMathFacts engine, you agree to push your limits.
        </p>

        <hr class="border-slate-200 my-6">

        <div class="space-y-8">
            <section>
                <h2 class="text-2xl font-black tracking-tight text-slate-900 mb-3">1. The FastMathFacts Agreement</h2>
                <p class="text-slate-600 leading-relaxed">
                    FastMathFacts is designed to reward grit, determination, and mastery. By accessing this engine, you agree to use it for its intended purpose: actively challenging yourself to improve your mathematical fluency. Coasting on easy equations yields zero points by design.
                </p>
            </section>

            <section>
                <h2 class="text-2xl font-black tracking-tight text-slate-900 mb-3">2. Fair Play & Leaderboard Conduct</h2>
                <p class="text-slate-600 leading-relaxed mb-3">
                    If you choose to opt-in and submit your scores to the Global Leaderboard, you agree to do so honestly. 
                </p>
                <ul class="list-disc list-inside space-y-2 font-medium text-slate-700 pl-2">
                    <li><strong>No Automation:</strong> The use of macros, scripts, bots, or automated key-pressers to artificially inflate your Mastery or Determination scores is strictly prohibited.</li>
                    <li><strong>Respectful Usernames:</strong> When submitting a score, you must use a username or initials that are appropriate for an educational environment. Our backend API actively filters profanity, but deliberately attempting to bypass these filters will result in your device being shadow-banned from the leaderboard.</li>
                </ul>
            </section>

            <section>
                <h2 class="text-2xl font-black tracking-tight text-slate-900 mb-3">3. Data Volatility (Local Storage)</h2>
                <p class="text-slate-600 leading-relaxed mb-3">
                    As outlined in our Privacy Policy, your practice data is stored <strong>locally on your device</strong>, not on our servers. 
                </p>
                <p class="text-slate-600 leading-relaxed">
                    Because we do not force you to create an account, we cannot recover your data if you clear your browser's cache, uninstall your browser, or switch to a new device. You acknowledge that FastMathFacts is not liable for any lost progression, unlocked tiers, or Determination scores.
                </p>
            </section>

            <section>
                <h2 class="text-2xl font-black tracking-tight text-slate-900 mb-3">4. Educational & Personal Use</h2>
                <p class="text-slate-600 leading-relaxed">
                    FastMathFacts is provided free of charge for personal and classroom use. Teachers and educators are highly encouraged to use the engine with their students. However, you may not commercially redistribute, scrape, or repackage the engine or its global leaderboard data behind a paywall without explicit permission.
                </p>
            </section>

            <section>
                <h2 class="text-2xl font-black tracking-tight text-slate-900 mb-3">5. "As Is" Disclaimer</h2>
                <p class="text-slate-600 leading-relaxed">
                    The engine is provided on an "as is" and "as available" basis. While we strive to keep the servers blazing fast and the math engine bug-free, we make no warranties that the service will be uninterrupted, error-free, or completely secure. 
                </p>
            </section>
        </div>

        <div class="mt-12 p-6 bg-slate-50 border border-slate-200 rounded-2xl">
            <p class="text-sm text-slate-500 font-bold text-center">
                Last Updated: June 2026. For privacy inquiries, please review our <router-link to="/privacy-policy/" class="text-indigo-500 hover:text-indigo-600 underline">Privacy Policy</router-link>.
            </p>
        </div>
    </div>
</template>

<script>
export default {
    name: 'TermsView'
}
</script>