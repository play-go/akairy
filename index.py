# -*- coding: utf-8 -*-
import disnake
from typing import Optional
from disnake.ext import commands, tasks
from randomtimestamp import random_time
import aiohttp, asyncio, time, psutil, platform, re, json, random, textwrap, threading
from math import *
from sqlitedict import SqliteDict
# Bot instance
activity = disnake.Activity(
    name="Версия 2.13 | 0 мс",
    type=disnake.ActivityType.watching,
)
intents=disnake.Intents.default()
bot = commands.AutoShardedInteractionBot(intents=intents, activity=activity, shard_count=3)
# bot.remove_message_command("help")
# bot.remove_slash_command("help")
ea='''# Предметы
 • Абсолютно все предметы имееют Название, Переменную, Модификатор, Количество, Описание
 • Информацию в предметах можно использовать только в бросках

- *О информации в предметах*

**Название**
> Название не может быть никак получено в бросках
> С помощю названия предмета вы и будете брать информацию о нём 
> В название предмета нельзя добавлять **"_"**
*Советую вместо пробелов ставить **"-"***

**Переменная**
> Может быть только числом
> Получается в бросках при помощи **"&*Название*&"**
> Максимальное значение 999999999999
*В ней хорошо хранить урон (если это оружие) или что-либо что будет нужно в бросках*

**Модификатор**
> Может быть только числом
> Получается в бросках при помощи **"&*Название*_mod&"**
> Максимальное значение 999999999999
*Тоже самое что и Переменная, только как дополнительная ячейка для записи*

**Количество**
> Может быть только числом
> Получается в бросках при помощи **"&*Название*_count&"**
> Максимальное значение 999999999999
> Если не указано при создании, является 1

**Использование**
> Нельзя получить

**Описание**
> Получается в бросках при помощи **"&*Название*_op&"**

- *О информации в талантах*

**Вызов**
> Таланты получаются в бросках при помощи %**(1-10)**%

# Ошибки
 • Если предмет не найден, заменяется на **"(Item error)"**
'''
emitem = disnake.Embed(
title="Предметы и то что о них нужно знать",
description=str(ea),
color=disnake.Colour.random()
)
emitem.set_footer(
text=f"Вдохновлено mRPG"
)
eb='''# Формулы
**Для того чтобы использовать формулы или функции, используйте "//" по бокам 
*(Пример: //1+1==3//)***
**Для того чтобы использовать текст в функциях, используйте " или ' по бокам
*(Пример: //pick("Ka", "Bot", "❤️")//)***

## Для формул доступны следующие операторы:
\+ (сложение)
\- (вычитание)
\* (умножение)
\/ (деление)
\% (взятие остатка от деления)
\*\* (возведение в степень)
\> (больше)
\< (меньше)
\=\= (проверка равенства)
\!\= (проверка неравенства)
\>\= (больше или равно)
\<\+ (меньше или равно)
or (или)
and (и)
not (не)

## Математические функции.
• floor(x): Округляет вниз до целого (берёт целую часть);
• round(x): Округляет до ближайшего целого (половина округляется вверх);
• ceil(x): Округляет вверх до целого;
• abs(x): Возвращает абсолютную величину (модуль);
*И так далее...*

## Дополнительные функции

• if(x,success,failure) - Если условие (первый аргумент) выполнено, возвращает второй аргумент, иначе — третий.
• set(x, value) - Записывает величину, полученную из броска или функции, под указанным именем; также возвращает эту величину.
• get(x, value) - Возвращает величину, записанную под данным именем.
• find(x, n) - Возращает количество **n** из **x**
• pick(value1, value2, value3, ...) - Выбирает один случайный указанный элемент
• pickn(n, value1, value2, value3, ...) - Выбирает **n** случайнх указанных элементов

# Броски

Бросок такого образца: **NdX**, где **N** — количество костей (до 20), а **X** — число граней одной кости (до 1000) (должно быть неотрицательным); Если **N** не указано, полагается единица.

Результат броска нескольких костей — сумма результатов. К броскам можно применять математические операции.

# Взрывные броски

Бросок такого образца: **NdX!**, где **N** — количество костей (до 20), **X** — число граней одной кости (до 1000) (должно быть неотрицательным), a **!** означает возможность взрывных бросков; Если **N** не указано, полагается единица.

Результат броска нескольких костей — сумма результатов и сумма взрывов. К взрывным броскам можно применять математические операции.

Взрыв - Когда число грани кости является максимальным числом в кости. Выбрасывается идентичная кость (Максимальное количество рекурсий 20)

# Fate броски

Бросок такого образца: **Ndf**, где **N** — количество костей (до 20), а **f** означает Fate бросок

Результат броска нескольких костей — сумма результатов. Результат это последовательность от -1 до 1 (включая 0)

# Ошибки

• Если вы превысили лимиты: Бросок заменяется на **"(Limit error)"**
• Если при использовании функций или формул происходит ошибка: формула заменяется на "**(Math error)**"

'''
emdice = disnake.Embed(
title="Броски и то что о них нужно знать",
description=str(eb),
color=disnake.Colour.random()
)
emdice.set_footer(
text=f"Вдохновлено mRPG"
)
ec='''# Таланты
 • Таланты можно использовать только в бросках

- *О информации в талантах*

**Вызов**
> Таланты получаются в бросках при помощи %**(1-10)**%

# Ошибки
 • Если талант не найден, заменяется на **"(Talents error)"**
'''
emtalent = disnake.Embed(
title="Таланты и то что о них нужно знать",
description=str(ec),
color=disnake.Colour.random()
)
emtalent.set_footer(
text=f"Вдохновлено mRPG"
)
ed='''# 1.13 - "Меньше знаешь - Крепче спишь"
## Добавлено
• Команда /info в которой находиться множество информации про бота

## Изменено
• Команды /item add, /item set и /item delete теперь входят в подгруппу admin (/item admin add)
'''
emhelp = disnake.Embed(
title="Инфо о новой версии",
description=str(ed),
color=disnake.Colour.random()
)
ef='''
### Системы
⟫ **Достижения**
⟫ **Описание канала**
⟫ **Предметы**
⟫ **Таланты**
⟫ **Время**
⟫ **Кости (Дайсы)**

### Остальное (RP/TRP)
⟫ **action** - Просто быстрые действия с gif
⟫ **do** - Отыгрывание действий от 3-его лица
⟫ **try** - Позволяет выполнить ваше рп действие с шансом (Удачно/Неудачно)
⟩ **(A)** *try_set_chance* - Изменяет шанс в try (Если обычный не понравился)
⟫ **random** - Вывод случайного аргумента который вы указали
⟫ **roll** - Рандомизация числа от a до b

### Fun команды
⟫ **ben** - Спросить что-нибудь у ben-a (Гав гав)
⟫ **embed** - Вывод embed сообщение которые вы хотите
⟫ **math** - Просто решает ваше что-либо простое
'''
emcoms = disnake.Embed(
description=str(ef),
color=disnake.Colour.random()
)
emcoms.set_footer(text="Выберите о какой системе вы хотите узнать! (A) - Указывает на то что для исполнения команды требуються права изменять сервер.")

cf=[disnake.ui.StringSelect(custom_id="setts_drop",options=[disnake.SelectOption(label="Достижения",value="achi",emoji="🎖️"),disnake.SelectOption(label="Описание канала",value="channel",emoji="🌳"),disnake.SelectOption(label="Предметы",value="item",emoji="💼"),disnake.SelectOption(label="Таланты",value="talent",emoji="🧿"),disnake.SelectOption(label="Время",value="time",emoji="⌚"),disnake.SelectOption(label="Кости",value="dice",emoji="🎲"),disnake.SelectOption(label="Выход",value="exit",emoji="❌")])]
eff=[disnake.ui.StringSelect(custom_id="help_drop",options=[disnake.SelectOption(label="Команды",value="coms",emoji="🎮"),disnake.SelectOption(label="Броски/Кости",value="dice",emoji="🎲"),disnake.SelectOption(label="Предметы",value="item",emoji="💼"),disnake.SelectOption(label="Таланты",value="talent",emoji="🧿")])]

eachi="""# Достижения
⟫ **(A)** **add** - Добавляет @ достижение
⟫ **(A)** **delete** - Снимает у @ достижение
⟫ **get** - Показывает ваши или чужие достижения

**Самая первая система. Существует как fun система**
"""
fachi=disnake.Embed(
description=str(eachi),
color=disnake.Colour.random()
)
fachi.set_footer(text="Выберите о какой системе вы хотите узнать! (A) - Указывает на то что для исполнения команды требуються права изменять сервер.")

echan="""# Описание канала
**(A)**
⟫ **set** - Изменяет рп/нонрп описание у канала
⟫ **show** - Отправляет описание отдельным сообщением

⟫ **info** - Показывает только вам описание канала

**В основном существует для того, чтобы сообщить какую-то информацию и "закрепить" её и в любой момент узнать её.
Также можно использовать для контекста в рп**
"""
fchan=disnake.Embed(
description=str(echan),
color=disnake.Colour.random()
)
fchan.set_footer(text="Выберите о какой системе вы хотите узнать! (A) - Указывает на то что для исполнения команды требуються права изменять сервер.")

