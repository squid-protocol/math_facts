<template>
  <div class="fixed top-0 left-0 right-0 z-[200] bg-slate-900 text-white shadow-lg border-b border-slate-700">
      <div class="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
          
          <div class="flex items-center gap-2 sm:gap-4 truncate">
              <a href="/" class="font-black tracking-tight flex items-center gap-1 sm:gap-2 hover:text-indigo-300 transition shrink-0">
                  <span class="text-indigo-400 text-lg sm:text-xl">⚡</span>
                  <span class="hidden sm:inline text-lg">FastMathFacts</span>
                  <span class="sm:hidden text-base">FMF</span>
              </a>
              <div id="navbar-module-slot" class="shrink min-w-0 truncate"></div>
          </div>
          
          <div class="flex items-center gap-4 sm:gap-6 font-bold text-sm shrink-0">
              <router-link to="/" class="hidden sm:block text-slate-300 hover:text-white transition">Practice</router-link>
              <router-link to="/analytics/" class="hidden sm:block text-slate-300 hover:text-white transition">Leaderboard</router-link>

              <div class="relative h-14 flex items-center">
                  <button @click.stop="toggleMenu" class="flex items-center gap-1 text-slate-300 hover:text-white transition cursor-pointer">
                      Menu 
                      <svg :class="isMenuOpen ? 'rotate-180' : ''" class="w-4 h-4 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M19 9l-7 7-7-7"></path></svg>
                  </button>
                  
                  <div :class="isMenuOpen ? 'opacity-100 visible scale-100' : 'opacity-0 invisible scale-95'"
                       class="absolute right-0 top-full mt-0 w-48 bg-white text-slate-800 rounded-xl shadow-xl transition-all duration-200 border border-slate-200 overflow-hidden transform origin-top-right">
                      <router-link @click="closeMenu" to="/analytics/" class="sm:hidden block px-4 py-3 hover:bg-slate-50 border-b border-slate-100">Leaderboard</router-link>
                      <router-link @click="closeMenu" to="/about/" class="block px-4 py-3 hover:bg-slate-50 border-b border-slate-100">About the Engine</router-link>
                      <router-link @click="closeMenu" to="/faq/" class="block px-4 py-3 hover:bg-slate-50">FAQ & Support</router-link>
                  </div>
              </div>

          </div>
      </div>
  </div>
</template>

<script>
export default {
  name: 'NavBar',
  data() {
      return {
          isMenuOpen: false
      }
  },
  mounted() {
      document.addEventListener('click', this.closeMenu);
  },
  beforeUnmount() {
      document.removeEventListener('click', this.closeMenu);
  },
  methods: {
      toggleMenu() {
          this.isMenuOpen = !this.isMenuOpen;
      },
      closeMenu() {
          if (this.isMenuOpen) {
              this.isMenuOpen = false;
          }
      }
  }
}
</script>