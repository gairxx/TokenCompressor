from flask import Flask, request, jsonify, send_file
import re
import os

app = Flask(__name__)

# Global tokens saved file
STATS_FILE = "global_stats.txt"

def get_total_saved():
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r") as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

def add_to_total(saved_amount):
    if saved_amount <= 0:
        return get_total_saved()
    
    current = get_total_saved()
    new_total = current + saved_amount
    with open(STATS_FILE, "w") as f:
        f.write(str(new_total))
    return new_total

STOP_WORDS = set([
    'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 
    'be', 'been', 'to', 'in', 'on', 'at', 'by', 'for', 'about', 
    'of', 'this', 'that', 'these', 'those', 'it', 'its', 'they', 
    'their', 'them', 'which', 'who', 'whom', 'whose', 'doesn\'t', 'don\'t',
    'can', 'could', 'would', 'should', 'has', 'have', 'had', 'do', 'does', 'did',
    'just', 'very', 'really', 'quite', 'actually', 'basically', 'literally'
])

PHRASE_REPLACEMENTS = [
    (re.compile(r'\bdue to the fact that\b', re.IGNORECASE), 'because'),
    (re.compile(r'\bin order to\b', re.IGNORECASE), 'to'),
    (re.compile(r'\bas a result of\b', re.IGNORECASE), 'from'),
    (re.compile(r'\bfor the purpose of\b', re.IGNORECASE), 'for'),
    (re.compile(r'\bwith the exception of\b', re.IGNORECASE), 'except'),
    (re.compile(r'\bin the event that\b', re.IGNORECASE), 'if'),
    (re.compile(r'\bat this point in time\b', re.IGNORECASE), 'now'),
    (re.compile(r'\bis able to\b', re.IGNORECASE), 'can'),
    (re.compile(r'\bhas the ability to\b', re.IGNORECASE), 'can')
]

def estimate_tokens(text):
    if not text.strip():
        return 0
    words = len(re.findall(r'\b\w+\b', text))
    punct = len(re.findall(r'[^\w\s]+', text))
    return words + int(punct * 0.5)

def compress_text(text):
    processed = text
    
    for pattern, replacement in PHRASE_REPLACEMENTS:
        processed = pattern.sub(replacement, processed)
        
    tokens = re.findall(r'\b\w+\b|[^\w\s]+|\s+', processed)
    result = []
    
    for t in tokens:
        if re.match(r'^\b\w+\b$', t):
            if t.lower() not in STOP_WORDS:
                result.append(t)
        elif re.match(r'^\s+$', t):
            if '\n' in t:
                result.append('\n')
            else:
                result.append(' ')
        else:
            result.append(t)
            
    final_str = "".join(result)
    final_str = re.sub(r'\s+([.,?!;:])', r'\1', final_str)
    final_str = re.sub(r' {2,}', ' ', final_str)
    return final_str.strip()


@app.route('/')
def serve_ui():
    return send_file('index.html')

@app.route('/stats', methods=['GET'])
def stats():
    return jsonify({"global_tokens_saved": get_total_saved()})

@app.route('/compress', methods=['POST'])
def compress_endpoint():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
        
    original_text = data['text']
    compressed_text = compress_text(original_text)
    
    orig_tokens = estimate_tokens(original_text)
    comp_tokens = estimate_tokens(compressed_text)
    saved = max(0, orig_tokens - comp_tokens)
    
    new_global_total = add_to_total(saved)
    
    # Text is NOT saved anywhere. Only token metrics are saved.
    return jsonify({
        "compressed_text": compressed_text,
        "tokens_saved": saved,
        "global_tokens_saved": new_global_total
    })

if __name__ == '__main__':
    print("Starting TokenCompressor API Site on port 5000...")
    app.run(host='0.0.0.0', port=5000)