eitemm="""# Предметы
**(A)**
⟫ **add** - Добавляет к @ в инвентарь предмет
⟫ **delete** - Полностью забирает у @ из инвентаря предмет
⟫ **set** - Изменяет предмет из инвентаря у @

⟫ **get** - Позволяет посмотреть инвентарь
⟫ **use** - Позволяет использовать предмет (после чего кол-во предмета убавиться на 1)

**Нужен для того чтобы облегчить работу в подсчётах ресурсов в контексте рп**
"""
fitemm=disnake.Embed(
description=str(eitemm),
color=disnake.Colour.random()
)
fitemm.set_footer(text="Выберите о какой системе вы хотите узнать! (A) - Указывает на то что для исполнения команды требуються права изменять сервер.")

etalents="""# Таланты
**(A)**
⟫ **give** - Выдаёт очки талантов участнику
⟫ **take** - Забирает очки таланта у участника (Очки могут уйти в минус)
⟫ **set** - Изменяет серверные переменные (название талантов и т.д)

⟫ **down** - Понижает таланты у вас (Если разрешено сервером)
⟫ **up** - Повышает таланты у вас
⟫ **get** - Показывает ваши или чужие таланты
⟫ **reset** - Сбрасывает ваши таланты к изначальным показателям (Если разрешено сервером) **(Не возвращает очки)**

**Существует для того чтобы использовать в формулях в /dice**
"""
ftalents=disnake.Embed(
description=str(etalents),
color=disnake.Colour.random()
)
ftalents.set_footer(text="Выберите о какой системе вы хотите узнать! (A) - Указывает на то что для исполнения команды требуються права изменять сервер.")

etime="""# Время
⟫ **(A)** **set** - Изменяет время в рп
⟫ **(A)** **setinter** - Изменяет сколько времени пройдёт в рп за 1 реальную минуту
⟫ **get** - Показывает время в контексте рп

**Нужна для подсчёта времени за вас!**
"""
ftime=disnake.Embed(
description=str(etime),
color=disnake.Colour.random()
)
ftime.set_footer(text="Выберите о какой системе вы хотите узнать! (A) - Указывает на то что для исполнения команды требуються права изменять сервер.")

edice="""# Кости (Дайсы)
⟫ **/dice** - Позволяет спользовать систему "Дайсов"

**Самое главное в рп это непредсказуемость! Для этого помогут команды по типу roll/random. 
Интересно что будет если совместить эти команды? Получиться /dice!
Все возможные функции можно посмотреть в /info > Броски/Кости**
"""
fdice=disnake.Embed(
description=str(edice),
color=disnake.Colour.random()
)
fdice.set_footer(text="Выберите о какой системе вы хотите узнать!")

#Vars

time_start = 0
command_pressed = 0
started=True
# Events

@bot.event
async def on_ready():
    global started
    if started:
        global time_start
        time_start = round(time.time())
        print(f"Бот {bot.user.name} запущен с {bot.shard_count} шардами.")
        started=False
    if not taskse.is_running():
        taskse.start()
    if not taskss.is_running():
        taskss.start()
    if not taskers.is_running():
       	taskers.start()

@bot.event
@commands.cooldown(1, 3, commands.BucketType.user)
async def on_slash_command_error(ctx, error):
    if isinstance(error, disnake.ext.commands.errors.MissingPermissions):
        await ctx.response.send_message(":x:У вас должны быть права изменять сервер чтобы использовать эту команду.", ephemeral=True)
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.response.send_message(f':x:Подождите немного перед использованием этой команды! {round(error.retry_after, 2)}')
    elif isinstance(error, commands.errors.CommandInvokeError):
        print(f"ERROR: ", error)
    else:
        print(f"ERROR: ", error)
        raise error


# Commands


async def notfalse(a):
    if a is not False:
        return a
    else:
        return None


async def list_sd(a, b,c):
    if c == "+":
        return a.append(b)
    elif c == "-":
        return a.remove(b)
@bot.slash_command(name = "try", description="Попытка выполнить какое либо действие🔮")
@commands.cooldown(1, 3, commands.BucketType.user)
async def tryss(ctx, commandd: str = commands.Param(name="действие", description="Ваше действие")) -> None:
    global command_pressed
    command_pressed+=1
    print(f"try {ctx.guild.name}")
    db = SqliteDict("example.sqlite", f"{ctx.guild.id}",autocommit=True)
    try:
        db["trych"]
    except:
        db["trych"]=50
    await ctx.response.defer()
    a = [f"*<@{ctx.author.id}> попробовал(а) {commandd} |  Удачно!*", f"*<@{ctx.author.id}> попробовал(а) {commandd} |  Неудачно!*"]
    b=random.randint(1,100)
    if b<=db["trych"]:
        await ctx.edit_original_response(a[0])
    else:
        await ctx.edit_original_response(a[1])
    

@bot.slash_command(name = "try_set_chance", description="Изменить шанс успеха в try🔮")
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd(ctx, commandd: int = commands.Param(name="шанс", description="Какой шанс успеха поставить?", ge=1, le=99)) -> None:
    global command_pressed
    command_pressed+=1
    db = SqliteDict("example.sqlite", f"{ctx.guild.id}",autocommit=True)
    print(f"try_set {ctx.guild.name}")
    await ctx.response.defer(ephemeral=True)
    db["trych"]=commandd
    await ctx.edit_original_response(f"Шанс изменён на {commandd}!")

@bot.slash_command(name = "roll", description="Рандомизация желаемого числа🎲")
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd(ctx, minim: int = commands.Param(name="мин", description="Минимальная цифра для рандом-а", ge=0), maxim: int = commands.Param(name="макс", description="Максимальная цифра для рандом-а", ge=1)) -> None:
    global command_pressed
    command_pressed+=1
    print(f"roll {ctx.guild.name}")
    if maxim <= minim:
        await ctx.response.defer(ephemeral=True)
        await ctx.edit_original_response(":x:'макс' не должен быть меньше или равен 'мин'")
    else:
        await ctx.response.defer()
        await ctx.edit_original_response(random.randint(minim, maxim))

@bot.slash_command(name = "random", description="Выводит один случайный текст из аргументов что вы указали💬")
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd(ctx, arguments: str = commands.Param(name="аргументы", description="Ваши аргументы. Для разделения используйте '|'")) -> None:
    global command_pressed
    command_pressed+=1
    print(f"random {ctx.guild.name}")
    await ctx.response.defer()
    await ctx.edit_original_response(f"Вывод: {random.choice(arguments.split('|'))}")

@bot.slash_command(name = "randtime", description="Узнать рандомное время (в рп)⌚")
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd(ctx) -> None:
    global command_pressed
    command_pressed+=1
    print(f"randtime {ctx.guild.name}")
    await ctx.response.defer()
    await ctx.edit_original_response(f"**{random_time(text=True,pattern='%H:%M')}**")

@bot.slash_command(name = "do", description="Отыгрывания действий от 3 лица🏙️")
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd(ctx, commandd: str = commands.Param(name="описание", description="Описание чего-либо (\\n - новая строка)")) -> None:
    await ctx.response.defer()
    await ctx.edit_original_response(commandd.replace('\\n','\n')+f"(<@{ctx.author.id}>)")

@bot.slash_command(name = "math", description="Математика📏")
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd(ctx, commandd: str = commands.Param(name="пример", description="Какой пример вы хотите задать?")) -> None:
    global command_pressed
    command_pressed+=1
    print(f"math {ctx.guild.name}")
    await ctx.response.defer()
    try:
        a = eval(commandd)
    except Exception:
        a = "Syntax error"
    embed = disnake.Embed(
    title="Math - ответ",
    description=a,
    color=disnake.Colour.random()
    )
    embed.set_footer(
    text=f"От {ctx.author.name}. С примером {commandd}"
    )
    await ctx.edit_original_response(embed=embed)

@bot.slash_command(name = "ben", description="Задать вопрос бен-у🐶")
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd(ctx, commandd: str = commands.Param(name="вопрос", description="Ваш вопрос!")) -> None:
    global command_pressed
    command_pressed+=1
    print(f"ben {ctx.guild.name}")
    await ctx.response.defer()
    embed1 = disnake.Embed(
    title="Ben - вопрос",
    description="Бен ответил: No",
    color=disnake.Colour.random()
    )
    embed1.set_footer(
    text=f"От {ctx.author.name}. С вопросом {commandd}"
    )
    embed1.set_image(url="https://c.tenor.com/x2u_MyapWvcAAAAd/no.gif")
    embed2 = disnake.Embed(
    title="Ben - вопрос",
    description="Бен ответил: Ugh",
    color=disnake.Colour.random()
    )
    embed2.set_footer(
    text=f"От {ctx.author.name}. С вопросом {commandd}"
    )
    embed2.set_image(url="https://c.tenor.com/fr6i8VzKJuEAAAAd/talking-ben-ugh.gif")
    embed3 = disnake.Embed(
    title="Ben - вопрос",
    description="Бен ответил: Hohoho",
    color=disnake.Colour.random()
    )
    embed3.set_footer(
    text=f"От {ctx.author.name}. С вопросом {commandd}"
    )
    embed3.set_image(url="https://c.tenor.com/agrQMQjQTzgAAAAd/talking-ben-laugh.gif")
    embed4 = disnake.Embed(
    title="Ben - вопрос",
    description="Бен ответил: Yes",
    color=disnake.Colour.random()
    )
    embed4.set_footer(
    text=f"От {ctx.author.name}. С вопросом {commandd}"
    )
    embed4.set_image(url="https://c.tenor.com/6St4vNHkyrcAAAAd/yes.gif")
    await ctx.edit_original_response(embed=random.choice([embed1,embed2,embed3,embed4]))

