import discord
from discord import message
from discord import member
from discord.ext import commands
from discord.ext.commands import Bot
from discord import member
import os
import shutil
import sys
import mysql
import mysql.connector
from mysql.connector import Error
client = commands.Bot(command_prefix = '!')

num_delo = 4
pl1 = None
pl2 = str()
st = str()
more = str()
nick = str()
verd = str()
sost = str('открыто')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Streaming(name="By GODMOD, special thx ModerNik", url="https://www.twitch.tv/nullexcept1on"))

@client.command()
async def иск(ctx):
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='bof'
        )
        cursor = connection.cursor()
    
        global num_delo
        nick = ctx.author.display_name
        pl1 = ctx.author.id

        await ctx.reply('Укажите ник игрока (User#0000)')
        print(pl1)
        def check(q):
            return q.author.id == pl1
        msg = await client.wait_for('message', check=check)
        print (msg.content+' это дс наушителя')
        pl2 = str(msg.content)

        await ctx.reply('Укажите возможные статьи. Если таковых нет - введите 0')
        def check2(w):
            return w.author.id == pl1
        msg2 = await client.wait_for('message', check=check2)
        print (msg2.content+' это статьи')
        st = msg2.content

        await ctx.reply('Опишите подробности дела')
        def check3(e):
            return e.author.id == pl1
        msg3 = await client.wait_for('message', check=check3)
        print (msg3.content+' это подобности дела')
        more = str(msg3.content)
        num_delo += 1

        embed = discord.Embed(
        title = '---------------------------------------------------------------------',
        colour = discord.Colour.dark_magenta()
        )
        embed.add_field(name='Дело:', value=num_delo, inline=False)
        embed.add_field(name='Подающий:', value='<@!'+str(pl1)+'>', inline=False)
        embed.add_field(name='Виновный:', value=pl2, inline=False)
        embed.add_field(name='Статьи:', value=st, inline=False)
        embed.add_field(name='Подробности:', value=more, inline=False)
        await ctx.channel.purge(limit=7)
        await ctx.channel.send(embed=embed)

        try:
            sql = '''INSERT INTO sud (pl1, pl2, st, more, disid, delosost) VALUES '''
            params = str(nick), str(pl2), str(st), str(more), str(pl1), str(sost)
            print(sql+ str(params))
            cursor.execute(sql+ str(params))
            connection.commit()
        except Exception as ex:
            print('ИСК')
            print(ex)
    except Error as e:
        print(f"The error '{e}' occurred")

@client.command()
async def вердикт(ctx):
    pl1 = ctx.author.id
    role = discord.utils.get(ctx.guild.roles, id=ROLE ID)
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='bof'
        )
        cursor = connection.cursor()
        delo = 0
        print(ctx.message.author.roles)
        if role in ctx.author.roles:
            await ctx.reply('Укажите номер дела')
            def check(r):
                return r.author.id == pl1
            answ = await client.wait_for('message', check=check)
            delo = answ.content

            await ctx.channel.send('Итог суда')
            def check(t):
                return t.author.id == pl1
            answ2 = await client.wait_for('message', check=check)
            verd = answ2.content
            embed = discord.Embed(
            title = '---------------------------------------------------------------------',
            colour = discord.Colour.dark_magenta()
            )
            embed.add_field(name='Дело:', value=delo, inline=False)
            embed.add_field(name='Вердикт:', value=verd, inline=False)
            await ctx.channel.purge(limit=5)
            await ctx.channel.send(embed=embed)

        try:
            sqlupdate = "UPDATE sud SET verd = '"+ str(verd) + "' " + '''WHERE id = ''' + "'" + str(delo) + "'"
            sqlupdate2 = "UPDATE sud SET delosost = 'закрыто' " + '''WHERE id = ''' + "'" + str(delo) + "'"
            print(sqlupdate)
            cursor.execute(sqlupdate)
            connection.commit()
            cursor.execute(sqlupdate2)
            connection.commit()
        except Exception as ex:
            print('ВЕРДИКТ')
    except Exception as ex:
        print('ВЕРДИКТ')

@client.command()
async def дело(ctx, *, deloansw):
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='bof'
        )
        cursor = connection.cursor()
        print(deloansw)
        try:
            cursor.execute("SELECT * FROM sud WHERE id='%s'" % (deloansw))
            rows = cursor.fetchall()
            print(rows)
            for row in rows:
                embed = discord.Embed(
                title = '---------------------------------------------------------------------',
                colour = discord.Colour.dark_magenta()
                )
                embed.add_field(name='Дело:', value=row[0], inline=False)
                embed.add_field(name='Подающий:', value='<@!'+row[6]+'>', inline=False)
                embed.add_field(name='Виновный:', value=row[2], inline=False)
                embed.add_field(name='Статьи:', value=row[3], inline=False)
                embed.add_field(name='Подробности:', value=row[4], inline=False)
                embed.add_field(name='Вердикт:', value=row[5], inline=False)
                embed.add_field(name='Состояние:', value=row[7], inline=False)
                await ctx.channel.purge(limit=1)
                await ctx.channel.send(embed=embed)
        except Error as e:
            print(f"The error '{e}' occurred")
    except Error as e:
        print(f"The error '{e}' occurred")

@client.command()
async def отменить(ctx):
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='bof'
        )
        cursor = connection.cursor()
        pl1 = ctx.author.id
        await ctx.reply('Укажите номе дела')
        def check(r):
            return r.author.id == pl1
        deloinfoansw = await client.wait_for('message', check=check)
        deloansw = deloinfoansw.content
        try:
            cursor.execute("SELECT disid FROM sud WHERE id = " + deloansw)
            rows = cursor.fetchall()
            print(str(rows)[3:-4])
            if str(rows)[3:-4] == str(pl1) or (pl1 == 296343158826991628 or pl1 == 446964150472802316 or pl1 == 437426147161276417):
                cursor.execute("DELETE FROM sud WHERE id = " + deloansw)
                connection.commit()
                await ctx.channel.send('удалено!')
            else:
                await ctx.channel.send('у вас нет прав')
        except Error as e:
            print('ОТМЕНА')
            print(f"The error '{e}' occurred")
    except Error as e:
        print('ОТМЕНА')
        print(f"The error '{e}' occurred")

@client.command()
async def заявки(ctx):
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='bof'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sud WHERE delosost='открыто'")
        rows = cursor.fetchall()
        print(rows)
        for row in rows:
            embed = discord.Embed(
            title = '---------------------------------------------------------------------',
            colour = discord.Colour.dark_magenta()
            )
            embed.add_field(name='Дело:', value=row[0], inline=False)
            embed.add_field(name='Подающий:', value='<@!'+row[6]+'>', inline=False)
            embed.add_field(name='Виновный:', value=row[2], inline=False)
            embed.add_field(name='Статьи:', value=row[3], inline=False)
            embed.add_field(name='Подобности:', value=row[4], inline=False)
            embed.add_field(name='Вердикт:', value=row[5], inline=False)
            await ctx.channel.send(embed=embed)
    except Error as e:
        print(f"The error '{e}' occurred")
        
client.run('???')
#!новое дело
#Tesaurus#0294
#1.3
#бла бла бла бла
#.решение
#. _.
