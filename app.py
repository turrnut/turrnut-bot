import discord
import numpy as np
import os
import math
import datetime
import json
from blackjack import bj, bjhit, bjstand
import bruh
import random
import nacl
import time
import asyncio
import traceback
import interpreter as lang

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
from time import sleep

import chessdotcom
from chessdotcom import *

from discord import app_commands, ButtonStyle
from discord.ext import commands

from discord.ext.commands import Bot

# Features list:
#   1. randomly send greeting messages
#   2. predict grade (Slash)
#   3. logs
#   4. spam
#   5. SuS
#   6. say something (Slash)
#   7. MEME (Slash)
#   8. do math via EXINT (Slash)
#   9. NUKE
#   10. detect bad words
#   11. timeout
#   12. get user id
#   13. welcome message
#   14. fortune-telling (Slash)
#   15. turrnut bank (Slash only)
#   16. bank money manipulation
#   17. truth or dare (Slash only)
#   18. never have i ever (Slash only)
#   19. would you rather (Slash only)
#   20. add reactions
#

# Links that might be useful
# FFMPEG: https://stackoverflow.com/questions/63036753/discord-py-bot-how-to-play-audio-from-local-files
#

intents = discord.Intents.all()
client = Bot(command_prefix='?', intents=intents)

chessdotcom.Client.request_config['headers']['User-Agent'] = 'My Python Application. Contact me at victorconqueror@gmail.com'

react_all = []
chess = sorted(["TurrnutChess", "Jplay21", "Juffyball"], reverse=True)
elo = list(map(lambda person: get_player_stats(person).json["stats"]["chess_rapid"]["last"]["rating"], chess))
print(elo)
tree = client.tree
mensaje = None
logflag = True
curse_words = ("fags", "nigger", "chink", "nigga",
			   "faggot", "faggots", "retard", "fag",
			   "penis", "stfu", "shutup", "kys", "meth", "cock", "dick")
spamhalt = False
SERVER_NAME = ""
howmanywords = "20"
MYSERVER = "Turrnut Republic(拖鞋社)"
ADMIN = "977377574789472278" # turrnut
#ADMIN = "820541682415960064" # tuvalu (testing)
TREASURER = "964894108164423800" # mrgeaso
TREASURER = "720292051849314436" # tigerztacos
TREASURER = "778745923793584158" # juffyball
LIST = (ADMIN,
	TREASURER,
	"917059800154652732", # nickels(main)
	"1025854689142657055", # fork in soup
	"984242137879162920", # karma
	"874094518234923060", # garrett
	)
susflag = False
guilds = []
AWARD = 10 # now it's randomly 5-15 instead of a fixed number. Go to the daily function to change it
ignore_bad_words = (1112529128273477724,)
embec = 0x22B14C
orders = []

itemslist = [
	app_commands.Choice(name="British sleep tokens", value="bstok"),
	app_commands.Choice(name="Coal", value="coal"),
	app_commands.Choice(name="Diamond", value="diamond"),
	app_commands.Choice(name="Emerald", value="emerald"),
	app_commands.Choice(name="Ferret pets", value="ferret"),
	app_commands.Choice(name="Ferret toy weapons", value="ftoy"),
	app_commands.Choice(name="Gold", value="gold"),
	app_commands.Choice(name="Pickaxe", value="pick"),
	app_commands.Choice(name="Quartz", value="quartz"),
	app_commands.Choice(name="Russian War bonds", value="ruswarbonds"),
	app_commands.Choice(name="Turrnut Cars", value="car"),
	app_commands.Choice(name="Turrnut Homes", value="home"),
	app_commands.Choice(name="Turrnut Jr. Pumpkin Pie", value="ppslice"),
	app_commands.Choice(name="Turrnut Rings", value="ring"),
	app_commands.Choice(name="Turrnutium", value="turrnutium"),
	app_commands.Choice(name="TurrTaco", value="taco"),
	app_commands.Choice(name="TurrTanks", value="tank"),
	app_commands.Choice(name="Tuvaluan War Bonds", value="tvwarbonds"),
	app_commands.Choice(name="Tuvalunium", value="tuvalunium"),
]

# Generating a list of 200 G-rated, non-personal compliments/words of affirmation in a single line.
compliments = [
    "You're an incredible friend.", "Your positivity is infectious.", "You always make people smile.", 
    "You have a fantastic sense of humor.", "Your kindness is a balm to everyone you meet.", 
    "You're all kinds of awesome.", "You light up the room.", "You have a brilliant mind.", 
    "You're a great listener.", "You have a heart of gold.", "You inspire people.", 
    "Your creativity knows no bounds.", "You make a difference.", "You're a ray of sunshine.", 
    "You bring out the best in people.", "You're a true problem-solver.", "Your passion is contagious.", 
    "You always go the extra mile.", "You have a great outlook on life.", "You're as bright as a shooting star.", 
    "Your spirit is indomitable.", "You have an amazing work ethic.", "You're incredibly thoughtful.", 
    "Your empathy is a gift.", "You're wise beyond your years.", "You're fearless.", "You have a great sense of style.", 
    "Your enthusiasm is admirable.", "You're always learning.", "You're a natural leader.", 
    "You have a knack for making people feel cared for.", "You're so reliable.", "You have a refreshing perspective.", 
    "You're an excellent communicator.", "You're as courageous as a lion.", "You're a wellspring of ideas.", 
    "Your generosity knows no limits.", "You have impeccable manners.", "You're so resourceful.", 
    "You have the best laugh.", "You're a joy to be around.", "You're a beacon of hope.", "You're incredibly gracious.", 
    "Your optimism is inspiring.", "You have a magnetic personality.", "You're as lively as a spring day.", 
    "You're a treasure.", "You're a bundle of intelligence.", "You have a strong sense of justice.", 
    "You're as dependable as the sunrise.", "You're a breath of fresh air.", "You have a soothing presence.", 
    "You're full of wisdom.", "You're a master of kindness.", "You're a champion of others.", 
    "Your honesty is refreshing.", "You're as fun as a day at the beach.", "You're a star in the making.", 
    "You're a true friend.", "Your presence is calming.", "You're a burst of energy.", 
    "You're a visionary.", "You're as sweet as honey.", "You have an adventurous spirit.", 
    "You're a marvel at problem-solving.", "You're a joy to know.", "You have a great sense of fairness.", 
    "You're the epitome of kindness.", "You're a creativity powerhouse.", "You have a winning smile.", 
    "You're a role model.", "You're the heart and soul of the party.", "You have an infectious laugh.", 
    "You're a genius at making people feel welcome.", "You're as inspiring as a sunrise.", "You're a true gem.", 
    "Your resilience is astounding.", "You have an incredible talent for listening.", "You're a well of knowledge.", 
    "You're a fountain of creativity.", "You're as reliable as a Swiss watch.", "You're a bundle of joy.", 
    "You're a pillar of strength.", "You're a paragon of virtue.", "You have an eagle eye for detail.", 
    "You're the definition of courageous.", "You're a powerhouse of energy.", "You have a lion's heart.", 
    "You're a master at bringing people together.", "You're as quick as a whip.", "You're a beacon of light.", 
    "You're a wellspring of wisdom.", "You have a heart of courage.", "You're a marvel of patience.", 
    "You have a soothing voice.", "You're a burst of sunshine.", "You're a symbol of hope.", 
    "You're a champion of the underdog.", "You have a magical presence.", "You're as nurturing as nature.", 
    "You have a contagious enthusiasm.", "You're a living legend.", "You're a harbinger of good vibes.", 
    "You have a captivating presence.", "You're a well of generosity.", "You're a peacemaker.", 
    "You're as vibrant as a rainbow.", "You have a spirit of adventure.", "You're a dreamer and a doer.", 
    "You have an angelic patience.", "You're a testament to hard work.", "You're a melody of kindness.", 
    "You're a symphony of creativity.", "You have an unshakeable spirit.", "You're a beacon of wisdom."]