@bot.slash_command(name = "embed", description="Создать встроенное сообщение👀")
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd(ctx, color: int = commands.Param(name="цвет", description="Цвет сообщения (HEX color)", min_length=6, max_length=6), title: str = commands.Param(name="заголовок", description="Заголовок сообщения", max_length=256, default = False), description: str = commands.Param(name="описание", description="Описание сообщения (\\n - новая строка)", max_length=4096, default = False), footer: str = commands.Param(name="футер", description="Нижний колонтитул сообщения", max_length=2048, default = False)) -> None:
    global command_pressed
    command_pressed+=1
    print(f"embed {ctx.guild.name}")
    await ctx.response.defer()
    embed = disnake.Embed(
    title=await notfalse(title),
    description=await notfalse(description.replace("\\n", '\n')),
    colour=color
    )
    if await notfalse(footer) is not None:
        embed.set_footer(text=footer)
    elif await notfalse(title) is None and await notfalse(description) is None and await notfalse(footer) is None:
        embed.set_footer(text="Empty embed")
    await ctx.edit_original_response(embed=embed)

# Time

@bot.slash_command(name = "time")
@commands.cooldown(1, 3, commands.BucketType.user)
async def times(ctx):
    global command_pressed
    command_pressed+=1
    print(f"time {ctx.guild.name}")

@times.sub_command(name = "set", description="Изменить время (в рп)⌚")
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd_time(ctx, hours: int = commands.Param(name="час", description="Изменить час в рп времени", ge=0, max_value=59), mins: int = commands.Param(name="минуты", description="Изменить минуты в рп времени", ge=0, max_value=23)) -> None:
    db = SqliteDict("example.sqlite", f"{ctx.guild.id}",autocommit=True)
    await ctx.response.defer(ephemeral=True)
    db["time_h"]=hours
    db["time_m"]=mins
    if mins < 10:
        await ctx.edit_original_response(f"Время изменено на **{hours}:0{mins}**")
    else:
        await ctx.edit_original_response(f"Время изменено на **{hours}:{mins}**")
    
@times.sub_command(name="get", description="Узнать сколько времени (в рп)⌚")
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd_time(ctx):
    db = SqliteDict("example.sqlite", f"{ctx.guild.id}",autocommit=True)
    await ctx.response.defer()
    if db["time_m"] < 10:
        await ctx.edit_original_response(f"**{db['time_h']}:0{db['time_m']}**")
    else:
        await ctx.edit_original_response(f"**{db['time_h']}:{db['time_m']}**")
    
@times.sub_command(name = "setinter", description="Изменить интервал изменения времени (в рп)⌚")
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd_time(ctx, inter: int = commands.Param(name="цифра", description="Во сколько изменить? (Каждую минуту к таймеру добавляется указанная вами цифра (по умолчанию 10))", ge=0, max_value=60)) -> None:
    db = SqliteDict("example.sqlite", f"{ctx.guild.id}",autocommit=True)
    await ctx.response.defer(ephemeral=True)
    db["time_s"]=inter
    await ctx.edit_original_response(f"Интервал изменён на **{inter}**")
    
# Achivments

@bot.slash_command(name = "achievement")
@commands.cooldown(1, 3, commands.BucketType.user)
async def achive(ctx) -> None:
    pl = SqliteDict("example.sqlite", f"{ctx.guild.id}-{ctx.author.id}",autocommit=True)
    global command_pressed
    command_pressed+=1
    print(f"achive {ctx.guild.name}")
    try:
        a = pl["achievement"]
    except KeyError:
        pl["achievement"]=[]
@achive.sub_command(name="delete", description="Снять достижение🎖️")
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd_achive(ctx, item: str = commands.Param(name="достижение", description="Ваше название достижения"), member: disnake.Member = commands.Param(default=False,name="пользователь", description="Кому?")):
    await ctx.response.defer(ephemeral=True)
    if isinstance(member, type(False)):
        pl = SqliteDict("example.sqlite", f"{ctx.guild.id}-{ctx.author.id}",autocommit=True)
        my_list = pl["achievement"]
        try:
            my_list.remove(item)
        except:
            ...
        pl["achievement"]=my_list
        await ctx.edit_original_response(f"Ваше достижение {item} удалено")
    else:
        mb = SqliteDict("example.sqlite", f"{ctx.guild.id}-{member.id}",autocommit=True)
        try:
            my_list = mb["achievement"]
            try:
                my_list.remove(item)
            except:
                ...
            mb["achievement"]=my_list
            await ctx.edit_original_response(f"Достижение {item} удалено у <@{member.id}>")
        except KeyError:
            mb["achievement"]=[]
            await ctx.edit_original_response(f"Достижение {item} удалено у <@{member.id}>")
    
@achive.sub_command(name="add", description="Добавить достижение🎖️")
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd_achive(ctx, item: str = commands.Param(name="достижение", description="Ваше название достижения"), member: disnake.Member = commands.Param(default=False,name="пользователь", description="Кому?")):
    await ctx.response.defer(ephemeral=True)
    if isinstance(member, type(False)):
        pl = SqliteDict("example.sqlite", f"{ctx.guild.id}-{ctx.author.id}",autocommit=True)
        pl["achievement"]=pl["achievement"]+[item]
        await ctx.edit_original_response(f"Вам добавлено достижение {item}")
    else:
        mb = SqliteDict("example.sqlite", f"{ctx.guild.id}-{member.id}",autocommit=True)
        try:
            mb["achievement"]=mb["achievement"]+[item]
            await ctx.edit_original_response(f"<@{member.id}> добавлено достижение {item}")
        except KeyError:
            mb["achievement"]=[item]
            await ctx.edit_original_response(f"<@{member.id}> добавлено достижение {item}")
    
@achive.sub_command(name="get", description="Посмотреть свои или чужие достижения🎖️")
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd_achive(ctx, member: disnake.Member = commands.Param(default=False,name="пользователь", description="У кого вы хотите посмотреть?")):
    await ctx.response.defer(ephemeral=True)
    if isinstance(member, type(False)):
        pl = SqliteDict("example.sqlite", f"{ctx.guild.id}-{ctx.author.id}",autocommit=True)
        await ctx.edit_original_response(f'Ваши достижения: {str(pl["achievement"]).replace("[", "").replace("]", "")}')
    else:
        mb = SqliteDict("example.sqlite", f"{ctx.guild.id}-{member.id}",autocommit=True)
        try:
            await ctx.edit_original_response(f'Достижения <@{member.id}>: {str(mb["achievement"]).replace("[", "").replace("]", "")}')
        except KeyError:
            mb["achievement"]=[]
            await ctx.edit_original_response(f'Достижения <@{member.id}>: {str(mb["achievement"]).replace("[", "").replace("]", "")}')
    
# Inventory

@bot.slash_command(name = "item")
@commands.cooldown(1, 3, commands.BucketType.user)
async def item(ctx) -> None:
    global command_pressed
    command_pressed+=1
    pl = SqliteDict("example.sqlite", f"{ctx.guild.id}-{ctx.author.id}",autocommit=True)
    print(f"item {ctx.guild.name}")
    #{'count':1, 'name':'', 'value':0,'mod':0, 'opis': '', 'canu': False}
    try:
        a = pl["items"]
    except KeyError:
        pl["items"]=[]

@item.sub_command(name="use", description="Использовать предмет (после использования его количество убавится)💼")
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd_achive(ctx, itemn: str = commands.Param(name="предмет", description="Название предмета? (Можно написать первое слово)"),member: disnake.Member = commands.Param(default=False,name="юзер", description="На кого вы хотите использовать предмет?")):
    mb = SqliteDict("example.sqlite", f"{ctx.guild.id}-{ctx.user.id}",autocommit=True)
    li=mb["items"]
    try:
        for i in li:
            if itemn.split()[0]==i["name"].split()[0]:
                try:
                    itemn.split()[1]
                    if itemn == i:
                        item_ind=li.index(i)
                        break
                except Exception:
                    item_ind=li.index(i)
                    break
        else:
            raise KeyError("Hello world!")
    except KeyError:
        await ctx.response.defer(ephemeral=True)
        await ctx.edit_original_response("Предмет не найден!")
        return None
    if li[item_ind]["canu"]==False:
        await ctx.response.defer(ephemeral=True)
        await ctx.edit_original_response(f"{li[item_ind]['name']} нельзя использовать!")
    if li[item_ind]["count"]==0:
        await ctx.response.defer(ephemeral=True)
        await ctx.edit_original_response(f"У вас не достаточного {li[item_ind]['name']}!")
    await ctx.response.defer(ephemeral=False)
    itemem=mb["items"]
    print(itemem[0])
    itemem[item_ind]["count"]-=1
    mb["items"]=itemem
    embed = disnake.Embed(title=f"{ctx.user.name} использует {textwrap.shorten(itemem[item_ind]['name'], width=10, placeholder='...')} {'на '+member.name if member != False else ''}",
    description=f"{'Теперь у '+itemem[item_ind]['name']+' осталось '+str(itemem[item_ind]['count'])+' использований' if itemem[item_ind]['count']>0 else 'Теперь '+itemem[item_ind]['name']+' нельзя больше использовать (но он остался в инвентаре)'}", color=disnake.Color.red())
    await ctx.edit_original_response(embed=embed)
    
    
