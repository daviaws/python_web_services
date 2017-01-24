from aiohttp import web
import asyncio

IP = '10.100.11.12'
PORT = 3000

@asyncio.coroutine
def handle(request):
    name = request.match_info.get('name', "Anonymous") #Pega variável da rota - Se existir ou Anonymous
    text = "Hello, " + name
    return web.Response(text=text) #Retorna uma resposta

#Loop de evento do asyncio
loop = asyncio.get_event_loop()

#App server
app = web.Application()

#Criar handler do Server
handler = app.make_handler()

#Cria rotas
app.router.add_route('GET', '/', handle) #Rota fixa
app.router.add_route('GET', '/{name}', handle) #Rota com variável

#Asyncio cria o servidor
server = loop.create_server(handler, IP, PORT)
srv = loop.run_until_complete(server)

#Inicia loop do servidor
loop.run_forever()