from ast import arg
from datetime import date
import os
from sys import argv
import requests
import json
from colorama import Fore
import socket

resolvedRelatedIps = set()
resolvedSubdomains = set()
resolvedBruteForce = dict()


VT_API_KEY = 'YOUR-API-KEY'

def welcome():
    print(Fore.YELLOW + """
         z$$$$P
        d$$$$"
      .$$$$$"
     z$$$$$"
    z$$$$P
   d$$$$$$$$$$"
  *******$$$"
       .$$$"
      .$$"
     4$P"
    z$"
   zP
  z"
 /""")
    print(f"{Fore.LIGHTMAGENTA_EX}< Welcome to {Fore.LIGHTYELLOW_EX}thund3r {Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTYELLOW_EX + os.getlogin() + Fore.LIGHTMAGENTA_EX}] >\n{Fore.LIGHTMAGENTA_EX}[{Fore.WHITE}?{Fore.LIGHTMAGENTA_EX}] Domain example: {Fore.LIGHTYELLOW_EX}google.com  {Fore.LIGHTMAGENTA_EX}->{Fore.LIGHTYELLOW_EX} [ *.* ] {Fore.LIGHTMAGENTA_EX}[{Fore.WHITE}?{Fore.LIGHTMAGENTA_EX}]\n")

def VirusTotal(domain):
    # Headers for the HTTP (GET) Request.
    HEADERS = {
    "Accept": "application/json",
    "x-apikey": VT_API_KEY
    }

    # Old & Related IP Addresses from {domain}.
    urlLastIps = f"https://www.virustotal.com/api/v3/domains/{domain}/resolutions"
    data = json.loads(requests.get(urlLastIps,headers=HEADERS).text)
    for resolution in data['data']:
        resolvedRelatedIps.add(resolution['attributes']['ip_address'])

    # VirusTotal's subdomain finder.
    urlSubdomains = f"https://www.virustotal.com/api/v3/domains/{domain}/relationships/subdomains?limit=40"
    data = json.loads(requests.get(urlSubdomains,headers=HEADERS).text)
    for resolution in data['data']:
        resolvedSubdomains.add(resolution['id'])

