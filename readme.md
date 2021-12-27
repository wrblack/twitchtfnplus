# Twitch TransFreeNext++
This is a refactor of the free to use software by [sayonrai](https://github.com/sayonari/twitchTransFreeNext).

Please feel free to use his software or this.

## The goal of TwitchTFN++
1. Clean up the code a bit.
2. Implement a GUI for easier use.
3. Implement Korean translation as well (GT doesn't do well and DeepL doesn't provide this service for now).

## Issue with package `google_trans_new`
1. The hosted package has an issue and has not been updated since its fix.
2. If you pulled this repo and installed requirements via pip, you will need to edit `google_trans_new.py` with these fixes:
    1. L151 - remove `+ ']'` and enclosing parens
    2. L233 - same as above

## Issue with TTS sound play (note you might not need this)
1. For Window users, you might need the (k-lite codec pack standard)[https://codecguide.com/download_k-lite_codec_pack_standard.htm].