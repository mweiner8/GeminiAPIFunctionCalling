# Gemini Function Calling Demo - Speed Camera API

This project demonstrates **Gemini API function calling** by integrating with a Speed Camera REST API. Gemini intelligently decides when to call your API based on natural language queries.

Available in **two modes**: Command-line interface (CLI) and Web GUI!

## 🎯 What This Demonstrates

1. **Function Declaration**: Teaching Gemini about your API endpoints
2. **Automatic Function Selection**: Gemini decides which function to call based on user intent
3. **Parameter Extraction**: Gemini extracts parameters from natural language
4. **API Integration**: Actual HTTP calls to your Speed Camera API
5. **Response Processing**: Gemini formats API responses into natural language

## 📋 Assignment Requirements Met

✅ Python program using Gemini API with function calling  
✅ Gemini calls YOUR API via function calling  
✅ Demonstrates 2+ different function calls:
   - `get_cameras_by_zipcode` - Get all cameras in a zipcode
   - `search_cameras_by_street` - Search cameras by street name
✅ Complete request/response flow shown with detailed logging  
✅ Professional web interface (bonus!)

## 📁 Project Files

- **gemini_functions.py** - Shared core logic (API calls, Gemini integration)
- **gemini_function_calling.py** - CLI version with detailed logging
- **app.py** - Flask backend for web GUI
- **index.html** - Beautiful web interface (sky blue, black, white theme)
- **requirements.txt** - All dependencies
- **.env.example** - Environment variable template

## 🚀 Setup Instructions

### Step 1: Clone/Download Files

Make sure you have all the project files in one directory.

### Step 2: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### Step 3: Set Up API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Gemini API key
# Get your key from: https://makersuite.google.com/app/apikey
```

Your `.env` file should look like:
```
GEMINI_API_KEY=AIzaSyC...your_actual_key_here
```

## 🎮 Usage - Two Ways to Run

### Option 1: Command-Line Interface (CLI)

Perfect for seeing detailed logs and understanding the flow.

```bash
python gemini_function_calling.py
```

**Menu Options:**
1. **Run predefined examples** - 4 demonstrations with complete logging
2. **Interactive mode** - Ask your own questions
3. **Exit**

**Example CLI Output:**
```
💬 USER: Show me all speed cameras in zipcode 10036

============================================================
🔧 FUNCTION CALL DETECTED
============================================================
Function: get_cameras_by_zipcode
Arguments: {
  "zipcode": "10036"
}
============================================================

📊 API RESPONSE:
{
  "success": true,
  "zipcode": "10036",
  "count": 1,
  "cameras": [...]
}

🤖 GEMINI: There is 1 speed camera in zipcode 10036...
```

### Option 2: Web GUI

Beautiful interface with real-time function call visualization!

**Step 1: Start the Backend**
```bash
python app.py
```

You'll see:
```
============================================================
🚀 Speed Camera Assistant Backend
============================================================
Server running on http://localhost:5000
Visit http://localhost:5000 in your browser to use the GUI
============================================================
```

**Step 2: Open Your Browser**
Simply go to:
```
http://localhost:5000
```

That's it! The GUI will load automatically.

**GUI Features:**
- 🎨 Sky blue, black, and white color scheme
- 💬 Modern chat interface with smooth animations
- 🔧 Live function call visualization
- 📱 Responsive design
- ⚡ 4 quick example buttons
- ⌨️ Keyboard shortcuts (Enter to send)

## 🎨 Web GUI Design

The web interface features a beautiful, modern design:

- **Sky Blue (#87CEEB)**: Primary accent, user messages, interactive elements
- **Black (#1a1a1a)**: Header, professional contrast
- **White (#FFFFFF)**: Clean background, readability

**What You'll See:**
- User messages in sky blue bubbles (right side)
- AI responses in white bubbles with borders (left side)
- Function calls highlighted in yellow boxes with parameters
- Smooth fade-in animations
- Loading dots while processing

## 🔍 How It Works

### 1. Function Declarations

The program defines functions available to Gemini:

```python
function_declarations = [
    {
        "name": "get_cameras_by_zipcode",
        "description": "Get all speed cameras in a specific zipcode...",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "zipcode": {
                    "type": "STRING",
                    "description": "5-digit US zipcode"
                }
            }
        }
    }
]
```

### 2. User Query Processing

User asks in natural language:
```
"Show me cameras in zipcode 10036"
```

### 3. Gemini Function Call

Gemini analyzes the query and decides to call:
```json
{
  "function": "get_cameras_by_zipcode",
  "arguments": {"zipcode": "10036"}
}
```

### 4. API Execution

Python code makes actual HTTP request:
```python
GET https://speedcameraapi.onrender.com/cameras/zipcode/10036
```

### 5. Response to Gemini

API response sent back to Gemini:
```json
{
  "success": true,
  "count": 1,
  "cameras": [{"id": 1, "cross_street_1": "5th Ave", ...}]
}
```

### 6. Natural Language Response

Gemini formats the data into readable text:
```
"There is 1 speed camera in zipcode 10036, located at the 
intersection of 5th Ave and W 42nd St..."
```

## 📊 Available Functions

### get_cameras_by_zipcode

**Purpose**: Get all speed cameras in a zipcode  
**Parameters**: `zipcode` (string, 5 digits)  
**Example queries**:
- "Show me cameras in 10036"
- "What cameras are in zipcode 90212?"
- "List all cameras in the 94103 area"

### search_cameras_by_street

**Purpose**: Search for cameras on a specific street  
**Parameters**: 
- `street` (string, street name)
- `zipcode` (string, 5 digits)

**Example queries**:
- "Are there cameras on Broadway in 10001?"
- "Find cameras on 5th Ave in zipcode 10036"
- "Show me Market St cameras in 94103"

## 🧪 Testing Tips

### Test with Known Data

Your API has sample data in these zipcodes:
- **10036** (NYC): 5th Ave & W 42nd St
- **10001** (NYC): Broadway & W 34th St
- **10022** (NYC): Park Ave & E 59th St
- **90212** (LA): Wilshire Blvd & S Beverly Dr
- **94103** (SF): Market St & 5th St

### Test Different Query Styles

The same query can be phrased many ways:
```
"Show me cameras in 10036"
"What cameras are in zipcode 10036?"
"10036 speed cameras"
"Find all cameras in the 10036 area"
```

Gemini handles all of these!

### GUI Quick Examples

The web interface includes 4 one-click examples:
1. **Cameras in 10036** - Get all cameras by zipcode
2. **Broadway cameras** - Search by street in 10001
3. **LA cameras (90212)** - Beverly Hills area
4. **SF Market St** - San Francisco Market Street

## 🐛 Troubleshooting

### Error: "GEMINI_API_KEY not found"

Make sure:
1. You created a `.env` file (not `.env.example`)
2. Added your API key: `GEMINI_API_KEY=AIzaSy...`
3. No spaces around the `=` sign

### Error: Connection refused / Timeout

The API at `https://speedcameraapi.onrender.com` might be slow to start (free tier). Wait 10-20 seconds and try again.

