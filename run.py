from RAK_ml.pipeline import answer_query

answer = answer_query(
    "Что такое Сокр?",
    model_name="llama3:latest",
    filepath="example.txt"  # ❗ Можно убрать, если уже был индексирован ранее
)
print(answer)