@item.sub_command(name="get", description="Посмотреть свой или чужой инвентарь💼")
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd_achive(ctx, member: disnake.Member = commands.Param(default=False,name="пользователь", description="У кого вы хотите посмотреть?")):
    await ctx.response.defer(ephemeral=True)
    def invent(guild,user):
        pl = SqliteDict("example.sqlite", f"{guild}-{user}",autocommit=True)
        a=pl["items"]
        res="Название - Количество (Переменная:Модификатор) **Можно_исп.** \|\|Описание\|\|\n"
        for i in a:
            res+=f'{i["name"]} - {i["count"]} ({i["value"]}:{i["mod"]}) **{str(i["canu"]).replace("True", "Да").replace("False", "Нет")}** ||{i["opis"]}|| \n'
        if a == []:
            return "(Пусто...)"
        return res
    if isinstance(member, type(False)):
        embed = disnake.Embed(title=f"Предметы {ctx.author.name}",
        description=invent(ctx.guild.id,ctx.author.id), color=disnake.Color.random())
        await ctx.edit_original_response(embed=embed)
    else:
        mb = SqliteDict("example.sqlite", f"{ctx.guild.id}-{member.id}",autocommit=True)
        try:
            embed = disnake.Embed(title=f"Предметы {member.name}",
            description=invent(ctx.guild.id,ctx.author.id), color=disnake.Color.random())
            await ctx.edit_original_response(embed=embed)
        except KeyError:
            mb["items"]=[]
            embed = disnake.Embed(title=f"Предметы {member.id}",
            description=invent(ctx.guild.id,ctx.author.id), color=disnake.Color.random())
            await ctx.edit_original_response(embed=embed)

@item.sub_command_group(name="admin", description="💼")
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def item_admin(ctx):
    pass

@item_admin.sub_command(name="set", description="Изменить предмет у кого-то в инвентаре💼")
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd_achive(ctx, member: disnake.Member = commands.Param(name="пользователь", description="Кому хотите добавить?"), name: str = commands.Param(name="название", description="Название предмета", max_length=30), value: int = commands.Param(default=False,name="переменная", description="Значение переменной предмета", max_value=999_999_999_999),count: int = commands.Param(default=False,name="количество", description="Количество предмета", min_value=1,max_value=999_999_999_999),modif: int = commands.Param(default=False,name="модификатор", description="Модификатор предмета", min_value=-9999,max_value=9999),opis: str = commands.Param(default=False,name="описание", description="Описание предмета", max_length=1500),canu: bool = commands.Param(default='',name="использование", description="Можно ли использовать предмет?")):
    mb = SqliteDict("example.sqlite", f"{ctx.guild.id}-{member.id}",autocommit=True)
    try:
        for i in mb["items"]:
            if i["name"].lower() == name.lower():
                name=i['name']
                if value==False:
                    value=i["value"]
                if modif == False:
                    modif=i["mod"]
                if opis == False:
                    opis=i["opis"]
                if count == False:
                    count=i["count"]
                if canu == '':
                    canu=i["canu"]
                My_list=mb["items"]
                index = My_list.index(i)
                item={'count':count, 'name':name, 'value':value,'mod':modif, 'opis': opis, 'canu': canu}
                My_list[index]=item
                mb["items"]=My_list
                break
        else:
            raise KeyError("Hello world!")
    except KeyError as e:
        print(e)
        await ctx.response.defer(ephemeral=True)
        await ctx.edit_original_response("Предмет не найден!")
        return None
    await ctx.response.defer(ephemeral=False)
    embed = disnake.Embed(title=f"Предмет {textwrap.shorten(name, width=10, placeholder='...')} у {member.name} изменён!",
    description=f"Название: {name}\nПеременная: {value}\nКоличество: {count}\nМодификатор: {modif}\nМожно ли использовать: **{str(canu).replace('True', 'Да').replace('False', 'Нет')}**\nОписание: `{opis}`", color=disnake.Color.blue())
    embed.set_footer(text=f"Изменил: {ctx.author.name}")
    await ctx.edit_original_response(embed=embed)
    

@item_admin.sub_command(name="add", description="Добавить предмет кому-нибудь в инвентарь💼")
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd_achive(ctx, member: disnake.Member = commands.Param(name="пользователь", description="Кому хотите добавить?"), name: str = commands.Param(name="название", description="Название предмета", max_length=30), value: int = commands.Param(name="переменная", description="Значение переменной предмета", max_value=999_999_999_999),count: int = commands.Param(default=False,name="количество", description="Количество предмета", min_value=1,max_value=999_999_999_999),modif: int = commands.Param(default=False,name="модификатор", description="Модификатор предмета", min_value=-9999,max_value=9999),opis: str = commands.Param(default=False,name="описание", description="Описание предмета", max_length=1500),canu: bool = commands.Param(default=False,name="использование", description="Можно ли использовать предмет?")):
    mb = SqliteDict("example.sqlite", f"{ctx.guild.id}-{member.id}",autocommit=True)
    if len(mb["items"]) >= 10:
        await ctx.response.defer(ephemeral=True)
        await ctx.edit_original_response(f"{member.name} уже имеет максимальное количество предметов")
        return None
    if name.find("_")!=-1:
        await ctx.response.defer(ephemeral=True)
        await ctx.edit_original_response(f"В названии предмета нельзя использовать символ '_'")
        return None
    await ctx.response.defer(ephemeral=False)
    if modif == False:
        modif=0
    if opis == False:
        opis="(Пусто...)"
    if count == False:
        count=1
    item={'count':count, 'name':name, 'value':value,'mod':modif, 'opis': opis, 'canu': canu}
    try:
        mb["items"]=mb["items"]+[item]
    except KeyError:
        mb["items"]=[item]
    embed = disnake.Embed(title=f"{member.name} получает {textwrap.shorten(name, width=10, placeholder='...')}",
    description=f"Название: {name}\nПеременная: {value}\nКоличество: {count}\nМодификатор: {modif}\nМожно ли использовать: **{str(canu).replace('True', 'Да').replace('False', 'Нет')}**\nОписание: `{opis}`", color=disnake.Color.blue())
    embed.set_footer(text=f"Добавил: {ctx.author.name}")
    await ctx.edit_original_response(embed=embed)
    

@item_admin.sub_command(name="delete", description="Удалить предмет из инвентаря пользователя💼")
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd_achive(ctx, member: disnake.Member = commands.Param(name="пользователь", description="Кому хотите добавить?"), name: str = commands.Param(name="название", description="Название предмета", max_length=30), count: int = commands.Param(name="кол-во", description="Количество предмета (-1 для полного удаления)")):
    mb = SqliteDict("example.sqlite", f"{ctx.guild.id}-{member.id}",autocommit=True)
    try:
        my_list = mb["items"]
        try:
            for i in range(len(my_list)):
                if my_list[i]["name"] == name:
                    my_list[i]["count"] = int(my_list[i]["count"])-count
                    if count==-1 or my_list[i]["count"]<=0:
                        my_list.remove(my_list[i])
                    break
        except Exception as ex:
            await ctx.response.defer(ephemeral=True)
            await ctx.edit_original_response(f"Данного предмета не существует у <@{member.id}>")
            return None
        await ctx.response.defer(ephemeral=False)
        mb["items"]=my_list
        if count==-1:
            await ctx.edit_original_response(f"Предмет **{name}** удалён у <@{member.id}>")
        else:
            await ctx.edit_original_response(f"Удалёно {count} **{name}** у <@{member.id}>")
    except KeyError:
        mb["items"]=[]
        await ctx.edit_original_response(f"<@{member.id}> не имел предметов раньше")
    
# talents

