```shell
curl -N -X POST "http://127.0.0.1:8000/ai_docs/generate" \
-H "Content-Type: application/json" \
-d '{
  "content": "当和尚也不容易",
  "question": "",
  "op_type": "polish",
  "op_sub_type": "colloquial"
}'

```

```shell
curl -N -X POST "http://127.0.0.1:8000/ai_docs/generate" \
-H "Content-Type: application/json" \
-d '{
  "content": "当和尚也不容易",
  "question": "",
  "op_type": "continue_writing",
  "op_sub_type": ""
}'
```

# 2. 使用conda生成需要的安装包

```shell
conda env export > environment.yml
```
