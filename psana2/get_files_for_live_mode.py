import requests
experiment_name="cxilx6520"
run_num =100
#experiment_name = "tmoc00118"
#run_num = 222
#experiment_name = "tmoly9120"
#run_num = 43
resp = requests.get(f"https://pswww.slac.stanford.edu/ws/lgbk/lgbk/{experiment_name}/ws/{run_num}/files_for_live_mode")
resp.raise_for_status()
files=resp.json()["value"]
print("\n".join(files))
