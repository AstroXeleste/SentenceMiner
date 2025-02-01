import genanki
import os

def create_anki_card(german_phrase, english_translation, audio_file, image_file, deck_name="German Phrases Deck", deck_filename='german_english_deck.apkg'):
    """
    Function to create an Anki card with a German phrase, English translation, audio file, and an image.
    """
    
    # Ensure the audio and image files exist
    if not os.path.exists(audio_file) or not os.path.exists(image_file):
        raise FileNotFoundError("Audio file or image file not found!")

    # Create an Anki model - CORRECTED FIELDS DEFINITION
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
                'qfmt': '{{German}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{English}}<br><audio src="{{Audio}}"></audio><br><img src="{{Image}}"/>',
            },
        ]
    )

    # Create an Anki deck
    my_deck = genanki.Deck(
        2059400110,  # Unique deck ID
        deck_name
    )

    # Create a note with the German phrase, English translation, and files
    my_note = genanki.Note(
        model=my_model,
        fields=[german_phrase, english_translation, audio_file, image_file]
    )

    # Add the note to the deck
    my_deck.add_note(my_note)

    # Save the deck to a file
    my_deck.write_to_file(deck_filename)

    print(f"Anki deck generated successfully! Saved as '{deck_filename}'.")


create_anki_card("Hallo alles", "hello goon", "ankioutput.mp3", "screenshot.png")