### GUI: "Connection refused" error

- Make sure `app.py` is running
- Check that it's running on port 5000
- Look for the "Server running" message in terminal

### GUI: CORS error in browser console

- Flask-CORS should handle this automatically
- Verify installation: `pip install flask-cors`

### Function not being called

If Gemini responds without calling functions:
- Make your query more specific
- Include zipcode explicitly
- Example: "cameras in 10036" instead of "cameras in NYC"

## 📚 Key Concepts for Your Assignment

### 1. Function Declaration
Teaching Gemini about available functions with descriptions and parameters.

### 2. Automatic Parameter Extraction
Gemini extracts structured data (zipcodes, street names) from natural language.

### 3. Multi-Turn Conversation
The program handles:
- User message → Gemini
- Gemini → Function call
- Function result → Gemini
- Gemini → Final response

### 4. Error Handling
Proper try-catch blocks for API failures and invalid inputs.

### 5. Python Best Practices
- Type hints (`Dict[str, Any]`)
- Docstrings for all functions
- Environment variables for secrets
- Clean separation of concerns

## 🎓 Understanding the Flow

```
┌─────────────────┐
│  User Question  │
│  "Cameras in    │
│   10036?"       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Gemini API     │
│  Analyzes query │
│  Selects        │
│  function       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Function Call  │
│  get_cameras_   │
│  by_zipcode     │
│  ("10036")      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Your API       │
│  GET /cameras/  │
│  zipcode/10036  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  JSON Response  │
│  {cameras: [...]}│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Back to Gemini │
│  Formats as text│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Final Response │
│  "There is 1    │
│   camera at..." │
└─────────────────┘
```

## 📝 Assignment Submission Checklist

- [ ] Code runs without errors (both CLI and GUI)
- [ ] Both functions demonstrated
- [ ] Console output shows complete request/response flow
- [ ] Screenshots/recording of both interfaces
- [ ] README explains how it works
- [ ] Comments in code explain key sections
- [ ] `.env.example` provided (not actual API key!)
- [ ] All dependencies listed in requirements.txt

## 🎬 Demo Recommendations

### For Live Demo
1. Start with the **Web GUI** for visual impact
2. Click example buttons to show function calling
3. Switch to **CLI** to show detailed logging
4. Demonstrate interactive mode with custom queries

### For Screenshots
- Web GUI showing function call boxes
- CLI output with detailed logging
- Both demonstrating the same query for comparison

## 🔒 Security Note

**Never commit your `.env` file or share your API key!**

The `.gitignore` should include:
```
.env
__pycache__/
*.pyc
venv/
```

## 📞 Support

If you run into issues:
1. Check your API key is valid
2. Ensure internet connection is stable
3. Verify the Speed Camera API is accessible
4. Check Python version (3.8+ recommended)
5. Make sure all dependencies are installed

## 🎉 Next Steps

To extend this project:
1. Add more functions (PUT, DELETE from your API)
2. Add conversation memory across queries
3. Implement caching for repeated queries
4. Add visualization of camera locations on a map
5. Deploy the web GUI to a hosting service

## 💡 Cool Features to Highlight

### CLI Version
- Detailed logging of every step
- Color-coded output with emojis
- Interactive and automated modes
- Professional console formatting

### Web GUI Version
- Modern, responsive design
- Real-time function call visualization
- Smooth animations and transitions
- Professional color scheme
- One-click example queries

---

**Good luck with your assignment! 🚀**

Both interfaces demonstrate the same powerful Gemini function calling - choose whichever works best for your presentation!