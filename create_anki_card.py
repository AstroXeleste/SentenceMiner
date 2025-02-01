import genanki
import os

def create_anki_card(german_phrase, english_translation, audio_file, image_file, deck_name="Sentences Mined from Immersion Material", deck_filename='german_english_deck.apkg'):
    """
    Function to create an Anki card with a German phrase, English translation, audio file, and an image.
    """
    
    # Ensure the audio and image files exist
    if not os.path.exists(audio_file) or not os.path.exists(image_file):
        raise FileNotFoundError("Audio file or image file not found!")

    # Create an Anki model
    my_model = genanki.Model(
        1607392319,  # Unique model ID
        'German-English Model',
        fields=[
            {'name': 'German'},
            {'name': 'English'},
            {'name': 'Audio'},
            {'name': 'Image'}
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{German}}',  # The question (German phrase)
                'afmt': '{{FrontSide}}<hr id="answer">{{English}}<br>[sound:{{Audio}}]<br><img src="{{Image}}"/>',  # The answer (English translation, audio, and image)
            },
        ]
    )

    # Create an Anki deck
    my_deck = genanki.Deck(
        2059400110,  # Unique deck ID
        deck_name
    )

    # Create a note with the German phrase, English translation, and media files (using the correct paths)
    my_note = genanki.Note(
        model=my_model,
        fields=[
            german_phrase,
            english_translation,
            os.path.basename(audio_file),  # Use just the filename, not the full path
            os.path.basename(image_file)   # Use just the filename, not the full path
        ]
    )

    # Add the note to the deck
    my_deck.add_note(my_note)

    # Create a package to support media
    my_package = genanki.Package(my_deck)

    # Include the media files in the package
    my_package.media_files = [audio_file, image_file]

    # Write the package to a file
    my_package.write_to_file("anki_cards\\"+deck_filename)

    print(f"Anki deck generated successfully! Saved as '{deck_filename}'.")
