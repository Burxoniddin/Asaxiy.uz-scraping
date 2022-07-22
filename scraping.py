import logging

import requests
from telegram import ParseMode
from bs4 import BeautifulSoup

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    URL = "https://asaxiy.uz/product?key=telefon"
    # URL+=str(update.message.text)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    item_divs= soup.find_all('div', class_="product__item d-flex flex-column justify-content-between")[:10]
    images = []
    titles =[]
    prices = []
    linkes = []
    for item_div in item_divs:
        image = item_div.find("div", class_="product__item-img").img["data-src"]
        images.append(image[:(len(image)-5)])
        
        product_info =item_div.find("div", class_="product__item-info")
        
        title = product_info.a.h5.text
        titles.append(title)
        
        link = product_info.a['href']
        
        linkes.append("asaxiy.uz"+link)
        
        price = product_info.find("div", class_="product__item-info--prices").find('span',class_="product__item-price").text
        prices.append(price)
    for i in range(10):
        update.message.reply_photo(photo=f"{images[i]}", caption=f"<a href='{linkes[i]}'> {titles[i]} </a> \n\n Price: {prices[i]}", parse_mode=ParseMode.HTML)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5465269312:AAF7eUzKZPVmXnGAgLx_3yQDA4jSLGpo8CM")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()