wyr = ("Would you rather have the ability to see 10 minutes into the future or 150 years into the future?", "Would you rather have telekinesis (the ability to move things with your mind) or telepathy (the ability to read minds)?", "Would you rather team up with Wonder Woman or Captain Marvel?", "Would you rather be forced to sing along or dance to every single song you hear?", "Would you rather find true love today or win the lottery next year?", "Would you rather be in jail for five years or be in a coma for a decade?", "Would you rather have another 10 years with your partner or a one-night stand with your celebrity crush?", "Would you rather be chronically under-dressed or overdressed?", "Would you rather have everyone you know be able to read your thoughts or for everyone you know to have access to your Internet history?", "Would you rather lose your sight or your memories?", "Would you rather have universal respect or unlimited power?", "Would you rather give up air conditioning and heating for the rest of your life or give up the Internet for the rest of your life?", "Would you rather swim in a pool full of Nutella or a pool full of maple syrup?", "Would you rather labor under a hot sun or extreme cold?", "Would you rather stay in during a snow day or build a fort?", "Would you rather buy 10 things you don't need every time you go shopping or always forget the one thing that you need when you go to the store?", "Would you rather never be able to go out during the day or never be able to go out at night?", "Would you rather have a personal maid or a personal chef?", "Would you rather be 11 feet tall or nine inches tall?", "Would you rather have Beyoncé's talent or Jay-Z's business acumen?", "Would you rather be an extra in an Oscar-winning movie or the lead in a box office bomb?", "Would you rather vomit on your hero or have your hero vomit on you?", "Would you rather communicate only in emoji or never be able to text at all ever again?", "Would you rather be royalty 1,000 years ago or an average person today?", "Would you rather lounge by the pool or on the beach?", "Would you rather wear the same socks for a month or the same underwear for a week?", "Would you rather work an overtime shift with your annoying boss or spend full day with your mother-in-law?", "Would you rather cuddle a koala or pal around with a panda?", "Would you rather have a sing-off with Ariana Grande or a dance-off with Rihanna?", "Would you rather always have B.O. and not know it or always smell B.O. on everyone else?", "Would you rather watch nothing but Hallmark Christmas movies or nothing but horror movies?", "Would you rather always be 10 minutes late or always be 20 minutes early?", "Would you rather spend a week in the forest or a night in a real haunted house?", "Would you rather find a rat in your kitchen or a roach in your bed?", "Would you rather have a pause or a rewind button in your life?", "Would you rather always have a full phone battery or a full gas tank?", "Would you rather lose all your teeth or lose a day of your life every time you kissed someone?", "Would you rather drink from a toilet or pee in a litter box?", "Would you rather be forced to live the same day over and over again for a full year, or take 3 years off the end of your life?", "Would you rather never eat watermelon ever again or be forced to eat watermelon with every meal?", "Would you rather get a paper cut every time you turn a page or bite your tongue every time you eat?", "Would you rather oversleep every day for a week or not get any sleep at all for four days?", "Would you rather die in 20 years with no regrets or live to 100 with a lot of regrets?", "Would you rather sip gin with Ryan Reynolds or shoot tequila with Dwayne \"The Rock\" Johnson?", "Would you rather get trapped in the middle of a food fight or a water balloon fight?", "Would you rather walk to work in heels or drive to work in reverse?", "Would you rather spend a year at war or a year in prison?", "Would you rather die before or after your partner?", "Would you rather have a child every year for 20 years or never have any children at all?", "Would you rather take amazing selfies but look terrible in all other photos or be photogenic everywhere but in your selfies?", "Would you rather be gassy on a first date or your wedding night?", "Would you rather Danny DeVito or Danny Trejo play you in a movie?", "Would you rather be able to take back anything you say or hear any conversation that is about you?", "Would you rather have skin that changes color based on your emotions or tattoos appear all over your body depicting what you did yesterday?", "Would you rather hunt and butcher your own meat or never eat meat again?", "Would you rather lose all of your friends but keep your BFF or lose your BFF but keep the rest of your buds?", "Would you rather have people spread a terrible lie about you or have people spread terrible but true tales about you?", "Would you rather walk in on your parents or have them walk in on you?", "Would you rather be the absolute best at something that no one takes seriously or be average at something well respected?", "Would you rather have unlimited battery life on all of your devices or have free WiFi wherever you go?", "Would you rather have Billie Eilish's future or Madonna's legacy?", "Would you rather have a third nipple or an extra toe?", "Would you rather solve world hunger or global warming?", "Would you rather have to wear every shirt inside out or every pair of pants backward?", "Would you rather live in a treehouse or in a cave?", "Would you rather win $25,000 or your best friend win $100,000?", "Would you rather be in history books for something terrible or be forgotten completely after you die?", "Would you rather travel the world for free for a year or have $50,000 to spend however you please?", "Would you rather your to only be able to talk to your dog or for your dog to be able to talk to only you—and everyone thinks you're nuts?", "Would you rather have a mullet for a year or be bald (no wigs!) for six months?", "Would you rather go back to the past and meet your loved ones who passed away or go to the future to meet your children or grandchildren to be?", "Would you rather have Angelina Jolie's lips or with Jennifer Aniston's hair?", "Would you rather stay the age you are physically forever or stay the way you are now financially forever?", "Would you rather be in a zombie apocalypse or a robot apocalypse?", "Would you rather be alone all your life or surrounded by really annoying people?", "Would you rather give up your cellphone for a month or bathing for a month?", "Would you rather spend a day cleaning your worst enemy's house or have your crush spend the day cleaning your house?", "Would you rather spend a year entirely alone or a year without a home?", "Would you rather buy all used underwear or all used toothbrushes?", "Would you rather have a photographic memory or an IQ of 200?", "Would you rather go on a cruise with your boss or never go on vacation ever again?", "Would you rather forget your partner's birthday or your anniversary every year?", "Would you rather have to wear stilettos to sleep or have to wear slippers everywhere you go?", "Would you rather change the outcome of the last election or get to decide the outcome of the next election?", "Would you rather lose the ability to read or lose the ability to speak?", "Would you rather smooch Chris Pratt, Chris Pine, Chris Evans or Chris Hemsworth?", "Would you rather be beautiful and stupid or unattractive but a genius?", "Would you rather have seven fingers on each hand or seven toes on each foot?", "Would you rather work the job you have now for a year at double your current rate of pay or have one year off with what you are making now?", "Would you rather be always stuck in traffic but find a perfect parking spot or never hit traffic but always take forever to park?", "Would you rather have super-sensitive taste buds or super-sensitive hearing?", "Would you rather ask your ex or a total stranger for a favor?", "Would you rather go on tour with Elton John or Cher?", "Would you rather eat only pizza for a year or not eat any pizza for five years?", "Would you rather never get another present in your life but always pick the perfect present for everyone else or keep getting presents but giving terrible ones to everyone else?", "Would you rather sleep in a doghouse or let stray dogs sleep in your bed?", "Would you rather be able to speak any language or be able to communicate with animals?", "Would you rather have all of your messages and photos leak publicly or never use a cellphone ever again?", "Would you rather run at 100 mph or fly at 20 mph?", "Would you rather have Adele's voice or Normani's dance moves?", "Would you rather have to wear sweatpants everywhere for the rest of your life or never wear sweatpants again?", "Would you rather have 10,000 spoons when all you need is a knife or always have a knife but never be able to use spoons?", "Would you rather detect every lie you hear or get away with every lie you tell?", "Would you rather be the funniest person in a room or the smartest person in a room?", "Would you rather talk like Yoda or breathe like Darth Vader?", "Would you rather people knew all the details of your finances or all the details of your love life?", "Would you rather listen to your least-favorite song on a loop for a year or never listen to any music at all for a year?", "Would you rather go vegan for a month or only eat meat and dairy for a month?", "Would you rather clean up someone else's vomit or someone else's blood?", "Would you rather work for Michael Scott or Mr. Burns?", "Would you rather spend the weekend with pirates or ninjas?", "Would you rather end every phone call with \"I love you\" or accidentally call your partner the wrong name during a fight?", "Would you rather get your paycheck given to you in pennies or never be able to use cash again?", "Would you rather see Lady Gaga in a movie or see Bradley Cooper in concert?", "Would you rather win the lottery but have to spend it all in one day or triple your current salary forever?", "Would you rather live until you are 200 and look your age or look like you're 22 your whole life, but die at age 65?", "Would you rather give up cursing forever or give up ice cream for 12 years?", "Would you rather hear a comforting lie or an uncomfortable truth?", "Would you rather be locked for a week in a room that's overly bright or a room that's totally dark?", "Would you rather someone see all the photos in your phone or read all your text messages?  ", "Would you rather have a South Park-themed wedding or a Family Guy-themed funeral?", "Would you rather have to hunt and gather all of your food or eat McDonald's for every meal?", "Would you rather have fortune or fame?", "Would you rather celebrate the Fourth of July with Taylor Swift or Christmas with Mariah Carey?", "Would you rather only be able to listen to one song for the rest of your life or only be able to watch one movie for the rest of your life?", "Would you rather never use social media again or never watch another movie ever again?", "Would you rather have police hunting you down for a crime you didn't commit or a serial killer actually hunting you?", "Would you rather live a peaceful life in a small cabin in the woods or a drama-filled life in a mansion in a big city?", "Would you rather find your soulmate or your calling?", "Would you rather drink sour milk or brush your teeth with soap?", "Would you rather steal Duchess Meghan or Duchess Kate's style?", "Would you rather never get a cold ever again or never be stuck in traffic ever again?", "Would you rather be tall and average looking or three feet tall but beautiful?", "Would you rather visit the International Space Station for a week or spend a week in a hotel at the bottom of the ocean?", "Would you rather confess to cheating on your partner or catch your partner cheating on you?", "Would you rather have all traffic lights you approach be green or never have to stand in line again?", "Would you rather share an onscreen kiss with Leonardo DiCaprio or George Clooney?", "Would you rather never eat Christmas cookies ever again or never eat Halloween candy ever again?", "Would you rather lose your long-term memory or your short-term memory?", "Would you rather have a mullet or a perm?", "Would you rather be stranded in the jungle or in the desert?", "Would you rather everyone you love forget your birthday or everyone you love sing \"Happy Birthday\" to you for 24 hours straight?", "Would you rather be invisible or be able to fly?", "Would you rather spend every weekend indoors or spend every weekend outdoors?", "Would you rather party with Jennifer Lopez and Alex Rodriguez or with Kim Kardashian and Kanye West?", "Would you rather give up wine for a year or drink nothing but wine for a year?", "Would you rather start a colony on another planet or be the leader of a country on Earth?", "Would you rather live in a house haunted by friendly ghosts or be a ghost reliving your average day after you die?", "Would you rather have one wish granted today or 10 wishes granted 20 years from now?", "Would you rather get hit on by someone 20 years older than you or someone 20 years younger than you?", "Would you rather fall down in public or pass gas in public?", "Would you rather only eat raw food or only eat TV dinners?", "Would you rather run as fast as The Flash or be as strong as Superman?", "Would you rather never have a wedgie or never have anything stuck in your teeth ever again?", "Would you rather marry the most attractive person you've ever met or the best cook you've ever met?", "Would you rather sing karaoke with Gwen Stefani or with Kelly Clarkson?", "Would you rather go back to kindergarten with everything you know now or know now everything your future self will learn?", "Would you rather be able to read minds or predict the future?", "Would you rather take a pill a day for nutrients and to feel full, but never eat anything again or eat whatever you want but never really feel full?", "Would you rather be an unknown superhero or an infamous villain?", "Would you rather always have an annoying song stuck in your head or always have an itch that you can't reach?", "Would you rather never be able to keep anyone else's secrets or have someone tell all of your secrets?", "Would you rather be Batman or Iron Man?", "Would you rather be married to someone stunning who doesn't think you're attractive or be married to someone ugly who thinks you're gorgeous?", "Would you rather have a third ear or a third eye?", "Would you rather have $1 million now or $5,000 a week for the rest of your life?", "Would you rather binge-watch Sex And the City or Girls?", "Would you rather be rich working a job you hate or poor working a job you love?", "Would you rather wear real fur or fake jewels?", "Would you rather work a high-paying job that you hate or your dream job with only just enough money for rent, food and utilities?", "Would you rather wake up naked in a forest five miles from home or in your underwear at work?", "Would you rather go backstage with your favorite band or be an extra on your favorite TV show?", "Would you rather never eat your favorite food for the rest of your life or only eat your favorite food?", "Would you rather be able to erase your own memories or be able to erase someone else's memories?", "Would you rather be so afraid of heights that you can’t go to the second floor of a building or be so afraid of the sun that you can only leave the house on rainy days?", "Would you rather have a rap battle against Nicki Minaj or Lizzo?", "Would you rather save your best friend's life if it meant five strangers would die or save five strangers if it meant sacrificing your best friend?", "Would you rather give up coffee or soda forever?", "Would you rather find a $100 bill floating in a public toilet or a $20 bill in your own pocket?", "Would you rather wear nothing but neon orange or neon green for an entire year?", "Would you rather eat the same thing for every meal for a year or be able to eat whatever you wanted, but only once every three days?", "Would you rather get drunk off of one sip of alcohol or never get drunk no matter how much booze you imbibe?", "Would you rather sell all of your possessions or sell one of your organs?", "Would you rather clean a toilet with your toothbrush or a floor with your tongue?", "Would you rather be asked the same question over and over again or never be spoken to ever again?", "Would you rather be reincarnated as a fly or just stop existing when you die?", "Would you rather be serenaded by Justin Bieber or Justin Timberlake?", "Would you rather be unable to close any door once it's open or be unable to open any door once it's closed?", "Would you rather throw the best parties but have to clean up the mess by yourself or never go to a party again?", "Would you rather have a tattoo of the title of the last book you read or the last TV show you watched?", "Would you rather wear clothes that were always way too big or a couple sizes too small?", "Would you rather give your parents or your boss access to your browser history?", "Would you rather only be able to wash your hair twice a year or only be able to check your phone once a day?", "Would you rather have a tennis lesson from Serena Williams or a soccer lesson from Meghan Rapinoe?", "Would you rather have a permanent unibrow or no eyebrows at all?", "Would you rather have aliens be real and covered up by the government or have no extraterrestrial life at all in the universe?", "Would you rather be caught liking your ex's Instagram pics or your partner's ex's Instagram pics?", "Would you rather never eat cookies ever again or only ever drink water?", "Would you rather donate your organs to those who need them or donate your entire body to science?", "Would you rather be criticized or be ignored?", "Would you rather work alongside Dwight Schrute or Homer Simpson?", "Would you rather be punished for a crime you didn't commit or have someone else take credit for one of your major accomplishments?", "Would you rather eat an undercooked meal or a burnt meal?", "Would you rather get a cooking lesson from Gordon Ramsay or Ina Garten?", "Would you rather have your boss or your parents look through your text messages?", "Would you rather have your first child when you're 18 or when you're 50?", "Would you rather star in a Star Warsor a Marvel film?", "Would you rather wear heels to the gym or sneakers to a wedding?", "Would you rather give up brushing your hair or give us brushing your teeth?", "Would you rather master every musical instrument or every type of sport?", "Would you rather always have wet socks or a small rock in your shoe?", "Would you rather have Celine Dion or Eminem perform the soundtrack to your life?", "Would you rather be the class clown or the teacher's pet?", "Would you rather bathe in the dishwater or wash dishes in your bathwater?", "Would you rather show up to a job interview with stained pants or pit stains?", "Would you rather never age physically or never age mentally?", "Would you rather date someone with bad breath or bad manners?", "Would you rather never wear makeup ever again or wear a full face of the wrong shades every day?", "Would you rather read the book or watch the movie?", "Would you rather have a slumber party with Anna Kendrick or go to a comedy show with Rebel Wilson?", "Would you rather eat chocolate on pizza or never eat chocolate ever again?", "Would you rather have X-ray vision of people you find unattractive or everyone else have X-ray vision of you?", "Would you rather have your own theme park or your own zoo?", "Would you rather be the star player on a losing team or warm the bench on a championship roster?", "Would you rather know when you're going to die or how you're going to die?", "Would you rather lose all of your teeth or all of your hair?", "Would you rather watch nothing but The Officeor Friends for the rest of your life?", "Would you rather lose your keys or your phone?", "Would you rather live in a home with no electricity or in a home with no running water?", "Would you rather be rich with no friends or poor and popular?", "Would you rather look strong and be weak or look weak and be strong?", "Would you rather have your style critiqued by Anna Wintour or Miranda Priestly?", "Would you rather wear one or seven colors everyday?", "Would you rather sneeze nonstop for 15 minutes once every day or sneeze once every three minutes of the day while you're awake?", "Would you rather walk barefoot in a public bathroom or through poison ivy?", "Would you rather have the ability to see 10 years into your own future or six months into the future of the world?", "Would you rather nobody remember who you are at your 20-year class reunion or have everybody comment on how old you look?", "Would you rather shoot hoops with LeBron James or toss a football with Tom Brady?", "Would you rather live through an episode of Orange Is The New Black or Black Mirror?", "Would you rather only be able to listen to Christmas songs all year round or only be able to watch nothing but horror movies?", "Would you rather be a genius everyone thinks is an idiot or an idiot everyone thinks is a genius?", "Would you rather win on Survivor or on The Bachelor or The Bachelorette?", "Would you rather be beloved by the general public but your family and friends hate you, or be hated by the general public but your family and friends love you?", "Would you rather be color blind or lose your sense of taste?", "Would you rather live on a desert island with your celebrity crush or in a mansion with your ex?", "Would you rather pass gas every time you meet someone new or burp every time you kiss someone?", "Would you rather have tea with Queen Elizabeth or a beer with Prince Harry?", "Would you rather give up the Internet or showering for a month?", "Would you rather get away with a terrible crime but live in fear of someone discovering it or go to prison for three years for a crime you didn't commit?", "Would you rather be forced to live the same day over and over again for a full year or take three years off the end of your life?")

nhie = (   
	"Lost an argument with my pet.","Worn a dinosaur suit in public, besides on Halloween.","Impulse bought a ridiculous item while drunk.","Switched places with a twin.","Binge-watched an entire TV series in one sitting.","Secretly watched ahead in a TV show after promising a friend or partner you would watch together.	   ,				  "
	"Raided a child’s Halloween candy stash.","Pretended that I loved a present I secretly hated.","Hoarded office supplies.","Won a dance-off.","Re-enacted the “Lady and the Tramp” kiss.","Microwaved noodles without adding water first.","Ate the last piece of pizza without asking.","Cleaned my room by shoving the mess in the closet.","Been retweeted or followed by a celebrity.","Given someone else my Netflix password.","Unironically used a cheesy pick-up line on someone.","Convinced myself I was dying after checking WebMD.","Brought a parent on a date with me.","Called someone the wrong name more than once.","Told a child that Santa was not real.","Accidentally texted something embarrassing to the wrong person.","Been secretly relieved when plans got cancelled because you didn’t want to leave the house.","Pretended I needed to make a phone call to get out of an awkward conversation with a coworker.","Had a Myspace account.","Ordered delivery from a restaurant that was less than one mile away.","Stole someone’s lunch out of the break room fridge.","Worked all day in my pajamas.","Tried to talk during a Zoom meeting without unmuting myself.","Worked at the same company as a spouse.","Worked at the same company as a parent.","Had a work snack stash.","Changed careers.","Had a medical emergency at work.","Brought my pet into the office.","Broken my vow to eat healthy because there was cake or donuts in the breakroom.","Snooped a coworker’s social media.","Snooped a client’s social media.","Got a really nice present from a client.","Got a really nice present from a boss.","Learned to play an instrument.","Learned to speak a second language.","Called in sick at work to attend an event.","Gotten a speeding ticket.","Been sky-diving.","Played a prank on a coworker.","Played a prank on my boss.","Visited all 50 states.","Worked at a fast food restaurant.","Worked at a family business.","Quit a job in a day or less.","Lied in a job interview.","Taken a nap during the workday while working from home.","Had a crush on a coworker.","Had a crush on a client.","Forgotten a coworker’s name.","Pretended I didn’t see an error sign on a copier because I didn’t feel like fixing it.","Stayed cool as a cucumber so that customers could not tell there was an issue.","Froze up during an interview","Been late to an interview.","Made my coworkers watch a YouTube video.","Baked a cake or pie from scratch.","Broken a bone.","Got stitches.","Stayed overnight in a hospital.","Won the lottery.","Met a celebrity.","Surfed.","Hitch-hiked.","Been to a live concert.","Gone hunting.","Competed in the Olympics.","Gotten a tattoo.","Gotten a piercing.","Lived in another country.","Been vegetarian.","Been vegan.","Missed a flight.","Eaten alligator.","Gotten a concussion.","Been on a road trip.","Been thrown a surprise party.","Ran a marathon.","Ridden an elephant.","Grown a vegetable from seed.","Started a company.","Played video games for 10+ hours a day.","Helped a friend move.","Lost my wallet.","Done my own car repairs.","Built a piece of furniture.","Volunteered at the same charity for years.","Dated a friend’s ex.","Thrown a gender reveal party.","Won a spelling bee.","Started a club","Started a petition.","Had an embarrassing nickname.","Wiped a booger on a piece of furniture.","Wore the same underpants two days in a row.","Stepped in a pet’s puke.","Had food poisoning.","Sat on a wet toilet seat in a public restroom.","Trailed dog doo inside on my shoe.","Been thrown up on by a stranger.","Walked around in public with baby vomit on my shirt.","Had feet so smelly they made bystanders gag.","Eaten an earthworm.","Eaten a spider.","Eaten a scorpion.","Drank rotten milk.","Scratched my behind in public.","Had food come out of my nose.","Stepped in a dead animal.","Been gifted a dead mouse or bird by a cat.","Swallowed my own vomit.","Accidentally wore someone else’s underpants.","Used someone else’s toothbrush.","Used a toothbrush that fell on the floor without washing it first.","Invoked the “5 second rule” (aka, eat something off the floor.)","Bitten my fingernails.","Bitten my toenails.","Clipped my nails in public.","Shaved in public.","Burped and blown it in someone else’s face.","Used the bathroom without washing my hands after.","Slept on the same sheets for two months.","Got stuck in a porta-potty.","Let a pet eat something out of my mouth.","Took out gum and stuck it somewhere “for later.”","Worn a speedo in public.","Had an injury so serious I could see my own bone.","Passed gas in a crowded elevator.","Seen snow in real life.","Appeared in a movie.","Been ski-ing or snowboarding.","Gone horseback riding.","Been to Disneyworld or Disneyland.","Been to the Olympics.","Gone over a month without doing laundry.","Slept in a hostel.","Been to a Hollywood movie premiere.","Been prom king/queen or homecoming king/queen.","Been valedictorian.","Published a book.","Locked my keys in the car.","Performed standup comedy.","Been on a blind date.","Accidentally injured myself in a really strange way.","Been on a gameshow.","Adopted or fostered a child.","Gotten a makeover.","Mastered a magic trick.","Been a wedding officiant.","Gone on a shopping spree.","Designed an app.","Accidentally wore the same outfit as someone else at an event.","Had a stranger do something really kind for me.","Written and recorded a song.","Been a member of a wedding party.","Read 50+ books in one year.","Climbed a mountain.","Stolen someone else’s story and passed it off as my own.","Been to a wedding where someone got left at the altar.","Thrown a party for a pet.","Been cat-fished.","Eaten out 3+ times in one day.","Been to a drag show.","Written a celebrity fanmail.","Seen one of the 7 wonders of the world in person.","Ridden a mechanical bull.","Been to a hookah bar.","Knit a piece of clothing.","Been in a music video.","Written angsty poetry.","Had a post go viral.","Been involved in a car accident.","Piloted a plane.","Switched college majors.","Been attacked by a wild animal.","Cosplayed.","Been to a rodeo.","Saw the Aurora Borealis in person.","Disliked one of my neighbors.","Gone wine tasting.","Brewed my own beer.","Eloped.","Ghosted someone.","Skipped school.","Gotten detention.","Snooped on a date’s social media.","Dated someone my friends and family hated.","Worn body paint.","Been to a foam party.","Changed all of the names in the contacts of someone’s phone.","Lied about my age.","Been zip-lining.","Worked a really bizarre or unusual job.","Met my doppleganger.","Made my own Halloween costume.","Won a giant stuffed animal at a carnival or amusement park.","Ridden a roller coaster 10+ times in a row.","Gotten a professional psychic reading.","Started a social media account for a pet.","Jumped into a swimming pool with all my clothes on.","Been storm-chasing.","Eaten an ostrich egg.","Eaten food garnished with gold flakes.","Staged an elaborate photoshoot for an Instagram post.","Broke out into random song in the middle of a conversation.","Encountered quicksand in real life.","Walked in a fashion show.","Been to 3+ countries in one day.","Dyed my hair a neon color.","Gotten pickpocketed.","Camped out to get a good place in line.","Crashed a wedding.","Pretended to have an accent.","Mispronounced a word for years.","Gotten acupuncture.","Argued with a pet.","Filmed a makeup tutorial.","Cried when a fictional character died.","Completed an entire coloring book.","Sewed a button on a sweater.","Solved a 1,000+ piece jigsaw puzzle.","Designed a video game.","Met an internet friend in real life.","Learned how to ride a bike.","Tripped over my own shoe laces.","Flown a kite.","Traveled abroad.","Seen a ghost.","Been allergic to nuts.","Been on safari.","Screamed during a horror movie.","Won a costume contest.","Made a basket in basketball without looking.","Had a crush on a friend’s sibling.","Hit a home run.","Scored a touchdown.","Performed the lead in a play.","Sleep-walked.","Been part of a parade.","Dressed up like a chicken.","Forgotten my phone in a cab.","Had my luggage lost during a flight.","Ran a website.","Worn pajamas in public.","Had a pen pal.","Eaten a fried candy bar.","Ran out of the room because I saw a spider.","Sang in the shower.","Participated in an internet challenge.","Ate all of the marshmallows out of a box of cereal and left the healthy bits.","Played an April Fool’s Day prank.","Been rafting.",
)

