<template>
    <div class="max-w-7xl w-full grid grid-cols-1 lg:grid-cols-12 gap-8 items-start relative">
        
        <div class="lg:col-span-12 bg-indigo-900 rounded-2xl shadow-md border border-indigo-700 p-6 flex justify-between items-center text-white">
            <div>
                <h1 class="text-3xl font-black tracking-tight flex items-center gap-3">
                    International Bragging Rights
                </h1>
                <p class="text-indigo-300 font-bold mt-1 text-sm">Tracking multiplication fluency and determination across the planet.</p>
            </div>
            <router-link to="/" class="bg-indigo-700 hover:bg-indigo-600 px-4 py-2 rounded-xl font-bold transition shadow-sm text-sm">
                ← Back to Practice
            </router-link>
        </div>

        <div class="bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-200 flex flex-col lg:col-span-5 h-[800px]">
            <div class="bg-slate-800 p-6 text-white">
                <h2 class="text-xl font-black tracking-tight mb-4">Leaderboard</h2>
                
                <div class="grid grid-cols-3 gap-3 mb-3">
                    <div>
                        <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Engine</label>
                        <select v-model="filterModule" class="w-full bg-slate-700 text-white rounded-lg px-3 py-2 text-sm font-bold focus:outline-none border border-slate-600">
                            <option v-for="mod in availableModules" :key="mod.value" :value="mod.value">
                                {{ mod.label }}
                            </option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Sort Metric</label>
                        <select v-model="sortBy" class="w-full bg-slate-700 text-white rounded-lg px-3 py-2 text-sm font-bold focus:outline-none border border-slate-600">
                            <option value="mastery_score">Mastery</option>
                            <option value="determination_score">Determination</option>
                            <option value="player_level">Highest Level</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Age Filter</label>
                        <select v-model="filterAge" class="w-full bg-slate-700 text-white rounded-lg px-3 py-2 text-sm font-bold focus:outline-none border border-slate-600">
                            <option value="ALL">All Ages</option>
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
                </div>
            </div>

            <div class="overflow-y-auto flex-grow p-4 space-y-2 bg-slate-50">
                <div v-for="(entry, index) in filteredAndSortedEntries" :key="index" 
                     class="bg-white border border-slate-200 rounded-xl p-4 flex items-center shadow-sm transition hover:shadow-md">
                    <div class="w-8 font-black text-slate-300 text-xl">{{ index + 1 }}</div>
                    <div class="flex-grow">
                        <div class="font-black text-slate-800 text-lg">{{ entry.username }}</div>
                        <div class="text-xs font-bold text-slate-500 uppercase tracking-wider">
                            {{ formatAge(entry.age_bracket) }} • {{ entry.state ? entry.state + ', ' : '' }}{{ formatCountry(entry.country) }}
                        </div>
                    </div>
                    <div class="text-right flex gap-3">
                        <div class="flex flex-col items-end">
                            <span class="text-[9px] font-black uppercase text-indigo-400 tracking-widest">Mastery</span>
                            <span class="font-mono font-black text-emerald-500">{{ entry.mastery_score }}</span>
                        </div>
                        <div class="flex flex-col items-end">
                            <span class="text-[9px] font-black uppercase text-amber-500 tracking-widest">Determination</span>
                            <span class="font-mono font-black text-amber-500">{{ entry.determination_score }}</span>
                        </div>
                    </div>
                </div>

                <div v-if="filteredAndSortedEntries.length === 0" class="text-center py-10 font-bold text-slate-400">
                    No data matches these filters.
                </div>
            </div>
        </div>

        <div class="bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-200 flex flex-col lg:col-span-7 h-[800px]">
            <div class="p-6 border-b border-slate-200 bg-slate-50 flex justify-between items-center">
                <h2 class="text-xl font-black text-slate-800">World Rankings</h2>
                <div class="bg-slate-200 p-1 rounded-lg flex gap-1">
                    <button @click="activeGraph = 'age'" :class="activeGraph === 'age' ? 'bg-white shadow-sm text-indigo-600' : 'text-slate-500 hover:text-slate-700'" class="px-4 py-1.5 rounded-md font-bold text-sm transition">Age Demographics</button>
                    <button @click="activeGraph = 'map'" :class="activeGraph === 'map' ? 'bg-white shadow-sm text-indigo-600' : 'text-slate-500 hover:text-slate-700'" class="px-4 py-1.5 rounded-md font-bold text-sm transition">Geographic Heatmap</button>
                </div>
            </div>

            <div class="flex-grow p-6 relative flex flex-col">
                <div class="flex justify-end mb-4 gap-3">
                    <div v-show="activeGraph === 'map'" class="flex items-center gap-2 bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-200">
                        <span class="text-xs font-bold text-slate-500 uppercase">Region:</span>
                        <select v-model="mapRegion" @change="drawCharts" class="bg-transparent text-indigo-700 font-black text-sm focus:outline-none cursor-pointer">
                            <option value="world">World</option>
                            <option value="US">United States</option>
                        </select>
                    </div>
                    <div class="flex items-center gap-2 bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-200">
                        <span class="text-xs font-bold text-slate-500 uppercase">Metric:</span>
                        <select v-model="graphMetric" @change="drawCharts" class="bg-transparent text-indigo-700 font-black text-sm focus:outline-none cursor-pointer">
                            <option value="mastery_score">Mastery</option>
                            <option value="determination_score">Determination</option>
                            <option value="player_level">Highest Level</option>
                        </select>
                    </div>
                </div>

                <div v-show="activeGraph === 'age'" id="age_chart" class="flex-grow w-full h-full"></div>
                <div v-show="activeGraph === 'map'" class="flex-grow w-full h-full relative">
                    <button v-if="mapRegion !== 'world'" 
                            @click="mapRegion = 'world'; drawCharts()" 
                            class="absolute top-4 left-4 z-[60] bg-white hover:bg-slate-50 text-slate-800 font-black py-2 px-4 rounded-xl shadow-lg border-2 border-slate-200 transition-all flex items-center gap-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
                        </svg>
                        Back to World Map
                    </button>
                    <div id="geo_chart" class="w-full h-full rounded-xl overflow-hidden border border-slate-200 shadow-inner"></div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
