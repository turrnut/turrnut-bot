import discord
import numpy as np
import os
import math
import datetime
import json
import bruh
import random
import nacl
import youtube_dl
import time
import asyncio
import exint.interpreter as lang

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf

from tensorflow import keras
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
#

# Links that might be useful
# FFMPEG: https://stackoverflow.com/questions/63036753/discord-py-bot-how-to-play-audio-from-local-files
#

intents = discord.Intents.all()
client = Bot(command_prefix='?', intents=intents)

voice_clients = {}

yt_dl_opts = {"format" : "bestaudio/best"}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_opts = {"options": "-vn"}

tree = client.tree
mensaje = None
logflag = True
curse_words = ("fags", "nigger", "chink", "nigga",
			   "faggot", "faggots", "retard", "fag",
			   "penis", "stfu", "shutup", "kys", "meth", "cock", "dik")
spamhalt = False
SERVER_NAME = ""
MYSERVER = "Turrnut Republic(拖鞋社)"
ADMIN = "turrnut#0"
TREASURER = "netcrosystem#0"
guilds = []
AWARD = 5
ignore_bad_words = (1112529128273477724,)
nhie = (   
	"Lost an argument with my pet.","Worn a dinosaur suit in public, besides on Halloween.","Impulse bought a ridiculous item while drunk.","Switched places with a twin.","Binge-watched an entire TV series in one sitting.","Secretly watched ahead in a TV show after promising a friend or partner you would watch together.	   ,				  "
	"Raided a child’s Halloween candy stash.","Pretended that I loved a present I secretly hated.","Hoarded office supplies.","Won a dance-off.","Re-enacted the “Lady and the Tramp” kiss.","Microwaved noodles without adding water first.","Ate the last piece of pizza without asking.","Cleaned my room by shoving the mess in the closet.","Been retweeted or followed by a celebrity.","Given someone else my Netflix password.","Unironically used a cheesy pick-up line on someone.","Convinced myself I was dying after checking WebMD.","Brought a parent on a date with me.","Called someone the wrong name more than once.","Told a child that Santa was not real.","Accidentally texted something embarrassing to the wrong person.","Been secretly relieved when plans got cancelled because you didn’t want to leave the house.","Pretended I needed to make a phone call to get out of an awkward conversation with a coworker.","Had a Myspace account.","Ordered delivery from a restaurant that was less than one mile away.","Stole someone’s lunch out of the break room fridge.","Worked all day in my pajamas.","Tried to talk during a Zoom meeting without unmuting myself.","Worked at the same company as a spouse.","Worked at the same company as a parent.","Had a work snack stash.","Changed careers.","Had a medical emergency at work.","Brought my pet into the office.","Broken my vow to eat healthy because there was cake or donuts in the breakroom.","Snooped a coworker’s social media.","Snooped a client’s social media.","Got a really nice present from a client.","Got a really nice present from a boss.","Learned to play an instrument.","Learned to speak a second language.","Called in sick at work to attend an event.","Gotten a speeding ticket.","Been sky-diving.","Played a prank on a coworker.","Played a prank on my boss.","Visited all 50 states.","Worked at a fast food restaurant.","Worked at a family business.","Quit a job in a day or less.","Lied in a job interview.","Taken a nap during the workday while working from home.","Had a crush on a coworker.","Had a crush on a client.","Forgotten a coworker’s name.","Pretended I didn’t see an error sign on a copier because I didn’t feel like fixing it.","Stayed cool as a cucumber so that customers could not tell there was an issue.","Froze up during an interview","Been late to an interview.","Made my coworkers watch a YouTube video.","Baked a cake or pie from scratch.","Broken a bone.","Got stitches.","Stayed overnight in a hospital.","Won the lottery.","Met a celebrity.","Surfed.","Hitch-hiked.","Been to a live concert.","Gone hunting.","Competed in the Olympics.","Gotten a tattoo.","Gotten a piercing.","Lived in another country.","Been vegetarian.","Been vegan.","Missed a flight.","Eaten alligator.","Gotten a concussion.","Been on a road trip.","Been thrown a surprise party.","Ran a marathon.","Ridden an elephant.","Grown a vegetable from seed.","Started a company.","Played video games for 10+ hours a day.","Helped a friend move.","Lost my wallet.","Done my own car repairs.","Built a piece of furniture.","Volunteered at the same charity for years.","Dated a friend’s ex.","Thrown a gender reveal party.","Won a spelling bee.","Started a club","Started a petition.","Had an embarrassing nickname.","Wiped a booger on a piece of furniture.","Wore the same underpants two days in a row.","Stepped in a pet’s puke.","Had food poisoning.","Sat on a wet toilet seat in a public restroom.","Trailed dog doo inside on my shoe.","Been thrown up on by a stranger.","Walked around in public with baby vomit on my shirt.","Had feet so smelly they made bystanders gag.","Eaten an earthworm.","Eaten a spider.","Eaten a scorpion.","Drank rotten milk.","Scratched my behind in public.","Had food come out of my nose.","Stepped in a dead animal.","Been gifted a dead mouse or bird by a cat.","Swallowed my own vomit.","Accidentally wore someone else’s underpants.","Used someone else’s toothbrush.","Used a toothbrush that fell on the floor without washing it first.","Invoked the “5 second rule” (aka, eat something off the floor.)","Bitten my fingernails.","Bitten my toenails.","Clipped my nails in public.","Shaved in public.","Burped and blown it in someone else’s face.","Used the bathroom without washing my hands after.","Slept on the same sheets for two months.","Got stuck in a porta-potty.","Let a pet eat something out of my mouth.","Took out gum and stuck it somewhere “for later.”","Worn a speedo in public.","Had an injury so serious I could see my own bone.","Passed gas in a crowded elevator.","Seen snow in real life.","Appeared in a movie.","Been ski-ing or snowboarding.","Gone horseback riding.","Been to Disneyworld or Disneyland.","Been to the Olympics.","Gone over a month without doing laundry.","Slept in a hostel.","Been to a Hollywood movie premiere.","Been prom king/queen or homecoming king/queen.","Been valedictorian.","Published a book.","Locked my keys in the car.","Performed standup comedy.","Been on a blind date.","Accidentally injured myself in a really strange way.","Been on a gameshow.","Adopted or fostered a child.","Gotten a makeover.","Mastered a magic trick.","Been a wedding officiant.","Gone on a shopping spree.","Designed an app.","Accidentally wore the same outfit as someone else at an event.","Had a stranger do something really kind for me.","Written and recorded a song.","Been a member of a wedding party.","Read 50+ books in one year.","Climbed a mountain.","Stolen someone else’s story and passed it off as my own.","Been to a wedding where someone got left at the altar.","Thrown a party for a pet.","Been cat-fished.","Eaten out 3+ times in one day.","Been to a drag show.","Written a celebrity fanmail.","Seen one of the 7 wonders of the world in person.","Ridden a mechanical bull.","Been to a hookah bar.","Knit a piece of clothing.","Been in a music video.","Written angsty poetry.","Had a post go viral.","Been involved in a car accident.","Piloted a plane.","Switched college majors.","Been attacked by a wild animal.","Cosplayed.","Been to a rodeo.","Saw the Aurora Borealis in person.","Disliked one of my neighbors.","Gone wine tasting.","Brewed my own beer.","Eloped.","Ghosted someone.","Skipped school.","Gotten detention.","Snooped on a date’s social media.","Dated someone my friends and family hated.","Worn body paint.","Been to a foam party.","Changed all of the names in the contacts of someone’s phone.","Lied about my age.","Been zip-lining.","Worked a really bizarre or unusual job.","Met my doppleganger.","Made my own Halloween costume.","Won a giant stuffed animal at a carnival or amusement park.","Ridden a roller coaster 10+ times in a row.","Gotten a professional psychic reading.","Started a social media account for a pet.","Jumped into a swimming pool with all my clothes on.","Been storm-chasing.","Eaten an ostrich egg.","Eaten food garnished with gold flakes.","Staged an elaborate photoshoot for an Instagram post.","Broke out into random song in the middle of a conversation.","Encountered quicksand in real life.","Walked in a fashion show.","Been to 3+ countries in one day.","Dyed my hair a neon color.","Gotten pickpocketed.","Camped out to get a good place in line.","Crashed a wedding.","Pretended to have an accent.","Mispronounced a word for years.","Gotten acupuncture.","Argued with a pet.","Filmed a makeup tutorial.","Cried when a fictional character died.","Completed an entire coloring book.","Sewed a button on a sweater.","Solved a 1,000+ piece jigsaw puzzle.","Designed a video game.","Met an internet friend in real life.","Learned how to ride a bike.","Tripped over my own shoe laces.","Flown a kite.","Traveled abroad.","Seen a ghost.","Been allergic to nuts.","Been on safari.","Screamed during a horror movie.","Won a costume contest.","Made a basket in basketball without looking.","Had a crush on a friend’s sibling.","Hit a home run.","Scored a touchdown.","Performed the lead in a play.","Sleep-walked.","Been part of a parade.","Dressed up like a chicken.","Forgotten my phone in a cab.","Had my luggage lost during a flight.","Ran a website.","Worn pajamas in public.","Had a pen pal.","Eaten a fried candy bar.","Ran out of the room because I saw a spider.","Sang in the shower.","Participated in an internet challenge.","Ate all of the marshmallows out of a box of cereal and left the healthy bits.","Played an April Fool’s Day prank.","Been rafting.",
)

