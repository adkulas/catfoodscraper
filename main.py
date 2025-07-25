# main.py

import sys
import asyncio
from crawlers import global_pet_foods, store2

SPIDERS = {
	"globalpetfoods": global_pet_foods,
	#"store2": store2,
	# Add more spiders here as needed
}

def main():
	if len(sys.argv) < 2:
		print("Usage: python main.py <store>")
		print(f"Available spiders: {', '.join(SPIDERS.keys())}")
		sys.exit(1)

	store = sys.argv[1]

	spider = SPIDERS.get(store).spider
	if not spider:
		print(f"[!] No spider found for '{store}'")
		print(f"Available spiders: {', '.join(SPIDERS.keys())}")
		sys.exit(1)

	print(f"[+] Starting crawl for: {store}")
	asyncio.run(spider.crawl())
	print(f"[✓] Done.")

if __name__ == "__main__":
	main()