export default {
    name: 'AnalyticsView',
    data() {
        return {
            entries: [],
            availableModules: [
                { value: 'multiplication', label: 'Multiplication' },
                { value: 'division', label: 'Division' },
                { value: 'addition', label: 'Addition' },
                { value: 'subtraction', label: 'Subtraction' }
            ],
            filterModule: 'multiplication',
            sortBy: 'mastery_score',
            filterAge: 'ALL',
            activeGraph: 'map',
            graphMetric: 'mastery_score',
            mapRegion: 'world',
            chartsLoaded: false
        }
    },
    computed: {
        filteredAndSortedEntries() {
            let result = this.entries;

            result = result.filter(e => {
                const dbModule = e.module_type || 'multiplication';
                return dbModule === this.filterModule;
            });

            if (this.filterAge !== 'ALL') {
                result = result.filter(e => e.age_bracket === this.filterAge);
            }

            return result.sort((a, b) => b[this.sortBy] - a[this.sortBy]);
        }
    },
    watch: {
        filteredAndSortedEntries() {
            if (this.chartsLoaded) this.drawCharts();
        },
        activeGraph() {
            if (this.chartsLoaded) {
                setTimeout(this.drawCharts, 50);
            }
        }
    },
    methods: {
        formatCountry(code) {
            if (!code) return 'Unknown';
            try {
                const regionNames = new Intl.DisplayNames(['en'], { type: 'region' });
                return regionNames.of(code) || code;
            } catch (e) {
                return code;
            }
        },

        formatAge(key) {
            const map = {
                'under_10': 'Under 10', '10_13': '10-13', '14_17': '14-17', 
                '18_19': '18-19', '20_29': '20-29', '30_39': '30-39', 
                '40_49': '40-49', '50_59': '50-59', '60_69': '60-69', 
                '70_79': '70-79', '80_plus': '80+'
            };
            return map[key] || 'Unspecified Age';
        },

        async fetchLeaderboard() {
            try {
                const response = await fetch('/api/leaderboard/data');
                
                // Safety Net: Did the server actually respond successfully?
                if (!response.ok) {
                    throw new Error(`Server returned status: ${response.status}`);
                }
                
                const data = await response.json();
                // Handle both { data: [...] } and direct array [...] Django responses
                this.entries = Array.isArray(data) ? data : (data.data || []);
            } catch (err) {
                console.error("Failed to load analytics. Is the Django server running?", err);
                this.entries = []; // Fallback to an empty list so the app doesn't crash
            }
        },

        initGoogleCharts() {
            google.charts.load('current', {
                'packages':['corechart', 'geochart']
            });
            google.charts.setOnLoadCallback(() => {
                this.chartsLoaded = true;
                this.drawCharts();
            });
        },

        drawCharts() {
            if (!this.chartsLoaded || this.entries.length === 0) return;
            if (this.activeGraph === 'age') {
                this.drawAgeChart();
            } else if (this.activeGraph === 'map') {
                this.drawGeoChart();
            }
        },

        drawAgeChart() {
            const ageGroups = {};
            this.filteredAndSortedEntries.forEach(entry => {
                const age = this.formatAge(entry.age_bracket);
                if (!ageGroups[age]) ageGroups[age] = { sum: 0, count: 0 };
                ageGroups[age].sum += entry[this.graphMetric];
                ageGroups[age].count += 1;
            });

            const dataArray = [['Age Bracket', 'Average Score']];
            for (const [age, stats] of Object.entries(ageGroups)) {
                dataArray.push([age, Math.round(stats.sum / stats.count)]);
            }

            if (dataArray.length === 1) return;

            const data = google.visualization.arrayToDataTable(dataArray);
            
            const titleMap = {
                'mastery_score': 'MASTERY',
                'determination_score': 'DETERMINATION',
                'player_level': 'LEVEL'
            };
            
            const options = {
                title: `Average ${titleMap[this.graphMetric] || 'SCORE'} by Age`,
                colors: ['#4f46e5'],
                legend: { position: 'none' },
                chartArea: { left: 90, top: 40, width: '75%', height: '70%' },
                bar: { groupWidth: '50%' },
                hAxis: { 
                    title: 'Average Score', 
                    minValue: 0,
                    textStyle: { fontSize: 10, color: '#64748b' }
                },
                vAxis: { 
                    title: 'Age Group',
                    textStyle: { fontSize: 12, bold: true, color: '#334155' }
                }
            };

            const chart = new google.visualization.BarChart(document.getElementById('age_chart'));
            chart.draw(data, options);
        },

        drawGeoChart() {
            const geoGroups = {};
            
            this.filteredAndSortedEntries.forEach(entry => {
                let location;
                if (this.mapRegion !== 'world') {
                    if (entry.country === this.mapRegion && entry.state) {
                        location = entry.country + '-' + entry.state;
                    } else {
                        return;
                    }
                } else {
                    location = entry.country;
                }
                    
                if (!location) return;

                if (!geoGroups[location]) geoGroups[location] = { sum: 0, count: 0, users: [] };
                geoGroups[location].sum += entry[this.graphMetric];
                geoGroups[location].count += 1;
                geoGroups[location].users.push(entry);
            });

            const dataArray = [
                ['Location', 'Average Score', { role: 'tooltip', type: 'string', p: { html: true } }]
            ];

            for (const [loc, stats] of Object.entries(geoGroups)) {
                const avg = Math.round(stats.sum / stats.count);
                const sortedUsers = stats.users.sort((a, b) => b[this.graphMetric] - a[this.graphMetric]);
                
                const uniqueTopUsers = [];
                const seenNames = new Set();
                for (const u of sortedUsers) {
                    if (!seenNames.has(u.username)) {
                        seenNames.add(u.username);
                        uniqueTopUsers.push(u);
                        if (uniqueTopUsers.length === 3) break;
                    }
                }

                const stateNames = {
                    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
                    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
                    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
                    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
                    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
                    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
                    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
                    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
                    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
                    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
                };
                
                let displayName = loc;
                if (loc.startsWith('US-')) {
                    let stateCode = loc.replace('US-', '');
                    displayName = stateNames[stateCode] || stateCode;
                } else {
                    try {
                        const regionNames = new Intl.DisplayNames(['en'], {type: 'region'});
                        displayName = regionNames.of(loc) || loc;
                    } catch (e) {
                        displayName = loc;
                    }
                }

                let tooltipHtml = `<div style="padding: 12px 16px; font-family: ui-sans-serif, system-ui, sans-serif; min-width: 170px; background: white; border-radius: 12px; box-shadow: 0 10px 25px -5px rgb(0 0 0 / 0.15), 0 8px 10px -6px rgb(0 0 0 / 0.1); border: 1px solid #e2e8f0; color: #0f172a; font-size: 14px;">`;
                
                tooltipHtml += `<div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 8px; border-bottom: 2px solid #f1f5f9; padding-bottom: 6px;">`;
                tooltipHtml += `<h4 style="margin: 0; font-size: 14px; font-weight: 900; color: #0f172a; letter-spacing: 0.02em;">${displayName}</h4>`;
                tooltipHtml += `<span style="font-size: 11px; font-weight: 900; color: #4f46e5; background: #e0e7ff; padding: 2px 6px; border-radius: 6px; margin-left: 12px;">AVG: ${avg}</span>`;
                tooltipHtml += `</div>`;
                
                tooltipHtml += `<p style="margin: 0 0 8px 0; font-size: 10px; font-weight: 800; color: #94a3b8; text-transform: uppercase;">Based on ${stats.count} tests</p>`;
                
                uniqueTopUsers.forEach((u, i) => {
                    const dotColor = i === 0 ? '#fbbf24' : i === 1 ? '#94a3b8' : '#d97706'; 
                    tooltipHtml += `<div style="font-size: 12px; display: flex; justify-content: space-between; align-items: center; margin-top: 4px;">
                                        <span style="font-weight: 800; color: #334155; display: flex; align-items: center;">
                                            <span style="color: ${dotColor}; font-size: 12px; margin-right: 6px;">●</span> ${u.username}
                                        </span> 
                                        <span style="color: #0f172a; font-family: monospace; font-weight: 900;">${u[this.graphMetric]}</span>
                                     </div>`;
                });
                
                tooltipHtml += `</div>`;
                dataArray.push([loc, avg, tooltipHtml]);
            }

            if (dataArray.length === 1) {
                const dummyLocation = this.mapRegion === 'world' ? 'US' : 'US-CA';
                const emptyTooltip = `<div style="padding: 12px 16px; font-family: ui-sans-serif, system-ui, sans-serif; min-width: 160px; background: white; border-radius: 12px; text-align: center;">
                    <h4 style="margin: 0 0 4px 0; font-size: 14px; font-weight: 900; color: #0f172a; text-transform: uppercase; letter-spacing: 0.05em;">No Data Yet</h4>
                    <p style="margin: 0; font-size: 10px; font-weight: 800; color: #94a3b8; text-transform: uppercase;">Be the first to score!</p>
                </div>`;
                
                dataArray.push([dummyLocation, null, emptyTooltip]); 
            }

            const data = google.visualization.arrayToDataTable(dataArray);
            const dataValues = Object.values(geoGroups).map(g => g.sum / g.count);
            const dataMax = dataValues.length > 0 ? Math.max(...dataValues) : 0;
            const baselineMax = this.graphMetric === 'player_level' ? 12 : 5000;
            const dynamicMax = Math.max(baselineMax, dataMax);
            
            const options = {
                region: this.mapRegion === 'world' ? 'world' : this.mapRegion,
                resolution: this.mapRegion === 'world' ? 'countries' : 'provinces',
                tooltip: { isHtml: true }, 
                colorAxis: {
                    minValue: 0,
                    maxValue: dynamicMax,
                    colors: [
                        '#dc2626', '#f97316', '#facc15', '#22c55e', '#10b981', 
                        '#14b8a6', '#06b6d4', '#3b82f6', '#6366f1', '#a855f7', '#ec4899'
                    ]
                },
                backgroundColor: '#f8fafc',
                datalessRegionColor: '#f1f5f9',
                defaultColor: '#f5f5f5',
            };

            const chart = new google.visualization.GeoChart(document.getElementById('geo_chart'));
            
            google.visualization.events.addListener(chart, 'regionClick', (eventData) => {
                if (this.mapRegion === 'world') {
                    this.mapRegion = eventData.region;
                    this.drawCharts();
                }
            });

            chart.draw(data, options);
        }
    },
    async mounted() {
        await this.fetchLeaderboard();
        this.initGoogleCharts();
    }
}
</script>