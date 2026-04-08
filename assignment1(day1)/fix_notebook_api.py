import json

notebook_path = "c:\\lakshya documents\\assignment1(day1)\\Customer_Support_Prompt_Library_up.ipynb"

with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

new_code_source = [
    "import os\n",
    "import json\n",
    "import urllib.request\n",
    "import urllib.error\n",
    "import getpass\n",
    "\n",
    "# 1. Try to fetch the API key from the environment variable\n",
    "api_key = os.environ.get(\"GROQ_API_KEY\")\n",
    "\n",
    "# 2. If it is not found in the environment, prompt the user to input it securely\n",
    "if not api_key:\n",
    "    print(\"\\u26a0\\ufe0f GROQ_API_KEY environment variable not found in this Jupyter session.\")\n",
    "    api_key = getpass.getpass(\"Please paste your Groq API Key (gsk_...) here and hit Enter: \")\n",
    "\n",
    "MODEL = \"llama3-8b-8192\"\n",
    "\n",
    "def generate_support_response(prompt_text):\n",
    "    if not api_key or not api_key.startswith(\"gsk_\"):\n",
    "        return \"Invalid or missing API key.\"\n",
    "    \n",
    "    url = \"https://api.groq.com/openai/v1/chat/completions\"\n",
    "    headers = {\n",
    "        \"Authorization\": f\"Bearer {api_key}\",\n",
    "        \"Content-Type\": \"application/json\"\n",
    "    }\n",
    "    data = {\n",
    "        \"model\": MODEL,\n",
    "        \"messages\": [{\"role\": \"user\", \"content\": prompt_text}],\n",
    "        \"temperature\": 0.7,\n",
    "        \"max_tokens\": 256\n",
    "    }\n",
    "    \n",
    "    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method=\"POST\")\n",
    "    try:\n",
    "        with urllib.request.urlopen(req) as response:\n",
    "            result = json.loads(response.read().decode('utf-8'))\n",
    "            return result['choices'][0]['message']['content']\n",
    "    except urllib.error.HTTPError as e:\n",
    "        return f\"HTTPError: {e.code} - {e.read().decode('utf-8')}\"\n",
    "    except Exception as e:\n",
    "        return f\"Error occurred: {str(e)}\"\n",
    "\n",
    "if api_key and api_key.startswith(\"gsk_\"):\n",
    "    print(\"\\u2705 Groq API initialized securely!\")\n",
    "else:\n",
    "    print(\"\\u274c API Key was not provided correctly.\")\n"
]

# Find the code setup cell and replace its source
for cell in nb["cells"]:
    if cell["cell_type"] == "code" and "def generate_support_response" in "".join(cell["source"]):
        cell["source"] = new_code_source
        if "outputs" in cell:
            cell["outputs"] = [] # clear error output
        break

with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print("Notebook patched to use getpass.")