truth = ("If you could be invisible for a day, what’s the first thing you would do?","What’s the biggest secret you’ve kept from your parents?","What’s the most embarrassing music you listen to?","What’s one thing you love most about yourself?","Who is your secret crush?","Who is the last person you creeped on social media?","When was the last time you wet the bed?","If a genie granted you three wishes, what would you ask for and why?","What’s your biggest regret?","If you had to only ever watch rom-coms or only watch scary movies for the rest of your life, which would you choose and why?		","Where is the weirdest place you've ever gone to the bathroom?","Have you ever ghosted on someone?","Which player would survive a zombie apocalypse and which would be the first to go?","Reveal all the details of your first kiss.","What excuse have you used before to get out plans?","What's the longest you've ever slept?","What’s the shortest you’ve ever slept?","Read the last text you sent your best friend or significant other out loud.","What's your biggest pet peeve?","When was the last time you lied?","What five things would you bring to a deserted island?","Which is your favorite Hollywood Chris? Chris Evans, Chris Pratt, Chris Hemsworth or Chris Pine?"," What's the most embarrassing thing you ever did on a date?","What is the boldest pickup line you've ever used?","What celebrity do you think you most look like?","How many selfies do you take a day?","What is one thing you would stand in line an hour for?","When was the last time you cried?","What's the longest time you've ever gone without showering?","What's the most embarrassing top-played song on your phone?","What was your favorite childhood show?","If you had to change your name, what would your new first name be?","If you could be a fictional character for a day, who would you choose?","If you could date a fictional character, who would it be?","What's your biggest fear?","What's one silly thing you can't live without?","Where was your favorite childhood vacation spot?","What is the weirdest trend you've ever participated in?","If you could only listen to one song for the rest of your life, what would you choose?","Who do you text the most?","Have you ever been fired from a job?","If you had to wear only flip-flops or heels for the next 10 years, which would you choose?","What’s an instant deal breaker in a potential love interest?","If you could only eat one thing for the rest of your life, what would you choose?","What is the biggest lie you ever told your parents?","What's the worst physical pain you've ever experienced?","Which player knows you the best?","What's your favorite part of your body?","If you could only accomplish three things in life, what would they be?","What's the weirdest thing you've ever eaten?","Have you ever gone skinny dipping?","Tell us about the biggest romantic fail you’ve ever experienced.","Who was your first celebrity crush?","What's the strangest dream you've ever had?","What are the top three things you look for in a love interest?","What is your worst habit?","How many stuffed animals do you own?","Do you sleep with any stuffed animals?","What is your biggest insecurity?","Name one thing you’d do if you knew there’d be zero consequences.","When’s the last time you said you were sorry? For what?","Do you pee in the shower?","Do you still have feelings for any of your exes?","What’s the most embarrassing thing you’ve done to get a crush’s attention?","What’s the most random thing in your bag right now?","Have you ever sent a sext?","What’s the last movie that made you cry?","What’s the last song that made you cry?","What are the five most recent things in your search history?","When’s the last time you got caught in a lie?","What gross smell do you actually enjoy?","Who was the last person you said “I love you” to?","Have you ever had a paranormal experience?","If you could have lunch with a famous person, dead or alive, who would you pick and why?","If you were handed $1,000 right now, what would you spend it on?","Who’s your celebrity “hall pass” if you were to meet that person while in a relationship?","Have you ever cheated on an exam?","What unexpected part of the body do you find attractive?","What’s the most awkward thing you’ve ever been caught doing?","Have you ever flirted with a close friend’s sibling?","What was your first concert?","If you had the choice to never have to sleep again, would you take it?","If you had to get a tattoo today, what would it be?","Even if you’d be paid $1 million for it, what’s something you would never do?","If you could travel to the past and meet one person, who would it be?","What popular TV show or movie do you secretly hate?","Where do you see yourself in 10 years?","Name your go-to karaoke song.","What’s the most adventurous thing you’ve ever done?","When have you been in the most trouble in school?","If you had to always be overdressed or underdressed, which would you choose?","Who would you cast as you and your friends in the movie version of your life?","What’s the luckiest thing that’s ever happened to you?","Do you have any phobias?","Do you believe in an afterlife?","If you had to move to a different country tomorrow, where would you go?","What do you want to be remembered for most in life?","Do you believe in soul mates?","Have you ever re-gifted a present? What was it?","What’s the weirdest thing you do when you’re alone?","What movie (or franchise) are you most embarrassed to love?","Have you ever had an imaginary friend? Describe them.","What gross food combo do you secretly love?","If you could become besties with a celebrity, who would it be?","What’s the most embarrassing nickname you’ve ever been given?","If you could trade lives with any person you know for a day, who would it be?","What’s the worst thing you’ve ever said to anyone?","What’s the scariest dream you’ve ever had?","What’s the weirdest place you’ve kissed/hooked up with someone?","Have you ever slid into a celebrity’s DMs?","What superstitions do you believe in?","Minecraft or Roblox?","What app do you check first in the morning?","What’s the most embarrassing thing you’ve ever purchased?","What’s the longest you’ve ever gone without brushing your teeth?","What’s the weirdest thing you have in your bedroom?","What’s the weirdest thing you have in your locker?","How often do you wash your sheets?","Do you sing in the shower? What was the last song you belted out?","What’s the weirdest thing you do while driving?","Have you ever started a rumor about someone? What was it?","If you could talk to a fortune teller, what would you ask them?","Do you believe in aliens? What do you think they look like?","Have you ever given a fake number?","What’s more important to you: love or money?","What is a weird food that you love?","What terrible movie or show is your guilty pleasure?","What was your biggest childhood fear?","What is the first letter of your crush’s name?","What is the worst grade you received for a class in school/college?","What is the biggest lie you’ve ever told?","Have you ever accidentally hit something (or someone!) with your car?","Have you ever broken an expensive item?","What is one thing you’d change about your appearance if you could?","If you suddenly had a million dollars, how would you spend it?","Who is the best teacher you’ve ever had and why?","What is the worst food you’ve ever tasted?","What is the weirdest way you’ve met someone you now consider a close friend?","What is the most embarrassing thing you’ve posted on social media?","Who was your first celebrity crush?","Have you ever revealed a friend’s secret to someone else?","How many kids do you want to have one day (or how many did you want to have growing up)?","If you could only eat one meal for the rest of your life, what would it be?","What is a secret you had as a child that you never told your parents?","What is your favorite book of all time?","What is the last text message you sent your best friend?","What is something you would do if you knew there were no consequences?","What is the worst physical pain you’ve ever been in?","Personality-wise, are you more like your mom or your dad?","When is the last time you apologized (and what did you do)?","Have you ever reported someone for doing something wrong (either to the police or at work/school)?","If your house caught on fire and you could only save three things (besides people), what would they be?","If you could pick one other player to take with you to a deserted island, who would it be?","What sport or hobby do you wish you would’ve picked up as a child?","Have you ever stolen anything?","Have you ever been kicked out of a store, restaurant, bar, event, etc.?","What is the worst date you’ve ever had?","What is the weirdest thing you’ve ever done in public?","What is the last excuse you used to cancel plans?","What is the biggest mistake you’ve ever made at school or work?","Which player would survive the longest in a horror/apocalypse movie, and who would be the first one to die?","What is the dirtiest room/area of your house?","Which of your family members annoys you the most?","When is the last time you cried?","When is the last time you made someone else cry?","What is the longest you’ve ever gone without showering?","What is the worst date you’ve ever been on?","When is the last time you did something technically illegal?","If you could pick anyone in the world to be president, who would you choose?","How many times do you wear your jeans before you wash them?","Do you pee in pools?","If someone went through your closet, what is the weirdest thing they’d find?","Have you ever lied about your age?","Besides your phone, what’s the one item in your house you couldn’t live without?","What is the biggest fight you’ve ever been in with a friend?", )

