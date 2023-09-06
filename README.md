```markdown
# Telegram Bot with Firebase Realtime Database

This Telegram bot is designed to interact with users and store their information in Firebase Realtime Database. It allows users to register, provide their information, and perform various actions such as providing feedback and viewing job vacancies.

## Features

- User registration and profile management.
- Feedback submission with multiple-choice options.
- Viewing active job vacancies.
- Integration with Firebase Realtime Database for data storage.

## Requirements

- Python 3.7+
- [aiogram](https://pypi.org/project/aiogram/) library for Telegram bot functionality.
- Firebase Realtime Database for data storage.

## Getting Started

1. Clone this repository:

   ```shell
   git clone https://github.com/kolya-trotsko/telegram_bot_recruiter.git
   ```

2. Install the required Python libraries:

   ```shell
   pip install aiogram
   ```

3. Create a Firebase Realtime Database and obtain the credentials.

4. Update the Firebase credentials in `db.py`.

5. Run the bot:

   ```shell
   python main.py
   ```

## Usage

- Start the bot and interact with it on Telegram.
- Register and provide your information.
- Submit feedback or view job vacancies.
- The bot will store user data in Firebase Realtime Database.

## Firebase Configuration

To set up Firebase for your bot, follow these steps:

1. Create a Firebase project on the [Firebase Console](https://console.firebase.google.com/).

2. Obtain your Firebase Admin SDK credentials and place the JSON file in the project directory.

3. Update the `db.py` file with your Firebase configuration.

## Contribution

Contributions are welcome! If you have any improvements, bug fixes, or new features to add, please open a pull request.

Enjoy using your Telegram bot!
```