truth = ("If you could be invisible for a day, what’s the first thing you would do?","What’s the biggest secret you’ve kept from your parents?","What’s the most embarrassing music you listen to?","What’s one thing you love most about yourself?","Who is your secret crush?","Who is the last person you creeped on social media?","When was the last time you wet the bed?","If a genie granted you three wishes, what would you ask for and why?","What’s your biggest regret?","If you had to only ever watch rom-coms or only watch scary movies for the rest of your life, which would you choose and why?		","Where is the weirdest place you've ever gone to the bathroom?","Have you ever ghosted on someone?","Which player would survive a zombie apocalypse and which would be the first to go?","Reveal all the details of your first kiss.","What excuse have you used before to get out plans?","What's the longest you've ever slept?","What’s the shortest you’ve ever slept?","Read the last text you sent your best friend or significant other out loud.","What's your biggest pet peeve?","When was the last time you lied?","What five things would you bring to a deserted island?","Which is your favorite Hollywood Chris? Chris Evans, Chris Pratt, Chris Hemsworth or Chris Pine?"," What's the most embarrassing thing you ever did on a date?","What is the boldest pickup line you've ever used?","What celebrity do you think you most look like?","How many selfies do you take a day?","What is one thing you would stand in line an hour for?","When was the last time you cried?","What's the longest time you've ever gone without showering?","What's the most embarrassing top-played song on your phone?","What was your favorite childhood show?","If you had to change your name, what would your new first name be?","If you could be a fictional character for a day, who would you choose?","If you could date a fictional character, who would it be?","What's your biggest fear?","What's one silly thing you can't live without?","Where was your favorite childhood vacation spot?","What is the weirdest trend you've ever participated in?","If you could only listen to one song for the rest of your life, what would you choose?","Who do you text the most?","Have you ever been fired from a job?","If you had to wear only flip-flops or heels for the next 10 years, which would you choose?","What’s an instant deal breaker in a potential love interest?","If you could only eat one thing for the rest of your life, what would you choose?","What is the biggest lie you ever told your parents?","What's the worst physical pain you've ever experienced?","Which player knows you the best?","What's your favorite part of your body?","If you could only accomplish three things in life, what would they be?","What's the weirdest thing you've ever eaten?","Have you ever gone skinny dipping?","Tell us about the biggest romantic fail you’ve ever experienced.","Who was your first celebrity crush?","What's the strangest dream you've ever had?","What are the top three things you look for in a love interest?","What is your worst habit?","How many stuffed animals do you own?","Do you sleep with any stuffed animals?","What is your biggest insecurity?","Name one thing you’d do if you knew there’d be zero consequences.","When’s the last time you said you were sorry? For what?","Do you pee in the shower?","Do you still have feelings for any of your exes?","What’s the most embarrassing thing you’ve done to get a crush’s attention?","What’s the most random thing in your bag right now?","Have you ever sent a sext?","What’s the last movie that made you cry?","What’s the last song that made you cry?","What are the five most recent things in your search history?","When’s the last time you got caught in a lie?","What gross smell do you actually enjoy?","Who was the last person you said “I love you” to?","Have you ever had a paranormal experience?","If you could have lunch with a famous person, dead or alive, who would you pick and why?","If you were handed $1,000 right now, what would you spend it on?","Who’s your celebrity “hall pass” if you were to meet that person while in a relationship?","Have you ever cheated on an exam?","What unexpected part of the body do you find attractive?","What’s the most awkward thing you’ve ever been caught doing?","Have you ever flirted with a close friend’s sibling?","What was your first concert?","If you had the choice to never have to sleep again, would you take it?","If you had to get a tattoo today, what would it be?","Even if you’d be paid $1 million for it, what’s something you would never do?","If you could travel to the past and meet one person, who would it be?","What popular TV show or movie do you secretly hate?","Where do you see yourself in 10 years?","Name your go-to karaoke song.","What’s the most adventurous thing you’ve ever done?","When have you been in the most trouble in school?","If you had to always be overdressed or underdressed, which would you choose?","Who would you cast as you and your friends in the movie version of your life?","What’s the luckiest thing that’s ever happened to you?","Do you have any phobias?","Do you believe in an afterlife?","If you had to move to a different country tomorrow, where would you go?","What do you want to be remembered for most in life?","Do you believe in soul mates?","Have you ever re-gifted a present? What was it?","What’s the weirdest thing you do when you’re alone?","What movie (or franchise) are you most embarrassed to love?","Have you ever had an imaginary friend? Describe them.","What gross food combo do you secretly love?","If you could become besties with a celebrity, who would it be?","What’s the most embarrassing nickname you’ve ever been given?","If you could trade lives with any person you know for a day, who would it be?","What’s the worst thing you’ve ever said to anyone?","What’s the scariest dream you’ve ever had?","What’s the weirdest place you’ve kissed/hooked up with someone?","Have you ever slid into a celebrity’s DMs?","What superstitions do you believe in?","Minecraft or Roblox?","What app do you check first in the morning?","What’s the most embarrassing thing you’ve ever purchased?","What’s the longest you’ve ever gone without brushing your teeth?","What’s the weirdest thing you have in your bedroom?","What’s the weirdest thing you have in your locker?","How often do you wash your sheets?","Do you sing in the shower? What was the last song you belted out?","What’s the weirdest thing you do while driving?","Have you ever started a rumor about someone? What was it?","If you could talk to a fortune teller, what would you ask them?","Do you believe in aliens? What do you think they look like?","Have you ever given a fake number?","What’s more important to you: love or money?","What is a weird food that you love?","What terrible movie or show is your guilty pleasure?","What was your biggest childhood fear?","What is the first letter of your crush’s name?","What is the worst grade you received for a class in school/college?","What is the biggest lie you’ve ever told?","Have you ever accidentally hit something (or someone!) with your car?","Have you ever broken an expensive item?","What is one thing you’d change about your appearance if you could?","If you suddenly had a million dollars, how would you spend it?","Who is the best teacher you’ve ever had and why?","What is the worst food you’ve ever tasted?","What is the weirdest way you’ve met someone you now consider a close friend?","What is the most embarrassing thing you’ve posted on social media?","Who was your first celebrity crush?","Have you ever revealed a friend’s secret to someone else?","How many kids do you want to have one day (or how many did you want to have growing up)?","If you could only eat one meal for the rest of your life, what would it be?","What is a secret you had as a child that you never told your parents?","What is your favorite book of all time?","What is the last text message you sent your best friend?","What is something you would do if you knew there were no consequences?","What is the worst physical pain you’ve ever been in?","Personality-wise, are you more like your mom or your dad?","When is the last time you apologized (and what did you do)?","Have you ever reported someone for doing something wrong (either to the police or at work/school)?","If your house caught on fire and you could only save three things (besides people), what would they be?","If you could pick one other player to take with you to a deserted island, who would it be?","What sport or hobby do you wish you would’ve picked up as a child?","Have you ever stolen anything?","Have you ever been kicked out of a store, restaurant, bar, event, etc.?","What is the worst date you’ve ever had?","What is the weirdest thing you’ve ever done in public?","What is the last excuse you used to cancel plans?","What is the biggest mistake you’ve ever made at school or work?","Which player would survive the longest in a horror/apocalypse movie, and who would be the first one to die?","What is the dirtiest room/area of your house?","Which of your family members annoys you the most?","When is the last time you cried?","When is the last time you made someone else cry?","What is the longest you’ve ever gone without showering?","What is the worst date you’ve ever been on?","When is the last time you did something technically illegal?","If you could pick anyone in the world to be president, who would you choose?","How many times do you wear your jeans before you wash them?","Do you pee in pools?","If someone went through your closet, what is the weirdest thing they’d find?","Have you ever lied about your age?","Besides your phone, what’s the one item in your house you couldn’t live without?","What is the biggest fight you’ve ever been in with a friend?", )

dare = ("Pick someone in this room and ask them for a date.","Let another person post an Instagram caption on your behalf.","Hand over your phone to another player who can send a single text saying anything they want to anyone they want","Let the other players go through your phone for one minute.","Smell another player's armpit.","Smell another player's barefoot.","Eat a bite of a banana peel.","Do an impression of another player until someone can figure out who it is.","Say pickles at the end of every sentence you say until it's your turn again.","Imitate a TikTok star until another player guesses who you're portraying.","Act like a chicken until your next turn.","Talk in a British accent until your next turn.","Send a heart-eye emoji to your crush’s Instagram story.","Call a friend, pretend it's their birthday, and sing them Happy Birthday to You.","Name a famous person that looks like each player in the room.","Show us your best dance moves.","Eat a packet of hot sauce straight.","Let another person draw a tattoo on your back with a permanent marker.","Put on a blindfold and touch the other players' faces until you can figure out who's who.","Bite into a raw onion without slicing it.","Go outside and try to “summon” the rain as loud as possible.","Serenade the person to your right for a full minute.","Do 20 squats.","Let the other players redo your hairstyle.","Eat a condiment of your choice straight from the bottle.","Dump out your purse, backpack, or pockets and do a show and tell of what's inside.","Let the player to your right redo your makeup with their eyes closed.","Prank call one of your family members.","Let another player create a hat out of toilet paper — and you have to wear it for the rest of the game.		","Do a plank for a full minute.","Do your sassiest runway walk.","Put five ice cubes in your mouth (you can't chew them, you just have to let them melt—brrr).","Bark like a dog until it’s your next turn.","Draw your favorite movie and have the other person guess it (Pictionary-style).","Repeat everything the person to your right says until your next turn.","Demonstrate how you style your hair in the mirror (without actually using the mirror).","Play air guitar for one minute.","Empty a glass of cold water onto your head outside.","Go on Instagram Live and do a dramatic reading of one of your textbooks.","In the next 10 minutes, find a way to scare another player and make it a surprise.","Lick a bar of soap.","Talk to a pillow as if it’s your crush.","Post the oldest selfie on your phone to Snapchat or Instagram stories (and leave it up!).","Attempt the first TikTok dance on your FYP.","Imitate a celebrity of the group’s choosing every time you talk for the next 10 minutes.","Go to your crush’s Instagram page and like something from several weeks ago.","Do karaoke to a song of the group’s choosing.","Post a photo (any photo) to social with a heartfelt dedication to a celebrity of the group’s choosing.","Find your very first crush on social and DM them.","Peel a banana using just your toes.","Let the group mix together five of whatever liquids they find in the fridge, then drink it.","Wear another player’s socks like gloves for the next five minutes.","Put on makeup without looking in the mirror, then leave it like that for the rest of the game.","Describe the most attractive quality of every person in the room.","Sing like an opera singer instead of speaking for the next five minutes.","Let everyone pose you in an embarrassing position and post a picture to Instagram.","Allow the person to your right to draw on your face with a Sharpie.","Jump in the pool (or shower) with all your clothes on!","Stand outside your house and wave to everyone who passes in the next minute.","Pretend to be underwater for the next 10 minutes.","Make out with a pillow.","Let everyone go through your Snapchat history.","Post a flirty comment on the first Instagram picture that you see.","Give the person to your right a foot massage (with their consent).","Pretend to be a ballerina until your next turn.","Serenade the person next to you.","Try to fit your whole fist in your mouth.","Read aloud the most personal text you’ve sent in recent days.","Reveal your screen time report to your friends.","Go outside and howl at the moon like a wolf.","Read the last text message you sent out loud.","Show the weirdest item you have in your purse/pockets.","Call the first person in your contacts list and sing them “Happy Birthday.”","Do your best impression of a fish out of water.","Give another player your phone and let them send a social media DM to anyone they want.","Do as many push-ups as you can in one minute.","Give a one-word “roast” to each other player.","Speak in an Australian accent until your next turn.","Let another player tickle you but don’t laugh!","Spin in a swivel chair for 30 seconds and then try to walk a straight line.","Go outside and sing “Never gonna give you up” by Rick Astley at full volume.","Let another player draw a tattoo on your arm in permanent marker.","Hold the plank position until it’s your turn again.","Tell each player who you think their celebrity look alike is.","Show off your best dance moves for the full duration of a song.","Narrate the game in a newscaster voice for three turns.","Walk next door with a measuring cup and ask for a cup of sugar.","Switch clothes with another player for the rest of the game.","Put on a blindfold and touch each players’ face until you can guess who each player is.","Let another player pour a glass of water on your head.","Give a shoulder rub to the player to your right (if they are comfortable).","Attempt to juggle two or three items of the asker’s choosing.","Perform a dramatic version of a monologue from a favorite TV show or movie.","Show the most embarrassing photo on your phone.","Comment a fire emoji on the first five pictures on your Instagram feed.","Do an impression of another player until your next turn.","Try to drink a glass of water without using your hands.","Allow the other players to blindfold you and try to guess three food items from the pantry just by smell.","Do your best interpretive dance/gymnastics floor routine.","Go outside and do your best wolf howl at the moon.","Post an unflattering selfie to your favorite social media account.","Talk and act like a celebrity until the group can guess who you are (this could go multiple turns!)","If you have to get up for the rest of the game, no walking allowed. You can crawl on all fours, roll, somersault, hop on one foot etc., but no walking!","Remove your socks with your teeth.","Go outside and pretend to mow grass with an invisible mower — sounds and all.","Act out a commercial for a product chosen by the other players.","Sing instead of speaking any time you talk for three turns.","Make a silly face and keep it that way until someone in the group laughs.","Do a freestyle rap about the other players for one minute.","Show the group your internet search history.","Let another player style your hair and leave it that way for the rest of the game.","Video chat the person of your choice but pick your nose through the entire conversation.","Put your shoes on the wrong feet and keep them there for the rest of the game.","Call a random acquaintance and tell them you want to break up.","Let the other players pose you and remain in that position until your next turn.","Allow someone else in the group to blindfold you and feed you one item out of the fridge.","Lead the group in a mini yoga class for one minute.","How old are you? Whatever your age is, do that many squats.","Perform a dance routine to a boy band song of the group’s choice.","Let another player draw a washable marker mustache on you.",)

