import cx_Freeze

executables = [cx_Freeze.Executable("Haudi_Script.py")]

cx_Freeze.setup(
    name="HaudiDuin",
    options={
        "build_exe": {
            "packages": ["pygame"],
            "include_files": [
                "Background.png",
                "HaudiHero.png",
                "Fireball.png",
                "HaudiVillain2.png",
                "Haudi_intro.png",
                "screen_pause.png"
            ]
        }
    },
    executables=executables
)