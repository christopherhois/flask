//import './assets/main.css'
//
//import { createApp } from 'vue'
//import App from './App.vue'
//
//createApp(App).mount('#app')
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';


createApp(App)
    .use(router)
    .use(store)
    .mount('#app');


router.beforeEach((to, from, next) => {
    const token = to.query.token;
    if (token) {
        // Speichere das Token
        localStorage.setItem('token', token);
        store.commit('setToken', token);

        // Entferne das Token aus der URL
        next({ path: to.path, query: {} });
    } else {
        next();
    }
});