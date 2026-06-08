<template>
    <div v-if="show" class="fixed inset-0 z-[100] bg-slate-900/80 backdrop-blur-sm flex flex-col items-center justify-center p-4">
        <div class="bg-white w-full max-w-md rounded-3xl shadow-2xl overflow-hidden p-8 border-4 border-indigo-500 transition-all duration-300">
            
            <template v-if="submissionState === 'success'">
                <div class="text-center py-6 animate-bounce">
                    <div class="text-6xl mb-4 drop-shadow-md">🚀</div>
                    <h2 class="text-3xl font-black text-emerald-500 mb-2">Score Saved!</h2>
                    <p class="text-slate-500 font-bold">Welcome to the leaderboards.</p>
                </div>
            </template>

            <template v-else-if="submissionState === 'error'">
                <div class="text-center py-6">
                    <div class="text-6xl mb-4 drop-shadow-md">⚠️</div>
                    <h2 class="text-3xl font-black text-red-500 mb-2">Network Error</h2>
                    <p class="text-slate-500 font-bold mb-6">Could not reach the server.</p>
                    <button @click="submissionState = 'idle'" class="w-full bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold py-3 rounded-xl transition">Try Again</button>
                </div>
            </template>

            <template v-else>
                <h2 class="text-3xl font-black text-slate-800 mb-2">Submit High Score</h2>
                <p class="text-slate-500 font-bold mb-6">Enter your details to join the global ranking.</p>
                
                <div class="space-y-4 mb-6">
                    <div>
                        <label class="block text-xs font-black text-slate-500 uppercase tracking-wider mb-1">Username / Initials (Required)</label>
                        <input type="text" v-model="leaderboardForm.username" class="w-full bg-slate-100 border-2 border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-800 focus:border-indigo-500 focus:outline-none" placeholder="e.g. MathWizard99">
                    </div>
                    <div>
                        <label class="block text-xs font-black text-slate-500 uppercase tracking-wider mb-1">Age Bracket (Optional)</label>
                        <select v-model="leaderboardForm.ageBracket" class="w-full bg-slate-100 border-2 border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-800 focus:border-indigo-500 focus:outline-none appearance-none">
                            <option value="">Select Age...</option>
                            <option value="under_10">Under 10</option>
                            <option value="10_13">10 to 13</option>
                            <option value="14_17">14 to 17</option>
                            <option value="18_19">18 to 19</option>
                            <option value="20_29">20 to 29</option>
                            <option value="30_39">30 to 39</option>
                            <option value="40_49">40 to 49</option>
                            <option value="50_59">50 to 59</option>
                            <option value="60_69">60 to 69</option>
                            <option value="70_79">70 to 79</option>
                            <option value="80_plus">80+</option>
                        </select>
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-xs font-black text-slate-500 uppercase tracking-wider mb-1">Country</label>
                            <select v-model="leaderboardForm.country" :disabled="isFetchingGeo" class="w-full bg-slate-100 border-2 border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-800 focus:border-indigo-500 focus:outline-none appearance-none disabled:opacity-50">
                                <option value="">{{ isFetchingGeo ? 'Loading Planet...' : 'Select Country...' }}</option>
                                <option v-for="c in globalCountries" :key="c.code2" :value="c.code2">{{ c.name }}</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs font-black text-slate-500 uppercase tracking-wider mb-1">State / Province</label>
                            <select v-model="leaderboardForm.state" :disabled="!leaderboardForm.country || availableRegions.length === 0" class="w-full bg-slate-100 border-2 border-slate-200 rounded-xl px-4 py-3 font-bold text-slate-800 focus:border-indigo-500 focus:outline-none appearance-none disabled:opacity-50 disabled:bg-slate-50">
                                <option value="">{{ availableRegions.length > 0 ? 'Select Region...' : 'N/A' }}</option>
                                <option v-for="r in availableRegions" :key="r.code" :value="r.code">{{ r.name }}</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div class="flex items-center gap-3 mb-8 bg-slate-50 p-3 rounded-xl border border-slate-200">
                    <input type="checkbox" id="consent" v-model="leaderboardForm.consentToTrack" class="w-5 h-5 accent-indigo-600 rounded cursor-pointer shrink-0">
                    <label for="consent" class="text-xs font-bold text-slate-600 leading-tight cursor-pointer">Remember this device to track my long-term growth across sessions.</label>
                </div>

                <div class="flex gap-3">
                    <button @click="closeModal" :disabled="submissionState === 'submitting'" class="flex-1 bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold py-3 rounded-xl transition">Cancel</button>
                    <button @click="submitLeaderboard" :disabled="!leaderboardForm.username || submissionState === 'submitting'" class="flex-1 bg-indigo-600 hover:bg-indigo-500 disabled:bg-indigo-300 text-white font-bold py-3 rounded-xl transition shadow-md flex justify-center items-center">
                        <span v-if="submissionState === 'submitting'" class="animate-pulse">Sending...</span>
                        <span v-else>Submit Score</span>
                    </button>
                </div>
            </template>

        </div>
    </div>
