# render-ai-web

#linked to webserver 'render-ai-web-v1' in Render -> https://dashboard.render.com/web/srv-d2k34un5r7bs73ebqoi0

#Curl testing:
curl -X POST \
  "https://render-ai-web-v1.onrender.com/ask" \
  -H "Content-Type: application/json" \
  -d '{"input_text":"what is render platform"}'

# 3) 忽略 .env，并提供示例文件（可选但强烈建议）
echo ".env" >> .gitignore
git add .gitignore

# 如果本地目录里有 .env，确保不纳入版本库
git rm --cached .env 2>/dev/null || true