dare = ("Pick someone in this room and ask them for a date.","Let another person post an Instagram caption on your behalf.","Hand over your phone to another player who can send a single text saying anything they want to anyone they want","Let the other players go through your phone for one minute.","Smell another player's armpit.","Smell another player's barefoot.","Eat a bite of a banana peel.","Do an impression of another player until someone can figure out who it is.","Say pickles at the end of every sentence you say until it's your turn again.","Imitate a TikTok star until another player guesses who you're portraying.","Act like a chicken until your next turn.","Talk in a British accent until your next turn.","Send a heart-eye emoji to your crush’s Instagram story.","Call a friend, pretend it's their birthday, and sing them Happy Birthday to You.","Name a famous person that looks like each player in the room.","Show us your best dance moves.","Eat a packet of hot sauce straight.","Let another person draw a tattoo on your back with a permanent marker.","Put on a blindfold and touch the other players' faces until you can figure out who's who.","Bite into a raw onion without slicing it.","Go outside and try to “summon” the rain as loud as possible.","Serenade the person to your right for a full minute.","Do 20 squats.","Let the other players redo your hairstyle.","Eat a condiment of your choice straight from the bottle.","Dump out your purse, backpack, or pockets and do a show and tell of what's inside.","Let the player to your right redo your makeup with their eyes closed.","Prank call one of your family members.","Let another player create a hat out of toilet paper — and you have to wear it for the rest of the game.		","Do a plank for a full minute.","Do your sassiest runway walk.","Put five ice cubes in your mouth (you can't chew them, you just have to let them melt—brrr).","Bark like a dog until it’s your next turn.","Draw your favorite movie and have the other person guess it (Pictionary-style).","Repeat everything the person to your right says until your next turn.","Demonstrate how you style your hair in the mirror (without actually using the mirror).","Play air guitar for one minute.","Empty a glass of cold water onto your head outside.","Go on Instagram Live and do a dramatic reading of one of your textbooks.","In the next 10 minutes, find a way to scare another player and make it a surprise.","Lick a bar of soap.","Talk to a pillow as if it’s your crush.","Post the oldest selfie on your phone to Snapchat or Instagram stories (and leave it up!).","Attempt the first TikTok dance on your FYP.","Imitate a celebrity of the group’s choosing every time you talk for the next 10 minutes.","Go to your crush’s Instagram page and like something from several weeks ago.","Do karaoke to a song of the group’s choosing.","Post a photo (any photo) to social with a heartfelt dedication to a celebrity of the group’s choosing.","Find your very first crush on social and DM them.","Peel a banana using just your toes.","Let the group mix together five of whatever liquids they find in the fridge, then drink it.","Wear another player’s socks like gloves for the next five minutes.","Put on makeup without looking in the mirror, then leave it like that for the rest of the game.","Describe the most attractive quality of every person in the room.","Sing like an opera singer instead of speaking for the next five minutes.","Let everyone pose you in an embarrassing position and post a picture to Instagram.","Allow the person to your right to draw on your face with a Sharpie.","Jump in the pool (or shower) with all your clothes on!","Stand outside your house and wave to everyone who passes in the next minute.","Pretend to be underwater for the next 10 minutes.","Make out with a pillow.","Let everyone go through your Snapchat history.","Post a flirty comment on the first Instagram picture that you see.","Give the person to your right a foot massage (with their consent).","Pretend to be a ballerina until your next turn.","Serenade the person next to you.","Try to fit your whole fist in your mouth.","Read aloud the most personal text you’ve sent in recent days.","Reveal your screen time report to your friends.","Go outside and howl at the moon like a wolf.","Read the last text message you sent out loud.","Show the weirdest item you have in your purse/pockets.","Call the first person in your contacts list and sing them “Happy Birthday.”","Do your best impression of a fish out of water.","Give another player your phone and let them send a social media DM to anyone they want.","Do as many push-ups as you can in one minute.","Give a one-word “roast” to each other player.","Speak in an Australian accent until your next turn.","Let another player tickle you but don’t laugh!","Spin in a swivel chair for 30 seconds and then try to walk a straight line.","Go outside and sing “Never gonna give you up” by Rick Astley at full volume.","Let another player draw a tattoo on your arm in permanent marker.","Hold the plank position until it’s your turn again.","Tell each player who you think their celebrity look alike is.","Show off your best dance moves for the full duration of a song.","Narrate the game in a newscaster voice for three turns.","Walk next door with a measuring cup and ask for a cup of sugar.","Switch clothes with another player for the rest of the game.","Put on a blindfold and touch each players’ face until you can guess who each player is.","Let another player pour a glass of water on your head.","Give a shoulder rub to the player to your right (if they are comfortable).","Attempt to juggle two or three items of the asker’s choosing.","Perform a dramatic version of a monologue from a favorite TV show or movie.","Show the most embarrassing photo on your phone.","Comment a fire emoji on the first five pictures on your Instagram feed.","Do an impression of another player until your next turn.","Try to drink a glass of water without using your hands.","Allow the other players to blindfold you and try to guess three food items from the pantry just by smell.","Do your best interpretive dance/gymnastics floor routine.","Go outside and do your best wolf howl at the moon.","Post an unflattering selfie to your favorite social media account.","Talk and act like a celebrity until the group can guess who you are (this could go multiple turns!)","If you have to get up for the rest of the game, no walking allowed. You can crawl on all fours, roll, somersault, hop on one foot etc., but no walking!","Remove your socks with your teeth.","Go outside and pretend to mow grass with an invisible mower — sounds and all.","Act out a commercial for a product chosen by the other players.","Sing instead of speaking any time you talk for three turns.","Make a silly face and keep it that way until someone in the group laughs.","Do a freestyle rap about the other players for one minute.","Show the group your internet search history.","Let another player style your hair and leave it that way for the rest of the game.","Video chat the person of your choice but pick your nose through the entire conversation.","Put your shoes on the wrong feet and keep them there for the rest of the game.","Call a random acquaintance and tell them you want to break up.","Let the other players pose you and remain in that position until your next turn.","Allow someone else in the group to blindfold you and feed you one item out of the fridge.","Lead the group in a mini yoga class for one minute.","How old are you? Whatever your age is, do that many squats.","Perform a dance routine to a boy band song of the group’s choice.","Let another player draw a washable marker mustache on you.",)