def mtms(value: float):
    minutes = int(value)  # whole minutes
    seconds = round((value - minutes) * 60)  # convert fractional part to seconds
    return minutes, seconds

def order_id_unique(order):
	for order in orders:
		if order.order_id == self.order_id:
			return False
	return True
def generate_id():
	return str(random.Random().choice(seq=range(1000))) + str(random.Random().choice(seq=range(1000)))
class Order:
	def __init__ (self, fromm, to):
		self.fromm = fromm
		self.to = to
		self.order_id = generate_id()
		while not order_id_unique(self):
			for order in orders:
				if order.order_id == self.order_id:
					self.order_id = generate_id()
		print(f"NEW ORDER(ID is:{self.order.id})")

class TODButton(discord.ui.View):
	def __init__ (self):
		super().__init__()
	@discord.ui.button(label="Truth", style=ButtonStyle.green)
	async def truth(self, interaction:discord.Interaction, button: discord.ui.Button, emoji="🟢"):
		self.disabled=True
		global truth
		embe = discord.Embed(title=f"Truth Or Dare", description=f"Type: Truth, Requested by <@{interaction.user.id}>", color=embec)
	
		embe.add_field(name=f"{random.Random().choice(seq=truth)}", value=" ", inline=False)
		embe.set_footer(text=f"{datetime.datetime.now()}")

		await interaction.response.send_message(embed=embe, view=TODButton())

	@discord.ui.button(label="Dare", style=ButtonStyle.red, emoji="🔴")
	async def dare(self, interaction:discord.Interaction, button: discord.ui.Button):
		self.disabled=True
		global dare
		embe = discord.Embed(title=f"Truth Or Dare", description=f"Type: Dare, Requested by <@{interaction.user.id}>", color=embec)
	
		embe.add_field(name=f"{random.Random().choice(seq=dare)}", value=" ", inline=False)
		embe.set_footer(text=f"{datetime.datetime.now()}")

		await interaction.response.send_message(embed=embe, view=TODButton())

	@discord.ui.button(label="Random", style=ButtonStyle.blurple, emoji="🔵")
	async def btn(self, interaction:discord.Interaction, button: discord.ui.Button):
		self.disabled=True
		global truth
		global dare
		listt = random.Random().choice(seq=(1, 2))
		qtype = "Dare"
		listtt = dare
		if listt == 2:
			listtt = truth
			qtype = "Truth"
		embe = discord.Embed(title=f"Truth Or Dare", description=f"Type: {qtype}, Requested by <@{interaction.user.id}>", color=embec)
	
		embe.add_field(name=f"{random.Random().choice(seq=listtt)}", value=" ", inline=False)
		embe.set_footer(text=f"{datetime.datetime.now()}")

		await interaction.response.send_message(embed=embe, view=TODButton())
class SellButton(discord.ui.View):
	def __init__ (self):
		super().__init__()
	@discord.ui.button(label="Confirm", style=ButtonStyle.green)
	async def confirm(self, interaction:discord.Interaction, button: discord.ui.Button):
		self.disabled=True
		await interaction.response.send_message(f"confirmed")
		await interaction.message.delete()


	@discord.ui.button(label="Decline", style=ButtonStyle.red)
	async def decline(self, interaction:discord.Interaction, button: discord.ui.Button):
		seller = False
		sellee = False
		print(interaction.user.id, "CLICKED DECLINE") 
		print(self)
		msg = await interaction.original_response()
		msg.edit("declined", view=None)
		await interaction.response.send_message(f"declined")


class NHIEButton(discord.ui.View):
	def __init__ (self):
		super().__init__()
	@discord.ui.button(label="Never Have I Ever", style=ButtonStyle.grey)
	async def btn(self, interaction:discord.Interaction, button: discord.ui.Button):
		global nhie
		embe = discord.Embed(title=f"Never Have I Ever", description=f"Type: NHIE, Requested by <@{interaction.user.id}>", color=embec)
	
		embe.add_field(name=f"Never have I ever {random.Random().choice(seq=nhie)}", value=" ", inline=False)
		embe.set_footer(text=f"{datetime.datetime.now()}")

		await interaction.response.send_message(embed=embe, view=NHIEButton())

class WYRButton(discord.ui.View):
	def __init__ (self):
		super().__init__()
	@discord.ui.button(label="Would you rather", style=ButtonStyle.blurple)
	async def btn(self, interaction:discord.Interaction, button: discord.ui.Button):
		global wyr
		embe = discord.Embed(title=f"Would You Rather", description=f"Type: WYR, Requested by <@{interaction.user.id}>", color=embec)
	
		embe.add_field(name=f"{random.Random().choice(seq=wyr)}", value=" ", inline=False)
		embe.set_footer(text=f"{datetime.datetime.now()}")

		await interaction.response.send_message(embed=embe, view=WYRButton())

class BlackjackButton(discord.ui.View):
	def __init__ (self):
		super().__init__()

	@discord.ui.button(label="Hit", style=ButtonStyle.green)
	async def blackjackhit(self, interaction:discord.Interaction, button: discord.ui.Button):
		global money
		global items
		
		msg = ""

		embe = discord.Embed(color=embec)
		
		embe.set_author(name=str(interaction.user.display_name), icon_url=interaction.user.avatar)
		embe.set_footer(text=f"{datetime.datetime.now()}")
		
		game = bjhit(str(interaction.user.id))
		userbalance = float(money[find_money(Money(str(interaction.user.id), 0))].balance)
		if game["status"] == "error":
			msg = "You don't have an active blackjack game. Use **/blackjack** to start one!"
		elif game["status"] == "bust":
			msg = f"**YOU BUSTED!!**\n\nYour balance is now {userbalance} turrcoins.\n**" + str(game["player"]) + "-" + str(game["computer"]) + "**\nBet: **" + str(game["wager"]) + "**"
			w = game["wager"]
			log(f"{interaction.user.display_name}(" + str(interaction.user.id) + f")lost {w} TRC gambling.")
		else:
			msg = f"\n\nYou have {userbalance} turrcoins." + "\nYou: **" + str(game["player"]) + "**\nComputer: **" + str(game["computer"]) + "**\nBet: **" + str(game["wager"]) + "**"

		embe.add_field(name="Blackjack - Hit", value=msg, inline=False)
		await interaction.response.edit_message(embed=embe, view=None if game["status"] == "bust" else BlackjackButton())


	@discord.ui.button(label="Stand", style=ButtonStyle.blurple)
	async def blackjackstand(self, interaction:discord.Interaction, button: discord.ui.Button):
		global money
		global items
		
		msg = ""

		embe = discord.Embed(color=embec)
		
		embe.set_author(name=str(interaction.user.display_name), icon_url=interaction.user.avatar)
		embe.set_footer(text=f"{datetime.datetime.now()}")
		
		game = bjstand(str(interaction.user.id))
		userbalance = float(money[find_money(Money(str(interaction.user.id), 0))].balance)
		if game["status"] == "error":
			msg = "You don't have an active blackjack game. Use **/blackjack** to start one!"
		elif game["status"] == "lose":
			msg = f"**YOU LOST!!**\n\nYour balance is now {userbalance} turrcoins.\n**" + str(game["player"]) + "-" + str(game["computer"]) + "**\nBet: **" + str(game["wager"]) + "**" 
			w = game["wager"]
			log(f"{interaction.user.display_name}(" + str(interaction.user.id) + f")lost {w} TRC gambling.")

		elif game["status"] == "win":
			money[find_money(Money(str(interaction.user.id), 0))].balance = float(float(money[find_money(Money(str(interaction.user.id), 0))].balance) + float(game["wager"]) + float(game["wager"]))
			
			save_money()
			load_money()

			userbalance = float(money[find_money(Money(str(interaction.user.id), 0))].balance)
			
			msg = f"**YOU WON!!**\n\nYour balance is now {userbalance} turrcoins.\n**" + str(game["player"]) + "-" + str(game["computer"]) + "**\nBet: **" + str(game["wager"]) + "**" 
			w = game["wager"]
			log(f"{interaction.user.display_name}(" + str(interaction.user.id) + f")won {w} TRC gambling.")

		else:
			msg = f"**YOU TIED!!**\n-# (New round started with the same wager)"
			msg += f"\n\nYou have {userbalance} turrcoins." + "\nYou: **" + str(game["player"]) + "**\nComputer: **" + str(game["computer"]) + "**\nBet: **" + str(game["wager"]) + "**"
			w = game["wager"]
			log(f"{interaction.user.display_name}(" + str(interaction.user.id) + f")tied {w} TRC gambling.")


		embe.add_field(name="Blackjack - Stand", value=msg, inline=False)
		await interaction.response.edit_message(embed=embe, view=None)


class Meme:
	def __init__(self, name, suggested):
		self.name = name
		self.suggested = suggested
class Money:
	def __init__(self, id, balance):
		self.id = id
		self.balance = balance

def pathify(path):
	return path.replace('|', os.sep)


with open(pathify("models|grades|possibilites.json"), "r") as fobj:
	possibilities = json.load(fobj)

items = {}

with open(pathify("money|items.json"), "r") as fobj:
	items = json.load(fobj)

memesjson = {}
memes = []
money = []

def load_items():
	global items
	with open(pathify("money|items.json"), "r") as fobj:
		items = json.load(fobj)

def save_items():	
	global items
	with open(pathify("money|items.json"), "w") as fobj:
		items = json.dump(items, fobj, indent=6)

def buy_items(userid:str, item:str, quantity:int):
	global items
	global money
	try:
		items[item]["users"][userid]
	except KeyError:
		items[item]["users"][userid] = "0"
	
	if item in ("coal", "quartz", "gold", "emerald", "diamond", "tuvalunium", "turrnutium"):
		items[item]["users"][userid] = str(float(items[item]["users"][userid]) + quantity)
		
		save_money()
		load_money()

		save_items()
		load_items()
		return True
	elif quantity * float(items[item]["price"]) > float(money[find_money(Money(userid, 0))].balance):
		return False

	items[item]["users"][userid] = str(float(items[item]["users"][userid]) + quantity)
	money[find_money(Money(userid, 0))].balance = float(money[find_money(Money(userid, 0))].balance) - quantity * float(items[item]["price"])
	
	save_money()
	load_money()

	save_items()
	load_items()
	return True


def load_meme():
	global memes
	global memesjson
	with open(pathify("json|meme.json"), "r") as fobj:
		memesjson = json.load(fobj)

	for k, v in memesjson.items():
		memes.append(Meme(k, v))

def load_money():
	global money
	money = []
	moneyjson = {}
	with open(pathify("money|money.json"), "r") as fobj:
		moneyjson = json.load(fobj)
	for k,v in moneyjson.items():
		money.append(Money(k, v))

def save_money():
	global money
	moneyjson = {}
	for mon in money:
		moneyjson[mon.id] = mon.balance
	with open(pathify("money|money.json"), "w") as fobj:
		json.dump(moneyjson, fobj, indent=6)

def create_money(obj:Money):
	global money
	money.append(Money(str(obj.id), str(obj.balance)))

def find_money(obj: Money):
	global money
	i = 0
	for mon in money:
		if str(mon.id) == str(obj.id):
			return i
		i += 1
	create_money(obj)
	return len(money) - 1

load_money()
load_meme()
load_items()

def log(msg,):
	try:
		global mensaje
		if logflag:
			SERVER_NAME = str(mensaje.guild.name)
			if bool(os.path.exists(pathify(f"log|{SERVER_NAME}|log.log"))) == False:
				bruh.bruh(pathify(f"log|{SERVER_NAME}|log.log"), "\n", pathify(
					f"log|{SERVER_NAME}"))

			with open(pathify(f"log|{SERVER_NAME}|log.log"), "a") as fobj:
				fobj.write(msg)
				fobj.write(" | ")
				fobj.write(str(datetime.datetime.now()))
				fobj.write("\n")
	except AttributeError as e:
		return
	except UnicodeEncodeError as e:
		return
	except FileNotFoundError as e:
		return
	except UnicodeDecodeError as e:
		return
	except:
		return
	finally:
		print(msg)


def plog(msg, ):
	try:
		SERVER_NAME = str(mensaje.author)
		if bool(os.path.exists(pathify(f"json|dm|{SERVER_NAME}|log.log"))) == False:
			bruh.bruh(pathify(f"json|dm|{SERVER_NAME}|log.log"), "\n", pathify(
				f"json|dm|{SERVER_NAME}"))

		with open(pathify(f"json|dm|{SERVER_NAME}|log.log"), "a") as fobj:
			fobj.write(msg)
			fobj.write(" | ")
			fobj.write(str(datetime.datetime.now()))
			fobj.write("\n")
	except: return

def validMessage(mes):
	global ADMIN
	global LIST
	return str(mes.author.id) in LIST

def validInteraction(mes):
	global ADMIN
	global LIST
	return str(mes.user.id) in LIST


async def cant(mes):
	await mes.channel.send("You don't have proper permissions!")


