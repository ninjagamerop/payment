import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Define your bot token (load it securely, e.g., from an environment variable)
BOT_TOKEN = os.getenv("BOT_TOKEN", "7601607062:AAGStyYPVSpo1VkB5nXNMAoHMKv3cYqIur4")
QR_CODE_PATH = "payment.png"  # Path to your QR code image
ADMIN_USER_ID = 123456789  # Replace with your Telegram user ID

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome To The NINJA's World! Send /pay to get the payment QR code."
    )

# Pay command handler
async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send QR code image
    chat_id = update.message.chat_id
    try:
        with open(QR_CODE_PATH, 'rb') as photo:
            await context.bot.send_photo(chat_id=chat_id, photo=photo)
        await update.message.reply_text("Here is the payment QR code. After paying, send a screenshot to @NINJAGAMEROP. Thanks!")
    except FileNotFoundError:
        await update.message.reply_text("Sorry, the QR code image is missing.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Forwarding handler
async def forward_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the message contains a photo or document
    if update.message.photo:
        file_id = update.message.photo[-1].file_id  # Get the highest resolution photo
    elif update.message.document:
        file_id = update.message.document.file_id
    else:
        await update.message.reply_text("Please send a photo or document.")
        return

    try:
        # Forward the file to the admin's Telegram DM
        await context.bot.send_document(chat_id=ADMIN_USER_ID, document=file_id)
        await update.message.reply_text("Your file has been forwarded successfully.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred while forwarding: {str(e)}")

def main():
    try:
        # Create Application
        application = Application.builder().token(BOT_TOKEN).build()

        # Add command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("pay", pay))

        # Add a message handler for forwarding files
        application.add_handler(MessageHandler(filters.PHOTO | filters.Document, forward_file))

        # Start polling for updates
        application.run_polling()
    except Exception as e:
        print(f"Error during bot initialization: {str(e)}")

if __name__ == "__main__":
    main()