class TODButton(discord.ui.View):
	def __init__ (self):
		super().__init__()
	@discord.ui.button(label="Truth", style=ButtonStyle.green)
	async def truth(self, interaction:discord.Interaction, button: discord.ui.Button):
		self.disabled=True
		global truth
		await interaction.response.send_message(f"Requested by: <@{interaction.user.id}>\nType: **Truth**\n{random.Random().choice(seq=truth)}", view=TODButton())

	@discord.ui.button(label="Dare", style=ButtonStyle.red)
	async def dare(self, interaction:discord.Interaction, button: discord.ui.Button):
		self.disabled=True
		global dare
		await interaction.response.send_message(f"Requested by: <@{interaction.user.id}>\nType: **Dare**\n{random.Random().choice(seq=dare)}", view=TODButton())

	@discord.ui.button(label="Random", style=ButtonStyle.blurple)
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
		await interaction.response.send_message(f"Requested by: <@{interaction.user.id}>\nType: **{qtype}**\n{random.Random().choice(seq=listtt)}", view=TODButton())
class NHIEButton(discord.ui.View):
	def __init__ (self):
		super().__init__()
	@discord.ui.button(label="Never Have I Ever", style=ButtonStyle.grey)
	async def btn(self, interaction:discord.Interaction, button: discord.ui.Button):
		global nhie
		await interaction.response.send_message(f"Requested by: <@{interaction.user.id}>\nType: **NHIE**\nNever have I ever {random.Random().choice(seq=nhie)}", view=NHIEButton())

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

