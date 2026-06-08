<template>
    <div class="max-w-7xl w-full grid grid-cols-1 lg:grid-cols-12 gap-8 items-start relative">
      
        <div id="calculator-box" class="relative bg-white rounded-3xl shadow-xl overflow-hidden border border-indigo-100 flex flex-col lg:col-span-5 sticky top-6">

            <Teleport to="#navbar-module-slot" v-if="isMounted">
                <div class="flex items-center gap-2 sm:gap-3">
                    <select :value="activeModule" @change="switchModule($event.target.value)" class="bg-slate-800 hover:bg-slate-700 text-slate-100 text-[10px] sm:text-[11px] uppercase tracking-widest font-black px-2 sm:px-3 py-2 rounded-lg cursor-pointer border border-slate-600 focus:outline-none transition-colors shadow-sm outline-none">
                        <option value="multiplication">Multiplication (×)</option>
                        <option value="division">Division (÷)</option>
                        <option value="addition">Addition (+)</option>
                        <option value="subtraction">Subtraction (-)</option>
                    </select>
                    
                    <div class="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 px-2 sm:px-3 py-2 rounded-lg border border-slate-600 transition-colors shadow-sm cursor-pointer">
                        <input type="checkbox" id="nav-negatives" v-model="allowNegatives" @change="saveData(); generateQuestion()" class="w-3.5 h-3.5 sm:w-4 sm:h-4 accent-indigo-500 rounded cursor-pointer shrink-0">
                        <label for="nav-negatives" class="text-[10px] sm:text-[11px] uppercase tracking-widest font-black text-slate-200 cursor-pointer select-none hidden sm:block">Negatives (-)</label>
                        <label for="nav-negatives" class="text-[10px] sm:text-[11px] uppercase tracking-widest font-black text-slate-200 cursor-pointer select-none sm:hidden">(-)</label>
                    </div>
                </div>
            </Teleport>

            <div v-if="isPaused" @click.stop="resumeGame" class="absolute inset-0 z-50 bg-slate-900 flex flex-col items-center justify-center cursor-pointer">
                <div class="bg-white p-8 rounded-2xl shadow-2xl text-center transform transition-transform hover:scale-105 border-4 border-slate-700">
                    <div class="text-5xl mb-4">⏸️</div>
                    <h3 class="text-2xl font-black text-slate-800 mb-2">Game Paused</h3>
                    <p v-if="wasIdle" class="text-amber-600 font-bold mb-2">Idle timeout: timer reset.</p>
                    <p class="text-slate-500 font-bold">Click here to resume</p>
                </div>
            </div>

            <div v-if="showAddPlayerModal" class="absolute inset-0 z-[100] bg-slate-900/80 backdrop-blur-sm flex flex-col items-center justify-center p-4 rounded-3xl">
                <div class="bg-white w-full max-w-sm rounded-3xl shadow-2xl overflow-hidden p-8 border-4 border-indigo-500 transform transition-all">
                    <h3 class="text-2xl font-black text-slate-800 mb-2">New Player</h3>
                    <p class="text-sm font-bold text-slate-500 mb-6">Enter your name or initials to track your personal growth.</p>
                    
                    <input type="text" v-model="newProfileName" 
                           @input="newProfileName = newProfileName.replace(/[^a-zA-Z0-9_-]/g, '').slice(0, 15)"
                           @keyup.enter="confirmAddPlayer"
                           placeholder="e.g. MathWizard" 
                           class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-4 font-black text-slate-800 focus:border-indigo-500 focus:outline-none mb-2 text-xl text-center shadow-inner">
                    <p class="text-[10px] text-slate-400 font-bold mb-8 text-center uppercase tracking-widest">Max 15 chars. Letters & numbers only.</p>
                    
                    <div class="flex gap-3">
                        <button @click="showAddPlayerModal = false; newProfileName = ''" class="flex-1 bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold py-3 rounded-xl transition">Cancel</button>
                        <button @click="confirmAddPlayer" :disabled="!newProfileName" class="flex-1 bg-indigo-600 hover:bg-indigo-500 disabled:bg-indigo-300 text-white font-bold py-3 rounded-xl transition shadow-md">Add Player</button>
                    </div>
                </div>
            </div>

            <div v-if="showProfileDropdown" @click="showProfileDropdown = false" class="fixed inset-0 z-40"></div>

             <div class="bg-indigo-600 p-6 text-white border-b border-indigo-700 relative">
                <div class="flex justify-between items-start mb-6">
                    
                    <div class="relative z-50">
                        <span class="block text-[10px] font-black uppercase tracking-widest text-indigo-300 mb-1">Practice Engine</span>
                        
                        <button @click="showProfileDropdown = !showProfileDropdown" class="flex items-center gap-2 group focus:outline-none">
                            <h1 class="text-4xl md:text-5xl font-black tracking-tight text-white group-hover:text-indigo-100 transition drop-shadow-sm">
                                {{ activeProfile }}
                            </h1>
                            <svg class="w-8 h-8 text-indigo-300 group-hover:text-white transition transform" :class="{'rotate-180': showProfileDropdown}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="4" d="M19 9l-7 7-7-7"></path></svg>
                        </button>
                        
                        <div v-if="showProfileDropdown" class="absolute left-0 top-full mt-3 w-64 bg-white rounded-2xl shadow-2xl overflow-hidden border border-slate-100 origin-top-left transform transition-all">
                            <div class="p-3 bg-slate-50 border-b border-slate-100">
                                <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest px-2">Switch Player</span>
                            </div>
                            <div class="max-h-60 overflow-y-auto">
                                <button @click="selectProfile('Guest'); showProfileDropdown = false" class="w-full text-left px-5 py-3 font-bold text-slate-600 hover:bg-indigo-50 hover:text-indigo-600 transition border-b border-slate-50 flex justify-between items-center">
                                    Guest Player
                                    <span v-if="'Guest' === activeProfile" class="text-indigo-500">✓</span>
                                </button>
                                <button v-for="p in profiles" :key="p" @click="selectProfile(p); showProfileDropdown = false" class="w-full text-left px-5 py-3 font-bold text-slate-800 hover:bg-indigo-50 hover:text-indigo-600 transition border-b border-slate-50 flex justify-between items-center">
                                    {{ p }}
                                    <span v-if="p === activeProfile" class="text-indigo-500 font-black">✓</span>
                                </button>
                            </div>
                            <div class="p-3 bg-slate-50 border-t border-slate-100">
                                <button @click="showProfileDropdown = false; showAddPlayerModal = true" class="w-full bg-indigo-100 hover:bg-indigo-200 text-indigo-700 font-black py-2.5 rounded-xl transition text-sm flex items-center justify-center gap-2 shadow-sm">
                                    <span class="text-lg leading-none">+</span> Add New Player
                                </button>
                            </div>
                        </div>
                    </div>

                    <div class="flex gap-2 mt-1 relative z-50">
                        <button v-if="currentView === 'game'" @click="currentView = 'settings'" class="text-sm bg-indigo-500 hover:bg-indigo-400 px-4 py-2 rounded-full font-bold transition shadow-sm flex items-center gap-2">
                            ⚙️ <span class="hidden sm:inline">Settings</span>
                        </button>
                        <button v-if="currentView === 'settings'" @click="currentView = 'game'" class="text-sm bg-emerald-500 hover:bg-emerald-400 px-4 py-2 rounded-full font-black transition shadow-md flex items-center gap-2">
                            ▶️ <span class="hidden sm:inline">Resume</span>
                        </button>
                    </div>
                </div>
                
                <div class="grid grid-cols-4 gap-2 bg-indigo-900/40 rounded-xl p-3 border border-indigo-500/30 shadow-inner">
                    <div class="text-center border-r border-indigo-500/30">
                        <span class="block text-[9px] font-black uppercase tracking-widest text-indigo-300">Level</span>
                        <span class="font-bold text-amber-400 text-lg leading-none">{{ playerLevel }}</span>
                    </div>
                    <div class="text-center border-r border-indigo-500/30">
                        <span class="block text-[9px] font-black uppercase tracking-widest text-indigo-300">Avg Speed</span>
                        <span class="font-mono font-bold text-lg leading-none" :class="(recentSpeed <= targetSpeed) ? 'text-emerald-400' : 'text-yellow-400'">{{ recentSpeed }}s</span>
                    </div>
                    <div class="text-center border-r border-indigo-500/30">
                        <span class="block text-[9px] font-black uppercase tracking-widest text-indigo-300">Accuracy</span>
                        <span class="font-mono font-bold text-white text-lg leading-none">{{ recentAccuracy }}%</span>
                    </div>
                    <div class="text-center">
                        <span class="block text-[9px] font-black uppercase tracking-widest text-indigo-300">Mode</span>
                        <span class="font-bold text-white capitalize text-xs leading-none mt-1 inline-block">{{ gameMode }}</span>
                    </div>
                </div>
            </div>

            <div v-if="currentView === 'settings'" class="p-6 flex-grow overflow-y-auto">
                <h2 class="text-xl font-bold text-slate-800 mb-4">Game Mode</h2>
                <div class="grid grid-cols-1 gap-2 mb-8">
                    <button @click="gameMode = 'campaign'; saveData(); generateQuestion()" :class="gameMode === 'campaign' ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-indigo-50'" class="font-bold py-3 rounded-xl text-sm transition flex justify-between px-4 shadow-sm">
                        <span>🏆 Campaign</span>
                        <span class="font-normal opacity-75">Infinite progression</span>
                    </button>
                    <button @click="gameMode = 'weak'; saveData(); generateQuestion()" :class="gameMode === 'weak' ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-indigo-50'" class="font-bold py-3 rounded-xl text-sm transition flex justify-between px-4 shadow-sm">
                        <span>🎯 Weak Spots</span>
                        <span class="font-normal opacity-75">Target slow squares</span>
                    </button>
                    <button @click="gameMode = 'total'; saveData(); generateQuestion()" :class="gameMode === 'total' ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-indigo-50'" class="font-bold py-3 rounded-xl text-sm transition flex justify-between px-4 shadow-sm">
                        <span>🌍 Total Test</span>
                        <span class="font-normal opacity-75">Random 0-12 (No progression)</span>
                    </button>
                </div>

                <h2 class="text-xl font-bold text-slate-800 mb-4">Mastery Thresholds</h2>
                
                <div class="space-y-6 mb-8">
                    <div>
                        <div class="flex justify-between mb-1">
                            <label class="font-bold text-slate-700 text-sm">Target Speed</label>
                            <span class="font-mono text-indigo-600 font-bold">{{ targetSpeed }}s</span>
                        </div>
                        <input type="range" v-model.number="targetSpeed" @change="saveData" min="1.0" max="8.0" step="0.5" class="w-full accent-indigo-600">
                    </div>

                    <div>
                        <div class="flex justify-between mb-1">
                            <label class="font-bold text-slate-700 text-sm">Target Accuracy</label>
                            <span class="font-mono text-indigo-600 font-bold">{{ targetAccuracy }}%</span>
                        </div>
                        <input type="range" v-model.number="targetAccuracy" @change="saveData" min="50" max="100" step="5" class="w-full accent-indigo-600">
                    </div>
                    
                    <div>
                        <div class="flex justify-between mb-1">
                            <label class="font-bold text-slate-700 text-sm">Base Evaluation Window</label>
                            <span class="font-mono text-indigo-600 font-bold">{{ windowSize }}</span>
                        </div>
                        <input type="range" v-model.number="windowSize" @change="saveData" min="5" max="30" step="1" class="w-full accent-indigo-600">
                    </div>
                </div>

                <div class="border-t border-slate-200 pt-6 mt-6 space-y-3">
                    <button @click="logoutProfile" class="w-full bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold py-3 rounded-xl transition">
                        Switch Player Profile
                    </button>
                    <button @click="resetProgress" class="w-full bg-red-50 hover:bg-red-100 text-red-600 font-bold py-3 rounded-xl transition">
                        Reset All Data (Start Over)
                    </button>
                </div>
            </div>

            <div v-if="currentView === 'game'" class="p-6 flex-grow flex flex-col justify-center">
                <div v-if="justUnlocked" class="animate-rainbow p-4 rounded-xl text-center font-black mb-6 shadow-lg transform transition-transform animate-bounce">
                    🎉 LEVEL UP! You unlocked the {{ justUnlocked }}s! 🎉
                </div>

                <div class="text-center mb-8 relative">
                    <div class="text-7xl font-black text-slate-800 tracking-tighter mb-6 drop-shadow-sm">
                        <template v-if="!isPaused">
                            {{ currentQuestion.displayString }}
                        </template>
                        <template v-else>
                            <span class="text-slate-300">?</span> 
                            <span class="text-indigo-200">{{ activeModule === 'addition' ? '+' : (activeModule === 'subtraction' ? '-' : (activeModule === 'division' ? '÷' : '×')) }}</span> 
                            <span class="text-slate-300">?</span>
                        </template>
                    </div>
                    
                    <input type="text" v-model="userAnswer" readonly :class="{'shake border-red-500 text-red-500': isWrong}"
                           class="w-full text-center text-5xl font-black py-4 rounded-2xl bg-slate-50 border-4 border-slate-200 focus:outline-none transition-colors duration-200 shadow-inner"
                           placeholder="?">
                           
                    <div v-if="feedback" class="absolute inset-0 flex items-center justify-center bg-white/90 backdrop-blur-sm rounded-2xl z-10">
                        <div class="text-center transform scale-150 transition-transform">
                            <div v-if="feedback.isCorrect" class="text-emerald-500 text-6xl drop-shadow-md">⭐</div>
                            <div v-else class="text-red-500 text-6xl drop-shadow-md">❌</div>
                            <div class="font-bold mt-2" :class="feedback.isCorrect ? 'text-emerald-600' : 'text-red-600'">
                                {{ feedback.message }}
                            </div>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-3 gap-3">
                    <button v-for="n in 9" :key="n" @click="appendNumber(n)" 
                            class="keypad-btn bg-slate-100 hover:bg-slate-200 text-slate-700 text-3xl font-black py-5 rounded-2xl shadow-sm border-b-4 border-slate-200 transition-all">
                        {{ n }}
                    </button>
                    
                    <button @click="appendNumber('-')" 
                            class="keypad-btn bg-slate-100 hover:bg-slate-200 text-slate-700 text-3xl font-black py-5 rounded-2xl shadow-sm border-b-4 border-slate-200 transition-all">
                        (-)
                    </button>
                    <button @click="appendNumber(0)" 
                            class="keypad-btn bg-slate-100 hover:bg-slate-200 text-slate-700 text-3xl font-black py-5 rounded-2xl shadow-sm border-b-4 border-slate-200 transition-all">
                        0
                    </button>
                    <button @click="clearAnswer" 
                            class="keypad-btn bg-red-50 hover:bg-red-100 text-red-500 text-xl font-bold py-5 rounded-2xl shadow-sm border-b-4 border-red-200 transition-all">
                        Clear
                    </button>
                    
                    <button @click="submitAnswer" 
                            class="col-span-3 keypad-btn bg-emerald-500 hover:bg-emerald-600 text-white text-3xl font-black py-5 rounded-2xl shadow-md border-b-4 border-emerald-700 transition-all">
                        Go
                    </button>
                </div>
            </div>

        </div>

        <MasteryDashboard 
          :determinationScore="determinationScore"
          :masteryScore="masteryScore"
          :playerLevel="playerLevel"
          :isSharing="isSharing"
          :gridColumns="gridColumns"
          :unlockedNumbers="unlockedNumbers"
          :bestPairStatsMap="bestPairStatsMap"
          :lastAnswered="lastAnswered"
          :activeModule="activeModule"
          :tierDistribution="tierDistribution"
          :maxTierCount="maxTierCount"
          :history="history"
          @open-leaderboard="openLeaderboard"
          @share-stats="shareStats"
        />

        <LeaderboardModal 
          :show="showLeaderboardModal"
          :activeModule="activeModule"
          :history="history"
          :determinationScore="determinationScore"
          :masteryScore="masteryScore"
          :playerLevel="playerLevel"
          :sessionStartTime="sessionStartTime"
          :initialPlayerLevel="initialPlayerLevel"
          :initialMasteryScore="initialMasteryScore"
          :initialDetermination="initialDetermination"
          @close="showLeaderboardModal = false; resumeGame()"
        />

        <ShareModal 
          :show="showShareModal"
          :playerLevel="playerLevel"
          :determinationScore="determinationScore"
          :currentUrl="currentUrl"
          @close="showShareModal = false; resumeGame()"
        />

    </div>
