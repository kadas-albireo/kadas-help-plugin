#!/bin/sh

# Regular build
../node_modules/.bin/gitbook build

# Clear theme.js
> _book/gitbook/theme.js

# Fixup style.css
echo '.book-summary {left: 0!important;} .book-body {left: 300px!important;}' >> _book/gitbook/style.css

# Add explicit index.html
for file in $(find _book/ -name '*.html'); do
    sed -Ei 's|href="(.*)/"|href="\1/index.html"|g' $file
    sed -Ei 's|href="(.*)/#(\w+)"|href="\1/index.html#\2"|g' $file
done
