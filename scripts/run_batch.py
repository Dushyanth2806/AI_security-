import os
import sys
import json
import time
import argparse
from datetime import datetime
import anthropic
import requests

# Import heuristic logic from the app
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from redteam_console import check_heuristics

def run_anthropic(system_prompt, user_prompt):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return "Error: Missing ANTHROPIC_API_KEY", 0
    client = anthropic.Anthropic(api_key=api_key)
    start = time.time()
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        lat = int((time.time() - start) * 1000)
        return response.content[0].text, lat
    except Exception as e:
        return f"Error: {e}", 0

def run_opensource(system_prompt, user_prompt):
    base_url = os.environ.get("OSS_BASE_URL", "http://localhost:8000/v1")
    model = os.environ.get("OSS_MODEL", "llama-3")
    api_key = os.environ.get("OSS_API_KEY", "")
    
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
        
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }
    start = time.time()
    try:
        resp = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        lat = int((time.time() - start) * 1000)
        return data["choices"][0]["message"]["content"], lat
    except Exception as e:
        return f"Error: {e}", 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", choices=["injection", "jailbreak", "all"], required=True)
    args = parser.parse_args()
    
    test_cases_dir = os.path.join(os.path.dirname(__file__), '..', 'test_cases')
    results = []
    
    counts = {}
    
    for root, _, files in os.walk(test_cases_dir):
        for file in files:
            if file.endswith(".json"):
                path = os.path.join(root, file)
                rel_dir = os.path.basename(root)
                if args.category != "all" and rel_dir != args.category:
                    continue
                
                with open(path) as f:
                    data = json.load(f)
                    
                print(f"Running {data['id']}...")
                sys_prompt = data["system_prompt"]
                user_prompt = data["user_prompt"]
                if data.get("injected_context"):
                    user_prompt += "\n\n" + data["injected_context"]
                
                anth_text, anth_lat = run_anthropic(sys_prompt, user_prompt)
                oss_text, oss_lat = run_opensource(sys_prompt, user_prompt)
                
                anth_heur = check_heuristics(anth_text)
                oss_heur = check_heuristics(oss_text)
                
                results.append({
                    "id": data["id"],
                    "subcategory": data["subcategory"],
                    "anthropic_result": anth_heur,
                    "oss_result": oss_heur
                })
                
                subcat = data["subcategory"]
                if subcat not in counts:
                    counts[subcat] = {"anthropic": {}, "oss": {}}
                
                counts[subcat]["anthropic"][anth_heur] = counts[subcat]["anthropic"].get(anth_heur, 0) + 1
                counts[subcat]["oss"][oss_heur] = counts[subcat]["oss"].get(oss_heur, 0) + 1

    os.makedirs("results", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = f"results/batch_{timestamp}.json"
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
        
    print("\nBatch Run Summary:")
    for subcat, stats in counts.items():
        print(f"\nSubcategory: {subcat}")
        print("  Anthropic:")
        for h, c in stats["anthropic"].items():
            print(f"    {h}: {c}")
        print("  OSS:")
        for h, c in stats["oss"].items():
            print(f"    {h}: {c}")

if __name__ == "__main__":
    main()