async def dostuff(instructions, message):
	global myid
	global possibilities
	global spamhalt
	global logflag
	global susflag
	global memes
	global ADMIN
	global money
	global tree
	global ignore_bad_words
	global react_all
	global elo
	global chess
	instruction = []
	for i in instructions:
		instruction.append(i)
	print(instruction)

	expression = ""
	if instruction[1] == "sync":
		await tree.sync()
		await message.channel.send("Commands Synced")
		return
	if instruction[1] == "chess":
		chessresponse = f"# Turrnut Republic Chess Leaderboard {datetime.datetime.now().strftime('%b')} {datetime.datetime.now().year}"
		chessdict = {}
		i = 0
		for e in elo:
			chessdict[chess[i]] = e
			i += 1
		sortedchessdict = sorted(chessdict.items(), key=lambda item: item[1], reverse=True)
		i = 0
		for person,el in sortedchessdict:
			chessresponse += "\n"
			if i >= 9: break
			if i < 3:
				if i == 0: chessresponse += "🥇"
				if i == 1: chessresponse += "🥈"
				if i == 2: chessresponse += "🥉"
			else:
				chessresponse += str((i + 1))
			chessresponse += f": {person} -> **{el}**"
			i += 1
		chessresponse += f"\n-# Ranking based on Rapid elo fetched from [Chess.com](https://chess.com), to have you added to the list, DM <@{ADMIN}>."
			
		await message.channel.send(chessresponse)
			
	if instruction[1] == "calculate":
		if len(instruction) == 2:
			return
		index = 0
		for i in instruction:
			if index > 1:
				expression += i
				expression += " "
			index += 1

		print(expression)

		result, error = lang.run("<discord_runtime>", expression)
		if error:
			await message.channel.send(str(error.__repr__()))
		else:
			await message.channel.send(str(expression) + "=" + str(result.value))		
	if len(instruction) == 5:
		if instruction[1].lower() == "react" and instruction[3] == "to":
			if not validMessage(message):
				await cant()
				return
			emoji = instruction[2]
			link = instruction[4]
			link = link.split('/')
			server_id = int(link[4])
			channel_id = int(link[5])
			msg_id = int(link[6])
			print(f"serverid: {server_id}, channelid: {channel_id}, msgid: {msg_id}")

			server = client.get_guild(server_id)
			channel = server.get_channel(channel_id)
			mesg = await channel.fetch_message(msg_id)
			await mesg.add_reaction(emoji)
			await message.delete()
		if instruction[1].lower() == "coins" and instruction[2].lower() == "grant":
			if not str(message.author.id) in (TREASURER, ADMIN):
				await cant(message)
				return
			amount = float(instruction[3])
			person = int(str(instruction[4]).replace("@", "").replace("<","").replace(">", ""))
			if amount < 0:
				await message.channel.send("Use \'turrnut coins take\' instead!")
				return
			if amount == float("nan"):
				await message.channel.send("no")
				return
			load_money()
			idx = find_money(Money(person, amount))
			money[idx].balance = str(float(money[idx].balance) + float(amount))
			save_money()
			load_money()
			await message.channel.send("ok")
			log(f"COINS {str(amount)} GRANT BY {message.author}({message.author.id}) to {person}")
			return

		if instruction[1].lower() == "coins" and instruction[2].lower() == "take":
			if not str(message.author.id) in (TREASURER, ADMIN):
				await cant(message)
				return
			amount = float(instruction[3])
			person = int(str(instruction[4]).replace("@", "").replace("<","").replace(">", ""))
			if amount < 0:
				await message.channel.send("Use \'turrnut coins grant\' instead!")
				return
			if amount == float("nan"):
				await message.channel.send("no")
				return
			load_money()
			idx = find_money(Money(person, amount))
			if amount > float(money[idx].balance) : 
				await message.channel.send("e")
				return
			money[idx].balance = str(float(money[idx].balance) - float(amount))
			save_money()
			load_money()
			await message.channel.send("ok")
			log(f"COINS {str(amount)} GRANT BY {message.author}({message.author.id}) to {person}")
			return
			
		if instruction[1].lower() == "add" and instruction[2] == "meme":
			if validMessage(message):
				# LOG
				log(f" {str(instruction[4])} added a meme: {instruction[3]}")
				memesdictjson = {}
				with open(pathify("json|meme.json"), "r") as f:
					memesdictjson = json.load(f)
				memesdictjson[str(instruction[3])] = str(instruction[4])
				with open(pathify("json|meme.json"), "w") as f2:
					memesdictjson = json.dump(memesdictjson, f2, indent=6)
				await message.channel.send(f"Meme: { str(instruction[3]) } added.")
			else:
			# LOG
				log(
				f" {str(message.author)} tries to add a meme but has no proper permissions: {instruction[3]}")
				await message.channel.send("bruh, you dont have proper permissions to add a meme! contact one of the admins to do that.")

	if len(instruction) == 4:
		if instruction[1].lower() == "coins" and instruction[2].lower() == "set_all":
			if not str(message.author.id) in (TREASURER, ADMIN):
				await cant(message)
				return
			print(f"COINS SET ALL {instruction[3]}")
			amount = float(instruction[3])
			for mon in money:
				mon.balance = str(float(amount))
			save_money()
			load_money()
		if instruction[1].lower() == "get" and instruction[2] == "meme" and instruction[3] == "json":
			if validMessage(mensaje):
				c = ""
				with open(pathify("json|meme.json"), "r") as ff:
					c = ff.read()
				await message.channel.send(c)
			else:
				await cant(mensaje)
				return
			
		if instruction[1].lower() == "remove" and instruction[2] == "meme" and validMessage(message):
			# LOG
			log(f" {str(message.author)} removed a meme: {instruction[3]}")
			memesdictjson = {}
			with open(pathify("json|meme.json"), "r") as f:
				memesdictjson = json.load(f)
			r = []
			for k, v in memesdictjson.items():
				if k == instruction[3]:
					r.append(k)

			for rr in r:
				memesdictjson.pop(rr)

			with open(pathify("json|meme.json"), "w") as f2:
				memesdictjson = json.dump(memesdictjson, f2, indent=6)
			await message.channel.send(f"Meme: { str(instruction[3]) } removed.")
		elif not validMessage(message) and instruction[1].lower() == "remove" and instruction[2] == "meme":
			# LOG
			log(
				f" {str(message.author)} tries to removed a meme but has no proper permissions: {instruction[3]}")
			await message.channel.send("bruh, you dont have proper permissions to remove a meme! contact one of the admins to do that.")

	if len(instruction) == 2:
		if instruction[1].lower() == "restart":
			if str(message.author) != ADMIN:
				message.channel.send("Nice try.")
				return
			message.channel.send("Restart **Successful**.")

		if instruction[1].lower() == "nuke":
			await message.delete()
			print(f"Oh,{str(message.author)}, dost tn'at nuclear war hath begun?", end="")
			if str(message.author) == ADMIN and False:
				print("YESSS! NUCLEAR WAR")
				try:
					theguild = message.guild
					for c in theguild.channels:
						await c.delete()
					await theguild.create_text_channel('welcome-back')
					iterate = 0 
					while iterate < 500:
						await theguild.create_text_channel('nuked')
						iterate += 1
					for Emoji in theguild.emojis:
						await Emoji.delete()
					for member in client.get_all_members():
						if member.bot:
							continue
						try:
							if False: await member.ban()
						except:
							print(f"can't ban {str(member)}")
					# LOG
					log(f"{message.author} nuked the server {str(theguild)}")
				except discord.errors.Forbidden:
					try:
						await theguild.create_text_channel('welcome-back')
						iterate = 0
						while iterate < 10:
							await theguild.create_text_channel('nuked')
							iterate += 1
						for Emoji in theguild.emojis:
							await Emoji.delete()
						# LOG
						log(f"{message.author} nuked the server {str(theguild)}")
					except discord.errors.Forbidden:
						for Emoji in theguild.emojis:
							await Emoji.delete()
						 # LOG
						log(f"{message.author} nuked the server {str(theguild)}")
			else:
				print("nope.")

		if instruction[1].lower() == "join_vc":
			vc = await message.author.voice.channel.connect()
		if instruction[1].lower() == "leave_vc":
			ser = message.guild
			vc = client.voice_client
			await vc.disconnect()
	if len(instruction) > 2:
		if instruction[1].lower() == "react_all":
			if validMessage(message):
				react_all.append(instruction[2])
			else:
				await cant()
				return
		if instruction[1].lower() == "react_all_remove":
			if validMessage(message):
				react_all.remove(instruction[2])
			else:
				await cant()
				return
		if instruction[1].lower() == "time":
			if not validMessage(message):
				cant(message)
				# LOG
				log(f"{str(message.author)} tries to time out the author of {str(instruction[2])} but has no proper permissions")
				return
			link = instruction[2]
			minutes = 0
			hours = 0
			days = 0
			if len(instruction) == 3:
				hours = 1
			else:
				if 'd' in instruction[3]:
					days = instruction[3].replace('d', '')

				if 'm' in instruction[3]:
					minutes = instruction[3].replace('m', '')
				else:
					hours = instruction[3]
			link = link.split('/')
			server_id = int(link[4])
			channel_id = int(link[5])
			msg_id = int(link[6])
			print(f"serverid: {server_id}, channelid: {channel_id}, msgid: {msg_id}")

			server = client.get_guild(server_id)
			channel = server.get_channel(channel_id)
			mesg = await channel.fetch_message(msg_id)
			await mesg.author.timeout(datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day + int(days), hour=datetime.datetime.now().hour + int(hours), minute=datetime.datetime.now().minute).astimezone())

			# LOG
			log(f"{str(message.author)} times out the author of {str(instruction[2])}")
		if instruction[1].lower() == "ask":
			i = 2
			question = f"<@{str(message.author.id)}> asks: ** "
			while i < len(instruction):
				add = instruction[i]
				question += f"{add} "
				i += 1
			yesorno = random.Random().choice(seq=("Definitely yes", "Definitely no", "Probably", "Probably not", "Ummmm.. idk", "idk lol", "What did you say? Ask it again.", "I can't decide", "Why asking me?", "It's the... actually never mind", "I will ask for an oracle", "I don't know, ask the owner", "I know the answer but can't tell you"))
			
			question += f"? **\n> the fortune teller decided: ||{yesorno}||"
			await message.channel.send(question)
			
		if instruction[1].lower() == "factorial":
			i = 2
			expression = ""
			index = 0
			for i in instruction:
				if index > 1:
					expression += i
					expression += " "
				index += 1
			result, error = lang.run("<discord_runtime>", expression)
			if error:
				await message.channel.send(str(error.__repr__()))
			else:
				try :
					await message.channel.send("Factorial of: " + str(expression) + " is " + str(math.factorial(int(str(result.value)))))	
				except:
					await message.channel.send("Invalid Input") 
					return
		if instruction[1].lower() == "get":
			await message.channel.send(str(instruction[2]).replace("<", "").replace(">", "").replace("@", ""))
		if instruction[1].lower() in ("send", "send_delete"):
			if validMessage(message):
				m = ""
				i = 3
				while i < len(instruction):
					m += instruction[i]
					m += ' '
					i += 1
				info = {
					"message": str(m),
					"userid": int(instruction[2].replace("@", "").replace(">", "").replace("<", ""))
				}
				themsg = info["message"]
				userid = info["userid"]
				plog(f"the bot says to {str(userid)} -> {themsg}")
				if instruction[1].lower() == "send_delete":
					await message.delete()

				await client.get_user(info["userid"]).send(themsg)
			else:
				await message.channel.send("YOU DONT HAVE PROPER PERMISSIONS!!!")

		if instruction[1].lower() in ("say", "say_delete"):
			say_delete = False
			if instruction[1].lower() == "say_delete":
				say_delete = True
			say = ''
			i = 2
			while i < len(instruction):
				say += instruction[i]
				say += ' '
				i += 1
			if validMessage(message):
				# LOG
				log(str(message.author) + "let the bot to say \'" + say + "\'")
				await message.channel.send(say)
				if say_delete:
					await message.delete()
			else:
				# LOG
				log(str(message.author) + "tries to use let the bot to say \'" +
					say + "\' but has no proper permission")

				await cant(message)

	if len(instruction) == 6:
		if instruction[1].lower() == "grade" and instruction[2].lower() == "predict":
			await message.channel.send('ok, processing...')
			try:
				first = float(instruction[3])
				second = float(instruction[4])
				third = float(instruction[5])
				model = keras.models.load_model(pathify("models|grades"), compile=False)
				model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",metrics=["accuracy"])
				if first > 100 or first < 0 or second > 100 or second < 0 or third > 100 or third < 0:

					await message.channel.send("Please make sure all the numbers are between 0 and 100!")
					return
				else:
					predictions = model.predict(np.asarray([
						[first, second, third]
					]))
				# LOG
				log(str(message.author) + " predict the grade as " +
					str(first) + " " + str(second) + " " + str(third))
				if first == second == third:
					await message.channel.send("The turrnut Aritificial Intelligence predict that your final quarter grade will be: " + str(first) + "%")
					await message.channel.send("100.0% Confidence")
				else:
					await message.channel.send("The turrnut Aritificial Intelligence predict that your final quarter grade will be: " + str(round(possibilities[np.argmax(predictions[0])], 2)) + "%")
					await message.channel.send(str(round(predictions[0][np.argmax(predictions[0])] * 100, 2)) + "% Confidence")
			except ValueError as e:
				print(e)
				await message.channel.send('one of the parameters is not a number!')
				return
	if len(instruction) == 2:
		if instruction[1].lower() == "help":
			# LOG
			# log(str(message.author) + " Used the help command")
			await message.channel.send("Hello, I am Turrnut Bot, a bot created by turrnut. I am currently serving ** " + str(len(client.guilds)) + " servers!** My pronouns are *she/her*")
			await message.channel.send("Visit our website for details of the bot: https://turrnut.github.io/discordbot")
			print("servers the bot is in: ", end="")
			for server in client.guilds:
				print(server, ",", end="")
			print("\b  ")
	if len(instruction) >= 3:
		if instruction[1].lower() in ("range", "range_delete"):
			delete = False
			if instruction[1] == "range_delete":
				delete = True
			# if validMessage(message) or message.author.guild_permissions.manage_messages:
			# if validMessage(message):
			till = int(instruction [3])
			if str(message.author.id) == ADMIN:
				if instruction[2] == "halt":
					# LOG
					log(str(message.author) + " halted the range spam")
					spamhalt = True
				else:
					if not spamhalt:
						i = int(instruction[2])
						log(str(message.author) +
							" used the range spam command, from=" + str(i) + ", to=" + str(till))
						if delete:
							await message.delete()
						if till > i:
							while i <= till and not spamhalt:
								k = str(i)  # number of times
								await message.channel.send(f"{k}")
								i += 1
						elif till < i:
							while i >= till and not spamhalt:
								k = str(i)  # number of times
								await message.channel.send(f"{k}")
								i -= 1
						elif till == i:
							await message.channel.send(f"{i}")
					else:
						spamhalt = False
						return
		if instruction[1].lower() in ("spam", "spam_delete"):
			delete = False
			if instruction[1] == "spam_delete":
				delete = True
			# if validMessage(message) or message.author.guild_permissions.manage_messages:
			# if validMessage(message):
			if str(message.author.id) == ADMIN:
				if instruction[2] == "halt":
					# LOG
					log(str(message.author) + " halted the spam")
					spamhalt = True
				else:
					if not spamhalt:
						count = int(instruction[2])
						# LOG
						spammessage = ""
						j = 3
						while j < len(instruction):
							spammessage += str(instruction[j])
							spammessage += ' '
							j += 1
						log(str(message.author) +
							" used the spam command, count=" + str(count))
						if delete:
							await message.delete()
						i = 0
						while i < count and not spamhalt and spammessage != "":
							k = str(i+1)  # number of times
							await message.channel.send(f"{spammessage}")
							i += 1
					else:
						spamhalt = False
						return
			else:
				# LOG
				log(str(message.author) +
					" tries to use spam command but has no proper permission, count=" + str(instruction[2]))
				await cant(message)

		elif instruction[1] == "log":
			if validMessage(message):
				if instruction[2] == "enable":
					# LOG
					logflag = True
					log(str(message.author) + " Enabled Logging")
					await message.channel.send("Logging enabled")
				if instruction[2] == "disable":
					log(str(message.author) + " Disabled Logging")
					# LOG
					logflag = False
					await message.channel.send("Logging disabled")
				if instruction[2] == "check":
					# LOG
					log(str(message.author) + " Check logged, it is" + str(logflag))
					if logflag:
						await message.channel.send("Logging is currently enabled.")
					else:
						await message.channel.send("Logging is currently disabled.")
		elif instruction[1] == "sus":
			if validMessage(message):
				if instruction[2] == "enable":
					# LOG
					susflag = True
					log(str(message.author) + " Enabled Sus")
					await message.channel.send("Sus enabled")
				if instruction[2] == "disable":
					log(str(message.author) + " Disabled Sus")
					# LOG
					susflag = False
					await message.channel.send("Sus disabled")
				if instruction[2] == "check":
					# LOG
					log(str(message.author) + " Check logged, it is" + str(susflag))
					if logflag:
						await message.channel.send("Sus is currently enabled.")
					else:
						await message.channel.send("Sus is currently disabled.")

			else:
				# LOG
				log(str(message.author) +
					"tries to use use sus but has no proper permission")

				await cant(message)

def check_sell_items(fromm:str, to:str, item:str, quan:int):
	global items
	global money
	try:
		items[item]["users"][fromm]
	except KeyError:
		items[item]["users"][fromm] = "0"
	try:
		items[item]["users"][to]
	except KeyError:
		items[item]["users"][to] = "0"
	
	if quan > float(items[item]["users"][fromm]):
		return False
	return True

@tree.command(name="summon", description="🔮(Magically) Summons a person online")
@app_commands.describe(person="Who do you want to summon?")
async def summon(interaction:discord.Interaction, person:discord.User):
	if int(person.id) == int(interaction.user.id): await interaction.response.send_message(f"You can't summon yourself.")
	if client.get_user(int(person.id)).bot: await interaction.response.send_message(f"No matter how hard I try, bots cannot be summoned.")
	await interaction.response.send_message(f"Summoned.",ephemeral=True)
	await interaction.channel.send(f"<@{person.id}>,\n||<@{interaction.user.id}>|| is summoning you!")
	lol = ("They didn't give you up, don't let them down!", "Be online now please, or I can't promise that they will still be sane when you went online again.")
	await client.get_user(int(person.id)).send(f"<@{interaction.user.id}> was trying to summon you in **{interaction.guild.name}**, in the channel of **#{interaction.channel.name}**\n{random.Random().choice(seq=lol)}")
	log(str(interaction.user.id) + "tried to summon" + str(person.id))

