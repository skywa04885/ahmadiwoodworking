const colors = require('tailwindcss/colors')

/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/**/*.html"
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
                padding: '1rem'
            },
        },

    },
    plugins: [
            require('tailwind-scrollbar')({ nocompatible: true }),
    ],
}

