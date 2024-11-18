# Gmail Monitoring Telegram Bot  

A Telegram bot for monitoring Gmail inboxes, fetching the latest emails, and notifying users of new messages. This bot is built using the **Aiogram** library and Google Gmail API, offering a clean and user-friendly interface for managing email notifications directly through Telegram.  

---

## Features  

### Email Monitoring  
- **Fetch Latest Emails:**  
  Users can fetch the 10 most recent emails from their Gmail inbox with `/mail_fetcher`.  

- **Continuous Monitoring:**  
  The bot monitors the Gmail inbox every 30 seconds and notifies users of new emails.

- **Profile:**
  Profile contents registration date, path to creds and more.

- **Stop Monitoring:**  
  Users can stop the monitoring process anytime using `/stop_mail`.  

### Gmail Authentication  
- Uses **Google OAuth 2.0** for secure access to user Gmail accounts.  
- Automatically handles expired tokens and refreshes credentials.  
- Generates an authorization link if the user is not authenticated.  

### Telegram Integration  
- Inline keyboard for seamless interaction.  
- Callback query handling for efficient command execution.  
- HTML-based message formatting for visually appealing email previews.  

### Database Support  
- Tracks user data and preferences using an SQLite database.  
- Ensures each user’s credentials are securely stored in their unique directory.  

---

## Installation  

### Requirements  
- Python 3.9 or higher  
- Telegram Bot Token (via [BotFather](https://core.telegram.org/bots#botfather))  
- Gmail API Credentials ([Get credentials](https://developers.google.com/gmail/api/quickstart/python))  

---

## License  

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.  

---

## Author  

👤 **atheop1337**  
- GitHub: [@atheop1337](https://github.com/atheop1337)  

Feel free to contribute, report issues, or request features! 😊
