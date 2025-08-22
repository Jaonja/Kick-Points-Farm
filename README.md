# Kick Points Farm 🎯

An automated Python bot for farming points on Kick.com by connecting to multiple streamers' WebSocket streams simultaneously.

## ⚠️ Disclaimer

This tool is for educational purposes only. Use at your own risk and ensure compliance with Kick.com's Terms of Service. The authors are not responsible for any consequences resulting from the use of this software.

## ✨ Features

- **Multi-streamer support**: Farm points from multiple streamers simultaneously
- **WebSocket connection**: Real-time connection to Kick.com streams
- **Points tracking**: Automatic monitoring and logging of points earned
- **Robust error handling**: Automatic reconnection and error recovery
- **Configurable**: Easy setup through JSON configuration
- **Logging**: Detailed logging with loguru for monitoring bot activity

## 🚀 Quick Start

### Prerequisites

- Valid Kick.com account and authentication token

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/cosney2115/Kick-Points-Farm.git
   cd Kick-Points-Farm
   ```

2. **Configure the bot**

   Edit `config.json` with your settings:

   ```json
   {
     "Private": {
       "token": "YOUR_KICK_TOKEN_HERE"
     },
     "Streamers": [
       {
         "name": "streamer1"
       },
       {
         "name": "streamer2"
       }
     ]
   }
   ```

3. **Run the bot**
   ```bash
   python main.py
   ```

## 🔧 Configuration

### Getting Your Kick.com Token

1. Log in to [Kick.com](https://kick.com)
2. Open browser developer tools (F12)
3. Go to the Network tab
4. Refresh the page
5. Look for requests to `kick.com` API
6. Find the `Authorization` header with `Bearer YOUR_TOKEN`
7. Copy the token (without "Bearer ")

### Config File Structure

```json
{
  "Private": {
    "token": "your_authentication_token"
  },
  "Streamers": [
    {
      "name": "streamer_username"
    }
  ]
}
```

- **token**: Your Kick.com authentication token
- **Streamers**: Array of streamer objects with their usernames

## 📁 Project Structure

```
Kick-Points-Farm/
├── main.py                 # Main application entry point
├── config.json            # Configuration file
├── README.md              # This file
├── _websockets/           # WebSocket handling modules
│   ├── ws_connect.py     # WebSocket connection management
│   └── ws_token.py       # Token handling for WebSocket auth
└── utils/                 # Utility modules
    ├── get_points_amount.py  # Points tracking functionality
    └── kick_utility.py      # Kick.com API utilities
```

## 🛠️ How It Works

1. **Authentication**: Uses your Kick.com token to authenticate with the API
2. **Stream Discovery**: Fetches live stream and channel IDs for each configured streamer
3. **WebSocket Connection**: Establishes persistent WebSocket connections to each stream
4. **Points Farming**: Maintains active connections to earn points automatically
5. **Monitoring**: Checks and logs points balance every 30 seconds
6. **Error Recovery**: Handles disconnections and network issues with automatic reconnection

## 📊 Features in Detail

### Multi-Streamer Support

- Connect to multiple streamers simultaneously
- Each streamer runs in its own async task
- Independent error handling per connection

### Robust WebSocket Management

- Automatic reconnection on connection loss
- Configurable reconnection attempts
- Proper cleanup on shutdown

### Points Tracking

- Real-time points balance monitoring
- Detailed logging of points earned
- Periodic status updates

### Error Handling

- Comprehensive exception handling
- Detailed error logging
- Graceful degradation on failures

## 🔍 Logging

The bot uses loguru for detailed logging:

- Connection status updates
- Points balance changes
- Error messages and stack traces
- WebSocket events

## ⚡ Performance

- Lightweight async implementation
- Minimal resource usage
- Efficient WebSocket management
- Concurrent processing of multiple streams

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚨 Important Notes

- **Rate Limiting**: Kick.com may have rate limits. The bot includes delays to respect these limits.
- **Account Safety**: Use responsibly to avoid potential account restrictions.
- **Token Security**: Keep your authentication token secure and never share it publicly.
- **Updates**: Kick.com may change their API. Update the bot accordingly.

## 🔗 Dependencies

- `asyncio` - Asynchronous programming support
- `curl-cffi` - HTTP client with browser-like headers
- `rnet` - WebSocket client library
- `loguru` - Advanced logging
- `json` - JSON parsing
- `traceback` - Error handling

## 📞 Support

If you encounter issues or have questions:

1. Check the logs for error messages
2. Verify your token is valid and up-to-date
3. Ensure the streamers are live and their usernames are correct
4. Open an issue with detailed error information

---

**Happy farming! 🌾**
