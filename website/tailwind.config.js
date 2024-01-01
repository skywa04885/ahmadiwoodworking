const colors = require('tailwindcss/colors')

/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/*.html",
        "./templates/components/*.html",
        "./templates/components/breadcrumb/*.html",
        "./templates/contact/*.html",
        "./templates/contact/header/*.html",
        "./templates/index/*.html",
        "./templates/index/faq/*.html",
        "./templates/index/products/*.html",
        "./templates/index/services/*.html",
    ],
    theme: {
        extend: {
            container: {
                center: true,
                screens: {
                    sm: '640px',
                    md: '768px',
                    lg: '1024px',
                    xl: '1280px',
                    '2xl': '1200px',
                },
            },
        },

    },
    plugins: [],
}