memesjson = {}
memes = []
money = []

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
	return str(mes.author) in (ADMIN, "nickelsthenby#0", "Nickels#3069", "Comte de Monte Cristo#4077", "netcrosystem#0", "rainisfalling#0", "a.fork.in.soup#0")

def validInteraction(mes):
	global ADMIN
	return str(mes.user) in (ADMIN, "nickelsthenby#0", "Nickels#3069", "Comte de Monte Cristo#4077", "netcrosystem#0", "SnowIsFalling#0514", "a.fork.in.soup#0")


async def cant(mes):
	await mes.channel.send("You don't have proper permissions!")


async def dostuff(instructions, message):
	global myid
	global possibilities
	global spamhalt
	global logflag
	global memes
	global ADMIN
	global money
	global tree
	global ignore_bad_words
	instruction = []
	for i in instructions:
		instruction.append(i)
	print(instruction)

	expression = ""
	if instruction[1] == "sync":
		await tree.sync()
		await message.channel.send("Commands Synced")
		return
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
		if instruction[1].lower() == "coins" and instruction[2].lower() == "grant":
			if not str(message.author) in (TREASURER, ADMIN):
				await cant(message)
				return
			amount = float(instruction[3])
			person = int(str(instruction[4]).replace("@", "").replace("<","").replace(">", ""))
			load_money()
			idx = find_money(Money(person, amount))
			money[idx].balance = str(float(money[idx].balance) + float(amount))
			save_money()
			load_money()
			await message.channel.send("ok")
			return

		if instruction[1].lower() == "coins" and instruction[2].lower() == "take":
			if not str(message.author) in (TREASURER, ADMIN):
				await cant(message)
				return
			amount = float(instruction[3])
			person = int(str(instruction[4]).replace("@", "").replace("<","").replace(">", ""))
			load_money()
			idx = find_money(Money(person, amount))
			if amount > float(money[idx].balance) : 
				await message.channel.send("e")
				return
			money[idx].balance = str(float(money[idx].balance) - float(amount))
			save_money()
			load_money()
			await message.channel.send("ok")
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
			if not str(message.author) in (TREASURER, ADMIN):
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
				plog(f"the bot says to {str(message.author)} -> {themsg}")
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
			await message.channel.send("Hello, I am Turrnut Bot, a bot created by turrnut. I am currently serving ** " + str(len(client.guilds)) + " servers!** My pronouns are *it/its*")
			await message.channel.send("Visit our website for details of the bot: https://turrnut.github.io/discordbot")
			print("servers the bot is in: ", end="")
			for server in client.guilds:
				print(server, ",", end="")
			print("\b  ")
	if len(instruction) >= 3:
		if instruction[1].lower() in ("spam", "spam_delete"):
			delete = False
			if instruction[1] == "spam_delete":
				delete = True
			if validMessage(message):
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

			else:
				# LOG
				log(str(message.author) +
					"tries to use use log but has no proper permission")

				await cant(message)