def BruteSubdomains(domain):
    subdomains = ["www", "www2", "dashboard", "anycast", "admin", "app", "panel", "embed", "autoconfig", "autodiscover", "private", "mail", "direct", "direct-connect", "cpanel", "ftp", "pop", "imap", "forum", "blog", "portal", "beta", "dev", "webmail", "record", "ssl", "dns", "ts3", "m", "mobile", "help", "wiki", "client", "server", "api", "i", "x", "cdn", "images", "my", "java", "swf", "smtp", "ns", "ns1", "ns2", "ns3", "mx", "server1", "server2", "test", "vpn", "secure", "login", "store", "shop", "zabbix", "cacti", "mysql", "search", "monitor", "nagios", "munin", "data", "old", "stat", "stats", "preview", "phpmyadmin", "db", "demo", "status", "gateway", "gateway1", "gateway2", "node", "mc", "play", "jogar", "serie", "tienda", "build", "buildteam", "new", "news", "ftb", "na", "us", "eu", "pr", "ts", "staff", "register", "ftb", "serie", "download", "descarga", "downloads", "descargas", "vm", "multicraft", "forums", "ssh", "administrator", "email", "access", "home", "game", "gaming", "idiom", "developer", "support", "photos", "app", "foro", "discord", "backup", "config", "demo", "web", "ban", "bans", "en", "ca", "ads", "ad", "archive", "es", "cloud", "developers", "development", "go", "host", "premium", "ded1", "ded", "dedi1", "dedi", "server01", "servidor", "dedicado", "dedicated", "nodo", "donate", "donaciones", "minecraft", "mc01", "mc02", "ayuda", "nl", "documentation", "ip", "sql", "priv", "redirect", "hg", "pixelmon", "ips", "server3", "dash", "www1", "menu", "hub", "inicio", "node01", "buy", "vote", "votar", "contact", "contacto", "guide", "guia", "baneos", "user", "info", "proxy", "proxy01", "proxy1", "mx1", "pay", "bb", "in", "as", "payment", "fun", "redirection", "lobby", "sv", "sv01", "sv1", "1", "2", "3", "01", "02", "03", "s1", "s2", "s", "d", "d1", "team", "ca1", "fr", "fr1", "pvp", "auth", "usk", "usk1", "domain", "img", "join", "stores", "tiendas", "mc1", "mc2", "mc3", "mc4", "mc5", "mc6", "mc7", "mc8", "mc9", "mc10", "mc11", "mc12", "mc8", "dox", "ozr", "ozr1", "manager", "manage", "vps", "vps1", "vps01", "t", "f", "fairness", "verify", "pass0", "service", "services", "service01", "service1", "services01", "services1", "srv", "srv1", "srv01", "ve", "br", "sys", "donatii", "survival", "mega", "ggtx", "uhc", "toxic", "open", "sf", "sf1", "sf01", "pixel", "ru", "node-2", "node-1", "node-01", "node-02", "sys1", "api1", "yt", "yt1", "apixelados", "youtube", "youtube1", "youtube01", "servidor1", "servidor2", "servidor01", "servidor02", "game1", "u", "prox.1", "prox", "prox1", "prox01", "uhc1", "ded.1", "de", "bungee", "bungeecord", "bungeecord1", "bungeecord01", "bungee1", "bungee01", "ovh", "ovh1", "ovh01", "ca-01", "ca-1", "builds", "mysql-1", "mysql-01", "srv-01", "srv-1", "srv-02", "srv-03", "mclogin", "zeusproxy", "ecplise", "craftbukkit", "spigot", "ovh2", "ovh3", "antiddos", "vs", "primary", "secondary", "one", "two", "testing", "tester", "mcauth", "proxypipe", "sql1", "sql01", "network", "la", "ar", "arg", "cl", "partner", "partners", "example", "prueba", "shoping", "privatevps", "members", "users", "vpn1", "vpn01", "dev1", "dev01", "build1", "build01", "subdomain", "canada", "france", "francia", "europa", "europe", "database", "database1", "database01", "ms", "ping", "suscribe", "su", "enter", "loja", "privado", "anuncio", "anuncios", "announce", "announces", "appeals", "appeal", "reports", "report", "bteam", "whitelist", "plugin", "script", "cloudfare", "pueblo", "pp", "cf", "skype", "contactanos", "contactar", "0", "mojang", "apelar", "code", "coder", "ww0", "ww1", "ww2", "port", "porta", "puerto", "ports", "puertos", "vnc", "putty", "ssh1", "ssh01", "root", "craft", "launcher", "voting", "voteserver", "servervote", "votos", "play1", "play01", "tekkit", "fml", "forge", "configurando", "configuracion", "configuration", "files", "us1", "na1", "eu1", "na01", "eu01", "us01", "mcna", "mcna1", "mcna01", "mceu", "mceu1", "mceu01", "ovhgame", "ovhgame1", "ovhgame01", "ovhgaming", "ovhgaming1", "ovhgaming01", "gameovh", "gamingovh", "gameovh01", "gameovh1", "gamingovh1", "gamingovh01", "govh", "ovhg", "root1", "root01", "tos", "terms", "comprar", "bot", "antibot", "antibots", "bots", "sw1", "sw01", "sw", "faction", "factions", "skywars", "serv1", "serv2", "serv01", "serv02", "serv", "buycraft", "mod", "mods", "hosting", "multicraft1", "multicraft01", "events", "event", "ipv4", "ipv6", "irc", "cdn1", "d1", "d2", "d01", "d02", "n1", "n2", "n01", "n02", "webdisk", "jouer", "facebook", "twitter", "serveur", "prive", "serveur1", "serveur2", "serveur01", "serveur02", "reset", "resetpassword", "password", "passwordreset", "js", "html", "php", "bungee-1", "bungee-2", "bungee-01", "bungee-02", "proxy-1", "proxy-2", "proxy-01", "proxy-02", "alpha", "vps-1", "vps-2", "vps-01", "vps-02", "mysql1", "mysql01", "mysql2", "mysql02", "ftp1", "ftp2", "ftp01", "ftp02", "ftp-1", "ftp-2", "ftp-01", "ftp-02", "ssh-1", "ssh-01", "ssh-2", "ssh-01", "error", "base", "pl", "25565", "bd", "buildt", "python", "paypal", "donar", "apache", "windows", "window", "linux", "e-mail", "uk", "it", "telegram", "ovh-1", "ovh-2", "ovh-01", "ovh-02", "sa", "teste", "loja1", "xd", "teamspeak", "teamspeak3", "none", "sr", "git", "svn", "remote", "sip", "firewall", "iptable", "iptables", "correo", "intranet", "da", "track", "ftpd", "ftpadmin", "localhost", "mg", "msg", "radio", "pop3", "directory", "imagenes", "repo", "vip", "sg", "be", "ep", "test2", "drive", "gb", "sites", "jobs", "marketing", "mail2", "lyncdiscover", "ci", "jira", "painel", "mssql", "maquina", "maquinats", "lists", "ts2", "agenda", "web01", "web1", "gitlab", "github", "straight", "msoid", "calendar", "mobilemail", "jp", "ticket", "tickets", "voice", "ok", "entrar", "logueo", "loguearse", "system", "sistema", "control", "remoto", "net", "usuario", "usuarios", "miembros", "miembro", "bukkit", "spigot01", "spigot1", "spigot2", "spigot02", "hi", "hello", "world", "gob", "google", "media", "sign", "signin", "aiuto", "built", "sesion", "session", "connection", "connecting", "reconnect", "reconectar", "redirectip", "red", "redip", "redireccionar", "archivos", "video", "videos", "codificacion", "edit", "editar", "lol", "cpanel1", "cpanel01", "cpanel2", "cpanel02", "alts", "alt", "stress", "stresser", "bw", "bedwars", "bw1", "bw01", "bw2", "bw02", "sk", "skript", "luckperms", "lp", "rank", "webhost", "hostweb", "web-host", "community", "sync", "we", "bdd", "basededatos", "acceso1", "acceso2", "access1", "access2", "sadre", "eventteam", "et", "clan", "clans", "placeholder", "placeholderapi", "vote2", "vote3", "vote4", "vote1", "pe", "mco", "pebg", "cvote1", "cvote", "cvote2", "cvote3", "xen", "xenforo", "reader", "confluence", "storeassets", "violations", "c", "pc", "r53", "chidev", "staticassets", "ma", "me", "pedev", "rpsrv", "gamehitodrh", "xenon", "mcp", "mu", "paysafe", "social", "baneados", "rp", "samp", "shoprp", "wow", "holo", "imprint", "chatlog", "rp1", "rp01", "acp", "shop-admin", "l1", "l2", "l11", "dl", "msp", "impressum", "impresora", "front", "beta-karambyte", "store-assets", "merch", "wwww", "playa", "front2", "front1", "release", "pss", "mvn", "mariaum", "bugs", "bug", "pirata", "insanehg", "antigo", "maquina1", "maquina2", "maquina3", "maquina01", "maquina02", "master", "antiguo", "postularte", "logs", "clanseu", "clansus", "nfo", "nfoservers", "nfoserver", "apidoc", "2017", "2018", "2016", "2015", "2014", "feedback", "bp", "evidence", "forumlink", "storeredirect", "avatar", "uno", "dos", "tres", "cuatro", "node1", "node2", "node3", "node4", "node5", "node6", "node7", "node8", "node9", "node10", "node11", "node12", "node13", "node14", "node15", "node16", "node17", "node18", "node19", "node20", "node21", "node22", "sys2", "sys3", "sys4", "sys5", "s3", "ded2", "ded3", "ded4", "ded5", "ded6", "ded7", "ded8", "ded9", "ded10", "ded11", "ded12", "ded13", "ded14", "ded15", "ded16", "ded17", "ded18", "ded19", "ded20", "ded21", "ded22", "vps2", "vps3", "vps4", "vps5", "serieyt", "ytserie", "location", "mexico", "cuenta", "account", "sqlstats", "sqlstats1", "sqlstats2", "accounts", "accounts2", "accounts1", "server4", "sv2", "api1", "api01", "api2", "api02", "owlmessenger", "hg1", "hg2", "hg3", "hg4", "hg5", "sc", "za", "heroes", "il", "se", "studio", "kids", "kid", "consent", "rules", "tv", "gdata", "pex", "rip", "olds", "feedproxy", "docs", "apis", "contributor", "gmail", "hotmail", "boutique", "play-main", "depositos", "deposit", "depositar", "buycraft", "einkaufen", "negozio", "tent", "compra", "compras", "extras", "bart", "lisa", "eva", "xxx", "execute", "console", "consola", "v1", "ip1", "ip2", "ip01", "ip02", "beta1", "beta2", "de1", "de2", "de01", "de02", "dedic1", "dedic2", "dedic01", "dedic02", "cfr", "v2", "v01", "v02", "rat", "njrat", "fast", "gbps", "10gbps", "1gbps", "100mbps", "tienda1", "tienda2", "tienda01", "tienda02", "ipts", "iptv", "premium1", "premium2", "premium01", "premium02", "adminpanel", "paneladmin", "admpanel", "paneladm", "adm", "private1", "private2", "private01", "private02", "ovhvps", "ovhded", "ovhdedi", "panelovh", "ovhpanel", "unodo", "unodos", "unodo1", "unodo2", "unodos1", "unodos2", "nodos1", "nodos2", "nodos01", "nodos02", "run", "bin", "sbin", "boot", "lib", "mnt", "opt", "lib64", "tmp", "proc", "var", "pockets", "testforums", "changelog", "files1", "files2", "files01", "files02", "au", "ha", "ha1", "ha2", "ha3", "ha4", "ha5", "mercury", "neptune", "mars", "venus", "jupiter", "uranus", "saturn", "earth"]
    for name in subdomains:
        completed = name + "." + domain
        if completed not in resolvedSubdomains:
            try:
                ipv4 = str(socket.gethostbyname(completed))
                actual = resolvedBruteForce.get(ipv4)
                if actual is None:
                    actual  = [completed]
                else:
                    actual = actual + completed

                resolvedBruteForce.update({ipv4 : actual})
            except:
                pass

