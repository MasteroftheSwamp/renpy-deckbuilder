# Should the user be allowed to rollback the game? If set to False, the user cannot interactively rollback.
define config.rollback_enabled = False


init python:
    LAYER_ENEMIES = "enemies"
    renpy.add_layer(LAYER_ENEMIES, below="screens")

    # FX layer sits above battle sprites so banners / cut-ins cover the field
    LAYER_FX = "fx"
    renpy.add_layer(LAYER_FX, above=LAYER_ENEMIES)

    MUSIC_CHANNEL_UI = "ui"
    renpy.music.register_channel(MUSIC_CHANNEL_UI, "sound", loop=False)


    def tooltip_tag(tag, argument, contents):
        return [(renpy.TEXT_TAG, "tooltip")]

    config.custom_text_tags["tooltip"] = tooltip_tag


# Edit images: game/scripts/utils/images.rpy
# Edit levels: game/scripts/data/levels.json