</template>

<script>
import MasteryDashboard from '../components/MasteryDashboard.vue';
import LeaderboardModal from '../components/LeaderboardModal.vue';
import ShareModal from '../components/ShareModal.vue';
import { QuestionFactory } from '../QuestionFactory.js';
import * as htmlToImage from 'html-to-image';

export default {
    name: 'GameView',
    components: {
        MasteryDashboard,
        LeaderboardModal,
        ShareModal
    },
    data() {
        return {
            isMounted: false,
            unlockSequence: [[7], [8], [9], [10], [11], [12]],
            unlockedNumbers: [0, 1, 2, 3, 4, 5, 6],
            
            currentQuestion: { num1: 0, num2: 0, displayString: '', correctAnswer: 0, trackingKey: '' },
            userAnswer: '',
            accumulatedTimeMs: 0,
            currentSegmentStartTime: 0,
            history: [], 
            determinationScore: 0,
            
            lastAnswered: { num1: null, num2: null, isCorrect: null, trigger: 0 },
            
            isPaused: false,
            wasIdle: false, 
            idleTimeout: null,
            
            feedback: null,
            isWrong: false,
            justUnlocked: null,
            currentView: 'game',

            profiles: [],
            activeProfile: 'Guest',
            showProfileDropdown: false,
            showAddPlayerModal: false,
            newProfileName: '',

            // Modals & Telemetry State
            showLeaderboardModal: false,
            showShareModal: false,
            isSharing: false,
            deviceId: null,

            sessionStartTime: Date.now(),
            initialMasteryScore: 0,
            initialPlayerLevel: 0,
            initialDetermination: 0,

            gameMode: 'campaign',
            targetSpeed: 3.5,
            targetAccuracy: 90,
            windowSize: 10, 
            activeModule: 'multiplication',
            allowNegatives: false,
        }
    },
    computed: {
        currentUrl() { return window.location.origin; },

        maxGridNumber() { return Math.max(...this.unlockedNumbers, 5); },
        
        gridColumns() {
            const maxLen = Math.max(13, this.maxGridNumber + 1);
            return Array.from({length: maxLen}, (_, i) => i); 
        },

        bestPairStatsMap() {
            const pairHistory = {};
            for (const att of this.history) {
                const min = Math.min(att.num1, att.num2);
                const max = Math.max(att.num1, att.num2);
                const key = this.activeModule === 'addition' ? `add_${min}+${max}` : (this.activeModule === 'subtraction' ? `sub_${max}-${min}` : (this.activeModule === 'division' ? `div_${min}/${max}` : `${min}x${max}`));
                if (!pairHistory[key]) pairHistory[key] = [];
                pairHistory[key].push(att);
            }

            const bestStats = {};
            for (const key in pairHistory) {
                const attempts = pairHistory[key];
                let bestSpeed = Infinity;
                let bestAccuracy = 0;

                if (attempts.length <= 5) {
                    const totalSpeed = attempts.reduce((sum, a) => sum + a.timeSeconds, 0);
                    const correctCount = attempts.filter(a => a.isCorrect).length;
                    bestSpeed = totalSpeed / attempts.length;
                    bestAccuracy = (correctCount / attempts.length) * 100;
                } else {
                    for (let i = 0; i <= attempts.length - 5; i++) {
                        const window = attempts.slice(i, i + 5);
                        const totalSpeed = window.reduce((sum, a) => sum + a.timeSeconds, 0);
                        const correctCount = window.filter(a => a.isCorrect).length;
                        const avgSpeed = totalSpeed / 5;
                        const accuracy = (correctCount / 5) * 100;

                        if (avgSpeed < bestSpeed) {
                            bestSpeed = avgSpeed;
                            bestAccuracy = accuracy;
                        }
                    }
                }
                bestStats[key] = {
                    attempts: attempts.length,
                    speed: bestSpeed.toFixed(1),
                    accuracy: Math.round(bestAccuracy)
                };
            }
            return bestStats;
        },

        tierDistribution() {
            const tiers = [
                { id: 'pink', label: '0.25s', colorClass: 'bg-gradient-to-br from-pink-400 to-pink-600 animate-metal-pulse', count: 0 },
                { id: 'purple', label: '0.5s', colorClass: 'bg-gradient-to-br from-purple-400 to-purple-600 animate-metal-pulse', count: 0 },
                { id: 'indigo', label: '0.75s', colorClass: 'bg-gradient-to-br from-indigo-400 to-indigo-600 animate-metal-pulse', count: 0 },
                { id: 'blue', label: '1s', colorClass: 'bg-gradient-to-br from-blue-400 to-blue-600 animate-metal-pulse', count: 0 },
                { id: 'cyan', label: '2s', colorClass: 'bg-cyan-500', count: 0 },
                { id: 'teal', label: '3s', colorClass: 'bg-teal-500', count: 0 },
                { id: 'emerald', label: '4s', colorClass: 'bg-emerald-500', count: 0 },
                { id: 'green', label: '5s', colorClass: 'bg-green-500', count: 0 },
                { id: 'yellow', label: '6s', colorClass: 'bg-yellow-400', count: 0 },
                { id: 'orange', label: '8s', colorClass: 'bg-orange-500', count: 0 },
                { id: 'red', label: '8s+', colorClass: 'bg-red-600', count: 0 }
            ];

            const countedKeys = new Set();
            for (const row of this.unlockedNumbers) {
                for (const col of this.gridColumns) {
                    const min = Math.min(row, col);
                    const max = Math.max(row, col);
                    const key = this.activeModule === 'addition' ? `add_${min}+${max}` : (this.activeModule === 'subtraction' ? `sub_${max}-${min}` : (this.activeModule === 'division' ? `div_${min}/${max}` : `${min}x${max}`));
                    
                    if (!countedKeys.has(key)) {
                        countedKeys.add(key);
                        const stat = this.bestPairStatsMap[key];
                        if (stat && stat.attempts > 0) {
                            const speed = parseFloat(stat.speed);
                            if (speed <= 0.25) tiers[0].count++;
                            else if (speed <= 0.50) tiers[1].count++;
                            else if (speed <= 0.75) tiers[2].count++;
                            else if (speed <= 1.00) tiers[3].count++;
                            else if (speed <= 2.0) tiers[4].count++;
                            else if (speed <= 3.0) tiers[5].count++;
                            else if (speed <= 4.0) tiers[6].count++;
                            else if (speed <= 5.0) tiers[7].count++;
                            else if (speed <= 6.0) tiers[8].count++;
                            else if (speed <= 8.0) tiers[9].count++;
                            else tiers[10].count++;
                        }
                    }
                }
            }
            return tiers;
        },

        maxTierCount() {
            const maxCount = Math.max(...this.tierDistribution.map(t => t.count));
            return Math.max(maxCount, 5); 
        },

        masteryScore() {
            let score = 0;
            const countedKeys = new Set();
            for (const row of this.unlockedNumbers) {
                for (const col of this.gridColumns) {
                    const min = Math.min(row, col);
                    const max = Math.max(row, col);
                    const key = this.activeModule === 'addition' ? `add_${min}+${max}` : (this.activeModule === 'subtraction' ? `sub_${max}-${min}` : (this.activeModule === 'division' ? `div_${min}/${max}` : `${min}x${max}`));
                    
                    if (!countedKeys.has(key)) {
                        countedKeys.add(key);
                        const stat = this.bestPairStatsMap[key];
                        if (stat && stat.attempts > 0) {
                            const speed = parseFloat(stat.speed);
                            if (speed <= 0.25) score += 1000;
                            else if (speed <= 0.50) score += 500;
                            else if (speed <= 0.75) score += 250;
                            else if (speed <= 1.00) score += 100;
                            else if (speed <= 2.0) score += 50;
                            else if (speed <= 3.0) score += 25;
                            else if (speed <= 4.0) score += 15;
                            else if (speed <= 5.0) score += 10;
                            else if (speed <= 6.0) score += 5;
                            else if (speed <= 8.0) score += 2;
                            else score += 1;
                        }
                    }
                }
            }
            return score;
        },

        playerLevel() { return Math.max(...this.unlockedNumbers); },

        dynamicWindowSize() {
            const base = this.windowSize || 10;
            const extra = (this.unlockedNumbers.length - 7) * 5;
            return Math.min(50, base + Math.max(0, extra));
        },

        recentAttempts() { return this.history.slice(-this.dynamicWindowSize); },
        recentSpeed() {
            if (this.recentAttempts.length === 0) return 0.00;
            const totalTime = this.recentAttempts.reduce((sum, att) => sum + att.timeSeconds, 0);
            return (totalTime / this.recentAttempts.length).toFixed(1);
        },
        recentAccuracy() {
            if (this.recentAttempts.length === 0) return 0;
            const correctCount = this.recentAttempts.filter(att => att.isCorrect).length;
            return Math.round((correctCount / this.recentAttempts.length) * 100);
        }
    },
    methods: {
        switchModule(newModule) {
            this.saveData(); 
            this.activeModule = newModule;
            localStorage.setItem(`fastMathLastModule_${this.activeProfile}`, newModule);
            
            this.history = [];
            this.unlockedNumbers = [0, 1, 2, 3, 4, 5, 6];
            this.unlockSequence = [[7], [8], [9], [10], [11], [12]];
            this.determinationScore = 0;

            this.loadData();
            this.generateQuestion();
        },

        confirmAddPlayer() {
            const cleanName = this.newProfileName.trim().replace(/[^a-zA-Z0-9_-]/g, '').slice(0, 15);
            if (cleanName && cleanName !== 'Guest') {
                if (!this.profiles.includes(cleanName)) {
                    this.profiles.push(cleanName);
                    localStorage.setItem('fastMathProfiles', JSON.stringify(this.profiles));
                }
                this.selectProfile(cleanName);
            }
            this.showAddPlayerModal = false;
            this.newProfileName = '';
        },

        selectProfile(name) {
            this.activeProfile = name;
            localStorage.setItem('fastMathLastProfile', name);
            
            const lastMod = localStorage.getItem(`fastMathLastModule_${name}`);
            this.activeModule = lastMod ? lastMod : 'multiplication';
            
            this.history = [];
            this.unlockedNumbers = [0, 1, 2, 3, 4, 5, 6];
            this.unlockSequence = [[7], [8], [9], [10], [11], [12]];
            this.determinationScore = 0;
            
            this.loadData();
            
            this.initialMasteryScore = this.masteryScore;
            this.initialPlayerLevel = this.playerLevel;
            this.initialDetermination = this.determinationScore;
            
            this.generateQuestion();
        },

        async shareStats() {
            if (this.isSharing) return;
            this.isSharing = true;
            this.pauseGame();

            try {
                const element = document.getElementById('mastery-dashboard-card');
                if (!element) return;

                const blob = await htmlToImage.toBlob(element, {
                    pixelRatio: 2, 
                    backgroundColor: '#ffffff',
                    skipFonts: true
                });

                const file = new File([blob], 'math-mastery.png', { type: 'image/png' });

                if (navigator.share && navigator.canShare && navigator.canShare({ files: [file] })) {
                    try {
                        await navigator.share({
                            title: 'My FastMathFacts Mastery!',
                            text: `I've reached Level ${this.playerLevel} with a Determination score of ${this.determinationScore}! Can you beat my math stats?`,
                            files: [file]
                        });
                    } catch (err) {
                        console.log('Share canceled or failed', err);
                    }
                } else {
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'FastMath-Mastery.png';
                    a.click();
                    URL.revokeObjectURL(url);
                    
                    this.showShareModal = true;
                }
                this.isSharing = false;
            } catch (err) {
                console.error("Failed to capture image", err);
                this.isSharing = false;
            }
        },

        openLeaderboard() {
            this.showLeaderboardModal = true;
            this.pauseGame();
        },

        loadData() {
            if (!this.activeProfile || !this.activeModule) return;
            
            const prefix = `math_${this.activeProfile}_${this.activeModule}_`;

            const savedHistory = localStorage.getItem(prefix + 'history');
            const savedUnlocks = localStorage.getItem(prefix + 'unlocked');
            const savedSettings = localStorage.getItem(prefix + 'settings');
            const savedDetermination = localStorage.getItem(prefix + 'determination');
            const savedSequence = localStorage.getItem(prefix + 'unlockSequence');
            
            if (savedHistory) this.history = JSON.parse(savedHistory);
            if (savedDetermination) this.determinationScore = parseInt(savedDetermination);
            if (savedSequence) this.unlockSequence = JSON.parse(savedSequence);
            if (savedUnlocks) {
                const loaded = JSON.parse(savedUnlocks);
                this.unlockedNumbers = [...new Set(loaded)].sort((a, b) => a - b);
            }
            if (savedSettings) {
                const settings = JSON.parse(savedSettings);
                this.targetSpeed = settings.targetSpeed || 3.5;
                this.targetAccuracy = settings.targetAccuracy || 90;
                this.windowSize = settings.windowSize || 10;
                this.gameMode = settings.gameMode || 'campaign';
                this.allowNegatives = settings.allowNegatives || false;
            }
        },
        
        saveData() {
            if (!this.activeProfile || !this.activeModule) return;
            const prefix = `math_${this.activeProfile}_${this.activeModule}_`;

            localStorage.setItem(prefix + 'history', JSON.stringify(this.history));
            localStorage.setItem(prefix + 'unlocked', JSON.stringify(this.unlockedNumbers));
            localStorage.setItem(prefix + 'determination', this.determinationScore.toString());
            localStorage.setItem(prefix + 'unlockSequence', JSON.stringify(this.unlockSequence));
            localStorage.setItem(prefix + 'settings', JSON.stringify({
                targetSpeed: this.targetSpeed,
                targetAccuracy: this.targetAccuracy,
                windowSize: this.windowSize,
                gameMode: this.gameMode,
                allowNegatives: this.allowNegatives
            }));
        },

        resetProgress() {
            if(confirm(`Are you sure you want to delete all saved data for ${this.activeProfile}? This cannot be undone.`)) {
                const prefix = `math_${this.activeProfile}_${this.activeModule}_`;
                localStorage.removeItem(prefix + 'history');
                localStorage.removeItem(prefix + 'unlocked');
                localStorage.removeItem(prefix + 'determination');
                localStorage.removeItem(prefix + 'unlockSequence');
                localStorage.removeItem(prefix + 'settings');
                
                this.history = [];
                this.determinationScore = 0;
                this.unlockedNumbers = [0, 1, 2, 3, 4, 5, 6];
                this.unlockSequence = [[7], [8], [9], [10], [11], [12]];
                this.generateQuestion();
                this.currentView = 'game';
            }
        },
        
        getWeakSpots() {
            const weak = [];
            const recentPairStats = {};
            for (const att of this.recentAttempts) {
                const min = Math.min(att.num1, att.num2);
                const max = Math.max(att.num1, att.num2);
                const key = this.activeModule === 'addition' ? `add_${min}+${max}` : (this.activeModule === 'subtraction' ? `sub_${max}-${min}` : (this.activeModule === 'division' ? `div_${min}/${max}` : `${min}x${max}`));
                if (!recentPairStats[key]) recentPairStats[key] = { attempts: 0, correct: 0, totalTime: 0 };
                recentPairStats[key].attempts++;
                if (att.isCorrect) recentPairStats[key].correct++;
                recentPairStats[key].totalTime += att.timeSeconds;
            }

            for (const key in recentPairStats) {
                const s = recentPairStats[key];
                const accuracy = (s.correct / s.attempts) * 100;
                const avgSpeed = s.totalTime / s.attempts;
                
                if (accuracy < this.targetAccuracy || avgSpeed > this.targetSpeed) {
                    let n1, n2;
                    if (key.startsWith('add_')) {
                        [n1, n2] = key.replace('add_', '').split('+').map(Number);
                    } else if (key.startsWith('sub_')) {
                        [n1, n2] = key.replace('sub_', '').split('-').map(Number);
                    } else if (key.startsWith('div_')) {
                        [n1, n2] = key.replace('div_', '').split('/').map(Number);
                    } else {
                        [n1, n2] = key.split('x').map(Number);
                    }
                    weak.push([n1, n2]);
                }
            }
            return weak;
        },

        getUntestedPairs() {
            const untested = [];
            for (const n1 of this.unlockedNumbers) {
                for (const n2 of this.unlockedNumbers) {
                    const min = Math.min(n1, n2);
                    const max = Math.max(n1, n2);
                    const key = this.activeModule === 'addition' ? `add_${min}+${max}` : (this.activeModule === 'subtraction' ? `sub_${max}-${min}` : (this.activeModule === 'division' ? `div_${min}/${max}` : `${min}x${max}`));
                    if (!this.bestPairStatsMap[key] || this.bestPairStatsMap[key].attempts === 0) {
                        untested.push([n1, n2]);
                    }
                }
            }
            return untested;
        },

        evaluateProgression() {
            if (this.recentAttempts.length < this.dynamicWindowSize) return;

            const untested = this.getUntestedPairs();
            if (untested.length > 0) return;

            if (this.recentSpeed <= this.targetSpeed && this.recentAccuracy >= this.targetAccuracy) {
                let nextUnlock;
                
                if (this.unlockSequence.length > 0) {
                    nextUnlock = this.unlockSequence.shift(); 
                } else {
                    const currentHighest = Math.max(...this.unlockedNumbers);
                    nextUnlock = [currentHighest + 1];
                }

                const combined = [...this.unlockedNumbers, ...nextUnlock];
                this.unlockedNumbers = [...new Set(combined)].sort((a, b) => a - b);
                
                this.justUnlocked = nextUnlock.join(' & ');
                this.saveData(); 
                
                setTimeout(() => { this.justUnlocked = null; }, 5000);
            }
        },
        
        generateQuestion() {
            this.resetIdleTimer();

            const context = {
                gameMode: this.gameMode,
                gridColumns: this.gridColumns,
                weakSpots: this.getWeakSpots(),
                untestedPairs: this.getUntestedPairs(),
                unlockedNumbers: this.unlockedNumbers
            };

            const activeModuleConfig = {
                type: this.activeModule,
                allowNegatives: this.allowNegatives
            };

            const question = QuestionFactory.create(activeModuleConfig, context);
            
            this.currentQuestion.num1 = question.num1;
            this.currentQuestion.num2 = question.num2;
            this.currentQuestion.displayString = question.displayString;
            this.currentQuestion.correctAnswer = question.correctAnswer;
            this.currentQuestion.trackingKey = question.trackingKey;
            
            this.userAnswer = '';
            this.feedback = null;
            this.isWrong = false;
            this.accumulatedTimeMs = 0;
            this.currentSegmentStartTime = performance.now();
            this.isPaused = false;
        },
        
        resetIdleTimer() {
            clearTimeout(this.idleTimeout);
            if (this.currentView === 'game' && !this.isPaused) {
                this.idleTimeout = setTimeout(() => {
                    this.wasIdle = true;
                    this.pauseGame(true);
                }, 15000); 
            }
        },
        pauseGame(isIdle = false) {
            if (this.isPaused || this.currentView !== 'game' || this.feedback) return;
            clearTimeout(this.idleTimeout);
            this.accumulatedTimeMs += (performance.now() - this.currentSegmentStartTime);
            this.isPaused = true;
        },
        resumeGame() {
            if (!this.isPaused) return;
            if (this.wasIdle) {
                this.accumulatedTimeMs = 0; 
                this.wasIdle = false;
            }
            this.currentSegmentStartTime = performance.now();
            this.isPaused = false;
            this.resetIdleTimer();
        },
        handleGlobalClick(event) {
            if (this.currentView !== 'game' || this.isPaused) return;
            const calcBox = document.getElementById('calculator-box');
            if (calcBox && !calcBox.contains(event.target)) {
                this.pauseGame();
            }
        },
        appendNumber(num) {
            this.resetIdleTimer();
            if (num === '-') {
                if (!this.userAnswer.includes('-')) {
                    this.userAnswer = '-' + this.userAnswer;
                } else {
                    this.userAnswer = this.userAnswer.replace('-', '');
                }
                return;
            }
            if (this.userAnswer.length < 5) {
                this.userAnswer += num.toString();
            }
        },
        clearAnswer() {
            this.resetIdleTimer();
            this.userAnswer = '';
        },

        submitAnswer() {
            if (this.userAnswer === '') return;
            clearTimeout(this.idleTimeout);

            const totalTimeMs = this.accumulatedTimeMs + (performance.now() - this.currentSegmentStartTime);
            const timeTakenSeconds = (totalTimeMs / 1000).toFixed(2);
            
            const correctAnswer = this.currentQuestion.correctAnswer;
            const isCorrect = parseInt(this.userAnswer) === correctAnswer;

            const key = this.currentQuestion.trackingKey;
            
            const oldStat = this.bestPairStatsMap[key];
            const oldBestSpeed = (oldStat && oldStat.attempts > 0) ? parseFloat(oldStat.speed) : 10.0;

            this.history.push({
                num1: this.currentQuestion.num1,
                num2: this.currentQuestion.num2,
                isCorrect: isCorrect,
                timeSeconds: parseFloat(timeTakenSeconds),
                timestamp: new Date().toISOString()
            });
            
            const newStat = this.bestPairStatsMap[key];
            const newBestSpeed = (newStat && newStat.attempts > 0) ? parseFloat(newStat.speed) : 10.0;

            let pointsEarned = 0;
            
            if (newBestSpeed < oldBestSpeed) {
                const improvement = oldBestSpeed - newBestSpeed;
                pointsEarned += Math.round(improvement * 50); 
            }

            if (oldBestSpeed > this.targetSpeed) {
                pointsEarned += isCorrect ? 10 : 5;
            }

            this.determinationScore += pointsEarned;
            
            const answeredNum1 = this.currentQuestion.num1;
            const answeredNum2 = this.currentQuestion.num2;

            this.lastAnswered.trigger = 0; 
            
            setTimeout(() => {
                this.lastAnswered = {
                    num1: answeredNum1,
                    num2: answeredNum2,
                    isCorrect: isCorrect,
                    trigger: Date.now()
                };
            }, 50);
            
            setTimeout(() => {
                if (this.lastAnswered) this.lastAnswered.trigger = 0;
            }, 4000);

            this.saveData();
            
            if (this.gameMode === 'campaign') {
                this.evaluateProgression(); 
            }

            if (isCorrect) {
                this.feedback = { isCorrect: true, message: `${timeTakenSeconds}s` };
                setTimeout(() => { this.generateQuestion(); }, 600);
            } else {
                this.isWrong = true;
                this.feedback = { isCorrect: false, message: correctAnswer };
                setTimeout(() => { this.generateQuestion(); }, 1500);
            }
        },
        handleKeydown(event) {
            if (this.currentView !== 'game') return;
            if (this.isPaused) {
                this.resumeGame();
                return;
            }
            if (event.key >= '0' && event.key <= '9') {
                this.appendNumber(parseInt(event.key));
            } else if (event.key === '-') {
                this.appendNumber('-');
            } else if (event.key === 'Enter') {
                this.submitAnswer();
            } else if (event.key === 'Backspace') {
                this.resetIdleTimer();
                this.userAnswer = this.userAnswer.slice(0, -1);
            } else if (event.key === 'Escape' || event.key === 'Delete') {
                this.clearAnswer();
            }
        }
    },
    mounted() {
        this.isMounted = true;
        
        const savedProfiles = localStorage.getItem('fastMathProfiles');
        if (savedProfiles) this.profiles = JSON.parse(savedProfiles);

        const lastProfile = localStorage.getItem('fastMathLastProfile');
        this.activeProfile = lastProfile && (this.profiles.includes(lastProfile) || lastProfile === 'Guest') ? lastProfile : 'Guest';
        
        this.selectProfile(this.activeProfile);

        this.deviceId = localStorage.getItem('fastMathDeviceId');
        window.addEventListener('keydown', this.handleKeydown);
        window.addEventListener('click', this.handleGlobalClick);
        window.addEventListener('blur', () => this.pauseGame(false)); 
    },
    unmounted() {
        window.removeEventListener('keydown', this.handleKeydown);
        window.removeEventListener('click', this.handleGlobalClick);
        window.removeEventListener('blur', () => this.pauseGame(false));
        clearTimeout(this.idleTimeout);
    }
}
</script>