#!/usr/bin/env python3
"""
ForgeBot Web 🔨 - Control your bot from a website!
"""

import os
import json
import subprocess
import threading
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pathlib import Path

app = Flask(__name__)
CORS(app)

# ============ CONFIGURATION ============

CONFIG_FILE = "config.json"
BOT_PATH = "bot/main.py"
LOG_FILE = "logs/web_app.log"

# Create logs folder
Path("logs").mkdir(exist_ok=True)

# ============ ROUTES ============

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get current bot status"""
    try:
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()
            last_lines = lines[-10:] if len(lines) > 10 else lines
            last_activity = ''.join(last_lines) if lines else "No activity yet"
    except:
        last_activity = "Bot not started yet"
    
    # Get current config
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    except:
        config = {}
    
    return jsonify({
        'status': 'running',
        'platform': config.get('platform', 'Not set'),
        'target': config.get('target', 'Not set'),
        'daily_views': config.get('daily_views', 0),
        'last_activity': last_activity,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/start', methods=['POST'])
def start_bot():
    """Start the bot with given parameters"""
    try:
        data = request.json
        
        # Validate input
        platform = data.get('platform')
        target = data.get('target')
        views = data.get('views', 100)
        
        if not platform or not target:
            return jsonify({'error': 'Platform and target are required'}), 400
        
        # Update config file
        config = {
            "platform": platform,
            "bot_account": {
                "username": data.get('bot_username', ''),
                "password": data.get('bot_password', '')
            },
            "target": target,
            "daily_views": views,
            "views_per_session": 10,
            "delay_range": [30, 120],
            "proxy": None,
            "headless": True,
            "like_chance": 0.3,
            "scroll_chance": 0.2
        }
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Start bot in background thread
        thread = threading.Thread(target=run_bot_background)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'status': 'started',
            'message': f'Bot started for @{target} on {platform}',
            'views': views
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop', methods=['POST'])
def stop_bot():
    """Stop the bot (placeholder - kill process)"""
    return jsonify({'status': 'stopped', 'message': 'Bot stopped'})

@app.route('/api/logs')
def get_logs():
    """Get recent logs"""
    try:
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()
            last_lines = lines[-50:] if len(lines) > 50 else lines
            return jsonify({'logs': ''.join(last_lines)})
    except:
        return jsonify({'logs': 'No logs available'})

@app.route('/favicon.ico')
def favicon():
    return '', 204

# ============ BOT RUNNER ============

def run_bot_background():
    """Run the bot in the background"""
    try:
        # Write start log
        with open(LOG_FILE, 'a') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"🔥 ForgeBot started at {datetime.now()}\n")
            f.write(f"{'='*50}\n")
        
        # Run the bot
        result = subprocess.run(
            ['python', '-m', 'bot.main'],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True,
            timeout=3600
        )
        
        # Write output to log
        with open(LOG_FILE, 'a') as f:
            f.write(result.stdout)
            if result.stderr:
                f.write(f"ERRORS:\n{result.stderr}")
        
        # Write completion log
        with open(LOG_FILE, 'a') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"✅ ForgeBot completed at {datetime.now()}\n")
            f.write(f"{'='*50}\n")
            
    except subprocess.TimeoutExpired:
        with open(LOG_FILE, 'a') as f:
            f.write(f"⏰ Bot timed out after 1 hour\n")
    except Exception as e:
        with open(LOG_FILE, 'a') as f:
            f.write(f"❌ Bot error: {e}\n")

# ============ RUN SERVER ============

if __name__ == '__main__':
    print("🔥 ForgeBot Web Server Starting...")
    print("🌐 Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
