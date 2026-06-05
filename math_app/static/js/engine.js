const { createApp } = Vue

createApp({
    data() {
        return {
            unlockSequence: [[7], [8], [9], [10], [11], [12]],
            unlockedNumbers: [0, 1, 2, 3, 4, 5, 6],
            
            currentQuestion: { num1: 0, num2: 0 },
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

            // Profile State
            profiles: [],
            activeProfile: 'Guest',
            showProfileDropdown: false,
            showAddPlayerModal: false,
            newProfileName: '',

            // Modals & Telemetry State
            showLeaderboardModal: false,
            showShareModal: false,
            isSharing: false,
            submissionState: 'idle', // 'idle' | 'submitting' | 'success' | 'error'
            leaderboardForm: { username: '', ageBracket: '', country: '', state: '', consentToTrack: false },
            deviceId: null,
            usStates: ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'],
            allCountries: ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czechia', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Korea', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Samoa', 'San Marino', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe'],

            sessionStartTime: Date.now(),
            initialMasteryScore: 0,
            initialPlayerLevel: 0,
            initialDetermination: 0,

            gameMode: 'campaign',
            targetSpeed: 3.5,
            targetAccuracy: 90,
            windowSize: 10, 

            globalCountries: [],
            availableRegions: [],
            isFetchingGeo: false
        }
    },
    watch: {
        showLeaderboardModal(isOpen) {
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
    computed: {
        currentUrl() { return window.location.origin; },

        maxGridNumber() { return Math.max(...this.unlockedNumbers, 5); },
        
        gridColumns() {
            const maxLen = Math.max(13, this.maxGridNumber + 1);
            return Array.from({length: maxLen}, (_, i) => i); 
        },
        isGridMassive() { return true; },
        
        cellSizeClass() { return 'w-7 h-7 md:w-8 md:h-8'; },
        headerSizeClass() { return 'w-7 h-5 text-[9px] md:w-8 md:text-[10px]'; },
        
        bestPairStatsMap() {
            const pairHistory = {};
            for (const att of this.history) {
                const min = Math.min(att.num1, att.num2);
                const max = Math.max(att.num1, att.num2);
                const key = `${min}x${max}`;
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
                    const key = `${min}x${max}`;
                    
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
                    const key = `${min}x${max}`;
                    
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
            
            // Wipe the state clean so we don't bleed data between profiles
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

                const canvas = await html2canvas(element, {
                    scale: 2, 
                    useCORS: true,
                    backgroundColor: '#ffffff'
                });

                canvas.toBlob(async (blob) => {
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
                        
                        // Silently download, then trigger our custom social modal
                        this.showShareModal = true;
                    }
                    this.isSharing = false;
                }, 'image/png');

            } catch (err) {
                console.error("Failed to capture image", err);
                this.isSharing = false;
            }
        },

        getPairStats(row, col) {
            const min = Math.min(row, col);
            const max = Math.max(row, col);
            const stat = this.bestPairStatsMap[`${min}x${max}`];
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
            if (!this.lastAnswered.trigger) return false;
            return (row === this.lastAnswered.num1 && col === this.lastAnswered.num2) ||
                   (row === this.lastAnswered.num2 && col === this.lastAnswered.num1);
        },

        isLastAnsweredBar(num) {
            if (!this.lastAnswered.trigger) return false;
            return num === this.lastAnswered.num1 || num === this.lastAnswered.num2;
        },

        getBestNumberAvgSpeed(num) {
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
        },

        loadData() {
            if (!this.activeProfile) return;
            const prefix = `math_${this.activeProfile}_`;

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
            }
        },
        
        saveData() {
            if (!this.activeProfile) return;
            const prefix = `math_${this.activeProfile}_`;

            localStorage.setItem(prefix + 'history', JSON.stringify(this.history));
            localStorage.setItem(prefix + 'unlocked', JSON.stringify(this.unlockedNumbers));
            localStorage.setItem(prefix + 'determination', this.determinationScore.toString());
            localStorage.setItem(prefix + 'unlockSequence', JSON.stringify(this.unlockSequence));
            localStorage.setItem(prefix + 'settings', JSON.stringify({
                targetSpeed: this.targetSpeed,
                targetAccuracy: this.targetAccuracy,
                windowSize: this.windowSize,
                gameMode: this.gameMode
            }));
        },

        async submitLeaderboard() {
            if (!this.leaderboardForm.username) return;

            const totalAttempts = this.history.length;
            const correctCount = this.history.filter(a => a.isCorrect).length;
            const sessionAccuracy = totalAttempts > 0 ? Math.round((correctCount / totalAttempts) * 100) : 0;

            if (this.leaderboardForm.consentToTrack) {
                if (!this.deviceId) {
                    this.deviceId = crypto.randomUUID();
                    localStorage.setItem('fastMathDeviceId', this.deviceId);
                }
            } else {
                this.deviceId = null;
                localStorage.removeItem('fastMathDeviceId');
            }

            const payload = {
                device_id: this.deviceId,
                username: this.leaderboardForm.username,
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
                    this.showLeaderboardModal = false;
                    this.submissionState = 'idle';
                    this.resumeGame();
                }, 2000);

            } catch (error) {
                this.submissionState = 'error';
                console.error(error);
            }
        },

        resetProgress() {
            if(confirm(`Are you sure you want to delete all saved data for ${this.activeProfile}? This cannot be undone.`)) {
                const prefix = `math_${this.activeProfile}_`;
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
                const key = `${min}x${max}`;
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
                    const [n1, n2] = key.split('x').map(Number);
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
                    const key = `${min}x${max}`;
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
            let n1 = 0;
            let n2 = 0;

            if (this.gameMode === 'total') {
                const maxIndex = this.gridColumns.length;
                n1 = Math.floor(Math.random() * maxIndex);
                n2 = Math.floor(Math.random() * maxIndex);
            } else if (this.gameMode === 'weak') {
                const weakSpots = this.getWeakSpots();
                if (weakSpots.length > 0) {
                    const spot = weakSpots[Math.floor(Math.random() * weakSpots.length)];
                    n1 = spot[0];
                    n2 = spot[1];
                } else {
                    const poolIndex1 = Math.floor(Math.random() * this.unlockedNumbers.length);
                    const poolIndex2 = Math.floor(Math.random() * this.unlockedNumbers.length);
                    n1 = this.unlockedNumbers[poolIndex1];
                    n2 = this.unlockedNumbers[poolIndex2];
                }
            } else {
                const r = Math.random();
                const untested = this.getUntestedPairs();
                const weakSpots = this.getWeakSpots();

                if (r <= 0.50 && untested.length > 0) {
                    const spot = untested[Math.floor(Math.random() * untested.length)];
                    n1 = spot[0];
                    n2 = spot[1];
                } else if (r > 0.75 && weakSpots.length > 0) {
                    const spot = weakSpots[Math.floor(Math.random() * weakSpots.length)];
                    n1 = spot[0];
                    n2 = spot[1];
                } else {
                    const poolIndex1 = Math.floor(Math.random() * this.unlockedNumbers.length);
                    const poolIndex2 = Math.floor(Math.random() * this.unlockedNumbers.length);
                    n1 = this.unlockedNumbers[poolIndex1];
                    n2 = this.unlockedNumbers[poolIndex2];
                }
            }
            
            if (Math.random() > 0.5) {
                this.currentQuestion.num1 = n1;
                this.currentQuestion.num2 = n2;
            } else {
                this.currentQuestion.num1 = n2;
                this.currentQuestion.num2 = n1;
            }
            
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
            if (this.userAnswer.length < 4) {
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
            const correctAnswer = this.currentQuestion.num1 * this.currentQuestion.num2;
            const isCorrect = parseInt(this.userAnswer) === correctAnswer;

            const min = Math.min(this.currentQuestion.num1, this.currentQuestion.num2);
            const max = Math.max(this.currentQuestion.num1, this.currentQuestion.num2);
            const key = `${min}x${max}`;
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
        const savedProfiles = localStorage.getItem('fastMathProfiles');
        if (savedProfiles) this.profiles = JSON.parse(savedProfiles);

        // Load whoever was playing last, otherwise default to Guest
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
}).mount('#app')