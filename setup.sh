mkdir -p ~/.streamlit/
#test
echo "\
[general]\n\
email = \"philipp.heitmann94@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
