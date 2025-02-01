import asyncio
from googletrans import Translator

# Define an asynchronous function to perform the translation
async def translate_text(txt, target, src):
    translator = Translator()

    # Use await to call the translate function
    translated_text = await translator.translate(text=txt, src=src, dest=target)

    # Print the translated text
    return translated_text.text

    # Run the asynchronous function

# Run the asynchronous function
asyncio.run(translate_text('überalles', 'en', 'de'))
