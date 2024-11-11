export default {
    // Global page headers
    head: {
        title: 'what the fuck is even that  ',
        meta: [
            { charset: 'utf-8' },
            { name: 'viewport', content: 'width=device-width, initial-scale=1' },
            { hid: 'description', name: 'description', content: '' }
        ],
        link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }]
    },

    // Global CSS
    css: [
    ],

    // Plugins to run before rendering page
    plugins: [
    ],

    // Auto import components
    components: true,

    // Modules for dev and build (recommended)
    buildModules: [
    ],

    // Modules
    modules: [
        '@nuxtjs/axios',
    ],

    // Axios module configuration
    axios: {
        baseURL: 'http://89.58.1.183:5000', // Replace with your backend API URL
    },

    // Build Configuration
    build: {
    }
}