@bot.slash_command(name = "talents")
@commands.cooldown(1, 3, commands.BucketType.user)
async def abilities(ctx) -> None:
    global command_pressed
    command_pressed+=1
    db = SqliteDict("example.sqlite", f"{ctx.guild.id}",autocommit=True)
    pl = SqliteDict("example.sqlite", f"{ctx.guild.id}-{ctx.author.id}",autocommit=True)
    print(f"talents {ctx.guild.name}")
    #{}
    try:
        a=db["talents"]
    except KeyError:
        db["talents"]={"canDown": True, "def":5,'1':'Сила', '2':'Ловкость', '3':'Интелект', '4':'-', '5':'-', '6':'-', '7':'-', '8':'-', '9':'-', '10':'-'}
    try:
        b=pl["talents"]
    except KeyError:
        pl["talents"]={'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, 'have':db["talents"]["def"]}
    

@abilities.sub_command(name="get", description="Посмотреть свои или чужие таланты🧿")
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd_talents(ctx, member: disnake.Member = commands.Param(default=False,name="пользователь", description="У кого вы хотите посмотреть?")):
    await ctx.response.defer(ephemeral=True)
    db = SqliteDict("example.sqlite", f"{ctx.guild.id}",autocommit=True)
    try:
        abil_s=db["talents"]
        if member==False:
            pl = SqliteDict("example.sqlite", f"{ctx.guild.id}-{ctx.author.id}",autocommit=True)
            abil=pl["talents"]
        else:
            mb = SqliteDict("example.sqlite", f"{ctx.guild.id}-{member.id}",autocommit=True)
            try:
                abil=mb["talents"]
            except KeyError:
                mb["talents"]={'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, 'have':db["talents"]["def"]}
                abil=mb["talents"]
        a=''
        for i in range(1,11):
            if str(abil_s[str(i)]) != '-':
                a+=f"> {i}." + str(abil_s[str(i)]) + ' **'+str(abil[str(i)])+'**'+'\n'
    except Exception as ex:
        print(ex)
        return None
    if member != False:
        b=f"Таланты {member.name}"
    else:
        b=f"Таланты {ctx.author.name}"
    embed = disnake.Embed(
    title=b,
    description=a,
    colour=disnake.Colour.random()
    )
    embed.set_footer(text=f"Доступных очков: {abil['have']}")
    await ctx.edit_original_response(embed=embed)
    

@abilities.sub_command(name="up", description="Прокачать таланты🧿")
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd_talents(ctx, count: int = commands.Param(default=1,name="количество", description="На сколько вы хотите повысить?")):
    await ctx.response.defer(ephemeral=True)
    db = SqliteDict("example.sqlite", f"{ctx.guild.id}",autocommit=True)
    pl = SqliteDict("example.sqlite", f"{ctx.guild.id}-{ctx.author.id}",autocommit=True)
    buts=[]
    try:
        abil_s=db["talents"]
        abil=pl["talents"]
        if abil["have"]<count:
            await ctx.edit_original_response("У вас не хватает очков улучшений!")
            return None
        a=''
        for i in range(1,11):
            if str(abil_s[str(i)]) != '-':
                a+=f"> {i}. " + str(abil_s[str(i)]) + ' **'+str(abil[str(i)])+'**'+'\n'
                buts.append(disnake.ui.Button(label=str(abil_s[str(i)]), style=disnake.ButtonStyle.success, custom_id=f"{str(abil_s[str(i)])}_{ctx.guild.id}_{ctx.author.id}_up_{count}_{str(i)}"))
    except Exception as ex:
        print(ex)
        return None
    view=disnake.ui.View(timeout=20)
    for i in buts:
        view.add_item(i)
    embed = disnake.Embed(
    title="Какой талант повысить?",
    description=a,
    colour=disnake.Colour.random()
    )
    await ctx.edit_original_response(embed=embed, view=view)
    

@abilities.sub_command(name="down", description="Понизить таланты🧿")
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd_talents(ctx, count: int = commands.Param(default=1,name="количество", description="На сколько вы хотите повысить?")):
    await ctx.response.defer(ephemeral=True)
    db = SqliteDict("example.sqlite", f"{ctx.guild.id}",autocommit=True)
    pl = SqliteDict("example.sqlite", f"{ctx.guild.id}-{ctx.author.id}",autocommit=True)
    try:
        buts=[]
        abil_s=db["talents"]
        abil=pl["talents"]
        if abil_s["canDown"]!=True:
            await ctx.edit_original_response("*На этом сервере запрещено понижать таланты!")
            return None
        a=''
        for i in range(1,11):
            if str(abil_s[str(i)]) != '-':
                a+=f"> {i}. " + str(abil_s[str(i)]) + ' **'+str(abil[str(i)])+'**'+'\n'
                buts.append(disnake.ui.Button(label=str(abil_s[str(i)]), style=disnake.ButtonStyle.success, custom_id=f"{str(abil_s[str(i)])}_{ctx.guild.id}_{ctx.author.id}_down_{count}_{str(i)}"))
    except Exception as ex:
        print(ex)
        return None
    view=disnake.ui.View(timeout=20)
    for i in buts:
        view.add_item(i)
    embed = disnake.Embed(
    title="Какой талант понизить?",
    description=a,
    colour=disnake.Colour.random()
    )
    await ctx.edit_original_response(embed=embed,view=view)
    
    
@abilities.sub_command(name="reset", description="Сбросить таланты🧿")
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd_talents(ctx):
    await ctx.response.defer(ephemeral=True)
    db = SqliteDict("example.sqlite", f"{ctx.guild.id}",autocommit=True)
    pl = SqliteDict("example.sqlite", f"{ctx.guild.id}-{ctx.author.id}",autocommit=True)
    try:
        abil_s=db["talents"]
        if abil_s["canDown"]!=True:
            await ctx.edit_original_response("*На этом сервере запрещено понижать таланты!")
            return None
        pl["talents"]={'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, 'have':db["talents"]["def"]}
    except Exception as ex:
        print(ex)
        return None
    await ctx.edit_original_response("Таланты сброшены")
    

@abilities.sub_command_group(name="admin", description="🧿")
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def talents_admin(ctx):
    pass

@talents_admin.sub_command(name="give", description="Добавить очки талантов участнику🧿")
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def comandd_talents_admin(ctx, member: disnake.Member = commands.Param(name="пользователь", description="Кому хотите добавить?"),count: int = commands.Param(name="количество", description="Сколько вы хотите добавить?")):
    await ctx.response.defer(ephemeral=False)
    db = SqliteDict("example.sqlite", f"{ctx.guild.id}",autocommit=True)
    mb = SqliteDict("example.sqlite", f"{ctx.guild.id}-{member.id}",autocommit=True)
    a=f"<@{member.id}> было добавлено {count} очков талантов!"
    try:
        abil=mb["talents"]
        abil["have"]+=count
        mb["talents"]=abil
    except KeyError:
        mb["talents"]={'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, 'have':db["talents"]["def"]+count}
    embed = disnake.Embed(
            title="Give",
            description=a,
            colour=disnake.Colour.random()
    )
    embed.set_footer(text=f"Добавил {ctx.author.name}")
    await ctx.edit_original_response(embed=embed)
    
    
@talents_admin.sub_command(name="set", description="Изменить переменные (название талантов и т.д)🧿")
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def comandd_talents_admin(ctx, settings: str =commands.Param(name="переменная", description="Какую переменную вы хотите изменить?", choices=[disnake.OptionChoice("Название 1-го таланта", "t_1"), disnake.OptionChoice("Название 2-го таланта", "t_2"), disnake.OptionChoice("Название 3-го таланта", "t_3"), disnake.OptionChoice("Название 4-го таланта", "t_4"), disnake.OptionChoice("Название 5-го таланта", "t_5"), disnake.OptionChoice("Название 6-го таланта", "t_6"), disnake.OptionChoice("Название 7-го таланта", "t_7"), disnake.OptionChoice("Название 8-го таланта", "t_8"), disnake.OptionChoice("Название 9-го таланта", "t_9"), disnake.OptionChoice("Название 10-го таланта", "t_10"), disnake.OptionChoice("Возможность забирать очки талантов", "canDown"), disnake.OptionChoice("Начальное кол-во очков талантов", "defN")]), value: str = commands.Param(name="изменяемая", description="На что хотите изменить? ('-' - ничего)", max_length=80)):
    db = SqliteDict("example.sqlite", f"{ctx.guild.id}",autocommit=True)
    abil_s=db["talents"]
    if settings.find("t_")!=-1:
        settings.replace("t_", '')
        abil_s[settings]=value
        db[ctx.guild.id] = {**db[ctx.guild.id], **{"talents":abil_s}}
        if value!="-":
            await ctx.response.defer(ephemeral=False)
            embed = disnake.Embed(
            title="Изменение",
            description=f'Название {settings}-го таланта теперь **{value}**',
            colour=disnake.Colour.random()
            )
            await ctx.edit_original_response(embed=embed)
        else:
            await ctx.response.defer(ephemeral=False)
            embed = disnake.Embed(
            title="Изменение",
            description=f'{settings}-й талант был отключён',
            colour=disnake.Colour.random()
            )
            await ctx.edit_original_response(embed=embed)
    elif settings=="canDown":
            try:
                await ctx.response.defer(ephemeral=False)
                def chk(e):
                    if e == "true":
                        return True
                    elif e == 'false':
                        return False
                    return False
                values=chk(value.lower().replace('да', "true").replace('нет', "false"))
                abil_s["canDown"]=values
                print(type(values))
                db[ctx.guild.id] = {**db[ctx.guild.id], **{"talents":abil_s}}
                
                if values:
                    embedT = disnake.Embed(
                    title="Изменение",
                    description=f'Возможность забирать очки талантов было включено',
                    colour=disnake.Colour.random()
                    )
                    await ctx.edit_original_response(embed=embedT)
                else:
                    embedF = disnake.Embed(
                    title="Изменение",
                    description=f'Возможность забирать очки талантов было отключено',
                    colour=disnake.Colour.random()
                    )
                    await ctx.edit_original_response(embed=embedF)
            except:
                await ctx.edit_original_response("Изменяемая должна быть да/нет/true/false!")
                return None
    elif settings=="defN":
        try:
            await ctx.response.defer(ephemeral=False)
            value=int(value)
            abil_s["def"]=value
            db[ctx.guild.id] = {**db[ctx.guild.id], **{"talents":abil_s}}
            embed = disnake.Embed(
            title="Изменение",
            description=f'Изначальное количество очков талантов стало: {value}',
            colour=disnake.Colour.random()
            )
            await ctx.edit_original_response(embed=embed)
        except:
            await ctx.edit_original_response("Изменяемая должна быть цифрой!")
            return None
    

@talents_admin.sub_command(name="take", description="Забрать очки талантов у участника🧿")
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def comandd_talents_admin(ctx, member: disnake.Member = commands.Param(name="пользователь", description="У кого вы хотите забрать?"),count: int = commands.Param(name="количество", description="Сколько вы хотите забрать?")):
    await ctx.response.defer(ephemeral=False)
    db = SqliteDict("example.sqlite", f"{ctx.guild.id}",autocommit=True)
    mb = SqliteDict("example.sqlite", f"{ctx.guild.id}-{member.id}",autocommit=True)
    a=f"У <@{member.id}> было забрано {count} очков талантов!"
    try:
        abil=mb["talents"]
        abil["have"]-=count
        mb["talents"]=abil
    except KeyError:
        mb["talents"]={'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, 'have':db["talents"]["def"]-count}
    embed = disnake.Embed(
            title="Take",
            description=a,
            colour=disnake.Colour.random()
    )
    embed.set_footer(text=f"Забрал {ctx.author.name}")
    await ctx.edit_original_response(embed=embed)

# channel

@bot.slash_command(name = "channel")
@commands.cooldown(1, 3, commands.BucketType.user)
async def channel(ctx) -> None:
    print(f"channel {ctx.guild.name}")
    db = SqliteDict("example.sqlite", f"ch-{ctx.channel.id}",autocommit=True)
    try:
        db["dess"]
        db["title"]
        db["color"]
        db["link_banner"]
    except:
        db["dess"]=""
        db["title"]="-"
        db["color"]=disnake.Colour.green()
        db["link_banner"]=""

@channel.sub_command(name="info", description="Узнать рп/нонрп описание канала🌳")
#@commands.has_permissions(manage_guild=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def comandd_channel(ctx):
    await ctx.response.defer(ephemeral=True)
    db = SqliteDict("example.sqlite", f"ch-{ctx.channel.id}",autocommit=True)
    titl=db["title"]
    des=db["dess"]
    colr=db["color"]
    link=db["link_banner"]
    if db["dess"]=='' and db["title"]=='-' and db["color"]=='' and db["link_banner"]=='':
        des="Ничего не известно об этом канале"
        colr=disnake.Colour.random()
        link="http://squarefaction.ru/files/user/189/storage/20160814163131_86d4303e.gif"
    embed = disnake.Embed(
            title=titl,
            description=des,
            colour=colr#disnake.Colour.random()
    )
    if link!='':
        embed.set_image(link)
    await ctx.edit_original_response(embed=embed)

@channel.sub_command_group(name="admin", description="🌳")
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def channel_admin(ctx):
    pass

@channel_admin.sub_command(name="show", description="Отправляет рп/нонрп описание канала отдельным сообщением🌳")
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def comandd_channel_admin(ctx: disnake.interactions.application_command.ApplicationCommandInteraction):
    await ctx.response.defer(ephemeral=True)
    db = SqliteDict("example.sqlite", f"ch-{ctx.channel.id}",autocommit=True)
    titl=db["title"]
    des=db["dess"]
    colr=db["color"]
    link=db["link_banner"]
    if db["dess"]=='' and db["title"]=='-' and db["color"]=='' and db["link_banner"]=='':
        await ctx.edit_original_response("В описании ничего нет!")
    else:
        embed = disnake.Embed(
                title=titl,
                description=des,
                colour=colr#disnake.Colour.random()
        )
        if link!='':
            embed.set_image(link)
        await ctx.edit_original_response("Отправляю! Надеюсь я могу отправлять сюда сообщения")
        time.sleep(1)
        try:
            await ctx.send(embed=embed)
        except:
            await ctx.edit_original_response("Похоже произошла ошибка! Возможно я не могу отправить сюда сообщение!")

@channel_admin.sub_command(name="set", description="Изменить рп/нонрп описание канала🌳")
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def comandd_channel_admin(ctx, title: str = commands.Param(name="заголовок", description="Заголовок сообщения ('-' чтобы удалить)", max_length=256, default = False), description: str = commands.Param(name="описание", description="Описание сообщения ('-' чтобы удалить) (\\n - новая строка)", max_length=4096, default = False), link: str = commands.Param(name="банер", description="баннер который будет виден в описании (ссылкой) ('-' чтобы удалить)", default = False), color: int = commands.Param(name="цвет", description="Цвет сообщения (HEX color) ('-' чтобы удалить)", min_length=6, max_length=6, default=False)):
    await ctx.response.defer(ephemeral=True)
    db = SqliteDict("example.sqlite", f"ch-{ctx.channel.id}",autocommit=True)
    if description=="-":db["dess"]=''
    elif description!=False:db["dess"]=description.replace("\\n", '\n')
    if title=="-":db["dess"]='-'
    elif title!=False:db["title"]=title
    if color=="-":db["dess"]=''
    elif color!=False:db["color"]=color
    if link=="-":db["dess"]=''
    elif link!=False:db["link_banner"]=link
    if db["dess"]=='' and db["title"]=='-' and db["color"]=='' and db["link_banner"]=='':
        await ctx.edit_original_response("От описания ничего не осталось!")
    else:
        embed = disnake.Embed(
                title=db["title"],
                description=db["dess"],
                colour=db["color"]#disnake.Colour.random()
        )
        if db["link_banner"]!='':
            embed.set_image(db["link_banner"])
        await ctx.edit_original_response("Вот так теперь описание выглядит!",embed=embed)

#event
    
@bot.event
async def on_guild_channel_delete(channel):
    if type(channel) == disnake.channel.TextChannel:
        db = SqliteDict("example.sqlite", f"ch-{channel.id}",autocommit=True)
        db["dess"]=""
        db["title"]=""
        db["color"]=""
        db["link_banner"]=""
        

@bot.event
async def on_button_click(inter: disnake.MessageInteraction):
    a=inter.component.custom_id.split("_")
    #msg = await inter.fetch_message(msgID)
    a[1]=int(a[1])
    a[2]=int(a[2])
    a[4]=int(a[4])
    db = SqliteDict("example.sqlite", f"{a[1]}",autocommit=True)
    pl = SqliteDict("example.sqlite", f"{a[1]}-{a[2]}",autocommit=True)
    abil_s=db["talents"]
    abil=pl["talents"]
    empty_view=disnake.ui.View()
    empty_view.stop()
    #embed=disnake.Embed()
    if a[3]=="up":
        if abil['have']<a[4]:
            embed=disnake.Embed(title=f"У вас не хватает очков улучшений!")
            await inter.response.edit_message(embed=embed, view=empty_view)
            return None
        embed=disnake.Embed(title=f"{a[0]} прокачано на {a[4]}", color=disnake.Color.random())
        abil[a[5]]+=a[4]
        abil["have"]-=a[4]
        await inter.response.edit_message(embed=embed, view=empty_view)
    elif a[3]=="down":
        if abil_s["canDown"]!=True:
            embed=disnake.Embed(title=f"*На этом сервере запрещено понижать таланты!", color=disnake.Color.red())
            await inter.response.edit_message(embed=embed, view=empty_view)
            return None
        if abil[a[5]]<a[4]:
            embed=disnake.Embed(title=f"У данного таланта меньше очков чем вы хотите забрать!", color=disnake.Color.red())
            await inter.response.edit_message(embed=embed, view=empty_view)
            return None
        embed=disnake.Embed(title=f"{a[0]} понижено на {a[4]}", color=disnake.Color.random())
        abil[a[5]]-=a[4]
        abil["have"]+=a[4]
        await inter.response.edit_message(embed=embed, view=empty_view)
    pl["talents"]=abil
    
# Commands

@bot.slash_command(name = "action", description="Выполнить какое либо действие для пользователей сервера👥")
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd(ctx, commandd: str = commands.Param(name="действие", description="Какое действие вы хотите выполнить?", choices=[disnake.OptionChoice("Погладить😻", "pat_action"), disnake.OptionChoice("Поцеловать😘", "kiss_action"), disnake.OptionChoice("Обнять🤗", "hug_action"), disnake.OptionChoice("Подмигнуть👁️", "wink_action")]), membur: disnake.Member = commands.Param(name="кого", description="Кого?")) -> None:
    global command_pressed
    command_pressed+=1
    print(f"action {ctx.guild.name}")
    if membur.id == ctx.author.id:
        await ctx.response.defer(ephemeral=True)
        await ctx.edit_original_response(":x:Нельзя делать действия сам с собой")
        return 0
    async with aiohttp.ClientSession() as session:
        if commandd == "wink_action":
            a = "Реакция - подмигнуть."
            b = "подмигнул(-а)"
            try:
                async with session.get("https://some-random-api.ml/animu/wink") as r:
                    if r.status == 200:
                        s_pre = await r.json()
                        s = s_pre["link"]
                    else:
                        await ctx.response.defer(ephemeral=True)
                        await ctx.edit_original_response(":question:Проблемы с API, попробуйте позже")
                        return 0
            except:
                await ctx.response.defer(ephemeral=True)
                await ctx.edit_original_response(":question:Проблемы с API, попробуйте позже")
                return 0
        elif commandd == "hug_action":
            a = "Реакция - обнятие."
            b = "обнял(-а)"
            try:
                async with session.get("https://nekos.life/api/v2/img/hug") as r:
                    if r.status == 200:
                        s_pre = await r.json()
                        s = s_pre["url"]
                    else:
                        await ctx.response.defer(ephemeral=True)
                        await ctx.edit_original_response(":question:Проблемы с API, попробуйте позже")
                        return 0
            except:
                await ctx.response.defer(ephemeral=True)
                await ctx.edit_original_response(":question:Проблемы с API, попробуйте позже")
                return 0
        elif commandd == "kiss_action":
            a = "Реакция - поцелуй."
            b = "поцеловал(-а)"
            try:
                async with session.get("https://nekos.life/api/v2/img/kiss") as r:
                    if r.status == 200:
                        s_pre = await r.json()
                        s = s_pre["url"]
                    else:
                        await ctx.response.defer(ephemeral=True)
                        await ctx.edit_original_response(":question:Проблемы с API, попробуйте позже")
                        return 0
            except:
                await ctx.response.defer(ephemeral=True)
                await ctx.edit_original_response(":question:Проблемы с API, попробуйте позже")
                return 0
            #s = random.choice(['https://media.discordapp.net/attachments/992431633544249403/992435168784695336/anime.gif','https://media.discordapp.net/attachments/992431633544249403/992435328096940072/kiss-anime.gif','https://media.discordapp.net/attachments/992431633544249403/992435816582369310/anime-cry-anime.gif','https://media.discordapp.net/attachments/992431633544249403/992435971016638504/good-morning.gif','https://media.discordapp.net/attachments/992431633544249403/992436114763808798/rakudai-kishi-kiss.gif','http://i.imgur.com/0D0Mijk.gif', 'http://i.imgur.com/TNhivqs.gif', 'http://i.imgur.com/3wv088f.gif', 'http://i.imgur.com/7mkRzr1.gif', 'http://i.imgur.com/8fEyFHe.gif', 'https://i.imgur.com/TBN5yWY.gif', 'https://i.imgur.com/UUuxJzq.gif', 'https://i.imgur.com/ivogXes.gif', 'https://i.imgur.com/YZAdekC.gif', 'https://i.imgur.com/ji6AZc2.gif', 'https://i.imgur.com/TEHAPd6.gif', 'https://i.imgur.com/iTD9whO.gif', 'https://i.imgur.com/GEWFMuu.gif', 'https://i.imgur.com/OhlN3e6.gif', 'https://i.imgur.com/anRd2nB.gif', 'https://i.imgur.com/fmuzqfg.gif', 'https://i.imgur.com/mQhGc3c.gif', 'https://i.imgur.com/IeWHXZ1.gif', 'https://i.imgur.com/gVo9B7b.gif', 'https://i.imgur.com/VjhcFXP.gif', 'https://i.imgur.com/KbY8A4c.gif', 'https://i.imgur.com/Uwpxpii.gif', 'https://i.imgur.com/mBZkGob.gif', 'https://i.imgur.com/fOqEnjX.gif', 'https://i.imgur.com/5xZySwF.gif', 'https://i.imgur.com/FcFHy6C.gif', 'https://i.imgur.com/H3L0eiR.gif', 'https://i.imgur.com/pU4DfAc.gif', 'https://i.imgur.com/RhZkqoH.gif', 'https://i.imgur.com/CNrADZg.gif', 'https://i.imgur.com/PEBfvGO.gif', 'https://i.imgur.com/Ac9x7bX.gif', 'https://i.imgur.com/EiTW8iL.gif', 'https://i.imgur.com/e0ep0v3.gif'])
        elif commandd == "pat_action":
            a = "Реакция - погладить."
            b = "погладил(-а)"
            try:
                async with session.get("https://nekos.life/api/v2/img/pat") as r:
                    if r.status == 200:
                        s_pre = await r.json()
                        s = s_pre["url"]
                    else:
                        await ctx.response.defer(ephemeral=True)
                        await ctx.edit_original_response(":question:Проблемы с API, попробуйте позже")
                        return 0
            except:
                await ctx.response.defer(ephemeral=True)
                await ctx.edit_original_response(":question:Проблемы с API, попробуйте позже")
                return 0
    await ctx.response.defer()
    embed = disnake.Embed(
    title=a,
    description=f"<@{ctx.author.id}> {b} <@{membur.id}>",
    colour=disnake.Colour.random()
    )
    embed.set_image(url=s)
    await ctx.edit_original_response(embed=embed)


@bot.slash_command(name = "dice", description="Игровые кости🎲")
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd_dice(ctx, commandd: str = commands.Param(name="формула", description="Формула для вашего броска!")) -> None:
    state=False
    db = SqliteDict("example.sqlite", f"ch-{ctx.channel.id}",autocommit=True)
    pl = SqliteDict("example.sqlite", f"{ctx.guild.id}-{ctx.author.id}",autocommit=True)
    #state:bool=commands.Param(default=False,name="ввод", description="Показывать результат кубиков?")
    global command_pressed
    command_pressed+=1
    commandd=commandd.replace("__import__",'').replace("__file__",'')
    await ctx.response.defer()
    print(f"Dice {ctx.guild.name}")
    a = commandd
    global p
    p = commandd
    global end, cend
    cend=0
    end=[]
    def main(x: str):
        global end, cend
        def check(j, m, r_s):
                if r_s==20:
                    return 0
                if j == m:
                    c.append(f"**{j}**")
                    if m>=0:
                        r_s+=1
                        return check(random.randint(1, m), m, r_s) + j
                    elif m<0:
                        r_s+=1
                        return check(random.randint(m, 0), m, r_s) + j
                else:
                    c.append(f"{j}")
                return j
        c=[]
        r_s=0
        res=0
        x=x.group().split("d")
        if x[0]=='': x[0]=1
        if x[1].find("!") != -1:
            x[1]=x[1].replace("!", '')
            if int(x[0]) > 20 or int(x[1]) > 1000 or int(x[1])==0:
                end.append(str("(Limit error)"))
                return "(Limit error)"
            for i in range(int(x[0])):
                if int(x[1])>=0:
                    res+=check(random.randint(1, int(x[1])), int(x[1]), r_s)
                elif int(x[1])<0:
                    res+=check(random.randint(int(x[1]), 0), int(x[1]), r_s)
            end.append(str(c).replace("'", ""))
            return str(res)
        if int(x[0]) > 20 or int(x[1]) > 1000 or int(x[1])==0:
                end.append(str("(Limit error)"))
                return "(Limit error)"
        for i in range(int(x[0])):
                if int(x[1])>=0:
                    r=random.randint(1, int(x[1]))
                    res+=r
                    c.append(r)
                elif int(x[1])<0:
                    r=random.randint(int(x[1]), 0)
                    res+=r
                    c.append(r)
        end.append(str(c))
        return str(res)
    def fate(x: str):
        global end, cend
        d=x.group().split('d')
        res=0
        c=[]
        if d[0]=='': d[0]=1
        if int(d[0]) > 20:
            end.append(str("(Limit error)"))
            return "(Limit error)"
        for i in range(int(d[0])):
            r=int(random.choice(["-1", "0","1"]))
            res+=r
            c.append(r)
        end.append(str(c))
        return str(res)
    def func2(x):
        x=x.group().replace("&", '').split("_")
        try:
            my_list = pl["items"]
        except:
            pl["items"]=[]
        
        for i in my_list:
            if i["name"] == x:
                return str(i["value"])
        return "(Item error)"
    def func2_count(x):
        x=x.group().replace("&", '').split("_")
        x = x[0]
        try:
            my_list = pl["items"]
        except:
            pl["items"]=[]
        
        for i in my_list:
            if i["name"] == x:
                return str(i["count"])
        return "(Item error)"
    def func2_mod(x):
        x=x.group().replace("&", '').split("_")
        x = x[0]
        try:
            my_list = pl["items"]
        except:
            pl["items"]=[]
        
        for i in my_list:
            if i["name"] == x:
                return str(i["mod"])
        return "(Item error)"
    def func2_opis(x):
        x=x.group().replace("&", '').split("_")
        x = x[0]
        try:
            my_list = pl["items"]
        except:
            pl["items"]=[]
        
        for i in my_list:
            if i["name"] == x:
                return str(i["opis"])
        return "(Item error)"
    def func_set_f(x):
            global end, cend
            c=end[cend]
            cend+=1
            return c
    def talents_c(x):
        x=x.group().replace("%", "")
        try:
            my_list_s = db["talents"]
        except:
            db["talents"]={"canDown": True, "def":5,'1':'Сила', '2':'Ловкость', '3':'Интелект', '4':'-', '5':'-', '6':'-', '7':'-', '8':'-', '9':'-', '10':'-'}
        
        try:
            my_list = pl["talents"]
        except:
            pl["talents"]={'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, '10':0, 'have':db["talents"]["def"]}
        
        try:
            if my_list_s[x] != '-':
                return str(my_list[x])
            else:
                raise KeyError("error")
        except:
            return "(Talents error)"

    a = re.sub("&[^_&]+_mod&", func2_mod,a, flags=re.IGNORECASE)
    a = re.sub("&[^_&]+_count&", func2_count,a, flags=re.IGNORECASE)
    a = re.sub("&[^_&]+_op&", func2_opis,a, flags=re.IGNORECASE)
    a = re.sub("&[^_&]+&", func2,a, flags=re.IGNORECASE)
    a = re.sub("\d*d\d+[!]*", main, a, flags=re.IGNORECASE)
    a = re.sub("\d*df", fate, a, flags=re.IGNORECASE)
    for i in ['1', "2", "3", "4", "5", '6', '7', '8', '9', '10']:
        a = re.sub(f"%{i}%", talents_c, a, flags=re.IGNORECASE)
    b = re.sub("\d*d\d+[!]*", func_set_f, p, flags=re.IGNORECASE)
    b = re.sub("\d*df", func_set_f, p, flags=re.IGNORECASE)
    def s(x):
        setv={}
        #Доп комманды
        def If(x,true,false):
            r=eval(str(x).replace("__import__",''))
            if r == True:
                return true
            elif r == False:
                return false
        def pick(*a):
            return random.choice(a)
        def pickn(n, *a):
            res=[]
            for i in range(int(n)+1):
                res.append(random.choice(f"\{a}"))
            return "".join(res)
        def set(x,v):
            setv[v]=x
            return x
        def get(x):
            return setv[x]
        def find(x, n):
            return len(re.findall(n,x))
        # Конец
        try:
            return str(eval(x.group().lower().replace("//", '').replace("if", "If")))
        except Exception as e:
            print(e)
            if e == "division by zero":
                return "0"
            if x.group().replace("//", '') == "(Limit error)":
                return "(Limit error)"
            return "(Math error)"
    a = re.sub("//(.*?)//", s,a)
    if state==True:
        embed = disnake.Embed(
    title="Dice - ответ",
    description="Вывод: "+str(a)+"\n"+f"Ввод: {p}",
    color=disnake.Colour.random()
    )
    elif state==False:
        embed = disnake.Embed(
    title="Dice - ответ",
    description=str(a).replace("\\n", '\n'),
    color=disnake.Colour.random()
    )
    embed.set_footer(
    text=f"От {ctx.author.name}. С примером {commandd}"
    )
    await ctx.edit_original_response(embed=embed)

@bot.slash_command(name = "info", description="Информация-Помощь об боте!")
@commands.cooldown(1, 3, commands.BucketType.user)
async def commandd_info(ctx) -> None:
    await ctx.response.defer(ephemeral=True)
    print(f"Help/info {ctx.guild.name}")
    await ctx.edit_original_response(embed=emhelp,components=eff)
@bot.listen("on_dropdown")
async def fav_animal_listener(inter: disnake.MessageInteraction):
    match inter.component.custom_id:
        case "help_drop":
            match inter.values[0]:
                case "coms": await inter.response.edit_message(embed=emcoms,components=cf)
                case "dice": await inter.response.edit_message(embed=emdice)
                case "item": await inter.response.edit_message(embed=emitem)
                case "talent": await inter.response.edit_message(embed=emtalent)
                case _: await inter.response.edit_message(embed=emhelp)
        case "setts_drop":
            match inter.values[0]:
                case "achi": await inter.response.edit_message(embed=fachi)
                case "channel": await inter.response.edit_message(embed=fchan)
                case "item": await inter.response.edit_message(embed=fitemm)
                case "talent": await inter.response.edit_message(embed=ftalents)
                case "time": await inter.response.edit_message(embed=ftime)
                case "dice": await inter.response.edit_message(embed=fdice)
                # -
                case "exit": await inter.response.edit_message(embed=emhelp,components=eff)


# Loops

@tasks.loop(seconds=60.0)
async def taskers():
    try:
        await bot.change_presence(activity=disnake.Activity(
        name=f"Версия 2.13 | {round(bot.latency * 1000)} мс",
        type=disnake.ActivityType.watching,
        ))
    except: ...

@tasks.loop(seconds=60.0)
async def taskss():
    try:
        messagess = await bot.get_guild(995086034058608711).get_channel(995093281165824060).fetch_message(1062262356073271316)
        guilds = bot.guilds
        member_count = 0
        for guild in guilds:
            member_count += guild.member_count
        process = psutil.Process()
        memory_info = process.memory_info()
        current_memory_usage = memory_info.rss / 1024 / 1024
        max_memory_usage = psutil.virtual_memory().total / 1024 / 1024
        bot_cpu_percent = process.cpu_percent()
        #embed
        embed = disnake.Embed( 
        title="🤖 | Статус бота",
        description=f'''*💻Время запуска:* <t:{time_start}:f>
*💻Последнее обновление:* <t:{round(time.time())}:R>
*⚙️Команд обработано:* {command_pressed}
*📨Задержка:* {round(bot.latency * 1000)}мс
*<:events:1063499816358903848>Количество серверов:* {len(guilds)}
*<:all_members:1063499568664285196>Все пользователи:* {member_count}
*💾ОЗУ:* {current_memory_usage:.2f} MB / {max_memory_usage:.2f} MB
*🧠ЦПУ:* {bot_cpu_percent:.2f}% / 100.00%
*💻OS:* {platform.system()}
*🐍Python:* {platform.python_version()}
        ''',
        colour=disnake.Colour.random()
        )
        embed.set_footer(text=f"Обновление статуса каждую минуту!")
        embed.set_thumbnail(url=bot.get_user(871424169013829672).avatar.url)
        await messagess.edit(embed=embed)
    except Exception:
        pass

@tasks.loop(seconds=60.0)
async def taskse():
    for i in bot.guilds:
        db = SqliteDict("example.sqlite", f"{i.id}",autocommit=True)
        try:
            db["time_m"]=db["time_m"] + db["time_s"]
            if db["time_m"] >= 60:
                db["time_m"]=db["time_m"] - 60
                db["time_h"]=db["time_h"] + 1
                if db["time_h"] >= 24:
                    db["time_h"]=0
        except KeyError:
            db["time_m"]=0
            db["time_s"]=10
            db["time_h"]=0
            db["time_m"]=db["time_m"] + db["time_s"]
            if db["time_m"] >= 60:
                db["time_m"]=0
                db["time_h"]=db["time_h"] + 1
                if db["time_h"] >= 24:
                    db["time_h"]=0

def site():
    from nicegui import ui,Client
    import psutil
    import asyncio, threading
    from os import getcwd
    #page
    def check_ping(a):
        if int(a)<=80:
            return "background: rgb(61,87,62);"
        elif int(a)<=120:
            return "background: rgb(87,87,61);"
        elif int(a)>120:
            return "background: rgb(87,61,61);"
    def disc_usage():
        def market_os(count, r: int = 1):
            if count // (1024 ** 4) > 0:
                text = f"{round(count / (1024 ** 4), r)}TB"
            if count // (1024 ** 4) == 0:
                text = f"{round(count / (1024 ** 3), r)}GB"
            if count // (1024 ** 3) == 0:
                text = f"{round(count / (1024 ** 2), r)}MB"
            if count // (1024 ** 2) == 0:
                text = f"{round(count / 1024, r)}KB"
            return text
        disc = psutil.disk_usage(getcwd())
        used = disc.used
        total = disc.total
        memory = psutil.virtual_memory()
        network = [i.bytes_sent for i in {"network": psutil.net_io_counters()}.values() if i.bytes_sent != 0][0]
        cp = round(psutil.cpu_percent(interval=1))
        disc_text = f"{market_os(used, 1)} / {market_os(total, 1)}"
        network_text = f"{market_os(network)}"
        mtot_text = f"{market_os(memory.used)} / {market_os(memory.total)}"

        return [disc_text, f"{cp}%", network_text, f"{mtot_text}"]
    @ui.page('/')
    async def init_page(client:Client):
        client.content.classes('px-0')
        load=ui.spinner(size='lg',color="green").style("position: absolute;top: 50%;left: 50%;margin: -25px 0 0 -25px;")
        await client.connected()
        print("User connected: "+client.ip)
        @ui.refreshable
        def mainds():
            guilds=[]
            member_count=0
            for i in bot.guilds:
                guilds.append(f"{i}")
            member_count = 0
            for guild in bot.guilds:
                member_count += guild.member_count
            a, b, c, d = disc_usage()
            with ui.row().style("flex-wrap: nowrap;").classes("absolute-center justify-center w-screen pb-[490px] text-4xl font-semibold "):
                ui.label(f"{bot.user.name} DashBoard").classes("bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500")
            with ui.row().style("flex-wrap: nowrap;").classes("absolute-center justify-center w-screen"):
                with ui.card().style(check_ping(str(round(bot.latency * 1000)))).classes('aspect-auto no-shadow'): #w-99 h-52 
                        with ui.row().style("flex-wrap: nowrap;"):
                            ui.icon('smart_toy', color='primary').classes('text-4xl')
                            #with ui.column().classes('q-pr-xl'):
                            with ui.scroll_area().classes('w-80 h-44 text-base'):
                                with ui.row():
                                    ui.label("Количество серверов: ")
                                    ui.label(str(len(guilds)))
                                with ui.row():
                                    ui.label("Количество юзеров: ")
                                    ui.label(str(round(member_count/1000, 1))+" тыс.")
                                with ui.row():
                                    ui.label("Использовано комманд: ")
                                    ui.label(f"{command_pressed}".replace("000", "к"))
                                with ui.row():
                                    ui.label("Задержка: ")
                                    try:
                                        ui.label(str(round(bot.latency * 1000))) #bot.latency
                                    except: ui.label("0")
                with ui.card().style("background: rgb(76,94,186,0.7);").classes('aspect-auto no-shadow'): #q-pr-xl h-52
                        with ui.row().style("flex-wrap: nowrap;"):
                            ui.icon('dns', color='primary').classes('text-4xl')
                            with ui.scroll_area().classes('w-80 text-base'): # h-52
                                for i in guilds:
                                    ui.label(i)               
                with ui.card().style("background: linear-gradient(90deg, rgba(76,94,186,0.7) 2%, rgba(41,41,41,1) "+b+");").classes('aspect-auto no-shadow'): #w-99 h-52 
                        with ui.row().style("flex-wrap: nowrap;"):
                            ui.icon('developer_board', color='primary').classes('text-4xl')
                            #with ui.column().classes('q-pr-xl'):
                            with ui.scroll_area().classes('w-96 h-44 text-base'):
                                ui.label("Занятое пространство: "+a)
                                ui.label("Протребление Памяти: "+a)
                                ui.label("Занятость процессора: "+b)
                                ui.label("Потребление Интернета: "+c)
        mainds()
        load.visible=False
        async def funct():
            while True:
                mainds.refresh()
                await asyncio.sleep(5)
        await funct()
    ui.run(title="DashBoard", dark=True, reload=False,show=False, port=1480)
t1=threading.Thread(target=site, daemon=True)
t1.start()

bot.run("ODcxNDI0MTY5MDEzODI5Njcy.GASZTG.-9EkQx9xoFjBgkFG0EgsWoXkoPgM43gpw595-8")