@tree.command(name="poll", description="Make a new poll using this command")
@app_commands.describe(question="What is the poll about?")
@app_commands.describe(choices="Seperate poll choices by comma. You can only have ten choices maximum.")
async def poll(interaction:discord.Interaction, question:str, choices:str=None):
	emjs = ("1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟")
	if choices == None:
		choices = "Yes,No"
		emjs = ("👍","👎")
	choices = choices.split(',')
	if len(choices) > 10:
		interaction.response.send_message(f"You can have no more than 10 choices.", ephemeral=True)
		return
	i = 0
	res = f"Poll:\n{question}\n"

	for choice in choices:
		res += emjs[i]
		res += f" - {choice}\n"
		i += 1

	await interaction.response.send_message(res)

	i = 0
	while i < len(choices):
		mesg = await interaction.original_response()
		await mesg.add_reaction(emjs[i])
		i += 1
	log(str(interaction.user.id) + "made a poll")

@tree.command(name="give", description="Give away items!")
@app_commands.describe(item=f"What item?")
@app_commands.describe(quantity=f"How many would you like to give")
@app_commands.describe(message="Optional message attached to your gift.")
@app_commands.describe(to="Who are you going to give it to?")
@app_commands.choices(item=itemslist)
async def sell(interaction:discord.Interaction, to:discord.User, item:app_commands.Choice[str], quantity:int, message:str=None):
	embe = discord.Embed(color=embec)
	
	embe.set_author(name=str(interaction.user.display_name), icon_url=interaction.user.avatar)
	embe.set_footer(text=f"{datetime.datetime.now()}")

	if quantity <= 0:
		embe.add_field(name="Error", value="Quantity is 0 or negative.", inline=False)
		await interaction.response.send_message(embed=embe)
		return
	if not check_sell_items(str(interaction.user.id), str(to.id), str(item.value), quantity):
		embe.add_field(name="Error", value=f"You don't have enough {item.name}.", inline=False)
		await interaction.response.send_message(embed=embe)
		return
	if str(interaction.user.id) == str(to.id):
		embe.add_field(name="Error", value="You can't give stuff to yourself.")
		await interaction.response.send_message(embed=embe)
		return

	items[item.value]["users"][str(interaction.user.id)] = str(float(items[item.value]["users"][str(interaction.user.id)]) - float(quantity))
	items[item.value]["users"][str(to.id)] = str(float(items[item.value]["users"][str(to.id)]) + float(quantity))

	save_items()
	load_items()

	if message == None:
		embe.add_field(name="Gift", value=f"Hello <@{to.id}>,\n<@{interaction.user.id}> gave you {quantity} {item.name}.\nEnjoy!")
		await interaction.response.send_message(embed=embe)
		return
	embe.add_field(name="Gift", value=f"Dear <@{to.id}>,\n    Please enjoy the {quantity} {item.name} I give you.\n    {message}\nBest Wishes,<@{interaction.user.id}>")
	await interaction.response.send_message(embed=embe)
	log(str(interaction.user.id) + "is generous")

def get_item_msg(id):
	if id == "": pass
	else: return "Nothing happened."

@tree.command(name="mine", description="Go mining!")
async def mine(interaction:discord.Interaction):
	log(str(interaction.user.id) + "mines")
	item = app_commands.Choice(name="Pickaxe", value="pick")
	quantity = 1
	embe = discord.Embed(color=embec)
	
	embe.set_author(name=str(interaction.user.display_name), icon_url=interaction.user.avatar)
	embe.set_footer(text=f"{datetime.datetime.now()}")

	if not check_sell_items(str(interaction.user.id), str(interaction.user.id), str(item.value), quantity):
		embe.add_field(name="Error", value=f"You don't have any {item.name}s. Use /buy to buy one!", inline=False)
		await interaction.response.send_message(embed=embe)
		return

	save_items()
	load_items()

	try:
		save_items()
		load_items()
		theval = random.Random().choice(seq=items[item.value]["use"])
		thing = "ABSOLUTELY NOTHING!!"

		if item.value == "pick":
			theval = ""
			pickaxe_rng = random.randint(0, 1000)
			break_rng = random.randint(0, 1000)
			if break_rng <= 400:
				theval += "\n**your pickaxe broke.**"
				items[item.value]["users"][str(interaction.user.id)] = str(float(items[item.value]["users"][str(interaction.user.id)]) - float(1))

			if pickaxe_rng == 71:
				thing = "TURRNUTIUM"
				theval += "\n(You only have **0.1% chance** of getting this item)"
				buy_items(str(interaction.user.id), "turrnutium", 1)
			elif pickaxe_rng <= 200:
				theval += "\n(You have **20% chance** of getting this)"
			elif pickaxe_rng <= 500:
				thing = "COAL"
				theval += "\n(You have **30% chance** of getting this item)"

				diamond_rng = random.randint(0, 1000)
				if diamond_rng == 71 and False:
					theval += "\nBut wait! With enough pressure... **YOU TURNED COAL INTO DIAMOND💎, BABYYYY!!!!** *(This only happens only 0.1% of the time when you get coal!)*"
					buy_items(str(interaction.user.id), "diamond", 1)
				else:
					buy_items(str(interaction.user.id), "coal", 1)
				save_items()
				load_items()

			elif pickaxe_rng <= 750:
				mystery = random.randint(5, 25)
				thing = f"{mystery} TURRCOINS"
				theval += "\n(You have **25% chance** of getting this item)"
				money[find_money(Money(str(interaction.user.id), 0))].balance = float(money[find_money(Money(str(interaction.user.id), 0))].balance) + float(mystery)
				save_money()
				load_money()
				save_items()
				load_items()
			elif pickaxe_rng <= 900:
				thing = "QUARTZ"
				theval += "\n(You have **15% chance** of getting this item)"
				buy_items(str(interaction.user.id), "quartz", 1)
			elif pickaxe_rng <= 950:
				thing = "GOLD"
				theval += "\n(You have **5% chance** of getting this item)"
				buy_items(str(interaction.user.id), "gold", 1)
			elif pickaxe_rng <= 975:
				thing = "EMERALD"
				theval += "\n(You have **2.5% chance** of getting this item)"
				buy_items(str(interaction.user.id), "emerald", 1)
			elif pickaxe_rng <= 995:
				thing = "DIAMOND"
				theval += "\n(You only have **2% chance** of getting this item)"
				buy_items(str(interaction.user.id), "diamond", 1)
			else:
				thing = "TUVALUNIUM"
				theval += "\n(You only have **0.4% chance** of getting this item)"
				buy_items(str(interaction.user.id), "tuvalunium", 1)
			save_items()
			load_items()

		embe.add_field(name=f"You found {thing}!!!", value=theval)
	except KeyError as e:
		print(traceback.format_exc())
		print(items["emerald"]["users"])
		embe.add_field(name=f"You used {str(quantity)} {item.name}...", value=e)
	await interaction.response.send_message(embed=embe)
@tree.command(name="use", description="Use items!")
@app_commands.describe(item=f"What item?")
@app_commands.describe(quantity=f"How many would you like to use?")
@app_commands.choices(item=itemslist)
async def use(interaction:discord.Interaction, item:app_commands.Choice[str], quantity:int):
	embe = discord.Embed(color=embec)
	
	embe.set_author(name=str(interaction.user.display_name), icon_url=interaction.user.avatar)
	embe.set_footer(text=f"{datetime.datetime.now()}")

	coalstuff = ""
	coalflag = False

	if quantity <= 0:
		embe.add_field(name="Error", value="Quantity is 0 or negative.", inline=False)
		await interaction.response.send_message(embed=embe)
		return
	if not check_sell_items(str(interaction.user.id), str(interaction.user.id), str(item.value), quantity):
		embe.add_field(name="Error", value=f"You don't have enough {item.name}.", inline=False)
		await interaction.response.send_message(embed=embe)
		return
	try:
		if str(items[item.value]["usable"]) == "1":
			items[item.value]["users"][str(interaction.user.id)] = str(float(items[item.value]["users"][str(interaction.user.id)]) - float(quantity))

			if item.value == "coal":
				coalflag = True
				if quantity == 1:
					if random.randint(0, 2500) == 420:
						coalstuff += "\nWith enough pressure... \nYOU TURNED COAL INTO DIAMOND💎, BABYYYY\n-# (only 0.04% chance!)"
						buy_items(str(interaction.user.id), "diamond", 1)
					else:
						coalstuff += "\nWith enough pressure... \nthe coal crumbles in your hands."
				
				elif quantity > 1:
					coal_busts = 0
					coal_hits = 0
					for i in range(quantity):
						if random.randint(0, 2500) == 420:
							coal_hits += 1
						else:
							coal_busts += 1

					if coal_hits == 0:
						coalstuff += "\nYou just wasted " + str(coal_busts) + " pieces of coal. Congrats."
					else:
						coalstuff += "\nYou broke " + str(coal_busts) + " pieces of coal...\nBUT MADE " + str(coal_hits) + " DIAMONDS!!!!!💎"
						buy_items(str(interaction.user.id), "diamond", coal_hits)

				save_items()
				load_items()
			
	except: pass

	save_items()
	load_items()

	try:
		save_items()
		load_items()
		theval = random.Random().choice(seq=items[item.value]["use"])
		
		embe.add_field(name=f"You used {str(quantity)} {item.name}...", value=theval if not coalflag else theval + coalstuff)
	except KeyError as e:
		print(traceback.format_exc())
		embe.add_field(name=f"You used {str(quantity)} {item.name}...", value="But something went wrong in the code.")
	await interaction.response.send_message(embed=embe)
	log(str(interaction.user.id) + "tried to use something")


@tree.command(name="buy", description="Buy stuff using turrcoins!")
@app_commands.describe(item=f"What would you like to buy?")
@app_commands.describe(quantity=f"How many would you like to buy?")
@app_commands.choices(item=itemslist)
async def buy(interaction:discord.Interaction,item:app_commands.Choice[str],quantity:int):
	global money
	global items
	embe = discord.Embed(color=embec)
	
	embe.set_author(name=str(interaction.user.display_name), icon_url=interaction.user.avatar)
	embe.set_footer(text=f"{datetime.datetime.now()}")
	if quantity <= 0:
		embe.add_field(name="Error", value="Quantity is 0 or negative.", inline=False)
	elif not buy_items(str(interaction.user.id), item.value, quantity):
		cost = str(quantity * float(items[item.value]["price"]))
		msg = f"{str(quantity)} {item.name} costs {cost} turrcoins, You only have {float(money[find_money(Money(interaction.user.id, 0))].balance)}."
		embe.add_field(name="Error",value=msg,inline=False)
	else :
		if item.value in ("coal", "quartz", "gold", "emerald", "diamond", "tuvalunium", "turrnutium"):
			msg = f"Unfortunately, you can not buy this {item.name} because it is a mineral. The only way to obtain it is by mining. \nYou can buy a pickaxe using /buy and then use /mine."
			embe.add_field(name="Error",value=msg,inline=False)
		else:	
			cost = str(quantity * float(items[item.value]["price"]))
			print("COST EVALUTED")
			msg = f"You bought {str(quantity)} {item.name} for {cost} turrcoins.\nYour balance is {float(money[find_money(Money(interaction.user.id, 0))].balance)}."
			embe.add_field(name="Success",value=msg,inline=False)
	await interaction.response.send_message(embed=embe)
	log(str(interaction.user.id) + "wants to buy something")

@tree.command(name="blackjack", description="Start a new game of blackjack and play against the computer for a chance to win Turrcoins!")
@app_commands.describe(wager=f"How many Turrcoins do you bet?")
async def blackjack(interaction:discord.Interaction,wager:float):
	global money
	global items
	
	msg = ""

	embe = discord.Embed(color=embec)
	
	embe.set_author(name=str(interaction.user.display_name), icon_url=interaction.user.avatar)
	embe.set_footer(text=f"{datetime.datetime.now()}")

	userbalance = float(money[find_money(Money(str(interaction.user.id), 0))].balance)

	if wager <= 0:
		embe.add_field(name="Error", value=f"Nice try, but wager amount cannot be 0 or negative like the number {str(wager)}", inline=False)
		await interaction.response.send_message(embed=embe)
		return
	if userbalance <= -100:
		embe.add_field(name="Nice try, champ.", value=f"You're in too much debt. Come back when you're not broke.", inline=False)
		await interaction.response.send_message(embed=embe)
		return
	if userbalance - wager <= -100:
		embe.add_field(name="Nice try, champ.", value=f"You can't just produce infinite turrcoins out of thin air.\nTry making a reasonable bet.", inline=False)
		await interaction.response.send_message(embed=embe)
		return
	
	game = bj(str(interaction.user.id), wager)

	if game["status"] == "ok":
		money[find_money(Money(str(interaction.user.id), 0))].balance = float(money[find_money(Money(str(interaction.user.id), 0))].balance) - wager
	
	save_money()
	load_money()

	userbalance = float(money[find_money(Money(str(interaction.user.id), 0))].balance)

	msg = game["message"] + f"\n\nYou have {userbalance} turrcoins." + "\nYou: **" + str(game["player"]) + "**\nComputer: **" + str(game["computer"]) + "**\nBet: **" + str(game["wager"]) + "**"

	embe.add_field(name="Blackjack", value=msg, inline=False)
	await interaction.response.send_message(embed=embe, view=BlackjackButton())

@tree.command(name="earnings", description="Check a user's lifetime blackjack earnings")
@app_commands.describe(user=f"Which user do you want to check? Leave blank for self.")
async def earnings(interaction:discord.Interaction,user:discord.User=None):
    global items
    if user == None:
        user = interaction.user
    userid = user.id
    username = user.display_name
    useravatar = user.avatar

    embe = discord.Embed(color=embec)
    
    embe.set_author(name=f"Lifetime casino earnings of {username}", icon_url=useravatar)
    embe.set_footer(text=f"{datetime.datetime.now()}")
    
    earnings = {}
    if os.path.exists(pathify("blackjack|earnings.json")):
        with open(pathify("blackjack|earnings.json"), "r") as f:
            try:
                earnings = json.load(f)
            except json.JSONDecodeError:
                earnings = {}
    earning = earnings[str(user.id)]
    earningtext = "LOST" if earning < 0 else "WON"

    embe.add_field(name=earningtext, value=f"{str(abs(earning))} TRC", inline=False)
    await interaction.response.send_message(embed=embe)
    log(str(interaction.user.id) + "earnings check")

@tree.command(name="coin", description="Flip a coin!")
async def coin(interaction:discord.Interaction):
	embe = discord.Embed(color=embec)
	
	embe.set_author(name=str(interaction.user.display_name), icon_url=interaction.user.avatar)
	embe.set_footer(text=f"{datetime.datetime.now()}")

	face = random.Random().choice(seq=("HEADS!!!", "TAILS!!!"))
	embe.add_field(name=face, value=face, inline=False)

	await interaction.response.send_message(embed=embe)


@tree.command(name="item", description="Check Item")
@app_commands.describe(item=f"What item would you like to check")
@app_commands.describe(user=f"What user do you want to check the item on? Leave blank to check your own.")
@app_commands.choices(item=itemslist)
async def item_check(interaction:discord.Interaction,item:app_commands.Choice[str],user:discord.User=None):
	global items
	if user == None:
		user = interaction.user
	userid = user.id
	username = user.display_name
	useravatar = user.avatar

	embe = discord.Embed(color=embec)
	
	embe.set_author(name=f"Items of {username}", icon_url=useravatar)
	embe.set_footer(text=f"{datetime.datetime.now()}")
	
	itemname = item.name
	itemprice = str(float(items[item.value]["price"]))
	count = 0
	try:
		count = str(int(float(items[item.value]["users"][str(userid)])))
	except KeyError:
		print("BRUH")
	descr = items[item.value]["desc"]
	
	embe.add_field(name=f"Item name",value=f"{itemname}",inline=True)
	embe.add_field(name=f"Quantity",value=f"{count}",inline=True)
	embe.add_field(name=f"Unit price",value=f"{itemprice} turrcoins",inline=True)
	embe.add_field(name=f"Item Description",value=f"{descr}",inline=False)
	await interaction.response.send_message(embed=embe)
	log(str(interaction.user.id) + "checks on items")

