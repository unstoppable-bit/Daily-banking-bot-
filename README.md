
# Taken777bot — P2P Profit Calculator

Этот бот позволяет рассчитать минимальную цену продажи USDT с учётом прибыли и комиссии Binance (0.1%).

## Команды

- `/start` — приветствие
- `/calc <цена> <прибыль>` — расчёт цены продажи

Пример:
```
/calc 3.72 0.1
```

Ответ:
```
Минимальная цена продажи: 4.0961 PLN
```

## Развёртывание на Render

1. Создай аккаунт на [https://render.com](https://render.com)
2. Импортируй этот репозиторий в свой GitHub
3. Создай новый Web Service:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
   - Add Environment Variable: `BOT_TOKEN`
4. Запусти сервис и используй бота!
