# Quiz-Chatbots 

It has scripts to use chatbots with quiz-challenges in Telegram or VK. You can get a question from bot, get an answer, you can check your answer, also you can check your current score. 

### How to install

* Dowload the code 
* Check that you have Python 3  
* Install requirements:  
```
pip install -r requirements.txt
```
* Create a bot at telegram channel `@BotFather` 

### How to create a quiz

You can find a file `example.txt` in repository. You can create your own txt-file with the same structure:
```
Вопрос 1(if english - Question 1):
Your question.

Ответ (if english - Answer):
Your answer.
```

### Environment Variables 

Add file `.env` with variables: 
- `TG_BOT_TOKEN` - token of your telegram bot. 
- `VK_TOKEN` - token of your VK bot. 
- `REDIS_DB` - add your database from [Redis](https://app.redislabs.com/). 
- `REDIS_DB_PASSWORD` - add password from your database. 

### How to run chatbots

- `python tg_bot.py` 
- `python vk_bot.py` 

### How it works

Telegram

![screenshot](media/tg_bot.gif)

Also you can write for these chatbots:
- `VK` - [write message](https://vk.com/im?media=&sel=-198809484) 
- `Telegram` - you can find a bot by username `DevQuizzerBot`. 
