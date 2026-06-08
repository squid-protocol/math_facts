<template>
  <div class="bg-slate-100 flex flex-col items-center min-h-screen font-sans pt-20">
    <NavBar />
    
    <main class="w-full flex-grow flex justify-center p-4 pb-24">
        <router-view></router-view>
    </main>

    <footer class="w-full text-center text-slate-500 text-sm py-8 border-t border-slate-200">
        <router-link to="/privacy-policy/" class="hover:text-slate-800 mx-2 font-bold transition">Privacy Policy</router-link> | 
        <router-link to="/terms/" class="hover:text-slate-800 mx-2 font-bold transition">Terms of Service</router-link>
    </footer>
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue';

export default {
    name: 'App',
    components: {
        NavBar
    }
}
</script>