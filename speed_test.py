import argparse
import time
import httpx


def measure_speed(url: str) -> None:
        total_bytes = 0
        total_time = 0.0
        request_count = 10

        try:
            with httpx.Client(
                    follow_redirects=True,
                    timeout=30.0,
                    headers={
                        "Accept-Encoding": "identity",
                        "Cache-Control": "no-cache",
                    },
            ) as client:
                for number in range(1, request_count + 1):
                    downloaded = 0
                    start = time.perf_counter()

                    with client.stream("GET", url) as response:
                        response.raise_for_status()

                        for chunk in response.iter_raw():
                            downloaded += len(chunk)

                    elapsed = time.perf_counter() - start
                    total_bytes += downloaded
                    total_time += elapsed

                    print(
                        f"Запрос {number}/{request_count}: "
                        f"{downloaded} байт за {elapsed:.3f} с"
                    )

        except (httpx.HTTPError, httpx.InvalidURL) as error:
            print(f"Ошибка скачивания: {error}")
            raise SystemExit(1) from None

        average_time = total_time / request_count
        speed_mbps = total_bytes * 8 / total_time / 1_000_000

        print(f"\nСреднее время запроса: {average_time:.3f} с")
        print(f"Всего скачано: {total_bytes} байт")
        print(f"Скорость скачивания: {speed_mbps:.2f} Мбит/с")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Измерение скорости скачивания"
    )
    parser.add_argument("url", help="Адрес файла для скачивания")
    args = parser.parse_args()
    measure_speed(args.url)