@tree.command(name="calculate", description="Try the turrnut mathematic and logical calculator!")
@app_commands.describe(expression="Arithmetic or boolean expression")
async def calc(interaction:discord.Interaction, expression: str):

	result, error = lang.run("<discord_runtime>", expression)
	if error:
		await interaction.response.send_message(str(error.__repr__()),ephemeral=True)
	else:
		await interaction.response.send_message(str(expression) + "=" + str(result.value))

@tree.command(name="daily", description="Get your daily turrcoin award using this command.")
async def daily(interaction:discord.Interaction):
	global money
	global AWARD

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
		if float(awards[str(interaction.user.id)]) > float(float(time.time())) - 86400:
			await interaction.response.send_message(f"You already got your award today! Try again in ||{ str(round(float(float(86400 - (float(float(time.time())) - float(awards[str(interaction.user.id)]))) / 60.0 / 60.0), 3 )) } hours||")
			return
	awards[str(interaction.user.id)] = str(float(time.time()))
	with open(pathify("awards|awards.json"), "w") as fobj2:
		json.dump(awards, fobj2, indent=6)
	

	money[i] = Money(str(interaction.user.id), str(float(money[i].balance) + AWARD))
	await interaction.response.send_message(f"Congrats <@{interaction.user.id}>, you have just earned {str(AWARD)} turrcoins!")
	save_money()
	load_money()
	

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

