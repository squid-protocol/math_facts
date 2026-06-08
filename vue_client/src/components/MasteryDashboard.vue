<template>
    <div id="mastery-dashboard-card" class="bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-200 flex flex-col lg:col-span-7">
        <div class="relative z-50 bg-slate-800 p-6 text-white flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
                <div class="flex items-center gap-3">
                    <h2 class="text-2xl font-black tracking-tight">Your Growth</h2>
                    <button @click="$emit('open-leaderboard')" class="bg-indigo-500 hover:bg-indigo-400 text-white text-xs font-black uppercase tracking-wider px-4 py-2 rounded-lg shadow-sm transition transform hover:scale-105">
                        Submit to Leaderboard
                    </button>
                </div>
            </div>
            <div class="flex gap-4">
                <div class="group relative bg-slate-900 border border-slate-700 rounded-xl p-3 text-right shadow-inner transform transition-transform hover:scale-105 cursor-default">
                    <span class="font-bold text-slate-400 text-[10px] block -mb-1 tracking-widest uppercase">Determination</span>
                    <span class="font-mono font-black text-amber-400 text-3xl drop-shadow-md">{{ determinationScore }}</span>
                    
                    <div class="absolute top-full right-0 mt-2 hidden group-hover:block w-64 bg-slate-800 text-white text-sm font-bold p-4 rounded-lg shadow-xl z-50 text-left border border-slate-600">
                        Earned by practicing new and hard-for-you questions only. Correct answers on easy-for-you problems count for nothing here. This measures how hard you pushed yourself to get to your mastery level. 
                    </div>
                </div>
                <div class="group relative bg-indigo-900 border border-indigo-700 rounded-xl p-3 text-right shadow-inner transform transition-transform hover:scale-105 cursor-default">
                    <span class="font-bold text-indigo-300 text-[10px] block -mb-1 tracking-widest uppercase">Mastery</span>
                    <span class="font-mono font-black text-emerald-400 text-3xl drop-shadow-md">{{ masteryScore }}</span>
                    
                    <div class="absolute top-full right-0 mt-2 hidden group-hover:block w-64 bg-indigo-950 text-white text-sm font-bold p-4 rounded-lg shadow-xl z-50 text-left border border-indigo-600">
                        Earned by mastery. This number grows when you answer correctly and faster than you have before. 
                    </div>
                </div>
            </div>
        </div>

        <div class="p-6 flex flex-col gap-10">
            <div data-html2canvas-ignore="true" class="bg-gradient-to-r from-emerald-50 to-teal-50 border-2 border-emerald-200 rounded-2xl p-5 flex flex-col sm:flex-row justify-between items-center gap-4 shadow-sm relative overflow-hidden">
                <div class="relative z-10">
                    <h3 class="text-xl font-black text-slate-800 flex items-center gap-2 mb-1">
                        Share Your Growth
                    </h3>
                    <p class="text-sm font-bold text-slate-600">Share these stats with your network</p>
                </div>
                <button @click="$emit('share-stats')" :disabled="isSharing" class="w-full sm:w-auto relative z-10 bg-emerald-500 hover:bg-emerald-400 disabled:bg-emerald-300 text-white font-black py-3 px-6 rounded-xl transition shadow-md flex items-center justify-center gap-2 transform hover:scale-105">
                    <span v-if="isSharing" class="animate-pulse">Capturing Image...</span>
                    <span v-else>Generate & Share</span>
                </button>
                <div class="absolute -right-10 -top-10 text-9xl opacity-5 pointer-events-none">🏆</div>
            </div>
            
            <div>
                <h3 class="text-lg font-bold text-slate-700 mb-4 flex items-center gap-2">
                    <span>🗺️</span> Mastery Map
                </h3>
                <div class="w-full flex justify-center overflow-x-auto pb-4">
                    <div class="inline-flex flex-col gap-0.5">
                        <div class="flex gap-0.5">
                            <div :class="headerSizeClass" class="shrink-0 transition-all duration-500"></div> 
                            <div v-for="col in gridColumns" :key="'header-'+col" 
                                 class="flex items-center justify-center font-bold text-slate-400 text-sm md:text-base shrink-0 transition-all duration-500"
                                 :class="headerSizeClass">
                                {{ col }}
                            </div>
                        </div>
                        
                        <div v-for="row in unlockedNumbers" :key="'row-'+row" class="flex gap-0.5">
                            <div class="flex items-center justify-center font-black text-slate-500 bg-slate-50 text-sm md:text-base rounded-sm shrink-0 transition-all duration-500"
                                 :class="headerSizeClass">
                                {{ row }}
                            </div>
                            
                            <div v-for="col in gridColumns" :key="row+'x'+col" 
                                 :class="[
                                    getSpeedColorClass(getPairStats(row, col).speed, getPairStats(row, col).attempts), 
                                    cellSizeClass,
                                    isLastAnsweredPair(row, col) ? (lastAnswered.isCorrect ? 'animate-glow-gold' : 'animate-glow-red') : ''
                                 ]"
                                 class="relative group rounded-sm flex flex-col items-center justify-center shadow-sm transition-colors duration-200 border border-black/5 shrink-0 cursor-pointer">
                                
                                <template v-if="!isGridMassive && getPairStats(row, col).attempts > 0">
                                    <span class="font-black leading-none mt-0.5 drop-shadow-sm text-sm sm:text-base">{{ getPairStats(row, col).speed }}s</span>
                                </template>
                                <template v-else-if="!isGridMassive">
                                    <span class="text-black/20 text-sm font-bold">-</span>
                                </template>

                                <div v-if="getPairStats(row, col).attempts > 0" 
                                     class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:flex flex-col items-center bg-slate-800 text-white rounded-lg py-2 px-3 z-50 whitespace-nowrap shadow-xl">
                                    <span class="font-bold text-sm text-indigo-300 mb-1">{{ row }} {{ activeModule === 'addition' ? '+' : (activeModule === 'subtraction' ? '-' : (activeModule === 'division' ? '÷' : '×')) }} {{ col }}</span>
                                    <span class="text-base font-black">{{ getPairStats(row, col).speed }}s</span>
                                    <span class="text-xs font-bold text-slate-300 mt-1">{{ getPairStats(row, col).accuracy }}% Accuracy</span>
                                    <div class="absolute top-full left-1/2 -translate-x-1/2 border-[5px] border-transparent border-t-slate-800"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div>
                <h3 class="text-lg font-bold text-slate-700 mb-4 flex items-center gap-2">
                    <span>📊</span> Time Mastery Thresholds
                </h3>
                
                <div class="bg-slate-50 border border-slate-200 p-4 pt-6 rounded-2xl relative shadow-inner">
                    <div class="relative z-10 flex gap-1 justify-around h-32 items-end">
                        <div v-for="tier in tierDistribution" :key="tier.id" class="flex flex-col items-center flex-1 group h-full justify-end">
                            <div class="w-full rounded-t-md transition-all duration-500 shadow-sm opacity-90 flex items-start justify-center pt-1 border border-b-0 border-white/20 relative" 
                                 :class="tier.colorClass"
                                 :style="{ height: Math.max(5, (tier.count / maxTierCount) * 100) + '%' }">
                                 <span v-if="tier.count > 0" class="text-xs sm:text-sm font-black text-slate-700 absolute -top-6 bg-white/90 px-1.5 py-0.5 rounded-sm shadow-sm">{{ tier.count }}</span>
                            </div>
                            <span class="text-xs sm:text-sm font-bold text-slate-500 mt-2 whitespace-nowrap">{{ tier.label }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <div>
                <h3 class="text-lg font-bold text-slate-700 mb-4 flex items-center gap-2">
                    <span>⚡</span> Best Average by Number
                </h3>
                
                <div class="bg-slate-50 border border-slate-200 p-4 pt-6 rounded-2xl relative shadow-inner overflow-hidden">
                    <div class="absolute left-4 right-4 top-6 h-32 flex flex-col justify-between z-0 pointer-events-none">
                        <div v-for="sec in [8, 7, 6, 5, 4, 3, 2, 1, 0]" :key="'line-'+sec" 
                             :class="sec === 0 ? 'border-slate-400' : 'border-slate-300/60'" 
                             class="border-t relative">
                            <span class="absolute -top-3 bg-slate-50 pr-1 text-xs font-bold text-slate-400">{{ sec }}s</span>
                        </div>
                    </div>

                    <div class="relative z-10 flex gap-1 sm:gap-2 justify-around pl-6">
                        <div v-for="num in gridColumns" :key="'bar-'+num" class="flex flex-col items-center flex-1">
                            <div class="w-full h-32 flex items-end relative group">
                                <div class="w-full rounded-t-md transition-all duration-500 opacity-90 shadow-sm border border-b-0 border-white/20" 
                                     :class="[
                                        getSpeedColorClass(getBestNumberAvgSpeed(num), getBestNumberAvgSpeed(num) > 0 ? 1 : 0),
                                        isLastAnsweredBar(num) ? (lastAnswered.isCorrect ? 'animate-glow-gold' : 'animate-glow-red') : ''
                                     ]"
                                     :style="{ height: getBarHeight(num) + '%' }"></div>
                                     
                                <div v-if="getBestNumberAvgSpeed(num) > 0" class="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 hidden group-hover:block bg-slate-800 text-white text-xs font-bold py-1 px-2 rounded whitespace-nowrap z-50">
                                    {{ getBestNumberAvgSpeed(num) }}s
                                </div>
                            </div>
                            <span class="text-xs sm:text-sm font-black text-slate-600 mt-2">{{ num }}</span>
                        </div>
                    </div>
                </div>
            </div>

        </div>

        <div class="bg-slate-50 py-3 px-6 border-t border-slate-200 flex justify-between items-center">
            <div class="font-black text-slate-800 tracking-tight flex items-center gap-2">
                <span class="text-indigo-500">⚡</span> FastMathFacts
            </div>
            <div class="font-bold text-slate-500 text-sm tracking-wide">
                fastmathfacts.io
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'MasteryDashboard',
    props: {
        determinationScore: Number,
        masteryScore: Number,
        playerLevel: Number,
        isSharing: Boolean,
        gridColumns: Array,
        unlockedNumbers: Array,
        bestPairStatsMap: Object,
        lastAnswered: Object,
        activeModule: String,
        tierDistribution: Array,
        maxTierCount: Number,
        history: Array
    },
    emits: ['open-leaderboard', 'share-stats'],
    computed: {
        isGridMassive() {
            return this.gridColumns.length > 15;
        },
        cellSizeClass() {
            return 'w-7 h-7 md:w-8 md:h-8';
        },
        headerSizeClass() {
            return 'w-7 h-5 text-[9px] md:w-8 md:text-[10px]';
        }
    },
    methods: {
        getPairStats(row, col) {
            const min = Math.min(row, col);
            const max = Math.max(row, col);
            const key = this.activeModule === 'addition' ? `add_${min}+${max}` : 
                        this.activeModule === 'subtraction' ? `sub_${max}-${min}` : 
                        this.activeModule === 'division' ? `div_${min}/${max}` : 
                        `${min}x${max}`;
            const stat = this.bestPairStatsMap[key];
            if (!stat) return { attempts: 0 };
            return stat;
        },
        getSpeedColorClass(speedStr, attempts) {
            if (attempts === 0) return 'bg-slate-50 text-black/20';
            const speed = parseFloat(speedStr);
            
            if (speed <= 0.25) return 'bg-gradient-to-br from-pink-400 to-pink-600 text-white animate-metal-pulse'; 
            if (speed <= 0.50) return 'bg-gradient-to-br from-purple-400 to-purple-600 text-white animate-metal-pulse'; 
            if (speed <= 0.75) return 'bg-gradient-to-br from-indigo-400 to-indigo-600 text-white animate-metal-pulse'; 
            if (speed <= 1.00) return 'bg-gradient-to-br from-blue-400 to-blue-600 text-white animate-metal-pulse';
            
            if (speed <= 2.0) return 'bg-cyan-500 text-white';
            if (speed <= 3.0) return 'bg-teal-500 text-white'; 
            if (speed <= 4.0) return 'bg-emerald-500 text-white';   
            if (speed <= 5.0) return 'bg-green-500 text-white';  
            if (speed <= 6.0) return 'bg-yellow-400 text-yellow-900'; 
            if (speed <= 8.0) return 'bg-orange-500 text-white'; 
            
            return 'bg-red-600 text-white'; 
        },
        isLastAnsweredPair(row, col) {
            if (!this.lastAnswered || !this.lastAnswered.trigger) return false;
            return (row === this.lastAnswered.num1 && col === this.lastAnswered.num2) ||
                   (row === this.lastAnswered.num2 && col === this.lastAnswered.num1);
        },
        isLastAnsweredBar(num) {
            if (!this.lastAnswered || !this.lastAnswered.trigger) return false;
            return num === this.lastAnswered.num1 || num === this.lastAnswered.num2;
        },
        getBestNumberAvgSpeed(num) {
            if (!this.history) return 0;
            const attempts = this.history.filter(att => att.num1 === num || att.num2 === num);
            if (attempts.length === 0) return 0;
            
            let bestSpeed = Infinity;
            if (attempts.length <= 10) {
                const total = attempts.reduce((sum, a) => sum + a.timeSeconds, 0);
                bestSpeed = total / attempts.length;
            } else {
                for (let i = 0; i <= attempts.length - 10; i++) {
                    const window = attempts.slice(i, i + 10);
                    const total = window.reduce((sum, a) => sum + a.timeSeconds, 0);
                    if ((total / 10) < bestSpeed) bestSpeed = total / 10;
                }
            }
            return bestSpeed.toFixed(1);
        },
        getBarHeight(num) {
            const speed = parseFloat(this.getBestNumberAvgSpeed(num));
            if (speed === 0) return 0; 
            let height = (speed / 8.0) * 100;
            return Math.max(5, Math.min(height, 100)); 
        }
    }
}
</script>