def PrintResults(domain):

    # Param '-s' to save results in a text file.
    if len(argv) > 1 and argv[1] == '-s':
        f = open(f"{domain}-{str(date.today())}.txt","w")


    # Results of Related IP Adresses [VirusTotal]
    print(f"{Fore.LIGHTMAGENTA_EX}\n[!] --- {Fore.LIGHTYELLOW_EX}Related IP Addresses found for the domain {Fore.LIGHTMAGENTA_EX}--- [!]")
    print(f"{Fore.LIGHTMAGENTA_EX}        Number of results found: {Fore.LIGHTYELLOW_EX + str(len(resolvedRelatedIps))}\n")
    for ip in resolvedRelatedIps:
        print(F"{Fore.LIGHTMAGENTA_EX} | :> {Fore.LIGHTYELLOW_EX + ip} ")
        if len(argv) > 1 and argv[1] == '-s':
            f.write(ip + "\n")

    # Results of Subdomains [VirusTotal]
    print(f"{Fore.LIGHTMAGENTA_EX}\n[!] --- {Fore.LIGHTYELLOW_EX}Subdomains found for the domain {Fore.LIGHTMAGENTA_EX}--- [!]")
    print(f"{Fore.LIGHTMAGENTA_EX}        Number of results found: {Fore.LIGHTYELLOW_EX + str(len(resolvedSubdomains))}\n")
    for domain in resolvedSubdomains:
        print(F"{Fore.LIGHTMAGENTA_EX} | :> {Fore.LIGHTYELLOW_EX + str(domain)} ")
        if len(argv) > 1 and argv[1] == '-s':
            f.write(str(domain) + "\n")

    # Results of Subdomains [BruteForce]
    keys = resolvedBruteForce.keys()
    print(f"{Fore.LIGHTMAGENTA_EX}\n[!] --- {Fore.LIGHTYELLOW_EX}Subdomain Bruteforce Dictionary {Fore.LIGHTMAGENTA_EX}[ip:[subdomain]]{Fore.LIGHTYELLOW_EX} found for the domain {Fore.LIGHTMAGENTA_EX}--- [!]")
    print(f"{Fore.LIGHTMAGENTA_EX}        Number of results found: {Fore.LIGHTYELLOW_EX + str(len(keys))}\n")

    for key in keys:
        print(F"{Fore.LIGHTMAGENTA_EX} | :> {Fore.LIGHTYELLOW_EX + key}  {Fore.LIGHTMAGENTA_EX}->  {Fore.LIGHTYELLOW_EX + str(resolvedBruteForce.get(key))}")
        if len(argv) > 1 and argv[1] == '-s':
            f.write(key + "-> " + str(resolvedBruteForce.get(key)) + "\n")

    # Close the file.
    if len(argv) > 1 and argv[1] == '-s':
        f.close()


def main():
    welcome()
    try:
        domain = input(Fore.LIGHTMAGENTA_EX + "[-] Domain: "+Fore.LIGHTYELLOW_EX)
        print(Fore.LIGHTMAGENTA_EX + f"[>] Looking up for {Fore.LIGHTYELLOW_EX + domain}" + Fore.LIGHTMAGENTA_EX + " please wait...")
        
        VirusTotal(domain)

        BruteSubdomains(domain)

        PrintResults(domain)
    except KeyboardInterrupt as e:
        print(Fore.RED + "\n[x] Leaving thund3r [x]" + Fore.RESET)

main()
print(Fore.RESET)