@tree.command(name="play", description="Play music")
@app_commands.describe(song="What song you want to play?")
@app_commands.choices(song=[
	app_commands.Choice(name="Never gonna give you up",value="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
])
async def music(ctx:discord.Interaction, song: app_commands.Choice[str]):
	global voice_clients
	global ytdl
	global ffmpeg_opts
	url = song.value

	voice_channel = ctx.user.voice
	if voice_channel == None:
		await ctx.response.send_message(f"You are not in a voice channel!")
		return
	voice_channel = voice_channel.channel
	channel = None
	if voice_channel != None:
		channel = voice_channel.name
		vc = await voice_channel.connect()
		voice_clients[vc.guild.id] = vc
		
		info = ytdl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]

		print("\n\nyYOYOYOYOOYOOYOYO!!!\n\n")

		player = discord.FFmpegOpusAudio(info['formats'][0]['url'], before_options="-reconnect 9 -reconnect_streamed 9 -reconnect_delay_max 5")

		vc.play(player)

		await ctx.response.send_message(f"Now playing {song.name} in {channel}")

@tree.command(name="never-have-i-ever", description="Never have I ever...?")
async def nh(interaction: discord.Interaction):
	global nhie
	await interaction.response.send_message(f"Requested by: <@{interaction.user.id}>\nType: **NHIE**\nNever have I ever {random.Random().choice(seq=nhie)}", view=NHIEButton())

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
		await interaction.response.send_message(f"Requested by: <@{interaction.user.id}>\nType: **Truth**\n{random.Random().choice(seq=truth)}", view=TODButton())
		return
	await interaction.response.send_message(f"Requested by: <@{interaction.user.id}>\nType: **Dare**\n{random.Random().choice(seq=dare)}", view=TODButton())

