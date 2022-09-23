import requests
experiment_name = "cxic0415"
run_num = 17
resp = requests.get(f"https://pswww.slac.stanford.edu/ws/lgbk/lgbk/{experiment_name}/ws/{run_num}/files_for_live_mode")
resp.raise_for_status()
files=resp.json()["value"]
print("\n".join(files))
