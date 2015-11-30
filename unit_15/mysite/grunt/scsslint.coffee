module.exports =

  # Lint your SCSS
  # https://github.com/ahmednuaman/grunt-scss-lint

  options:
    colorizeOutput: true
    config: '.scss-lint.yml'
  stylesheets: [
    '<%= paths.css %>/scss/**/*.scss'
    '!<%= paths.css %>/scss/lib/**/*.scss'
  ]