@tree.command(name="give", description="Give someone an amount of turrcoins")
@app_commands.describe(receiver="The person who receive this money")
@app_commands.describe(amount="How much money to transfer")
async def give(interaction: discord.Interaction, receiver: discord.Member, amount: float):
	global money
	load_money()
	hasacc = False
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
		await interaction.response.send_message(f"Can't complete transcation. You only have {str(account.balance)} coins but you attempt to transfer {amount}", ephemeral=True)
		return
	if amount < 0:
		await interaction.response.send_message(f"Can't complete transcation. the amount is negative", ephemeral=True)
		return
	if amount > float(account.balance):
		await interaction.response.send_message(f"Can't complete transcation. {amount} is a negative number", ephemeral=True)
		return
	if str(receiver.id) == str(interaction.user.id):
		await interaction.response.send_message(f"Can't complete transcation. You can't give yourself money", ephemeral=True)
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
	await interaction.response.send_message(f"<@{interaction.user.id}> gave <@{receiver.id}> {amount} turrcoins")

def mykey(obj: Money):
	return float(obj.balance)

@tree.command(name="leaderboard", description="See the top ranked turrcoin owners")
async def rank(interaction: discord.Interaction):
	global money
	load_money()
	money.sort(key=mykey, reverse=True)
	until = 20
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
	embe = discord.Embed(title="Turrcoins Leaderboard", description="Top 20 turrcoin holders", color=0x00ff00)
	embe.add_field(name="Ranking", value=resp, inline=False)
	await interaction.response.send_message(embed=embe)

@tree.command(name="balance", description="Check how much turrcoins you have")
@app_commands.describe(person="Leave blank to check your own balance")
async def balance(interaction: discord.Interaction, person: discord.Member=None):
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
	await interaction.response.send_message(f"User: <@{str(theid)}>\nAccount Balance:{money[index].balance}")

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
async def inv(interaction: discord.Interaction):
	num_of_servers = 0
	for server in client.guilds:
		num_of_servers += 1
	await interaction.channel.send(f"<:turrnut:1124769501087543358><:turrnut:1124769501087543358><:turrnut:1124769501087543358><:turrnut:1124769501087543358><:turrnut:1124769501087543358><:turrnut:1124769501087543358><:turrnut:1124769501087543358><:turrnut:1124769501087543358><:turrnut:1124769501087543358><:turrnut:1124769501087543358>")
	await interaction.response.send_message(f"Hello, I am <@{str(client.user.id)}>\n# I am currently in {num_of_servers} servers!\n## My pronouns are it/its.\n### Click this link to invite me to your server: https://discord.com/oauth2/authorize?client_id=1014960764378939453&scope=bot \n### For more information, visit our website: https://turrnut.github.io/discordbot\n### For technical support, join our server: https://discord.gg/JBB8C33pKS")

@tree.command(name="meme", description="Get a random meme!")
async def say(interaction: discord.Interaction):
	log(str(interaction.user) + " prompted a random meme")

	load_meme()

	meme = random.Random().choice(seq=memes)
	await interaction.response.send_message(str(meme.name))
	await interaction.channel.send("\nAs suggested by: " + str(meme.suggested))

@tree.command(name="speak", description="Make me say something!")
@app_commands.describe(message="What do you want me to say?")
async def say(interaction: discord.Interaction, message:str):
	if validInteraction(interaction):
		await interaction.response.send_message("ok", ephemeral=True)
		await interaction.channel.send(message)
	else:
		await interaction.response.send_message(message)

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
	await client.change_presence(status=discord.Status.idle, activity=discord.Activity(name="Minecraft",type=5))
	print("\n\n\n")


@client.event
async def on_member_join(member):
	global SERVER_NAME
	global MYSERVER
	if True:
		print('new member!')
		await member.send('!!!!!!!!!!!!!!!!!\nHello! Welcome to the Offical Turrnut Republic Discord Server! In this server you can chat, socialize and play games with other people.\nTo customize your experience at our server, please pick your pronoun roles and ping roles in the #roles channel\nAlso, it\'s good to read the #server-rules channel because it contains useful information about what to do and not to do in our server\n\nGoodbye, have fun!')
		await member.send('https://tenor.com/view/morgan-freeman-gif-24496452')

@client.event
async def on_member_remove(member):
	await client.get_user(int(member.id)).send("bye nerd")
	await client.get_user(int(member.id)).send("https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713")
@client.event
async def on_message(message):
	global mensaje
	global ignore_bad_words
	global curse_words
	mensaje = message
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
	if 'sus' in message.content.lower() or 'amogus' in message.content.lower() or 'sussy baka' in message.content.lower():
		log(str(message.author) + " is sus. Ewww. ")
		await message.channel.send(random.Random().choice(seq=('sus', 'when the message is sus', 'AMOGUS', 'dun dun dun dun', 'yo sussy baka', 'https://tenor.com/view/19dollar-fortnite-card-among-us-amogus-sus-red-among-sus-gif-20549014')))

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
