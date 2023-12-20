import sys

import time
import httpx
from colorama import Fore, Style
from progress.bar import IncrementalBar

DERIBIT = 'https://www.deribit.com/api/v2//public/test'
BINANCE_UM = 'https://fapi.binance.com/fapi/v1/ping'
BINANCE_CM = 'https://dapi.binance.com/dapi/v1/ping'


def _run_benchmark(url: str, market: str, count: int) -> None:
    total_time = 0
    successful_attempts = 0
    bar = IncrementalBar(f"{market}\t\t", max=count)

    for _ in range(count):
        start_time = time.time()
        try:
            response = httpx.get(url)
            if response.status_code == 200:
                request_duration = time.time() - start_time
                total_time += request_duration
                successful_attempts += 1
        except httpx.RequestError:
            pass
        bar.next()

    bar.finish()

    avg_speed = count / total_time if total_time > 0 else 0
    avg_response_time = total_time / successful_attempts if successful_attempts > 0 else 0

    print(
        f"{Fore.YELLOW}{market}{Style.RESET_ALL}\t\t",
        f"| {Fore.BLUE}Avg Speed:{Style.RESET_ALL}\t{Fore.GREEN}{avg_speed:.2f} [req/sec]{Style.RESET_ALL}",
        f"| {Fore.BLUE}Successful Attempts:{Style.RESET_ALL}\t{Fore.GREEN}{successful_attempts}{Style.RESET_ALL}",
        f"| {Fore.BLUE}Avg Response Time:{Style.RESET_ALL}\t{Fore.GREEN}{avg_response_time:.4f} [sec]{Style.RESET_ALL}"
    )


def main(count: int) -> None:
    _run_benchmark(DERIBIT, 'Deribit MAIN', count)
    _run_benchmark(BINANCE_CM, 'Binance COIN-M', count)
    _run_benchmark(BINANCE_UM, 'Binance USD-M', count)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 10)