</template>

<script>
export default {
    name: 'LeaderboardModal',
    props: {
        show: Boolean,
        activeModule: String,
        history: Array,
        determinationScore: Number,
        masteryScore: Number,
        playerLevel: Number,
        sessionStartTime: Number,
        initialPlayerLevel: Number,
        initialMasteryScore: Number,
        initialDetermination: Number
    },
    emits: ['close'],
    data() {
        return {
            submissionState: 'idle', 
            leaderboardForm: { username: '', ageBracket: '', country: '', state: '', consentToTrack: false },
            globalCountries: [],
            availableRegions: [],
            isFetchingGeo: false
        }
    },
    watch: {
        show(isOpen) {
            if (isOpen && this.globalCountries.length === 0) {
                this.isFetchingGeo = true;
                fetch('https://raw.githubusercontent.com/stefanbinder/countries-states/master/countries.json')
                    .then(res => res.json())
                    .then(data => {
                        this.globalCountries = data;
                        this.isFetchingGeo = false;
                    })
                    .catch(err => {
                        console.error('Failed to load global geography', err);
                        this.isFetchingGeo = false;
                    });
            }
        },
        'leaderboardForm.country'(newCode) {
            this.leaderboardForm.state = '';
            const country = this.globalCountries.find(c => c.code2 === newCode);
            this.availableRegions = country && country.states ? country.states : [];
        }
    },
    methods: {
        closeModal() {
            this.$emit('close');
        },
        async submitLeaderboard() {
            if (!this.leaderboardForm.username) return;

            const totalAttempts = this.history.length;
            const correctCount = this.history.filter(a => a.isCorrect).length;
            const sessionAccuracy = totalAttempts > 0 ? Math.round((correctCount / totalAttempts) * 100) : 0;

            let deviceId = localStorage.getItem('fastMathDeviceId');

            if (this.leaderboardForm.consentToTrack) {
                if (!deviceId) {
                    deviceId = crypto.randomUUID();
                    localStorage.setItem('fastMathDeviceId', deviceId);
                }
            } else {
                deviceId = null;
                localStorage.removeItem('fastMathDeviceId');
            }

            const payload = {
                device_id: deviceId,
                username: this.leaderboardForm.username,
                module_type: this.activeModule, 
                age_bracket: this.leaderboardForm.ageBracket || null,
                country: this.leaderboardForm.country || null,
                state: this.leaderboardForm.state || null,
                determination_score: this.determinationScore,
                mastery_score: this.masteryScore,
                player_level: this.playerLevel,
                session_duration_seconds: Math.floor((Date.now() - this.sessionStartTime) / 1000),
                total_questions_answered: totalAttempts,
                session_accuracy_percent: sessionAccuracy,
                levels_gained: this.playerLevel - this.initialPlayerLevel,
                mastery_gained: this.masteryScore - this.initialMasteryScore,
                determination_gained: this.determinationScore - this.initialDetermination
            };

            this.submissionState = 'submitting';

            try {
                await fetch('/api/leaderboard/submit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                
                this.submissionState = 'success';
                
                setTimeout(() => {
                    this.submissionState = 'idle';
                    this.closeModal();
                }, 2000);

            } catch (error) {
                this.submissionState = 'error';
                console.error(error);
            }
        }
    }
}
</script>