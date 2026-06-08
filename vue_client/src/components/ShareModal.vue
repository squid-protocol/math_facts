<template>
    <div v-if="show" @click.self="$emit('close')" class="fixed inset-0 z-[100] bg-slate-900/80 backdrop-blur-sm flex flex-col items-center justify-center p-4">
        <div class="bg-white w-full max-w-md rounded-3xl shadow-2xl overflow-hidden p-8 border-4 border-emerald-500 transition-all duration-300">
            <div class="text-center mb-6">
                <div class="text-6xl mb-4 drop-shadow-md">📥</div>
                <h2 class="text-3xl font-black text-slate-800 mb-2">Card Saved!</h2>
                <p class="text-slate-500 font-bold leading-tight">Your high-res Player Card just downloaded. Pick a platform below and attach your new image to show off your grit!</p>
            </div>

            <div class="space-y-3 mb-6">
                <a :href="'https://twitter.com/intent/tweet?text=' + encodeURIComponent('I just reached Level ' + playerLevel + ' with a Determination score of ' + determinationScore + ' on FastMathFacts! Can you beat my stats? 🧠⚡ #MathFacts')" target="_blank" class="w-full bg-slate-900 hover:bg-slate-800 text-white font-bold py-3 px-4 rounded-xl transition shadow-md flex items-center justify-center gap-3">
                    <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 22.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.008 5.96H5.078z"/></svg>
                    Share on X
                </a>
                
                <a :href="'https://bsky.app/intent/compose?text=' + encodeURIComponent('I just reached Level ' + playerLevel + ' with a Determination score of ' + determinationScore + ' on FastMathFacts! Can you beat my stats? 🧠⚡ #MathFacts')" target="_blank" class="w-full bg-[#1185fe] hover:bg-[#0f75e0] text-white font-bold py-3 px-4 rounded-xl transition shadow-md flex items-center justify-center gap-3">
                    <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M12 10.8c-1.087-2.114-4.046-6.053-6.798-7.995C2.566 1.05 1.343 1.761 1.25 3.324c-.05 1.052.26 4.312.464 5.093 1.036 3.957 4.701 5.034 8.243 4.414-3.527 1.134-7.558 2.05-8.239 6.27-.406 2.507 1.849 3.42 4.49 2.515 2.652-.907 5.437-3.901 5.792-4.301.355.4 3.14 3.394 5.792 4.301 2.64.905 4.896-.008 4.49-2.515-.68-4.22-4.712-5.136-8.239-6.27 3.542.62 7.207-.457 8.243-4.414.204-.781.514-4.041.464-5.093-.093-1.563-1.316-2.274-3.952-.519-2.752 1.942-5.711 5.881-6.798 7.995z"/></svg>
                    Bluesky
                </a>

                <a :href="'https://www.reddit.com/submit?title=' + encodeURIComponent('I just reached Level ' + playerLevel + ' with a Determination score of ' + determinationScore + ' on FastMathFacts! 🧠⚡')" target="_blank" class="w-full bg-[#FF4500] hover:bg-[#e03d00] text-white font-bold py-3 px-4 rounded-xl transition shadow-md flex items-center justify-center gap-3">
                    <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M12.001 22.106c-5.467 0-9.914-3.23-9.914-7.21 0-1.748.814-3.376 2.183-4.66-1.15-1.341-1.848-3.102-1.848-5.02 0-4.084 3.32-7.402 7.402-7.402 2.22 0 4.225.986 5.584 2.545 1.359-1.559 3.363-2.545 5.584-2.545 4.082 0 7.401 3.318 7.401 7.402 0 1.918-.698 3.679-1.848 5.02 1.369 1.284 2.183 2.912 2.183 4.66 0 3.98-4.447 7.21-9.914 7.21zm-4.707-4.65c1.036 0 1.875-.84 1.875-1.875s-.839-1.875-1.875-1.875-1.875.84-1.875 1.875.839 1.875 1.875 1.875zm9.414 0c1.036 0 1.875-.84 1.875-1.875s-.839-1.875-1.875-1.875-1.875.84-1.875 1.875.839 1.875 1.875 1.875zm-4.707 1.875c2.316 0 4.25-1.68 4.25-3.75h-8.5c0 2.07 1.934 3.75 4.25 3.75z"/></svg>
                    Reddit
                </a>
                
                <a href="https://www.facebook.com/sharer/sharer.php" target="_blank" class="w-full bg-[#1877F2] hover:bg-[#166fe5] text-white font-bold py-3 px-4 rounded-xl transition shadow-md flex items-center justify-center gap-3">
                    <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.469h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.469h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                    Share on Facebook
                </a>
                
                <a :href="'https://www.linkedin.com/sharing/share-offsite/?url=' + encodeURIComponent(currentUrl)" target="_blank" class="w-full bg-[#0a66c2] hover:bg-[#084e96] text-white font-bold py-3 px-4 rounded-xl transition shadow-md flex items-center justify-center gap-3">
                    <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                    Share on LinkedIn
                </a>
            </div>

            <button @click="$emit('close')" class="w-full bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold py-3 rounded-xl transition">Got it</button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ShareModal',
    props: {
        show: Boolean,
        playerLevel: Number,
        determinationScore: Number,
        currentUrl: String
    },
    emits: ['close']
}
</script>