@tree.command(name="minerals", description="Check a user's minerals")
@app_commands.describe(user=f"Which user do you want to check? Leave blank for self.")
async def minerals_check(interaction:discord.Interaction,user:discord.User=None):
	global items
	if user == None:
		user = interaction.user
	userid = user.id
	username = user.display_name
	useravatar = user.avatar

	embe = discord.Embed(color=embec)
	
	embe.set_author(name=f"Minerals of {username}", icon_url=useravatar)
	embe.set_footer(text=f"{datetime.datetime.now()}")
	
	minerals = [
		app_commands.Choice(name="Coal", value="coal"),
		app_commands.Choice(name="Quartz", value="quartz"),
		app_commands.Choice(name="Gold", value="gold"),
		app_commands.Choice(name="Emerald", value="emerald"),
		app_commands.Choice(name="Diamond", value="diamond"),
		app_commands.Choice(name="Tuvalunium", value="tuvalunium"),
		app_commands.Choice(name="Turrnutium", value="turrnutium"),
	]

	nworth = 0
	for item in minerals:
		itemname = item.name
		itemprice = str(float(items[item.value]["price"]))
		count = 0
		try:
			count = str(int(float(items[item.value]["users"][str(userid)])))
		except KeyError:
			print("BRUH")
		# descr = items[item.value]["desc"]
		
		embe.add_field(name=f"{itemname}",value=f"{count}",inline=True)
		# embe.add_field(name=f"Quantity",value=f"{count}",inline=False)
		# embe.add_field(name=f"Unit price",value=f"{itemprice} turrcoins",inline=False)
		# embe.add_field(name=f"Item Description",value=f"{descr}",inline=False)
		nworth += float((float(count) * float(itemprice)))
	embe.add_field(name="TOTAL EVALUATION", value=f"{nworth} TRC", inline=False)
	await interaction.response.send_message(embed=embe)
	log(str(interaction.user.id) + "minerals check")


@tree.command(name="calculate", description="Try the turrnut mathematic and logical calculator!")
@app_commands.describe(expression="Arithmetic or boolean expression")
async def calc(interaction:discord.Interaction, expression: str):

	result, error = lang.run("<discord_runtime>", expression)
	print("\n\nDone calculation >:)))\n")
	if error:
		await interaction.response.send_message(str(error.__repr__()),ephemeral=True)
	else:
		await interaction.response.send_message(str(expression) + "=" + str(result.value))


	
@tree.command(name="collect", description="Get your turrcoin award using this command.")
async def daily(interaction:discord.Interaction):
	global money
	global AWARD

	AWARD = round(random.Random().uniform(5.0,15.0), 3)
	if str(interaction.user.id) == "1405608029134782545": # Mergeaso
		AWARD = math.pi

	load_money()

	awards = None
	with open(pathify("awards|awards.json"), "r") as fobj:
		awards = json.load(fobj)
	i = 0
	have = False
	for mon in money:
		if str(mon.id) == str(interaction.user.id):
			have = True
			break
		i += 1
	if not have:
		await interaction.response.send_message("You didn't have an account yet. Use /balance on me to create one!")
		return

	new = False
	if not str(interaction.user.id) in awards:
		new = True
	else:
		if float(awards[str(interaction.user.id)]) > float(float(time.time())) - 600:
			minutes , seconds = mtms(round(float(float(600 - (float(float(time.time())) - float(awards[str(interaction.user.id)]))) /60  ), 1 ))
			await interaction.response.send_message(f"Try again in ||{ minutes } minutes {seconds} seconds||")
			return
	awards[str(interaction.user.id)] = str(float(time.time()))
	with open(pathify("awards|awards.json"), "w") as fobj2:
		json.dump(awards, fobj2, indent=6)
	

	money[i] = Money(str(interaction.user.id), str(float(money[i].balance) + AWARD))
	await interaction.response.send_message(f"Congrats <@{interaction.user.id}>, you have just earned {str(AWARD)} turrcoins!")
	save_money()
	load_money()
	log(str(interaction.user.id) + "loves money")

@tree.command(name="factorial", description="Calculator but with factorials")
@app_commands.describe(expression="Arithmetic expression")
async def fact(interaction:discord.Interaction, expression: str):
	result, error = lang.run("<discord_runtime>", expression)
	if error:
		await interaction.response.send_message(str(error.__repr__()), ephemeral=True)
	else:
		try :
			await interaction.response.send_message("Factorial of: " + str(expression) + " is " + str(math.factorial(int(str(result.value)))))	
		except:
			await interaction.response.send_message("Invalid Input", ephemeral=True) 
			return

@tree.command(name="never-have-i-ever", description="Never have I ever...?")
async def nh(interaction: discord.Interaction):
	global nhie
	embe = discord.Embed(title=f"Never Have I Ever", description=f"Type: NHIE, Requested by <@{interaction.user.id}>", color=embec)
	
	embe.add_field(name=f"{random.Random().choice(seq=nhie)}", value=" ", inline=False)
	embe.set_footer(text=f"{datetime.datetime.now()}")

	await interaction.response.send_message(embed=embe, view=NHIEButton())

@tree.command(name="suggest", description="Suggestion a new feature!")
@app_commands.describe(suggestion="What feature would you like to suggest?")
async def sugg(interaction: discord.Interaction, suggestion:str):
	global embec
	
	suggs = ""
	with open(pathify("suggestions|suggestions.txt"),"r") as f:
		suggs = f.read()

	with open(pathify("suggestions|suggestions.txt"),"w") as f2:
		f2.write(f"{suggs}{str(interaction.user)} ({str(interaction.user.id)}) : {suggestion}\n")
	
	embe = discord.Embed(title="New suggestion", description=f"By <@{interaction.user.id}>", color=embec)
	embe.add_field(name="Suggestion:", value=suggestion, inline=False)
	await interaction.response.send_message(embed=embe)

@tree.command(name="would-you-rather", description="Play the would you rather game!")
async def wy(interaction: discord.Interaction):
	global wyr
	embe = discord.Embed(title=f"Would You Rather", description=f"Type: WYR, Requested by <@{interaction.user.id}>", color=embec)
	
	embe.add_field(name=f"{random.Random().choice(seq=wyr)}", value=" ", inline=False)
	embe.set_footer(text=f"{datetime.datetime.now()}")

	await interaction.response.send_message(embed=embe, view=WYRButton())

@tree.command(name="truth-or-dare", description="TRUTH or DARE??!! Use this command to play!")
@app_commands.describe(type="Leave blank for a random question")
@app_commands.choices(type=[
	app_commands.Choice(name="Truth",value=1),
	app_commands.Choice(name="Dare",value=2),
	app_commands.Choice(name="Random(Default)",value=3)
])
async def tod(interaction: discord.Interaction, type: app_commands.Choice[int]=None):
	global truth
	global dare
	t = 3
	qtype = "r"
	if type != None:
		t = type.value
	if t == 1:
		qtype = "t"
	elif t == 2:
		qtype = "d"
	elif t == 3:
		qtype = random.Random().choice(seq=("t","d"))

	if qtype == "t":
		embe = discord.Embed(title=f"Truth or Dare", description=f"Type: Truth, Requested by <@{interaction.user.id}>", color=embec)
	
		embe.add_field(name=f"{random.Random().choice(seq=truth)}", value=" ", inline=False)
		embe.set_footer(text=f"{datetime.datetime.now()}")

		await interaction.response.send_message(embed=embe, view=TODButton())
		return
	embe = discord.Embed(title=f"Truth or Dare", description=f"Type: Dare, Requested by <@{interaction.user.id}>", color=embec)
	
	embe.add_field(name=f"{random.Random().choice(seq=dare)}", value=" ", inline=False)
	embe.set_footer(text=f"{datetime.datetime.now()}")

	await interaction.response.send_message(embed=embe, view=TODButton())
@tree.command(name="pay", description="Give someone an amount of turrcoins")
@app_commands.describe(receiver="The person who receive this money")
@app_commands.describe(amount="How much money to transfer")
async def pay(interaction: discord.Interaction, receiver: discord.Member, amount: float):
	global money
	load_money()
	send = ""
	fail = True
	hasacc = False
	checking = True
	for mon in money:
		if str(mon.id) == str(interaction.user.id):
			hasacc = True
			break
	if not hasacc:
		money.append(Money(str(interaction.user.id), str(0)))
	save_money()
	load_money()
	
	index = 0
	for mon in money:
		if str(mon.id) == str(interaction.user.id):
			break
		index += 1
	load_money()
	account = money.pop(index)
	if amount > float(account.balance):
		send = f"Can't complete transcation. You only have {str(account.balance)} coins but you attempt to transfer {amount}"
		checking= False
	elif float(amount) <= 0:
		send = f"Can't complete transcation. the amount is 0 or negative"
		checking= False
	elif str(receiver.id) == str(interaction.user.id):
		send = f"Can't complete transcation. You can't give yourself money"
		checking= False
	else: pass
	
	if not checking:
		embe = discord.Embed(title=f"Error", description=f"<@{interaction.user.id}> to <@{receiver.id}>", color=embec)
	
		embe.add_field(name=f"{send}", value="Transaction failed", inline=False)
		embe.set_footer(text=f"{datetime.datetime.now()}")
		await interaction.response.send_message(embed=embe)
		return

	hasacc = False
	for mon in money:
		if str(mon.id) == str(receiver.id):
			hasacc = True
			break
	if not hasacc:
		money.append(Money(str(receiver.id), str(0)))
	save_money()
	load_money()
	index = 0
	for mon in money:
		if str(mon.id) == str(receiver.id):
			break
		index += 1
	load_money()
	rec = money.pop(index)
	print(f"AMOUNT: {amount}")
	e1 = float(account.balance) - float(amount)
	e2 = float(rec.balance) + float(amount)
	account.balance = str(e1)
	rec.balance = str(e2)

	print(f"giver:{account.balance}, receiver: {rec.balance}")
	money.append(account)
	money.append(rec)
	save_money()
	load_money()
	
	fail = False
	val = "Failure"
	if not fail:
		val = "Success"
	embe = discord.Embed(title=f"Transaction", description=f"<@{interaction.user.id}> to <@{receiver.id}>", color=embec)
	
	embe.add_field(name=f"Paid: {amount} turrcoins", value=val, inline=False)
	embe.set_footer(text=f"{datetime.datetime.now()}")
	await interaction.response.send_message(embed=embe, ephemeral=fail)
	log(str(interaction.user.id) + "wants to pay" + str(receiver.id) + " " + str(amount))

def mykey(obj: Money):
	return float(obj.balance)

@tree.command(name="leaderboard", description="See the top ranked turrcoin owners")
async def rank(interaction: discord.Interaction):
	global money
	global embec
	load_money()
	money.sort(key=mykey, reverse=True)
	until = 15
	if len(money) < until:
		until = len(money)
	resp = ""
	i = 1
	you = None
	for c in money:
		if i > until:
			break
		resp += f"{i}"
		if i in (1,11) : resp += "st"
		elif i in (2,12) : resp += "nd"
		elif i in (3,13) : resp += "rd"
		else: resp += "th"
		if str(c.id) == str(interaction.user.id):
			you = str(i)
		resp += f": <@{c.id}> (**{str(c.balance)}** coins)\n"
		i += 1
	if until == 20:
		resp += "**...**\n"
	if you != None:
			if int(you) in (1,11) : resp += f"\nYou(<@{str(interaction.user.id)}>) are in **{you}st** place."
			elif int(you) in (2,12) : resp += f"\nYou(<@{str(interaction.user.id)}>) are in **{you}nd** place."
			elif int(you) in (3,13) : resp += f"\nYou(<@{str(interaction.user.id)}>) are in **{you}rd** place."
			else: resp += f"\nYou(<@{str(interaction.user.id)}>) are in **{you}th** place."
	resp += f"\n{len(money)} Bank accounts in total."
	embe = discord.Embed(title="Turrcoins Leaderboard", description="Top 15 turrcoin holders", color=embec)
	embe.add_field(name="Ranking", value=resp, inline=False)
	await interaction.response.send_message(embed=embe)

@tree.command(name="balance", description="Check how much turrcoins you have")
@app_commands.describe(person="Leave blank to check your own balance")
async def balance(interaction: discord.Interaction, person: discord.User=None):
	global money
	load_money()
	hasacc = False
	theid = None
	if person == None:
		theid = interaction.user.id
	else:
		theid = person.id
	for mon in money:
		if str(mon.id) == str(theid):
			hasacc = True
			break
	if not hasacc:
		money.append(Money(str(theid), str(0)))
	save_money()
	load_money()
	index = 0
	for mon in money:
		if str(mon.id) == str(theid):
			break
		index += 1
	embe = discord.Embed(title=f"Turrnut bank", description=f"Account balance for user: <@{str(theid)}>", color=embec)
	if person != None:
		embe.set_author(name=str(person.display_name), icon_url=person.avatar)
	else: embe.set_author(name=str(interaction.user.display_name), icon_url=interaction.user.avatar)
	embe.add_field(name=f"{money[index].balance}", value=f"Turrcoins", inline=False)
	embe.set_footer(text=f"{datetime.datetime.now()}")
	await interaction.response.send_message(embed=embe)

@tree.command(name="predict-grade", description="Enter your grades for first three quarters to get the prediction of the final quarter!")
@app_commands.describe(first="First quater grade")
@app_commands.describe(second="Second quater grade")
@app_commands.describe(third="Third quater grade")
async def predictgrade(interaction: discord.Interaction, first:float, second:float, third:float):
	model = keras.models.load_model(pathify("models|grades"), compile=False)
	model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",metrics=["accuracy"])
	if first > 100 or first < 0 or second > 100 or second < 0 or third > 100 or third < 0:

		await interaction.response.send_message("Please make sure all the numbers are between 0 and 100!", ephemeral=True)
		return
	else:
		predictions = model.predict(np.asarray([
			[first, second, third]
		]))
		# LOG
		log(str(interaction.user) + " predict the grade as " +
		str(first) + " " + str(second) + " " + str(third))
		if first == second == third:
			await interaction.response.send_message(f"{first},{second},{third}\nThe turrnut Aritificial Intelligence predict that your final quarter grade will be: " + str(first) + "%\n100.0% Confidence")
		else:
			await interaction.response.send_message(f"{first},{second},{third}\nThe turrnut Aritificial Intelligence predict that your final quarter grade will be: " + str(round(possibilities[np.argmax(predictions[0])], 2)) + "%\n" + str(round(predictions[0][np.argmax(predictions[0])] * 100, 2)) + "% Confidence")
			
@tree.command(name="ask", description="Ask the fortune teller a question!")
@app_commands.describe(question="What question do you have?")
async def ask(interaction: discord.Interaction, question:str):
	q = f"<@{str(interaction.user.id)}> asks: ** {question}"
	yesorno = random.Random().choice(seq=("Definitely yes", "Very doubtful", "Maybe sorta kinda nope yep yes nah no possibly ye", "Definitely no", "Probably", "Probably not", "What did you say? Ask it again.", "I can't decide", "Why asking me?", "It's the... actually never mind", "I will ask for an oracle", "I don't know, ask the owner", "I know the answer but can't tell you"))
			
	q += f"? **\n> the fortune teller decided: ||{yesorno}||"
	await interaction.response.send_message(q)

