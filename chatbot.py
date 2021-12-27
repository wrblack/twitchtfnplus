from translator import Translator
from twitchio.ext import commands
from tts import MyTTS
import asyncio

# ! Edit site-packages google_trans_new, delete "+ ']'"
# ! https://github.com/lushan88a/google_trans_new/issues/36

class Bot(commands.Bot):
    def __init__(self, config):
        self.config = config
        super().__init__(
            token=self.config.Trans_ACCESS_TOKEN,
            prefix='!',
            initial_channels=[self.config.Twitch_Channel.lower()]
        )

    def cleanup(self):
        if self.config.Debug: print(f'** [Bot::cleanup] Closing event loop')
        loop = asyncio.get_event_loop()
        loop.stop()
        loop.close() # idempotent af
        # ? put something in here for gTTS

    def set_tts(self, my_tts: MyTTS):
        self.my_tts = my_tts
        self.my_tts.run()

    def send_message(self, msg):
        chan = self.get_channel(self.config.Twitch_Channel.lower())
        loop = asyncio.get_event_loop()
        loop.create_task(chan.send(msg))

    async def event_ready(self):
        if self.config.Debug: print(f'** [Bot::event_ready] Logged in as {self.nick} **')
        try:
            self.send_message(f"/me translator bot is loaded.")
        except Exception as e:
            print(f'[Bot::event_ready] Error: {e}')
            return

    def filter_message(self, message):
        # Messages with echo=True are messages by the bot.
        if message.echo:
            if self.config.Debug: print(f'** [Bot Echo] "{message.content}" **')
            return None

        # filter out bot commands with "!"
        if message.content.startswith('!'):
            print('** [Bot::filter_message] message with ! received. **')
            # TODO: Handle these later
            return None

        # Ignore specific users
        user = message.author.name.lower()
        if user in self.config.Ignore_Users:
            print(f'** [Bot::filter_message] Ignoring User: {user} **')
            return None

        return message

    async def event_message(self, message):
        # Filter out messages
        message = self.filter_message(message)
        if message is None:
            return

        # Get translation
        mutarjim = Translator(self.config.lang_TransToHome)
        processed = mutarjim.process(message)
        outgoing_text = processed[0]
        detected_lang = processed[1]

        # Then send it
        self.send_message(outgoing_text)

        # Handle TTS
        if self.config.gTTS_In and self.my_tts:
            self.my_tts.put(message, detected_lang)

        if self.config.gTTS_Out and self.my_tts:
            self.my_tts.put(outgoing_text, detected_lang)

        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command()
    async def ver(self, ctx: commands.Context):
        await ctx.send('** Custom Dubs tTFN. ver 0.1 **')