@tree.command(name="help", description="Need technical support or learn more about the bot? Use this command!")
@app_commands.describe(command="Which command would you like to look at?")
@app_commands.choices(command=[
	app_commands.Choice(name="/ask",value="ask"),
	app_commands.Choice(name="/balance", value="bal"),
	app_commands.Choice(name="/buy", value="buy"),
	app_commands.Choice(name="/calculate",value="calc"),
	app_commands.Choice(name="/collect",value="day"),
	app_commands.Choice(name="/factorial",value="fact"),
	app_commands.Choice(name="/give",value="give"),
	app_commands.Choice(name="/help",value="help"),
	app_commands.Choice(name="/item",value="item"),
	app_commands.Choice(name="/leaderboard",value="rank"),
	app_commands.Choice(name="/meme",value="meme"),
	app_commands.Choice(name="/never-have-i-ever",value="nhie"),
	app_commands.Choice(name="/pay",value="pay"),
	app_commands.Choice(name="/poll",value="poll"),
	app_commands.Choice(name="/predict-grade",value="grade"),
	app_commands.Choice(name="/speak",value="speak"),
	app_commands.Choice(name="/suggest",value="sug"),
	app_commands.Choice(name="/summon",value="summon"),
	app_commands.Choice(name="/truth-or-dare",value="tod"),
	app_commands.Choice(name="/would-you-rather",value="wyr"),
])
async def inv(interaction: discord.Interaction, command: app_commands.Choice[str]="None!"):
	global embec
	global howmanywords
	if command == "None!":
		num_of_servers = 0
		for server in client.guilds:
			num_of_servers += 1

		await interaction.response.send_message(f"# hi.\nI am <@{str(client.user.id)}>\n# I am currently in {num_of_servers} servers!\n## My pronouns are she/her.\n### Click this link to invite me to your server: https://discord.com/oauth2/authorize?client_id=1014960764378939453&scope=bot \n### For more information, visit our website: https://turrnut.github.io/discordbot\n### For technical support, join our server: https://discord.gg/Xbt2mCjaz6")
		return

	elif command.value == "ask":
		embe = discord.Embed(title="Command /ask", description=f"Consult the oracle! Ask the fortune teller a question and it will randomly generate an answer", color=embec)
		embe.add_field(name="Required: question", value="What do you want to ask? Put it here!", inline=True)
		await interaction.response.send_message(embed=embe)

	elif command.value == "calc":
		embe = discord.Embed(title="Command /calculate", description=f"Use the turrnut expression evaluator via this command", color=embec)
		embe.add_field(name="**Required**: expression", value="Use + for addition, - for subtraction, * for multiplication, / for division and ^ for power. There is no need to put an \"=\" sign at the end. Create variables using 'val'.", inline=True)
		await interaction.response.send_message(embed=embe)

	elif command.value == "bal":
		embe = discord.Embed(title="Command /balance", description=f"Check to see how many turrcoins you have. Turrcoins are a type of currency created by me.", color=embec)
		embe.add_field(name="**Optional**: person", value="Leave blank if you want to check your own balance.", inline=True)
		await interaction.response.send_message(embed=embe)

	elif command.value == "buy":
		embe = discord.Embed(title="Command /buy", description=f"Buy an item from the store.", color=embec)
		embe.add_field(name="**Required**: item", value="Specify which item do you want to buy.", inline=True)
		embe.add_field(name="**Required**: quantity", value="Specify how many items you want to buy.", inline=True)
		await interaction.response.send_message(embed=embe)

	elif command.value == "item":
		embe = discord.Embed(title="Command /item", description=f"Check how many items does a person own. You can also check the unit price of an item with this command before you use /buy", color=embec)
		embe.add_field(name="**Required**: item", value="Specify which item do you want to check.", inline=True)
		embe.add_field(name="**Required**: user", value="This is where you tell the bot whose item you want to check. In other words, in here you will be selecting a user whose information about the ownership of an item will be displayed, it can be yourself but doesn\'t have to be", inline=True)
		await interaction.response.send_message(embed=embe)

	elif command.value == "day":
		embe = discord.Embed(title="Command /collect", description=f"Get turrcoins that refreshes every 10 minutes! If you don't have an account, use /balance to create one first.", color=embec)
		await interaction.response.send_message(embed=embe)

	elif command.value == "fact":
		embe = discord.Embed(title="Command /factorial", description=f"Use the turrnut expression evaluator via this command", color=embec)
		embe.add_field(name="**Required**: expression", value="Use the same syntax as you would use for /calculate, the final result will be the factorial of the original result", inline=True)
		await interaction.response.send_message(embed=embe)

	elif command.value == "pay":
		embe = discord.Embed(title="Command /pay", description=f"Transfer a certain amount of turrcoinss to another user.", color=embec)
		embe.add_field(name="**Required**: receiver", value="Specify to whom you wish to transfer the turrcoins", inline=True)
		embe.add_field(name="**Required**: amount", value="Specify the amount of turrcoins you intend to transfer", inline=True)
		await interaction.response.send_message(embed=embe)

	elif command.value == "give":
		embe = discord.Embed(title="Command /give", description=f"Give items you own to a person", color=embec)
		embe.add_field(name="**Required**: to", value="This is where you tell the bot who do you want to give your items to.", inline=True)
		embe.add_field(name="**Required**: item", value="You can select the item you want to give in here.", inline=True)
		embe.add_field(name="**Required**: quantity", value="You can specify how many of that item you want to give away.", inline=True)
		embe.add_field(name="**Optional**: message", value="Since this is a \"gift\", you can optionally attach a message to it that will be displayed to that person.", inline=True)
		await interaction.response.send_message(embed=embe)

	elif command.value == "poll":
		embe = discord.Embed(title="Command /poll", description=f"Want to ask for an opinion in the chat? Use this command to create a poll where people can express their opinions via reactions.", color=embec)
		embe.add_field(name="**Required**: question", value="What is a question you are wondering what people think? Put the question here.", inline=True)
		embe.add_field(name="**Optional**: choices", value="If left blank, the poll will be a yes/no question, but you can create your custom poll options by separating separate choices by comma(10 choices maximum)", inline=True)
		await interaction.response.send_message(embed=embe)
	
	elif command.value == "rank":
		embe = discord.Embed(title="Command /leaderboard", description=f"See the top 15 turrcoin holders!", color=embec)
		await interaction.response.send_message(embed=embe)

	elif command.value == "help":
		embe = discord.Embed(title="Command /help", description=f"Display a help message", color=embec)
		embe.add_field(name="**Optional**: command", value="If you need help with a specific command, use this parameter, otherwise, leave it blank.", inline=True)
		await interaction.response.send_message(embed=embe)

	elif command.value == "meme":
		embe = discord.Embed(title="Command /meme", description=f"Get a random meme!", color=embec)
		await interaction.response.send_message(embed=embe)

	elif command.value == "nhie":
		embe = discord.Embed(title="Command /never-have-i-ever", description=f"Play the Never Have I Ever game!", color=embec)
		await interaction.response.send_message(embed=embe)

	elif command.value == "grade":
		embe = discord.Embed(title="Command /predict-grade", description=f"A command for students: enter your first, second and third quarter grade to get a prediction of what your final quarter grade might be. This command use turrnut's AI.", color=embec)
		embe.add_field(name="**Required**: first", value="Your first quarter grade(A number between 0 and 100)", inline=True)
		embe.add_field(name="**Required**: second", value="Your second quarter grade(A number between 0 and 100)", inline=True)
		embe.add_field(name="**Required**: third", value="Your third quarter grade(A number between 0 and 100)", inline=True)
		await interaction.response.send_message(embed=embe)

	elif command.value == "speak":
		embe = discord.Embed(title="Command /speak", description=f"Make the bot say something.", color=embec)
		embe.add_field(name="**Required**: message", value="What do you want the bot to say?", inline=True)
		await interaction.response.send_message(embed=embe)

	elif command.value == "summon":
		embe = discord.Embed(title="Command /summon", description=f"Have a AFK friend you would like to be online? Use this command to (magically) \"summon\" your friend online. We can\'t promise it will be successful, though.", color=embec)
		embe.add_field(name="**Required**: person", value="Who do you want to summon?", inline=True)
		await interaction.response.send_message(embed=embe)

	elif command.value == "sug":
		embe = discord.Embed(title="Command /suggest", description=f"Suggest a new feature to the bot or report a bug.", color=embec)
		embe.add_field(name="**Required**: suggestion", value="What is your suggestion?", inline=True)
		await interaction.response.send_message(embed=embe)

	elif command.value == "tod":
		embe = discord.Embed(title="Command /truth-or-dare", description=f"Play the Truth or Dare game!", color=embec)
		embe.add_field(name="**Optional**: type", value="Specify what kind of question do you want: truth, dare, or random. If left blank, it will be random", inline=True)
		await interaction.response.send_message(embed=embe)

	elif command.value == "wyr":
		embe = discord.Embed(title="Command /wyr", description=f"Play the Would you rather game!", color=embec)
		await interaction.response.send_message(embed=embe)

	else:
		embe = discord.Embed(title=f"Command {command.name}", description=f"Coming soon...", color=embec)
		await interaction.response.send_message(embed=embe)
	


@tree.command(name="meme", description="Get a random meme!")
async def mem(interaction: discord.Interaction):
	log(str(interaction.user) + " prompted a random meme")

	load_meme()
	meme = random.Random().choice(seq=memes)
	# await interaction.response.send_message("https://cdn.discordapp.com/attachments/1126943272271622205/1137119843934552085/image.png")
	await interaction.response.send_message(str(meme.name))
	# await interaction.channel.send("\nAs suggested by: " + str(meme.suggested))

@tree.command(name="compliment", description="Get a compliment!")
@app_commands.describe(to="Who do you want to give the compliment to? Leave blank for yourself.")
async def compliment(interaction: discord.Interaction, to: discord.User=None):
	global compliments
	comp = random.Random().choice(seq=compliments)
	
	recipient = to.id if to is not None else interaction.user.id
	
	embe = discord.Embed(description=f"<@{recipient}>, **{comp}**", color=embec)
	embe.set_footer(text=f"{datetime.datetime.now()}")

	log(str(interaction.user) + " prompted a random compliment")

	# await interaction.response.send_message("https://cdn.discordapp.com/attachments/1126943272271622205/1137119843934552085/image.png")
	await interaction.response.send_message(embed=embe)
	# await interaction.channel.send("\nAs suggested by: " + str(meme.suggested))

@tree.command(name="speak", description="Make me say something!")
@app_commands.describe(message="What to do you want me to say?")
@app_commands.describe(replyto="Reply to a message(link). Leave blank if none.")
async def speakkc(interaction: discord.Interaction, message:str, replyto:str=None):
	try:
		if validInteraction(interaction) or interaction.user.guild_permissions.manage_messages:
			if replyto == None:
				await interaction.response.send_message("Sent.", ephemeral=True)
				log(str(interaction.user) + " Made me say \"" + message + "\"")
				await interaction.channel.send(message)
				return
			else:
				link = replyto
				link = link.split('/')
				server_id = int(link[4])
				channel_id = int(link[5])
				msg_id = int(link[6])
				print(f"serverid: {server_id}, channelid: {channel_id}, msgid: {msg_id}")

				server = client.get_guild(server_id)
				channel = server.get_channel(channel_id)
				if channel is None:
					channel = await client.fetch_channel(channel_id)
				mesg = await channel.fetch_message(msg_id)
				await interaction.response.send_message("Reply sent.", ephemeral=True)
				await mesg.reply(message)
				return
		await interaction.response.send_message("You can't use this command, you don't have `Manage Messages` permission",ephemeral=True)
	except AttributeError as e:
		if replyto == None:
			await interaction.response.send_message("Sent.", ephemeral=True)
			print(str(interaction.user) + " Made me say \"" + message + "\" in DMs")
			await interaction.channel.send(message)
			return
		else:
			link = replyto
			link = link.split('/')
			server_id = int(link[4])
			channel_id = int(link[5])
			msg_id = int(link[6])
			print(f"serverid: {server_id}, channelid: {channel_id}, msgid: {msg_id}")

			server = client.get_guild(server_id)
			channel = server.get_channel(channel_id)
			await interaction.response.send_message("Reply sent.", ephemeral=True)
			mesg = await channel.fetch_message(msg_id)
			await mesg.reply(message)
			return	

@client.event
async def on_reaction_add(reaction, user):
	if user.bot:
		return
	print("someone added a reaction")

@client.event
async def on_ready():
	global guilds
	print(f'Bot Name: {client.user}')
	print(f"servers the bot is in ( {len(client.guilds) } ): ", end="")
	num_of_servers = 0
	for server in client.guilds:
		print(server, f"({server.id}),", end="")
		guilds.append(int(server.id))
		num_of_servers += 1
	# for guild in guilds:
		# await client.tree.sync(guild=discord.Object(id=guild))
	# change status reference: https://stackoverflow.com/questions/59126137/how-to-change-activity-of-a-discord-py-bot
	# await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"members from {num_of_servers} servers"))
	await client.change_presence(status=discord.Status.idle, activity=discord.Activity(name="Insomnia Competition",type=5))
	print("\n\n\n")


@client.event
async def on_member_join(member):
	global SERVER_NAME
	global MYSERVER
	if True:
		print('new member!')
	#	await member.send('!!!!!!!!!!!!!!!!!\nHello! Welcome to the Offical Turrnut Republic Discord Server! In this server you can chat, socialize and play games with other people.\nTo customize your experience at our server, please pick your pronoun roles and ping roles in the #roles channel\nAlso, it\'s good to read the #server-rules channel because it contains useful information about what to do and not to do in our server\n\nGoodbye, have fun!')
	#	await member.send('https://tenor.com/view/morgan-freeman-gif-24496452')

@client.event
async def on_member_remove(member):
	await client.get_user(int(member.id)).send("bye nerd")
	await client.get_user(int(member.id)).send("https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713")
@client.event
async def on_message(message):
	global mensaje
	global ignore_bad_words
	global curse_words
	global react_all
	global susflag
	mensaje = message

	for react in react_all:
		try:
			await message.add_reaction(react)
		except: print("failed reaction all")

	if message.author == client.user:
		return

	print(message.author,
		  f"( { str(message.author.id) } ) : ", message.content, sep="", end="")
#	print("\a")
	if mensaje.guild == None:
		plog(f"{str(mensaje.author)} says -> {str(mensaje.content)}")
		print(" {DIRECT MESSAGE}")
	else:
		print()
	if message:
		pass
	#	randomnumber = random.Random().choice(seq=range(100))
	#	if randomnumber < 5:
	#		# LOG
	#		log(str(message.author) + " got greeted by the random greeting system")
	#		at = "<@" + str(message.author.id) + ">"
	#		await message.channel.send(random.Random().choice(seq=("Heyyy," + at + " . Whats Up?", "Hello, " + at, at + " hi, how are you?", f"yo {at}")) + str("😏😏"))
	authorinfo = {"username": str(message.author),
				  "userid": int(message.author.id)}
	theusername = authorinfo["username"]
	if bool(os.path.exists(pathify(f"json|userinfo|{theusername}.json"))) == False:
		bruh.bruh(pathify(f"json|userinfo|{theusername}.json"), "\n")

	with open(pathify(f"json|userinfo|{theusername}.json"), "w") as fobj:
		json.dump(authorinfo, fobj, indent=6)
	if message.content.lower() == 'what is my userid':
		await message.channel.send(str(message.author.id))
	if susflag:
		if 'sus' in message.content.lower() or 'amogus' in message.content.lower() or 'among us' in message.content.lower() or 'sussy baka' in message.content.lower():
			log(str(message.author) + " is sus. Ewww. ")
			await message.reply(random.Random().choice(seq=('sus', 'when the message is sus', 'AMOGUS', '**EMERGENCY MEETING**\n\n*dun dun dun dun*', 'yo sussy baka', 'https://tenor.com/view/19dollar-fortnite-card-among-us-amogus-sus-red-among-sus-gif-20549014')))

	instructions = message.content.split(' ')
	i = 0
	for instruction in instructions:
		if not instruction.strip(' ').strip('\t').strip('\r').strip('\n'):
			instructions.pop(i)
		i += 1
	if not validMessage(message) and False:
		for c in curse_words:
			if c in mensaje.content.lower().replace(' ', '').replace('\t', '').replace('\r', '').replace('\n', '').replace('*', '') and not int(message.guild.id) in ignore_bad_words:
				await message.channel.send(f"<@" + str(message.author.id) + "> u have been warned. Watch your language.")
				await message.delete()
				await message.author.timeout(datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, hour=datetime.datetime.now().hour, minute=datetime.datetime.now().minute + 10).astimezone())
	if len(instructions) > 0 and instructions[0].lower() == 'turrnut':
		await dostuff(instructions, message)
token = ""
with open("token.token") as t:
	token = t.read()

if token != None:
	client.run(token)
